from fastapi import FastAPI
import uvicorn

from example.bit_bank import BitBank
from example.bmi import BMI

app = FastAPI()


@app.get("/")
async def root():
    # m = BMI()
    return {"message": "Hello World 3"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8100)

def BitBank():
    while True:
        menu = input('0-종료  1. 계좌개설 : ')
        if menu == '0': break
        if menu == '1': BitBank().create_account()

def main():
    print("1")


if __name__ == "__main__":
    main()

