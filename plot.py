import csv

import numpy as np
import matplotlib as mpl

mpl.use("TkAgg")
import matplotlib.pylab as plt

filenames = [
    "measure_1.csv",
    "measure_2.csv",
    "measure_4.csv",
    "measure_8.csv",
    "measure_16.csv",
]

gets = []
puts = []
deletes = []
total = []

for i in range(len(filenames)):
    one_gets = []
    one_puts = []
    one_deletes = []
    one_total = []

    with open(filenames[i], newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for row in csvreader:
            if row[0] == "get":
                one_gets.append(float(row[1]))
            if row[0] == "put":
                one_puts.append(float(row[1]))
            if row[0] == "delete":
                one_deletes.append(float(row[1]))
            if row[0] == "scenario":
                one_total = float(row[1])

        gets.append(one_gets)
        puts.append(one_puts)
        deletes.append(one_deletes)
        total.append(one_total)

get_total = np.sum(gets[0])
put_total = np.sum(puts[0])
delete_total = np.sum(deletes[0])

# A pie chart to show the ratio of get/put/delete.
labels = "Get", "Put", "Delete"
sizes = [get_total * 1000, put_total * 1000, delete_total * 1000]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, shadow=True, autopct="%1.1f%%")
ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

# A stacked bar graph to show total time for different experiments.
N = len(filenames)
ind = np.arange(N)  # the x locations for the experiments
width = 0.6  # the width of the bars: can also be len(x) sequence

get_means = [np.mean(gets[i]) for i in range(N)]
get_stds = [np.std(gets[i]) for i in range(N)]
put_means = [np.mean(puts[i]) for i in range(N)]
put_stds = [np.std(puts[i]) for i in range(N)]
delete_means = [np.mean(deletes[i]) for i in range(N)]
delete_stds = [np.std(deletes[i]) for i in range(N)]

p_get = plt.bar(ind - width / 3, get_means, width / 3, yerr=get_stds)
p_put = plt.bar(ind, put_means, width / 3, yerr=put_stds)
p_delete = plt.bar(ind + width / 3, delete_means, width / 3, yerr=delete_stds)

plt.ylabel("Average request round trip time on one node")
plt.xlabel("Number of nodes")
plt.xticks(ind, [(2 ** i) for i in range(0, N)])
plt.legend((p_get[0], p_put[0], p_delete[0]), ("Get", "Put", "Delete"))
plt.show()


print(f"total times: {total}")
print(f"get means: {get_means}")
print(f"put means: {put_means}")
print(f"delete means: {delete_means}")
