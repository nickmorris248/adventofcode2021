file_path = "day9_input/"


def basin_finder(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    count = 0
    hm_matrix = [[int(i) for i in line] for line in data.splitlines()]

    print(hm_matrix)

    # Checks (shifts on [row, col] indices)
    # Check all surrounding heights for inner measurements (clockwise from 12)
    inner = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    basins = []
    # Loop through heights
    for r_index, row in enumerate(hm_matrix):
        for c_index, col in enumerate(row):
            # Height at this point
            this_height = hm_matrix[r_index][c_index]
            # Nine's aren't in any basins so skip if this is a nine
            if this_height == 9:
                continue
            lower_than_all_adj = True
            # Create node
            this_node = [r_index, c_index]
            # Check adjacent heights
            for check in inner:
                # Skip if the check index is outside the matrix (ie. this is an edge or corner)
                check_row = r_index + check[0]
                check_col = c_index + check[1]
                # Create adjacent node
                adj_node = [check_row, check_col]
                if check_row > (len(hm_matrix) - 1) or (0 > check_row):
                    continue
                elif check_col > (len(row) - 1) or (0 > check_col):
                    continue
                # If an adjacent node is lower, add both this node and the adjacent one to a basin
                elif this_height > hm_matrix[check_row][check_col]:
                    adj_height = hm_matrix[check_row][check_col]
                    #print(f'New basin node found at {adj_node}. Height: {adj_height}')
                    #print(f'This node ({this_node}) height: {this_height}')
                    lower_than_all_adj = False
                    # Check if either nodes are in an existing basin
                    create_new_basin = True
                    if len(basins) > 0:
                        for basin in basins:
                            #print(f'Checking if {this_node} or {adj_node} are in {basin}')
                            if (this_node in basin) or (adj_node in basin):
                                #print('Yes, one of them is')
                                # Don't need to create a new basin
                                create_new_basin = False
                                # Add the extra node to the existing basin
                                if this_node not in basin:
                                    basin.append(this_node)
                                if adj_node not in basin:
                                    basin.append(adj_node)
                    else:
                        create_new_basin = True

                    if create_new_basin:
                        # Add these two nodes to a new basin
                        new_basin = [this_node, adj_node]
                        # Add this basin to the basins list
                        basins.append(new_basin)
                        #print(f'New basin created: {new_basin}')
                else:
                    # Remains a candidate for 'lower than all adj'
                    pass

            if lower_than_all_adj:
                # Create a new basin of one
                #new_basin_of_one = [this_node]
                # Add this basin to the list
                #basins.append(new_basin_of_one)
                pass

    # Consolidated any basins with common nodes
    # Outer loop of basins
    for ind_ol, basin_ol in enumerate(basins):
        for node in basin_ol:
            # Inner loop of basins
            for ind_il, basin_il in enumerate(basins):
                # Check if this node is in another basin
                # Skip the basin this node is already in
                if ind_il == ind_ol:
                    continue
                elif node in basin_il:
                    #print(f'Found node ({node}) from basin {basin_ol} in basin {basin_il}')
                    # These basins have common nodes and should be combined
                    combined_basin = basin_ol.copy()
                    for combining_node in basin_il:
                        if combining_node not in combined_basin:
                            combined_basin.append(combining_node)
                    # Remove the old basins
                    #print(f'Number of basins before deleting old 1: {len(basins)}')
                    if basin_ol in basins:
                        basins.remove(basin_ol)
                    #print(f'Number of basins before deleting old 2: {len(basins)}')
                    if basin_il in basins:
                        basins.remove(basin_il)
                    # Add the new combined basin
                    #print(f'Number of basins before adding combined: {len(basins)}')
                    if combined_basin not in basins:
                        basins.append(combined_basin)
                    #print(f'Number of basins after adding combined: {len(basins)}')

    # Find the three largest basins
    #print(basins)
    basin_lengths = []
    for basin in basins:
        basin_lengths.append(len(basin))
        #print(f'Basin Length: {len(basin)}. Basin: {basin}')

    print(f'Basin lengths sorted: {sorted(basin_lengths, reverse=True)}')
    longest = sorted(basin_lengths, reverse=True)[0]
    sec_long = sorted(basin_lengths, reverse=True)[1]
    thir_long = sorted(basin_lengths, reverse=True)[2]

    answer = longest * sec_long * thir_long

    print(f'Answer is: {answer}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    basin_finder("heightmap")
