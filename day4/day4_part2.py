
file_path = "day4_input/"


def bingo_winner(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        lines = f.readlines()

    fst_line = True
    board_row = 0
    boards_list = []
    for line_txt in lines:
        line_txt = line_txt.rstrip('\n')
        # The first line is the bingo numbers to be called out
        if fst_line:
            # Convert text string into list
            bingo_nums = line_txt.split(",")
            fst_line = False
            continue
        # Skip blank lines
        elif line_txt == '\n':
            pass

        # The other data are lines of the bingo boards (5 x 5 numbers grid)
        else:
            # Break boards into:
            # Each board has a dict with each row and each col represented in a list and each dict is in a master list
            board_row += 1
            if board_row == 1:
                # Create new board dict
                this_board = {
                    'row1': [[], []],
                    'row2': [[], []],
                    'row3': [[], []],
                    'row4': [[], []],
                    'row5': [[], []],
                    'col1': [[], []],
                    'col2': [[], []],
                    'col3': [[], []],
                    'col4': [[], []],
                    'col5': [[], []],
                }

            # Split row on double space then single space to get list of single numbers
            this_row_lst = []
            fully_split_lst = []
            fst_split = line_txt.split("  ")

            # Second split
            for split_str in fst_split:
                snd_split = split_str.split(" ")
                fully_split_lst += snd_split

            # Clean up empty values
            for value in fully_split_lst:
                if value == '':
                    pass
                else:
                    this_row_lst.append(value)

            # If the row is empty, discard it
            if len(this_row_lst) == 0:
                # Reset board row as a blank line means a break between boards
                board_row = 0
                continue

            # Distribute values amongst rows and cols in dict
            # Add the row
            this_board[f'row{board_row}'][0] = this_row_lst
            col_index = 0
            for num in this_row_lst:
                col_index += 1
                this_board[f'col{col_index}'][0].append(num)

            # If this is the 5th row, the board is complete so put it a way and prepare a new one
            if board_row == 5:
                boards_list.append(this_board)
                board_row = 0

    print(boards_list)

    print(bingo_nums)

    # Iterate through bingo numbers and boards to find the winner

    # Running total of number of boards won
    boards_won = 0
    list_of_boards_won = []
    # Keep track of board progress in the empty lists in each board dict
    no_winner = True
    while no_winner:
        for num in bingo_nums:
            # Iterate through boards
            for board in boards_list:
                # Check if this board has already won
                if board in list_of_boards_won:
                    # Skip it
                    continue
                # Iterate through items in dict
                for value in board:
                    # Check if the bingo number is in this list
                    if num in board[value][0]:
                        # Add value to the 'called' list
                        board[value][1].append(num)
                        # Check if length of called list is now 5
                        if len(board[value][1]) == 5:
                            if board not in list_of_boards_won:
                                boards_won += 1
                            list_of_boards_won.append(board)
                            print(f'Winner #{boards_won} of {len(boards_list)} found')
                            print(f'{value}:\nAll Numbers: {board[value][0]}\nCalled Numbers: {board[value][1]}')
                            print(board)
                            # Check if this is the last board to win
                            if boards_won == len(boards_list):
                                print("Last Winner Found")
                                print(f'{value}:\nAll Numbers: {board[value][0]}\nCalled Numbers: {board[value][1]}')
                                no_winner = False
                                winning_board = board
                                winning_num = num

                if not no_winner:
                    break
            if not no_winner:
                break
        if not no_winner:
            break


    # Calculate final score
    # Iterate through items in dict
    uncalled_numbers_lst = []
    uncalled_numbers_total = 0
    print(winning_board)
    for value in winning_board:
        # Iterate through numbers in the list
        for num in winning_board[value][0]:
            # Check if this value was not called
            if num not in winning_board[value][1]:
                # Add to uncalled numbers list only if not already in the list
                if num not in uncalled_numbers_lst:
                    print(f'Uncalled: {num}')
                    uncalled_numbers_lst.append(num)
                    uncalled_numbers_total += int(num)

    print(uncalled_numbers_lst)
    print(uncalled_numbers_total)
    # Subtract the winning number value from the uncalled value because it will be added due to the
    final_score = uncalled_numbers_total * int(winning_num)

    print(f'Final Score: {final_score}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bingo_winner("bingo")

