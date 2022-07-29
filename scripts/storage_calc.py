import csv
from math import log2


def calculate_seemless_storage(
    num_starting_keys, num_ep, num_insertion_per_ep, state_size
):
    nodes_per_init_key = 2
    nodes_per_updated_key = 4
    num_nodes = nodes_per_init_key * num_starting_keys
    num_states = num_nodes
    for ep in range(num_ep):
        num_inserted_nodes = nodes_per_updated_key * num_insertion_per_ep
        num_states = num_states + (num_inserted_nodes * log2(num_nodes) / log2(2))
        num_nodes = num_nodes + num_inserted_nodes
    print("num nodes = " + str(num_nodes))
    print("num states = " + str(num_states))
    print("final memory = " + str(state_size * num_states / (2.0**30)) + " GB")


def calculate_parakeet_storage(
    num_starting_keys, num_ep, num_insertion_per_ep, state_size
):
    nodes_per_init_key = 2
    nodes_per_updated_key = 4
    num_nodes = nodes_per_init_key * num_starting_keys
    num_states = num_nodes
    for ep in range(num_ep):
        num_inserted_nodes = nodes_per_updated_key * num_insertion_per_ep
        num_states = num_states + num_inserted_nodes
        num_nodes = num_nodes + num_inserted_nodes
    print("num nodes = " + str(num_nodes))
    print("final memory = " + str(state_size * num_states / (2.0**30)) + " GB")


# These should give storage data for seemless with 10M insertions per day for a year,
# starting state is 2B keys.


epochs_per_day = [1, 10, 24, 24 * 6]

number_of_years = [1, 2, 3, 4, 5]

# Vary the number of epochs per day over a year
file_seemless_one_yr = open("./simulated_storage/seemless_one_year.csv", "w")
writer_seemless_one_yr = csv.writer(file_seemless_one_yr)
title = ["Epochs per day", "Storage size required"]
writer_seemless_one_yr.writerow(title)
for epochs in epochs_per_day:
    print("**********************************")
    print(
        "SEEMless storage for "
        + str(epochs)
        + " ep/day over a year, with 10M/day keys inserted"
    )
    storage_needed = calculate_seemless_storage(
        2000000000, 366 * epochs, 10000000.0 / epochs, 64.0
    )
    writer_seemless_one_yr.writerow([epochs, storage_needed])
file_seemless_one_yr.close()


file_seemless_mult_yr = open("./simulated_storage/seemless_one_year.csv", "w")
writer_seemless_mult_yr = csv.writer(file_seemless_mult_yr)
title = ["Number of years", "Storage size required"]
for years in number_of_years:
    print("**********************************")
    print(
        "SEEMless storage for "
        + str(24 * 6)
        + " ep/day over"
        + str(years)
        + " years, with 10M/day keys inserted"
    )
    storage_needed = calculate_seemless_storage(
        2000000000, years * 366 * 24 * 6, 10000000.0 / (24 * 6), 64.0
    )
    writer_seemless_mult_yr.writerow([years, storage_needed])
file_seemless_mult_yr.close()


print("**********************************")
print("**********************************")
print("**********************************")
print("**********************************")

# These should give storage data for parakeet with 10M insertions per day for a year,
# starting state is 2B keys.
# Vary the number of epochs per day over a year
file_parakeet_one_yr = open("./simulated_storage/parakeet_one_year.csv", "w")
writer_parakeet_one_yr = csv.writer(file_parakeet_one_yr)
title = ["Epochs per day", "Storage size required"]
writer_parakeet_one_yr.writerow(title)
for epochs in epochs_per_day:
    print("**********************************")
    print(
        "Parakeet storage for "
        + str(epochs)
        + " ep/day over a year, with 10M/day keys inserted"
    )
    calculate_parakeet_storage(2000000000, 366 * epochs, 10000000.0 / epochs, 64.0)
    writer_parakeet_one_yr.writerow([epochs, storage_needed])
file_parakeet_one_yr.close()


file_parakeet_mult_yr = open("./simulated_storage/seemless_one_year.csv", "w")
writer_parakeet_mult_yr = csv.writer(file_parakeet_mult_yr)
title = ["Number of years", "Storage size required"]
writer_parakeet_mult_yr.writerow(title)
for years in number_of_years:
    print("**********************************")
    print(
        "Parakeet storage for "
        + str(24 * 6)
        + " ep/day over"
        + str(years)
        + " years, with 10M/day keys inserted"
    )
    calculate_parakeet_storage(
        2000000000, years * 366 * 24 * 6, 10000000.0 / (24 * 6), 64.0
    )
    writer_parakeet_mult_yr.writerow([epochs, storage_needed])
file_parakeet_mult_yr.close()
