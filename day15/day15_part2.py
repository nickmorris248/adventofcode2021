from queue import PriorityQueue

file_path = "day15_input/"


def lowest_neighbours(node, value_map):
    # Results dict
    results_dict = {
        'check_up': [0, []],
        'check_right': [0, []],
        'check_down': [0, []],
        'check_left': [0, []]
    }

    # Checking shifts required
    check_up = [0, -1]
    check_right = [1, 0]
    check_down = [0, 1]
    check_left = [-1, 0]
    # Determine checking options
    checks = [check_up, check_right, check_down, check_left]
    check_names = ['check_up', 'check_right', 'check_down', 'check_left']

    for check, check_name in zip(checks, check_names):
        x_value = node[0] + check[0]
        y_value = node[1] + check[1]


        # Does node exist?
        node_exists = False

        # Use try except to deal with corners and edges (ala Tim)
        try:
            checked_node_coords = [x_value, y_value]
            checking_node_value = value_map[y_value][x_value]
            #print(checking_node_value)
            if checking_node_value > 0:
                node_exists = True

        except IndexError:
            pass

        if node_exists and (x_value >= 0) and (y_value >= 0):
            results_dict[str(check_name)] = [checking_node_value, checked_node_coords]
        else:
            results_dict[str(check_name)] = 'n/a'

            #print(f'Lowest value found: {lowest_this_check}')
    return results_dict


def build_full_map(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    # Extracting and formatting data
    risk_map = [[int(i) for i in line] for line in data.splitlines()]
    for row in risk_map:
        print(row)

    # Building new map
    original_row_length = len(risk_map[0]) - 1
    original_col_length = len(risk_map) - 1
    risk_map_new = []
    for col_tile_no in range(5):
        for r_idx, row in enumerate(risk_map):
            new_row = []
            for tile_no in range(5):
                for c_idx, col in enumerate(row):
                    input_value = risk_map[r_idx][c_idx]
                    new_value = input_value + tile_no + col_tile_no
                    if new_value > 9:
                        new_value -= 9
                    new_row.append(new_value)
            # Add the completed new row to the new risk map
            risk_map_new.append(new_row)

    # Print new risk map
    for row in risk_map_new:
        print(row)

    return risk_map_new


def path_finder(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    # Extracting and formatting data
    risk_map_small = [[int(i) for i in line] for line in data.splitlines()]
    for row in risk_map_small:
        print(row)

    new_risk_map = build_full_map(file_name)

    risk_map = new_risk_map

    # Create dictionary with each node having a ref number
    risk_map_dict = {}
    for r_inx, row in enumerate(risk_map):
        for c_idx, col in enumerate(row):
            node = [c_idx, r_inx]
            risk_map_dict[str(node)] = 1000000000

    #print(risk_map_dict)

    # Starting node is [0, 0] (top left corner) and isn't counted in the risk score so the
    # total assigned to that node in the dict is 0
    starting_node = [0, 0]
    # Add starting node to dict
    risk_map_dict[str(starting_node)] = 0
    nodes_visited = []
    #print(risk_map_dict)
    pq = PriorityQueue()
    pq.put((0, starting_node))

    while not pq.empty():
        (risk, current_node) = pq.get()
        nodes_visited.append(current_node)

        # Check the adjacent nodes
        adj_nodes_dict = lowest_neighbours(current_node, risk_map)
        #print(adj_nodes_dict)
        for adj_node_record in adj_nodes_dict:
            if adj_nodes_dict[adj_node_record] != 'n/a':
                adj_node = adj_nodes_dict[adj_node_record][1]
                current_risk_to_node = risk_map_dict[str(adj_node)]
                pot_new_risk_to_node = adj_nodes_dict[adj_node_record][0] + risk_map_dict[str(current_node)]
                # Compare new score to current score
                if pot_new_risk_to_node < current_risk_to_node:
                    # Update the risk to node value in the dict
                    risk_map_dict[str(adj_node)] = pot_new_risk_to_node
                    # Add adj node to the que for processing
                    pq.put((pot_new_risk_to_node, adj_node))

        #print(risk_map_dict)

    final_node = [len(risk_map[0]) - 1, len(risk_map) - 1]
    risk_to_final_node = risk_map_dict[str(final_node)]
    print(f'\nMinimum risk: {risk_to_final_node}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path_finder("riskmap")
