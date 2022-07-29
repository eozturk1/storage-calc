import csv
from itertools import cycle

import matplotlib.pyplot as plt
import storage_calc


def get_csv_reader(solution_name, multi_year):
    log_file_name = storage_calc.get_log_file_name(solution_name, multi_year)
    log_file = open(log_file_name, "r")
    return csv.reader(log_file)


def default_major_formatter(x, pos):
    if pos is None:
        return
    if x >= 1_000:
        return f"{x/1000:.0f}k"
    else:
        return f"{x:.0f}"


# Format: Year,Epoch,Storage(GB)
def get_storage_results(csv_reader):
    storage_results = []
    for row in csv_reader:
        storage_results.append(row[2])
    return storage_results


def plot_one_year_results():
    plt.figure(figsize=(6.4, 2.4))
    markers = cycle(["o", "v", "s", "p", "D", "P"])

    parakeet_csv_reader = get_csv_reader(storage_calc.PARAKEET, False)
    _parakeet_header = next(parakeet_csv_reader)

    seemless_csv_reader = get_csv_reader(storage_calc.SEEMLESS, False)
    _seemless_header = next(seemless_csv_reader)

    parakeet_storage = get_storage_results(parakeet_csv_reader)
    seemless_storage = get_storage_results(seemless_csv_reader)

    plt.errorbar(
        parakeet_storage,
        storage_calc.EPOCHS_PER_DAY,
        label="Test",
        linestyle="dotted",
        marker=next(markers),
        capsize=3,
    )

    plt.errorbar(
        seemless_storage,
        storage_calc.EPOCHS_PER_DAY,
        label="Test",
        linestyle="dotted",
        marker=next(markers),
        capsize=3,
    )

    plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1), ncol=2)
    plt.xlim(xmin=0)
    plt.ylim(bottom=0, top=None)
    plt.xlabel("Number of epochs per day", fontweight="bold")
    plt.ylabel("Storage (GB)", fontweight="bold")
    plt.xticks(weight="bold")
    plt.yticks(weight="bold")
    plt.grid()
    ax = plt.gca()
    ax.xaxis.set_major_formatter(default_major_formatter)
    ax.yaxis.set_major_formatter(default_major_formatter)
    plt.savefig("test_plot.pdf", bbox_inches="tight")


def main():
    plot_one_year_results()
    # plot_multi_year_results()


if __name__ == "__main__":
    main()
