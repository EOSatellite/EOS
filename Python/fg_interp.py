import matplotlib.pyplot as plt

with open("fg.txt", "r", encoding="ISO-8859-1") as f:
    data = f.readlines()

data = [d.strip().split() for d in data if len(d.strip().split()) is 2]

for d in range(len(data)):
    data[d][0] = int(data[d][0])/1000000
    data[d][1] = int(data[d][1])

x = []
y = []
for d in data:
    x.append(d[0])
    y.append(d[1])

ys = y[:]
xs = x[:]

onoffs_x = []
onoffs_y = []
while 1:
    try:
        _1 = ys.index(1)
        _0 = ys.index(0)
        onoffs_y.append(ys[_1:_0])
        onoffs_x.append(xs[_1:_0])

        ys = ys[_0:]
        xs = xs[_0:]

        _1 = ys.index(1)
        _0 = ys.index(0)
        onoffs_y.append(ys[_0:_1])
        onoffs_x.append(xs[_0:_1])

        ys = ys[_1:]
        xs = xs[_1:]
    except:
        break

#for o in onoffs_x:
#    print(f"{len(o)}\t{o}")
#print()

i = 0
while i >= 0:
    try:
        Tstart = onoffs_x[i][0]
        Tend = onoffs_x[i+2][0]
    except: break

    T = Tend - Tstart
    freq = 1/T
    rpm = (freq * 120) / 4

    print(rpm)

    i += 1

#plt.plot(x, y)
#plt.show()
