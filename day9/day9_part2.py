file_path = "day9_input/"


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




def basin_finder(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    hm_matrix = [[int(i) for i in line] for line in data.splitlines()]

    #print(hm_matrix)

    # Checks (shifts on [row, col] indices)
    # Check all surrounding heights for inner measurements (clockwise from 12)
    checks = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    basins = []
    nodes_in_any_basin = []
    height_map = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: []
    }
    # First map the locations of the nodes of each height
    for r_index, row in enumerate(hm_matrix):
        for c_index, col in enumerate(row):
            # Height at this point
            this_height = hm_matrix[r_index][c_index]
            # Create node
            this_node = [r_index, c_index]
            # Skip 9s
            if this_height != 9:
                height_map[this_height].append(this_node)

    # Loop through the nodes, starting from the lowest (0s)
    for number in height_map:
        for node in height_map[number]:
            # Check this node isn't in existing basin
            if node not in nodes_in_any_basin:
                # Start a new basin with this node
                new_basin = [node]
                basin_height_map = {
                    0: [],
                    1: [],
                    2: [],
                    3: [],
                    4: [],
                    5: [],
                    6: [],
                    7: [],
                    8: []
                }
                # Check the surrounding nodes for greater heights
                # This node
                r_index = node[0]
                c_index = node[1]
                for check in checks:
                    # Skip if the check index is outside the matrix (ie. this is an edge or corner)
                    check_row = r_index + check[0]
                    check_col = c_index + check[1]
                    if check_row > (len(hm_matrix) - 1) or (0 > check_row):
                        continue
                    elif check_col > (len(hm_matrix[0]) - 1) or (0 > check_col):
                        continue
                    # Create adjacent node
                    adj_node = [check_row, check_col]
                    # Height at adjacent node
                    adj_height = hm_matrix[check_row][check_col]
                    if adj_height == 9:
                        # Skip 9s
                        continue
                    # Skip if already in another basin
                    elif adj_node in nodes_in_any_basin:
                        continue
                    elif adj_height > number:
                        # Add to the basin
                        new_basin.append(adj_node)
                        nodes_in_any_basin.append(adj_node)
                        # Add node to height map for this basin
                        basin_height_map[adj_height].append(adj_node)
                # Run checks for each of the nodes identified in the last round of checks
                for number_b in basin_height_map:
                    for node_b in basin_height_map[number_b]:
                        # Check the surrounding nodes for greater heights
                        # This node
                        r_index_b = node_b[0]
                        c_index_b = node_b[1]
                        for check in checks:
                            # Skip if the check index is outside the matrix (ie. this is an edge or corner)
                            check_row = r_index_b + check[0]
                            check_col = c_index_b + check[1]
                            if check_row > (len(hm_matrix) - 1) or (0 > check_row):
                                continue
                            elif check_col > (len(hm_matrix[0]) - 1) or (0 > check_col):
                                continue
                            # Create adjacent node
                            adj_node = [check_row, check_col]
                            # Height at adjacent node
                            adj_height = hm_matrix[check_row][check_col]
                            if adj_height == 9:
                                # Skip 9s
                                continue
                            # Skip if already in another basin
                            elif adj_node in nodes_in_any_basin:
                                continue
                            elif adj_height > number_b:
                                # Add to the basin
                                new_basin.append(adj_node)
                                nodes_in_any_basin.append(adj_node)
                                # Add node to height map for this basin
                                basin_height_map[adj_height].append(adj_node)
                # Finished mapping this basin
                # Add basin to basins list
                basins.append(new_basin)
                #print(f'Fully mapped basin: {new_basin}')
                #print(f'Basin height map: {basin_height_map}')

    # Find the three largest basins
    #print(basins)
    basin_lengths = []
    for basin in basins:
        basin_lengths.append(len(basin))
        #print(f'Basin Length: {len(basin)}. Basin: {basin}')

    #print(f'Basin lengths sorted: {sorted(basin_lengths, reverse=True)}')
    longest = sorted(basin_lengths, reverse=True)[0]
    sec_long = sorted(basin_lengths, reverse=True)[1]
    thir_long = sorted(basin_lengths, reverse=True)[2]

    answer = longest * sec_long * thir_long

    print(f'Answer is: {answer}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    basin_finder("heightmap")
