from itertools import cycle

import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("ozks_timing.csv", sep=",", header=None)
values = df.values

user = [int((int(ks) / 100_000)) for ks in values[:, 0]]
insert = values[:, 1] / 1000.0 / 60
read = values[:, 2] / 60.0
write = values[:, 3] / 60.0

plt.figure(figsize=(6.4, 2.4))
markers = cycle(["o", "v", "s", "p", "D", "P"])


plt.errorbar(
    user,
    insert,
    label="Total Time to Insert 100K Users",
    linestyle="dotted",
    marker=next(markers),
    capsize=3,
)

plt.errorbar(
    user,
    read,
    label="Database Read Time",
    linestyle="dotted",
    marker=next(markers),
    capsize=3,
)

plt.errorbar(
    user,
    write,
    label="Database Write Time",
    linestyle="dotted",
    marker=next(markers),
    capsize=3,
)


plt.legend(loc="lower right", ncol=2)
plt.xlim(xmin=0)
plt.ylim(bottom=0, top=None)
plt.xlabel("Number of keys (100K)", fontweight="bold")
plt.ylabel("Time (mins)", fontweight="bold")
plt.xticks(weight="bold")
plt.yticks(weight="bold")
# ax = plt.gca()
# ax.set_xlim(x_seemless[0], x_seemless[-1])
# plt.xticks(x_seemless, weight="bold")
# plt.yticks(y_seemless + [y_parakeet[-1]], weight="bold")
plt.grid()
plt.savefig("ozks_timing.pdf", bbox_inches="tight")
