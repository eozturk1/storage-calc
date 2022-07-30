from itertools import cycle

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("ozks_memory_longer.csv", sep=",", header=None)
values = df.values

keys = [int((int(ks) / 100_000)) for ks in values[:, 0]]
times = values[:, 2]
history = values[:, 3] / (2.0**10)
users = values[:, 4] / (2.0**10)
ozks = values[:, 5] / (2.0**10)
total = history + users + ozks

plt.figure(figsize=(6.4, 2.4))
markers = cycle(["o", "v", "s", "p", "D", "P"])


plt.errorbar(
    keys,
    total,
    label="Total",
    linestyle="dotted",
    marker=next(markers),
    capsize=3,
)

plt.errorbar(
    keys,
    history,
    label="Merkle Tree Data",
    linestyle="dotted",
    marker=next(markers),
    capsize=3,
)

plt.errorbar(
    keys,
    users,
    label="User Data",
    linestyle="dotted",
    marker=next(markers),
    capsize=3,
)

plt.errorbar(
    keys,
    ozks,
    label="Tree Metadata",
    linestyle="dotted",
    marker=next(markers),
    capsize=3,
)


plt.legend(loc="upper left", ncol=2)
plt.xlim(xmin=0)
plt.ylim(bottom=0, top=None)
plt.xlabel("Number of keys (100K)", fontweight="bold")
plt.ylabel("Parakeet Storage (GB)", fontweight="bold")
plt.xticks(weight="bold")
plt.yticks(weight="bold")
# ax = plt.gca()
# ax.set_xlim(x_seemless[0], x_seemless[-1])
# plt.xticks(x_seemless, weight="bold")
# plt.yticks(y_seemless + [y_parakeet[-1]], weight="bold")
plt.grid()
plt.savefig("ozks_memory_longer.pdf", bbox_inches="tight")
