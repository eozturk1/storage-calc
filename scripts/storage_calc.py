import csv
import sys
from math import log2

# Calculates storage cost of a (compressed) Patricia Merkle Trie based key transparency solution.
# NOTE: b refers to bytes in all functions.

# Since no previous key is marked as stale only 1 node is added to the tree -- which incurs a 2-node cost with its parent.
NODES_PER_NEW_KEY = 2
# An updated key incurs 4 new nodes -- 2 for the new key and 2 for marking the previous key as stale.
NODES_PER_UPDATED_KEY = 4

NUM_STARTING_KEYS = 2_000_000_000


def b_to_gb(b):
    return b / (2.0**30)


def final_storage_in_gb(num_states, state_size):
    return b_to_gb(num_states * state_size)


def get_initial_num_nodes(num_initial_keys):
    # Initial keys ARE new keys.
    return NODES_PER_NEW_KEY * num_initial_keys


def get_initial_num_states(num_initial_nodes):
    return num_initial_nodes


def calculate_num_inserted_nodes(num_new_keys, num_key_updates):
    return (num_new_keys * NODES_PER_NEW_KEY) + (
        num_key_updates * NODES_PER_UPDATED_KEY
    )


# For SEEMless number of state increase depends on
# number of inserted nodes + number of nodes with updated states due to the insertions.
# The latter depends on the tree depth.
def calculate_seemless_additional_num_states(num_inserted_nodes, num_existing_nodes):
    return num_inserted_nodes * log2(num_existing_nodes)


def calculate_parakeet_additional_num_states(num_inserted_nodes):
    return num_inserted_nodes


def print_stuff(
    solution_name,
    num_starting_keys,
    num_epochs,
    num_new_key_per_ep,
    num_updated_key_per_ep,
    num_total_nodes,
    num_total_states,
    state_size,
    final_storage_gb,
):
    print("For " + solution_name)
    print("\tNum starting keys: " + str(num_starting_keys))
    print("\tNum epochs: " + str(num_epochs))
    print("\tNum new key per epoch: " + str(num_new_key_per_ep))
    print("\tNum updated key per epoch: " + str(num_updated_key_per_ep))
    print("\tNum total nodes: " + str(num_total_nodes))
    print("\tNum total states: " + str(num_total_states))
    print("\tState size: " + str(state_size))
    print("\tFinal storage: " + str(final_storage_gb) + " GB")


def calculate_seemless_storage(
    num_starting_keys, num_ep, num_new_key_per_ep, num_updated_key_per_ep, state_size
):
    # Initial calculations.
    num_total_nodes = get_initial_num_nodes(num_starting_keys)
    num_total_states = get_initial_num_states(num_total_nodes)

    # Additions over epochs.
    for ep in range(num_ep):
        num_inserted_nodes = calculate_num_inserted_nodes(
            num_new_keys=num_new_key_per_ep, num_key_updates=num_updated_key_per_ep
        )
        num_total_states = num_total_states + calculate_seemless_additional_num_states(
            num_inserted_nodes=num_inserted_nodes, num_existing_nodes=num_total_nodes
        )
        num_total_nodes = num_total_nodes + num_inserted_nodes

    # Final.
    final_storage = final_storage_in_gb(num_total_states, state_size)

    print_stuff(
        SEEMLESS,
        num_starting_keys=num_starting_keys,
        num_epochs=num_ep,
        num_new_key_per_ep=num_new_key_per_ep,
        num_updated_key_per_ep=num_updated_key_per_ep,
        num_total_nodes=num_total_nodes,
        num_total_states=num_total_states,
        state_size=state_size,
        final_storage_gb=final_storage,
    )

    return final_storage


def calculate_parakeet_storage(
    num_starting_keys, num_ep, num_new_key_per_ep, num_updated_key_per_ep, state_size
):
    # Initial calculations
    num_total_nodes = get_initial_num_nodes(num_starting_keys)
    num_total_states = get_initial_num_states(num_total_nodes)

    # Additions over epochs.
    for ep in range(num_ep):
        num_inserted_nodes = calculate_num_inserted_nodes(
            num_new_keys=num_new_key_per_ep, num_key_updates=num_updated_key_per_ep
        )
        num_total_states = num_total_states + calculate_parakeet_additional_num_states(
            num_inserted_nodes=num_inserted_nodes
        )
        num_total_nodes = num_total_nodes + num_inserted_nodes

    # Final
    final_storage = final_storage_in_gb(num_total_states, state_size)

    print_stuff(
        PARAKEET,
        num_starting_keys=num_starting_keys,
        num_epochs=num_ep,
        num_new_key_per_ep=num_new_key_per_ep,
        num_updated_key_per_ep=num_updated_key_per_ep,
        num_total_nodes=num_total_nodes,
        num_total_states=num_total_states,
        state_size=state_size,
        final_storage_gb=final_storage,
    )

    return final_storage


