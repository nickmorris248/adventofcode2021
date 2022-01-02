file_path = "day15_input/"


def lowest_neighbours(node, value_map, option, paths, current_path_id):
    # Skip nodes that are already in our current path
    current_path_nodes = paths[current_path_id][1]
    lowest_neighbour_coords = []
    #print(f'Checking lowest neighbours from: {node}')
    # Checking shifts required
    check_up = [0, -1]
    check_right = [1, 0]
    check_down = [0, 1]
    check_left = [-1, 0]
    # Determine checking options
    if option == 'all':
        checks = [check_up, check_right, check_down, check_left]
    elif option == 'RD':
        checks = [check_right, check_down]
    else:
        raise AssertionError(f'Invalid checking option: {option}')

    lowest_this_check = 10
    for check in checks:
        x_value = node[0] + check[0]
        y_value = node[1] + check[1]

        # Use try except to deal with corners and edges (ala Tim)
        try:
            checking_node_value = value_map[y_value][x_value]
            #print(f'Checking value: {checking_node_value}')
            checked_node_coords = [x_value, y_value]
            if checked_node_coords not in current_path_nodes:
                if checking_node_value < lowest_this_check:
                    lowest_this_check = checking_node_value
                    lowest_neighbour_coords = [checked_node_coords]
                elif checking_node_value == lowest_this_check:
                    lowest_neighbour_coords.append(checked_node_coords)

        except IndexError:
            pass

    #print(f'Lowest value found: {lowest_this_check}')
    return lowest_neighbour_coords


def calculate_tri_avg(start_node, risk_map):
    # print
    #print(f'Calc. Avg. from node: {start_node}')
    # Checking shifts required
    check_right = [1, 0]
    check_down = [0, 1]
    checks = [check_right, check_down]
    start_node_value = risk_map[start_node[1]][start_node[0]]
    values = [start_node_value]
    for check in checks:
        x_value = start_node[0] + check[1]
        y_value = start_node[1] + check[0]
        # Use try except to deal with corners and edges (ala Tim)
        try:
            checking_node_value = risk_map[y_value][x_value]
            values.append(checking_node_value)
            #print(f'Node value: {checking_node_value} (from y: {y_value} & x: {x_value}')

        except IndexError:
            pass

    # Calculate the average

    average = sum(values) / len(values)

    return round(average, 1)


