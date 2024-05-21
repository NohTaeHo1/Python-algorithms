import os

import sys
import folium
import numpy as np
from sklearn import preprocessing

from python_algorithms.example.crime_model import CrimeModel
from python_algorithms.example.crime_util import Reader

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from icecream import ic
import pandas as pd
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(os.path.join(BASE_DIR, ".env")))

'''
문제정의 !
서울시의 범죄현황과 CCTV현황을 분석해서
정해진 예산안에서 구별로 다음해에 배분하는 기준을 마련하시오.
예산금액을 입력하면, 구당 할당되는 CCTV 카운터를 자동으로
알려주는 AI 프로그램을 작성하시오.
'''


class CrimeService:
    def __init__(self):
        self.data = CrimeModel()
        self.data.dname = 'C:\\Users\\bitcamp\\docker_pod\\python-algorithms\\Python-algorithms\\python_algorithms\\crime\\data\\'
        self.data.sname = 'C:\\Users\\bitcamp\\docker_pod\\python-algorithms\\Python-algorithms\\python_algorithms\\crime\\save\\'
        self.data.crime = 'crime_in_seoul.csv'
        self.data.cctv = 'cctv_in_seoul.csv'
        self.data.pop = 'pop_in_seoul'
        self.crime_rate_columns = ['살인 검거율', '강도 검거율', '강감 검거율', '절도 검거율', '폭력 검거율']
        self.crime_columns = ['살인 발생', '강도 발생', '강간 발생', '절도 발생', '폭력 발생']
        self.arrest_columns = ['살인 검거', '강도 검거', '강감 검거', '절도 검거', '폭력 검거']
        self.pop_columns = ['자치구', '합계', '한국인', '등록외국인', '65세이상고령자']

    def crime_dataframe(self) -> pd.DataFrame:
        # index_col=0 해야 기존 index 값이 유지된다.
        # 0은 컴럼명 중에서 첫번째를 의미한다.(배열구조)
        # pd.read_csv(f'경로/파일명/csv', index_col=0 '인덱스로 저장할 column 명') Index 지정

        return pd.read_csv(f'{self.data.dname}{self.data.crime}', encoding='UTF-8',
                           thousands=',')  # f'' 는 변수처리 # index_col=0 인덱스 고정

    def cctv_dataframe(self) -> pd.DataFrame:
        # pd.read_csv('경로/파일명.csv') Index를 지정하지 않음
        return pd.read_csv(f'{self.data.dname}{self.data.cctv}', encoding='UTF-8', thousands=',')

    def pop_dataframe(self) -> pd.DataFrame:
        # pd.read_csv('경로/파일명.csv') Index를 지정하지 않음
        return Reader.excel(self, f'{self.data.dname}{self.data.pop}', 2, 'B, D, G, J, N')

    def save_model(self, fname, dframe: pd.DataFrame) -> pd.DataFrame:
        '''
        풀옵션은 다음과 같다.
        df.to_csv(f'{self.ds.sname}{fname}',sep=',',na_rep='NaN',
                        float_format='%.2f',  # 2 decimal places
                        columns=['ID', 'X2'],  # columns to write
                        index=False)  # do not write index
        '''
        return dframe.to_csv(f'{self.ds.sname}{fname}', sep=',', na_rep='NaN')

    def save_police_position(self) -> None:
        station_names = []
        crime = self.crime_dataframe()
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        station_addreess = []
        station_lats = []
        station_lngs = []

        reader = Reader()
        gmaps = reader.gmaps(os.environ.get("api_key"))
        stations = pd.DataFrame(columns=['경찰서명', '위도', '경도', '구별'])
        stations['경찰서명'] = ['서울' + str(name[:-1]) + '경찰서' for name in crime['관서명']]
        for i in range(len(stations['경찰서명'])):
            tmpMap = gmaps.geocode(stations['경찰서명'][i], language='ko')
            station_addrs = tmpMap[0].get('geometry')
            stations['위도'][i] = station_addrs['location']['lat']
            stations['경도'][i] = station_addrs['location']['lng']
            stations['구별'][i] = \
                [gu['short_name'] for gu in tmpMap[0]['address_components'] if gu['short_name'][-1] == '구'][0]

        for name in station_names:
            t = gmaps.geocode(name, language='ko')
            print(t)
            station_addreess.append(t[0].get("formatted_address"))
            t_loc = t[0].get("geometry")
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])

        gu_names = []
        for name in station_addreess:
            tmp = name.split()
            print(tmp)
            gu_name = [gu for gu in tmp if gu[-1] == '구'][0]
            gu_names.append(gu_name)

        crime['구별'] = gu_names
        # 구 와 경찰서의 위치가 다른 경우 수작업
        crime.loc[crime['관서명'] == '혜화서', ['구별']] = '종로구'
        crime.loc[crime['관서명'] == '서부서', ['구별']] = '은평구'
        crime.loc[crime['관서명'] == '강서서', ['구별']] = '양천구'
        crime.loc[crime['관서명'] == '종암서', ['구별']] = '성북구'
        crime.loc[crime['관서명'] == '방배서', ['구별']] = '서초구'
        crime.loc[crime['관서명'] == '수서서', ['구별']] = '강남구'
        crime.to_csv(f'{self.data.sname}police_position.csv')
        stations.to_csv(f'{self.data.sname}police_position.csv')

    def save_cctv_population(self) -> None:
        reader = Reader()
        population = reader.excel(f'{self.data.dname}pop_in_seoul', 2, 'B, D, G, J, N')
        cctv = self.cctv_dataframe()
        cctv.rename(columns={cctv.columns[0]: '구별'}, inplace=True)
        population.rename(columns={population.columns[0]: '구별',
                                   population.columns[1]: '인구수',
                                   population.columns[2]: '한국인',
                                   population.columns[3]: '외국인',
                                   population.columns[4]: '고령자'}
                          , inplace=True)  # inplace = True는 원본을 수정, 기본값은 false(이때는 할당 필요)

        ic(population.head(10))
        ic(cctv.head(10))
        # population.dropna(how='all', inplace=True) #NaN 값이 있는 행을 삭제
        population.drop(26, axis=0, inplace=True)  # 26번째 행을 삭제
        # 0:행 1:열
        population['외국인비율'] = population['외국인'].astype(int) / population['인구수'].astype(int) * 100
        population['고령자비율'] = population['고령자'].astype(int) / population['인구수'].astype(int) * 100

        cctv.drop(['2013년도 이전', '2014년', '2015년', '2016년'], axis=1, inplace=True)
        cctv_per_populations = pd.merge(cctv, population, on='구별')
        ic(cctv_per_populations)
        cor1 = np.corrcoef(cctv_per_populations['고령자비율'], cctv_per_populations['소계'])
        cor2 = np.corrcoef(cctv_per_populations['외국인비율'], cctv_per_populations['소계'])
        ic(f'고령자비율과 CCTV의 상관계수 {str(cor1)}\n'
           f'외국인비율과 CCTV의 상관계수 {str(cor2)}')

    def save_crime_per_cctv(self) -> pd.DataFrame:
        crime = self.crime_dataframe()
        cctv = self.cctv_dataframe()

        crime.loc[crime['관서명'] == '혜화서', ['관서명']] = '종로구'
        crime.loc[crime['관서명'] == '서부서', ['관서명']] = '은평구'
        crime.loc[crime['관서명'] == '강서서', ['관서명']] = '양천구'
        crime.loc[crime['관서명'] == '종암서', ['관서명']] = '성북구'
        crime.loc[crime['관서명'] == '방배서', ['관서명']] = '서초구'
        crime.loc[crime['관서명'] == '수서서', ['관서명']] = '강남구'

        cctv.rename(columns={cctv.columns[0]: '구별'}, inplace=True)
        crime.rename(columns={crime.columns[0]: '구별'}, inplace=True)

        crime['구별'] = crime['구별'].str[:-1]
        cctv['구별'] = cctv['구별'].str[:-1]

        crime = crime.astype({'살인 발생': float, '강도 발생': float, '강간 발생': float, '절도 발생': float, '폭력 발생': float})
        crime = crime.assign(범죄수=crime['살인 발생'] + crime['강도 발생'] + crime['강간 발생'] + crime['절도 발생'] + crime['폭력 발생'])
        crime = crime.assign(
            검거비율=crime['살인 검거'] / crime['살인 발생'] + crime['강도 검거'] / crime['강도 발생'] + crime['강간 검거'] / crime['강간 발생'] +
                 crime['절도 검거'] / crime['절도 발생'] + crime['폭력 검거'] / crime['폭력 발생'])
        crime = crime.astype({'범죄수': float, '검거비율': float})
        cctv = cctv.astype({'소계': float})

        cctv_per_crime = pd.merge(crime, cctv, on='구별')  #how의 default값은 inner(교집합)
        cctv_per_crime.dropna(how='all', inplace=True)

        ic(cctv_per_crime)
        cor1 = np.corrcoef(cctv_per_crime['범죄수'], cctv_per_crime['소계'])
        cor2 = np.corrcoef(cctv_per_crime['검거비율'], cctv_per_crime['소계'])

        ic(f'범죄발생수와 CCTV의 상관계수 {str(cor1)}\n')
        ic(f'검거비율과 CCTV의 상관계수 {str(cor2)}\n')

        cctv_per_crime.to_csv(f'{self.data.sname}cctv_per_crime.csv')

    def save_crime_arrest_normalization(self) -> None:
        crime = self.crime_dataframe()
        reader = Reader()
        police_position = reader.csv(f'{self.data.sname}police_position')
        police = pd.pivot_table(police_position, index='구별', aggfunc=np.sum)
        print('피봇 결과 :')
        ic(police)

        police['살인검거율'] = police['살인 검거'].astype(int) / police['강간 발생'].astype(int) * 100
        police['강도검거율'] = police['강도 검거'].astype(int) / police['강도 발생'].astype(int) * 100
        police['강간검거율'] = police['강간 검거'].astype(int) / police['살인 발생'].astype(int) * 100
        police['절도검거율'] = police['절도 검거'].astype(int) / police['절도 발생'].astype(int) * 100
        police['폭력검거율'] = police['폭력 검거'].astype(int) / police['폭력 발생'].astype(int) * 100
        police.drop(['강간 검거', '강도 검거', '살인 검거', '절도 검거', '폭력 검거'], axis=1, inplace=True)

        for i in self.crime_rate_columns:
            police.loc[police[i] > 100, i] = 100

        police.rename(columns={'강간 발생': '강간',
                               '강도 발생': '강도',
                               '살인 발생': '살인',
                               '절도 발생': '절도',
                               '폭력 발생': '폭력'}, inplace=True)
        print('loc 결과 :')
        ic(police)
        x = police[self.crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler()
        """     
        피쳐 스케일링(Feature scalining)은 해당 피쳐들의 값을 일정한 수준으로 맞춰주는 것이다.
        이때 적용되는 스케일링 방법이 표준화(standardization) 와 정규화(normalization)다.

        1단계: 표준화(공통 척도)를 진행한다.
            표준화는 정규분포를 데이터의 평균을 0, 분산이 1인 표준정규분포로 만드는 것이다.
            x = (x - mu) / sigma
            scale = (x - np.mean(x, axis=0)) / np.std(x, axis=0)
        2단계: 이상치 발견 및 제거
        3단계: 정규화(공통 간격)를 진행한다.
            정규화에는 평균 정규화, 최소-최대 정규화, 분위수 정규화가 있다.
             * 최소최대 정규화는 모든 데이터를 최대값을 1, 최솟값을 0으로 만드는 것이다.
            도메인은 데이터의 범위이다.
            스케일은 데이터의 분포이다.
            목적은 도메인을 일치시키거나 스케일을 유사하게 만든다.     
        """
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        police_norm = pd.DataFrame(x_scaled, columns=self.crime_rate_columns, index=police.index)
        police_norm[self.crime_columns] = police[self.crime_columns]
        police_norm['범죄'] = np.sum(police_norm[self.crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[self.crime_columns], axis=1)
        police_norm.to_csv(f'{self.data.sname}police_norm.csv', sep=',', encoding='UTF-8')

    def folium_test(self):
        reader = Reader()
        state_geo = reader.json(f'{self.data.dname}us-states')
        state_data = reader.csv(f'{self.data.dname}us_unemployment')
        m = folium.Map(location=[48, -102], zoom_start=3)

        folium.Choropleth(
            geo_data=state_geo,
            name="choropleth",
            data=state_data,
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Unemployment Rate (%)",
        ).add_to(m)

        folium.LayerControl().add_to(m)
        m.save(f'{self.data.sname}us_states.html')

    def draw_crime_map(self):
        reader = Reader()
        state_geo = reader.json(f'{self.data.dname}kr-states')
        state_data = reader.csv(f'{self.data.sname}police_norm')
        m = folium.Map(location=[37.5502, 126.982], zoom_start=12, title="Stamen Toner")
        police_position = reader.csv(f'{self.data.sname}police_position')
        police_norm = reader.csv(f'{self.data.sname}police_norm')
        crime = self.crime_dataframe()
        station_names = []
        for name in crime['관서명']:
            station_names.append('서울' + str(name[:-1]) + '경찰서')
        station_addreess = []
        station_lats = []
        station_lngs = []
        gmaps = reader.gmaps(os.environ.get("api_key"))
        for name in station_names:
            t = gmaps.geocode(name, language='ko')
            station_addreess.append(t[0].get("formatted_address"))
            t_loc = t[0].get("geometry")
            station_lats.append(t_loc['location']['lat'])
            station_lngs.append(t_loc['location']['lng'])
        police_position['lat'] = station_lats
        police_position['lng'] = station_lngs

        temp = police_position[self.arrest_columns] / police_position[self.arrest_columns].max()
        police_position['검거'] = np.sum(temp, axis=1)

        folium.Choropleth(
            geo_data=state_geo,
            name="choropleth",
            data=tuple(zip(police_norm['구별'], police_norm['범죄'])),
            columns=["State", "Crime Rate"],
            key_on="feature.id",
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Crime Rate (%)",
            reset=True
        ).add_to(m)

        folium.LayerControl().add_to(m)
        m.save(f'{self.data.sname}kr_states.html')




if __name__ == '__main__':

    service = CrimeService()
    # crime_df = service.crime_dataframe()
    # cctv_df = service.cctv_dataframe()
    # service.save_police_position()
    # service.save_crime_arrest_normalization()
    # service.save_crime_per_cctv()
    # ic(service.pop_dataframe())
    # service.save_crime_arrest_normalization()
    # ic(service.save_cctv_population())
    # crime_df = service.crime_dataframe()
    # cctv_df = service.cctv_dataframe()
    # # ic(crime_df)
    # # ic(cctv_df)
    # service.folium_test()
    service.draw_crime_map()

'''
상관계수 [[ 1.         -0.28078554]
             [-0.28078554  1.        ]] 
상관계수 [[ 1.         -0.13607433]
             [-0.13607433  1.        ]]
r이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,
r이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,
r이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,
r이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,
r이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,
r이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,
r이 +0.7과 +1.0 사이이면, 강한 양적 선형관계
상관계수 [[ 1.         -0.28078554] 약한 음적 선형관계
            [-0.28078554  1.        ]]
상관계수 [[ 1.         -0.13607433] 거의 무시될 수 있는
            [-0.13607433  1.        ]]                        
'''
