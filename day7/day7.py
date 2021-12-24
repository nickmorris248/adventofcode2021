file_path = "day7_input/"


def align_crabs(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    starting_positions = [int(i) for i in data.split(',')]

    print(starting_positions)

    n = len(starting_positions)

    avg = sum(starting_positions) / n

    print(f'Average: {avg}')

    # Median
    starting_positions.sort()
    print(starting_positions)
    if n % 2 == 0:
        median1 = starting_positions[n//2]
        median2 = starting_positions[n//2 - 1]
        median = (median1 + median2) / 2
    else:
        median = starting_positions[n//2]

    print(f'Median: {median}')

    # Fuel to reach median
    total_fuel = 0
    for sub in starting_positions:
        fuel_required = abs(sub - median)
        total_fuel += fuel_required

    print(f'Fuel required to reach median: {total_fuel}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    align_crabs("crab_positions")