def path_finder(file_name, look_ahead, strategy):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    # Extracting and formatting data
    risk_map = [[int(i) for i in line] for line in data.splitlines()]
    #print(risk_map)

    # Create a new map with each value replaced by the average of
    # that value, the one to the right and the one below in the old map
    tri_avg_risk_map = []
    for ridx, row in enumerate(risk_map):
        new_row = []
        for nidx, node in enumerate(row):
            start_node = [nidx, ridx]
            new_node = calculate_tri_avg(start_node, risk_map)
            new_row.append(new_node)
        tri_avg_risk_map.append(new_row)

    # Print new map
    for row in tri_avg_risk_map:
        print(row)

    # Explore paths
    target_node = [len(risk_map[0]) - 1, len(risk_map) - 1]
    finished_paths = []
    paths = {}
    nodes_to_check = [[[0, 0], '1']]  # Starting node and starting path number string
    starting_node_value = risk_map[0][0]
    paths['1'] = [0, [[0, 0]]]
    current_min_risk = 10000000000
    for node_record in nodes_to_check:
        #print(f'\nNodes to check: {nodes_to_check}')
        # Unpack node record
        current_path_id = node_record[1]
        current_path_nodes_list = paths[current_path_id][1].copy()
        current_path_risk_total = paths[current_path_id][0]
        node = node_record[0]
        #print(f'Node: {node}')
        #print(f'Current path id: {current_path_id}')
        #print(f'Current path in paths dict: \n{paths[current_path_id]}')

        # The map used for looking up the next value depends on the strategy
        if strategy == 'tri_avg':
            lookup_map = tri_avg_risk_map
            check_option = 'RD'
        elif strategy == 'normal':
            lookup_map = risk_map
            check_option = 'all'
        else:
            raise AssertionError(f'Invalid strategy: {strategy}')

        # Determine the next node in the path
        next_node = lowest_neighbours(node, lookup_map, check_option, paths, current_path_id)
        #print(f'Next_node result: {next_node}')
        # Determine how many options
        if len(next_node) == 0:
            # Is this the target node
            if next_node == target_node:
                raise AssertionError(f'Reached target node error')
            else:
                continue
                #raise AssertionError(f'Next node not found')
        for idx_paths, path_option in enumerate(next_node):
            option_no = idx_paths
            # For this first option, add it to the existing path
            if option_no == 0:
                # Add this node to the end of the existing path id
                paths[current_path_id][1].append(path_option)
                #print(f'Adding node ({path_option}) to path id: {current_path_id}')
                #print(f'Updated path in paths dict: \n{paths[current_path_id]}')
                # Risk value for this node
                next_node_risk = risk_map[path_option[1]][path_option[0]]
                #print(f'Adding next node risk of: {next_node_risk}')
                # Add to the total risk score for this path
                paths[current_path_id][0] += next_node_risk
                #print(f'Risk total for this path now: {paths[current_path_id][0]}')
                if path_option == target_node:
                    # Add this path id to the finished paths list
                    finished_paths.append(current_path_id)
                    #print(f'Finished path found. ID: {current_path_id}\n'
                    #      f'Risk: {paths[current_path_id][0]}')
                    total_risk_finished_path = paths[current_path_id][0]
                    if total_risk_finished_path < current_min_risk:
                        print(f'New min risk found: {total_risk_finished_path}')
                        current_min_risk = total_risk_finished_path
                else:
                    # Add new node to the list of nodes to process
                    nodes_to_check.append([path_option, current_path_id])
                    #print(f'Updated nodes to check: {nodes_to_check}')
            else:
                # Create new paths for the forking options
                next_node_risk = risk_map[path_option[1]][path_option[0]]
                new_path_id = current_path_id + str(option_no)
                # Check that this path id isn't already being used
                new_id = False
                add_option_no = 0
                while not new_id:
                    add_option_no += 1
                    if new_path_id in paths:
                        new_path_id = new_path_id + str(add_option_no)
                    else:
                        new_id = True
                new_path_nodes_list = current_path_nodes_list
                new_path_nodes_list.append(path_option)
                new_path_risk_total = current_path_risk_total + next_node_risk
                paths[new_path_id] = [new_path_risk_total, new_path_nodes_list]
                # Check if this is the end node
                if path_option == target_node:
                    # Add this path id to the finished paths list
                    finished_paths.append(new_path_id)
                    total_risk_finished_path = paths[new_path_id][0]
                    if total_risk_finished_path < current_min_risk:
                        print(f'New min risk found: {total_risk_finished_path}')
                        current_min_risk = total_risk_finished_path
                else:
                    # Add the new node to the end of the list of nodes to process
                    nodes_to_check.append([path_option, new_path_id])
                #print(f'Adding node ({path_option}) to path id: {new_path_id}')
                #print(f'Updated path in paths dict: \n{paths[new_path_id]}')

    # Print finished paths and results
    min_risk = paths[finished_paths[0]][0]
    for idx, finished_path in enumerate(finished_paths):
        total_risk = paths[finished_path][0]
        path_nodes_list = paths[finished_path][1]
        print(f'Finished Path #{idx + 1}: Length: {len(path_nodes_list)}, Total risk: {total_risk}')
        print(f'Finished path nodes: {path_nodes_list}')
        if total_risk < min_risk:
            min_risk = total_risk

    print(f'\n\nAnswer: {min_risk}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path_finder("example", 2, 'normal')
