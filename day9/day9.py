file_path = "day9_input/"


def heightmap_risks(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    count = 0
    hm_matrix = [[int(i) for i in line] for line in data.splitlines()]

    print(hm_matrix)

    # Checks (shifts on [row, col] indices)
    # Check all surrounding heights for inner measurements (clockwise from 12)
    inner = [[-1, 0], [0, 1], [1, 0], [0, -1]]

    risk_level_total = 0
    # Loop through heights
    for r_index, row in enumerate(hm_matrix):
        for c_index, col in enumerate(row):
            # Check adjacent heights
            this_height = hm_matrix[r_index][c_index]
            higher_than_adj = False
            for check in inner:
                # Skip if the check index is outside the matrix (ie. this is an edge or corner)
                check_row = r_index + check[0]
                check_col = c_index + check[1]
                if check_row > (len(hm_matrix) - 1) or (0 > check_row):
                    continue
                elif check_col > (len(row) - 1) or (0 > check_col):
                    continue
                # Stop checking if any of the adjacent heights are lower
                elif this_height >= hm_matrix[check_row][check_col]:
                    higher_than_adj = True
                    break
                else:
                    # This is a candidate for lowest in this check group
                    #print(f'This height ({this_height}) is lower than this check ({hm_matrix[check_row][check_col]})')
                    pass
            # If this height is lower than all adjacent, add the risk level to the running total
            if not higher_than_adj:
                risk_level = this_height + 1
                #print(f'Found low height at Row: {r_index}, Col: {c_index}: {this_height}')
                risk_level_total += risk_level

    print(f'Answer is: {risk_level_total}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    heightmap_risks("heightmap")
