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


def plot(x_label, x_values, y_label, y_values, y_max=None):
    plt.figure(figsize=(6.4, 2.4))
    markers = cycle(["o", "v", "s", "p", "D", "P"])

    plt.errorbar(
        x_values,
        y_values,
        label="Test",
        linestyle="dotted",
        marker=next(markers),
        capsize=3,
    )
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1), ncol=2)
    plt.xlim(xmin=0)
    plt.ylim(bottom=0, top=y_max)
    plt.xlabel(x_label, fontweight="bold")
    plt.ylabel(y_label, fontweight="bold")
    plt.xticks(weight="bold")
    plt.yticks(weight="bold")
    plt.grid()
    ax = plt.gca()
    ax.xaxis.set_major_formatter(default_major_formatter)
    ax.yaxis.set_major_formatter(default_major_formatter)
    plt.savefig("test_plot.pdf", bbox_inches="tight")


def plot_results(solution_name):
    csv_reader = get_csv_reader(solution_name, True)
    header = next(csv_reader)
    plot(
        x_label="Number of epochs per day",
        x_values=storage_calc.EPOCHS_PER_DAY,
        y_label="Storage(GB)",
        y_values=[5, 10, 100, 1000],
    )


def main():
    plot_results(storage_calc.SEEMLESS)
    plot_results(storage_calc.PARAKEET)


if __name__ == "__main__":
    main()
