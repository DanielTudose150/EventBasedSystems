import matplotlib.pyplot as plt
import os
import json

times = {}

ths = list(range(1, 17))

for t in ths:
    threads = t
    file = f"{t}.txt"
    with open(f"times\\{file}", "r") as fd:
        line = fd.read()
        splits = line.split(",")
        times[int(splits[0])] = float(splits[1])


x = times.keys()
y = times.values()

plt.plot(x, y)

plt.xlabel('No. Processes')
plt.ylabel('Time in seconds')
plt.title('How the number of processes affects the execution time')

plt.savefig('threads.png')
plt.show()


plt.plot(x, y)

plt.xlabel('No. Processes')
plt.ylabel('Time in seconds')
plt.title('How the number of processes affects the execution time')
plt.ylim(ymin=0)
plt.savefig('threads0.png')
plt.show()
