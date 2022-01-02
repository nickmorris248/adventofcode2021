file_path = "day15_input/"


def lowest_neighbours(node, risk_map):
    # Checking shifts required
    check_up = [0, -1]
    check_right = [1, 0]
    check_down = [0, 1]
    check_left = [-1, 0]
    checks = [check_up, check_right, check_down, check_left]

    for check in checks:
        x_value = node[0] + check[0]
        y_value = node[1] + check[1]
        lowest_this_check = [10, []]
        # Use try except to deal with corners and edges (ala Tim)
        try:
            checking_node_value = risk_map[y_value][x_value]
            checked_node_coords = [x_value, y_value]
            if checking_node_value < lowest_this_check[0]:
                lowest_this_check[0] = checking_node_value
                lowest_this_check[1] = [checked_node_coords]
            elif checking_node_value == lowest_this_check:
                lowest_this_check[1].append(checked_node_coords)

        except KeyError:
            pass

    return lowest_this_check


def path_finder(file_name, look_ahead):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    # Extracting and formatting data
    risk_map = [[int(i) for i in line] for line in data.splitlines()]
    print(risk_map)


    # Dynamically build path candidates
    results_dict = {}
    nodes_to_process = [[0, 0]]  # Add the starting node (top left corner)
    final_node = [len(risk_map[0]) - 1, len(risk_map) - 1]
    for node in nodes_to_process:
        # Stop when the last node is reached
        if node == final_node:
            # Add the value of this node
            #todo
            break
        # Look ahead a certain number of steps to determine the best path
        from_nodes = [[node, 1]]  # [[node, step#], [node, step#]]
        checked_paths = {}
        looking_ahead = True
        step = 0
        while looking_ahead:
            step += 1
            for from_node_record in from_nodes:
                from_node = from_node_record[0]
                from_node_step = from_node_record[1]
                # Find the lowest node adjacent to this node
                lwst_neighbour = lowest_neighbours(from_node, risk_map)  # [10, []]
                risk_score = lwst_neighbour[0]
                nodes_found = lwst_neighbour[1]
                # Add this result to the checked paths list
                for node_found in nodes_found:
                    # Check if this step # is already in the dict
                    if from_node_step in checked_paths:
                        # Check if this node is already in the
                        if
                if
                else:
                    # Append to open paths in list
                    for path in checked_paths:
                        if
                # Add the new nodes to the 'from nodes' to be analysed on the next step
                for node_found in nodes_found:
                    from_nodes.append(node_found)


            # Change the 'from node' to the lowest value just checked
            #todo



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path_finder("example", 2)