# These should give storage data for seemless with 10M insertions per day for a year,
# starting state is 2B keys.
EPOCHS_PER_DAY = [1, 10, 24, 24 * 6]
NUMBER_OF_YEARS = [1, 2, 3, 4, 5]
NUM_DAILY_NEW_KEYS = 5_000_000.0
NUM_DAILY_UPDATED_KEYS = 5_000_000.0
NUM_DAILY_TEN_MIN_EPOCHS = 24 * 6
STATE_SIZE = 64
NUM_DAYS_IN_ONE_YEAR = 366
PARAKEET = "Parakeet"
SEEMLESS = "SEEMless"

LOG_FILE_PREFIX = ".simulated_storage_"


def get_log_file_name(solution_name, multi_year):
    year_suffix = "one_year"
    if multi_year:
        year_suffix = "multi_year"
    return LOG_FILE_PREFIX + solution_name + "_" + year_suffix + ".csv"


def get_csv_writer(solution_name, multi_year):
    log_file_name = get_log_file_name(solution_name, multi_year)
    log_file = open(log_file_name, "w")
    csv_writer = csv.writer(log_file)
    write_header(csv_writer)
    return csv_writer


def write_header(csv_writer):
    title = ["Epochs per day", "Storage size required"]
    csv_writer.writerow(title)


def get_storage(
    solution_name,
    num_starting_keys,
    num_epoch,
    num_new_key_per_ep,
    num_updated_key_per_ep,
    state_size,
):
    storage_needed = 0
    if solution_name == SEEMLESS:
        storage_needed = calculate_seemless_storage(
            num_starting_keys,
            num_epoch,
            num_new_key_per_ep,
            num_updated_key_per_ep,
            state_size,
        )
    elif solution_name == PARAKEET:
        storage_needed = calculate_parakeet_storage(
            num_starting_keys,
            num_epoch,
            num_new_key_per_ep,
            num_updated_key_per_ep,
            state_size,
        )
    else:
        print("Uknown solution name: " + solution_name)
        sys.exit(-1)
    return storage_needed


def write_storage_row(csv_writer, num_years, num_epochs, storage_gb):
    csv_writer.writerow([num_years, num_epochs, storage_gb])


# Vary the number of epochs per day over a year
def storage_one_year_varying_epochs(solution_name, csv_writer):
    for epoch_per_day in EPOCHS_PER_DAY:
        epochs_in_a_year = NUM_DAYS_IN_ONE_YEAR * epoch_per_day
        new_keys_per_epoch = NUM_DAILY_NEW_KEYS / epoch_per_day
        updated_keys_per_epoch = NUM_DAILY_UPDATED_KEYS / epoch_per_day
        storage_needed = get_storage(
            solution_name,
            NUM_STARTING_KEYS,
            epochs_in_a_year,
            new_keys_per_epoch,
            updated_keys_per_epoch,
            STATE_SIZE,
        )
        print(
            solution_name
            + " storage over a year with "
            + str(epochs_in_a_year)
            + " epochs: "
            + str(storage_needed)
            + "GB"
        )
        write_storage_row(csv_writer, 1, epochs_in_a_year, storage_needed)


def storage_over_multiple_years(solution_name, csv_writer):
    storage_needed = 0
    for years in NUMBER_OF_YEARS:
        num_ten_minute_epochs = years * NUM_DAYS_IN_ONE_YEAR * NUM_DAILY_TEN_MIN_EPOCHS
        new_keys_per_epoch = NUM_DAILY_NEW_KEYS / NUM_DAILY_TEN_MIN_EPOCHS
        updated_keys_per_epoch = NUM_DAILY_UPDATED_KEYS / NUM_DAILY_TEN_MIN_EPOCHS
        storage_needed = get_storage(
            solution_name,
            NUM_STARTING_KEYS,
            num_ten_minute_epochs,
            new_keys_per_epoch,
            updated_keys_per_epoch,
            STATE_SIZE,
        )
        print(
            solution_name
            + " storage over "
            + str(years)
            + " years with "
            + str(num_ten_minute_epochs)
            + " epochs: "
            + str(storage_needed)
            + "GB"
        )
        write_storage_row(csv_writer, years, num_ten_minute_epochs, storage_needed)


