import sys

N, M, B = map(int, input().split())

ground = []
total_ston = 0

for i in range(N):
    ground.extend(int(i) for i in input().split())

total_ston = sum(ground)
time = []
total_time = sys.maxsize
land_height = 0

for i in range(min(ground), min(256, (total_ston+B)//(N*M)+1)):
    add_blocks = 0
    remove_blocks = 0
    for height in ground:
        if height < i:
            add_blocks += (i - height)
        else:
            remove_blocks += (height - i)

    if add_blocks <= remove_blocks + B:
        time = add_blocks + remove_blocks * 2
        if total_time >= time:
            total_time = time
            land_height = i

# for i in range(min(ground), min(256, (total_ston+B)//(N*M)+1)):
#     time = sum([(k-i)*2 if k-i>0 else (i-k) if k-i<0 else 0 for k in ground])
#     if total_time >= time:
#         total_time = time
#         land_height = i

print(total_time, land_height)
