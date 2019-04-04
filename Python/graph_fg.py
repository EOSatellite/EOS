import matplotlib.pyplot as plt

with open("fg.txt", "r", encoding="ISO-8859-1") as f:
    data = f.readlines()

data = [d.strip() for d in data]
data = [int(d) for d in data if d in ["0", "1"]]

lil_d = data[:500]

vals = []
while 1:
    try:
        _1 = lil_d.index(1)
        _0 = lil_d.index(0)
        vals.append(lil_d[_1:_0])

        lil_d = lil_d[_0:]

        _1 = lil_d.index(1)
        _0 = lil_d.index(0)
        vals.append(lil_d[_0:_1])

        lil_d = lil_d[_1:]
    except:
        break

for v in vals:
    print(f"{len(v)}\t{v}")
print()

i = 0
for v in range(0, len(vals), 2):
    try:
        T = len(vals[v]) + len(vals[v+1])
        print(f"T{i} = ", T, "\trpm = ", T * 2 * 60)
    except:
        continue
    i += 1

plt.plot(data[:500])
plt.show()
