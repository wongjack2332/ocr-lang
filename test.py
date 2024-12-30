import time
def solution():
    with open("input.txt", "r") as f:
        s = [list(map(int, i.split("   "))) for i in f.read().splitlines()]


    a, b = list(), list()

    for i in s:
        a.append(i[0])
        b.append(i[1])

    total = 0
    for i in a:
        counter = 0
        for j in b:
            if i == j:
                counter += 1
        
        total += counter * i

    print(total)


start = time.perf_counter()
solution()
end = time.perf_counter()
print(f"runtime: {end - start}")