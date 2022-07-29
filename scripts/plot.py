import csv
from itertools import cycle

import matplotlib.pyplot as plt
import storage_calc


def get_csv_reader(solution_name, multi_year):
    log_file_name = storage_calc.get_log_file_name(solution_name, multi_year)
    log_file = open(log_file_name, "r")
    return csv.reader(log_file)


def gb_to_tb(gb):
    return gb / (2.0**10)


# Format: Year,Epoch,Storage(GB)
def get_storage_results(csv_reader):
    storage_results = []
    for row in csv_reader:
        storage_results.append(gb_to_tb(int(float(row[2]))))
    return storage_results


def plot_results(
    x_axis_label,
    y_axis_label,
    x_seemless,
    y_seemless,
    x_parakeet,
    y_parakeet,
    plot_name,
    legend_loc,
):
    plt.figure(figsize=(6.4, 2.4))
    markers = cycle(["o", "v", "s", "p", "D", "P"])

    plt.errorbar(
        x_seemless,
        y_seemless,
        label=storage_calc.SEEMLESS,
        linestyle="dotted",
        marker=next(markers),
        capsize=3,
    )

    plt.errorbar(
        x_parakeet,
        y_parakeet,
        label=storage_calc.PARAKEET,
        linestyle="dotted",
        marker=next(markers),
        capsize=3,
    )

    plt.legend(loc=legend_loc, ncol=2)
    plt.xlim(xmin=0)
    plt.ylim(bottom=0, top=None)
    plt.xlabel(x_axis_label, fontweight="bold")
    plt.ylabel(y_axis_label, fontweight="bold")
    plt.xticks(weight="bold")
    plt.yticks(weight="bold")
    ax = plt.gca()
    ax.set_xlim(x_seemless[0], x_seemless[-1])
    plt.xticks(x_seemless, weight="bold")
    plt.yticks(y_seemless + [y_parakeet[-1]], weight="bold")
    plt.grid()
    plt.savefig(plot_name, bbox_inches="tight")


def plot_one_year_results():
    parakeet_csv_reader = get_csv_reader(storage_calc.PARAKEET, False)
    _parakeet_header = next(parakeet_csv_reader)

    seemless_csv_reader = get_csv_reader(storage_calc.SEEMLESS, False)
    _seemless_header = next(seemless_csv_reader)

    parakeet_storage = get_storage_results(parakeet_csv_reader)
    seemless_storage = get_storage_results(seemless_csv_reader)
    print(
        "One year storage results for SEEMless for epochs ("
        + str(storage_calc.EPOCHS_PER_DAY)
        + "): "
        + str(seemless_storage)
    )
    print(
        "One year storage results for Parakeet for epochs ("
        + str(storage_calc.EPOCHS_PER_DAY)
        + "): "
        + str(parakeet_storage)
    )

    plot_results(
        "Number of epochs per day",
        "Storage (TB)",
        storage_calc.EPOCHS_PER_DAY,
        seemless_storage,
        storage_calc.EPOCHS_PER_DAY,
        parakeet_storage,
        "storage_comparison_parakeet_seemless_one_year.pdf",
        "center",
    )


def plot_multi_year_results():
    parakeet_csv_reader = get_csv_reader(storage_calc.PARAKEET, True)
    _parakeet_header = next(parakeet_csv_reader)

    seemless_csv_reader = get_csv_reader(storage_calc.SEEMLESS, True)
    _seemless_header = next(seemless_csv_reader)

    parakeet_storage = get_storage_results(parakeet_csv_reader)
    seemless_storage = get_storage_results(seemless_csv_reader)
    print(
        "Multi year storage results for SEEMless for 144 epochs per day years ("
        + str(storage_calc.NUMBER_OF_YEARS)
        + "): "
        + str(seemless_storage)
    )
    print(
        "Multi year storage results for Parakeet for 144 epochs per day years ("
        + str(storage_calc.NUMBER_OF_YEARS)
        + "): "
        + str(parakeet_storage)
    )

    plot_results(
        "Years",
        "Storage (TB)",
        storage_calc.NUMBER_OF_YEARS,
        seemless_storage,
        storage_calc.NUMBER_OF_YEARS,
        parakeet_storage,
        "storage_comparison_parakeet_seemless_multi_year.pdf",
        "upper left",
    )


def main():
    plot_one_year_results()
    plot_multi_year_results()


if __name__ == "__main__":
    main()