def main():
    # Calculate and log storage costs over one year.
    seemless_csv_writer = get_csv_writer(SEEMLESS, False)
    parakeet_csv_writer = get_csv_writer(PARAKEET, False)
    storage_one_year_varying_epochs(SEEMLESS, seemless_csv_writer)
    storage_one_year_varying_epochs(PARAKEET, parakeet_csv_writer)

    # Calcualte and log storage costs over multiple years.
    seemless_csv_writer = get_csv_writer(SEEMLESS, True)
    parakeet_csv_writer = get_csv_writer(PARAKEET, True)
    storage_over_multiple_years(SEEMLESS, seemless_csv_writer)
    storage_over_multiple_years(PARAKEET, parakeet_csv_writer)


if __name__ == "__main__":
    main()


# # Vary the number of epochs per day over a year
# file_seemless_one_yr = open("./simulated_storage/seemless_one_year.csv", "w")
# writer_seemless_one_yr = csv.writer(file_seemless_one_yr)


# for num_epochs in num_epochs_per_day:
#     print("**********************************")
#     print(
#         "SEEMless storage for "
#         + str(epochs)
#         + " ep/day over a year, with 10M/day keys inserted"
#     )
#     storage_needed = calculate_seemless_storage(
#         NUM_STARTING_KEYS, 366 * num_epochs, NUM_DAILY_NEW_KEYS / epochs, NUM_DAILY_UPDATED_KEYS / epochs, 64.0
#     )
#     writer_seemless_one_yr.writerow([num_epochs, storage_needed])
# file_seemless_one_yr.close()


# file_seemless_mult_yr = open("./simulated_storage/seemless_one_year.csv", "w")
# writer_seemless_mult_yr = csv.writer(file_seemless_mult_yr)
# title = ["Number of years", "Storage size required"]
# for years in number_of_years:
#     print("**********************************")
#     print(
#         "SEEMless storage for "
#         + str(24 * 6)
#         + " ep/day over"
#         + str(years)
#         + " years, with 10M/day keys inserted"
#     )
#     storage_needed = calculate_seemless_storage(
#         NUM_STARTING_KEYS, years * 366 * 24 * 6, 10000000.0 / (24 * 6), 64.0
#     )
#     writer_seemless_mult_yr.writerow([years, storage_needed])
# file_seemless_mult_yr.close()


# print("**********************************")
# print("**********************************")
# print("**********************************")
# print("**********************************")

# # These should give storage data for parakeet with 10M insertions per day for a year,
# # starting state is 2B keys.
# # Vary the number of epochs per day over a year
# file_parakeet_one_yr = open("./simulated_storage/parakeet_one_year.csv", "w")
# writer_parakeet_one_yr = csv.writer(file_parakeet_one_yr)
# title = ["Epochs per day", "Storage size required"]
# writer_parakeet_one_yr.writerow(title)
# for epochs in epochs_per_day:
#     print("**********************************")
#     print(
#         "Parakeet storage for "
#         + str(epochs)
#         + " ep/day over a year, with 10M/day keys inserted"
#     )
#     calculate_parakeet_storage(2000000000, 366 * epochs, NUM_DAILY_NEW_KEYS / epochs, NUM_DAILY_UPDATED_KEYS / epochs, 64.0)
#     writer_parakeet_one_yr.writerow([epochs, storage_needed])
# file_parakeet_one_yr.close()


# file_parakeet_mult_yr = open("./simulated_storage/seemless_one_year.csv", "w")
# writer_parakeet_mult_yr = csv.writer(file_parakeet_mult_yr)
# title = ["Number of years", "Storage size required"]
# writer_parakeet_mult_yr.writerow(title)
# for years in number_of_years:
#     print("**********************************")
#     print(
#         "Parakeet storage for "
#         + str(24 * 6)
#         + " ep/day over"
#         + str(years)
#         + " years, with 10M/day keys inserted"
#     )
#     calculate_parakeet_storage(
#         2000000000, years * 366 * 24 * 6, 10000000.0 / (24 * 6), 64.0
#     )
#     writer_parakeet_mult_yr.writerow([epochs, storage_needed])
# file_parakeet_mult_yr.close()
