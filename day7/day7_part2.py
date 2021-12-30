file_path = "day7_input/"


def calculate_fuel(target, positions_list):
    total_fuel = 0

    # My original calculation

    """for sub in positions_list:
        distance = abs(sub - target)
        fuel_increments = [i for i in range(int(distance + 1))]
        fuel_required = sum(fuel_increments)
        total_fuel += fuel_required"""

    # Calculation optimised for speed, taken from Jay:
    # https://github.com/PythonForForex/advent-of-code-2021/blob/main/day7.py

    total_fuel = sum([abs(target - start_pos) * (abs(target - start_pos) + 1) / 2 for start_pos in positions_list])

    return total_fuel


def align_crabs(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    starting_positions = [int(i) for i in data.split(',')]
    #print(f'Starting positions: {starting_positions}')
    starting_positions.sort()
    #print(f'Sorted: {starting_positions}')
    # Possible positions
    possible = [i for i in range(starting_positions[-1] + 1)]
    #print(possible)

    eval_list = possible
    results = []
    searching = True
    test_round = 0
    results_this_round = []
    while searching:
        #print(f'Starting list: {starting_positions}')

        # Create Eval List for this round
        # If its the first round, use the whole list
        if len(results) == 0:
            eval_list = possible
        else:
            # Determine which guess from the last round was the lowest
            min_fuel_last_round = min(results_this_round)

            # Set the new eval list centred on the best guess from last round
            if min_fuel_last_round == min_fuel:
                eval_list = eval_list[minimum:lower + 1]
            elif min_fuel_last_round == low_fuel:
                eval_list = eval_list[minimum:middle + 1]
            elif min_fuel_last_round == mid_fuel:
                eval_list = eval_list[lower:upper + 1]
            elif min_fuel_last_round == up_fuel:
                eval_list = eval_list[middle:]
            elif min_fuel_last_round == max_fuel:
                eval_list = eval_list[upper:]
            else:
                pass
                #print('Unexpected result of choosing eval list round 2+')

        #print(f'Eval list: {eval_list}')

        # Guess Indices
        length = len(eval_list)
        middle = length // 2
        lower = length // 4
        upper = middle + lower
        minimum = 0
        maximum = length - 1

        guess_ind = [minimum, lower, middle, upper, maximum]

        # Minimum
        min_value = eval_list[minimum]
        min_fuel = calculate_fuel(min_value, starting_positions)
        #print(f'Lowest Position Fuel: {min_fuel}')
        results.append(min_fuel)

        # Lower
        low_value = eval_list[lower]
        low_fuel = calculate_fuel(low_value, starting_positions)
        #print(f'Low Position Fuel: {low_fuel}')
        results.append(low_fuel)

        # Middle
        mid_value = eval_list[middle]
        mid_fuel = calculate_fuel(mid_value, starting_positions)
        #print(f'Middle Position Fuel: {mid_fuel}')
        results.append(mid_fuel)

        # Upper
        up_value = eval_list[upper]
        up_fuel = calculate_fuel(up_value, starting_positions)
        #print(f'Upper Position Fuel: {up_fuel}')
        results.append(up_fuel)

        # Max
        max_value = eval_list[maximum]
        max_fuel = calculate_fuel(max_value, starting_positions)
        #print(f'Maximum Position Fuel: {max_fuel}')
        results.append(max_fuel)

        # Results
        results_this_round = [min_fuel, low_fuel, mid_fuel, up_fuel, max_fuel]
        #print(f'Results so far: {results}')

        # Testing
        if len(eval_list) == 1:
            searching = False
        elif len(eval_list) == 2:
            searching = False
        else:
            test_round += 1

    # Results
    #print(f'All results: {results}')
    best_guess = min(results)
    print(f'\n\nBest guess fuel: {best_guess}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    align_crabs("crab_positions")
