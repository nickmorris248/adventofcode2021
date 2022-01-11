file_path = "day18_input/"


def magnify_number(snail_number):

    line_answer = snail_number

    # Magnitude calculation
    magnifying = True
    magnifying_loop_count = 0
    while magnifying:
        magnifying_loop_count += 1
        magnitude_progress = []
        char_restart_at = 0
        for idx_char, char in enumerate(line_answer):
            # Look for pattern: [ int , int ]
            if idx_char < char_restart_at:
                continue

            if idx_char + 5 <= len(line_answer):
                char0 = char
                char1 = line_answer[idx_char + 1]
                char2 = line_answer[idx_char + 2]
                char3 = line_answer[idx_char + 3]
                char4 = line_answer[idx_char + 4]
                print(f'Inspecting chars: {char0} {char1} {char2} {char3} {char4}')
                if char0 == "[" and str(char1).isdigit() and char2 == "," and str(char3).isdigit() and char4 == "]":
                    print(f'Pair found')
                    mag_num = (char1 * 3) + (char3 * 2)
                    print(f'Mag num: {mag_num}')
                    magnitude_progress.append(mag_num)

                    char_restart_at = idx_char + 5

                else:
                    magnitude_progress.append(char)
            else:
                magnitude_progress.append(char)

            print(f'Mag progress: {"".join(str(i) for i in magnitude_progress)}')

        line_answer = magnitude_progress
        print("".join(str(i) for i in line_answer))
        if len(line_answer) == 1:
            magnifying = False

    print(f'\nFinal magnified number: {line_answer[0]}')

    return line_answer[0]


def snail_maths_solver(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    # explosion test strings

    homework_lines = [[i for i in line] for line in data.splitlines()]

    print(f'Homework lines: {homework_lines}')

    # Convert numbers into numbers

    number_s = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    homework = []
    for idx_line, line in enumerate(homework_lines):
        list_depth = 0
        new_line = []
        n_start = int
        char_restart_at = 0
        for idx_char, char in enumerate(line):
            #print(f'Line: {line}')
            #print(f'char restart at: {char_restart_at}')
            if idx_char < char_restart_at:
                continue
            elif char in number_s:
                #print(f'Char ({char}) detected in: {number_s}')
                # Loop through next characters until we have the full number
                new_number_string = ''
                for next_char in line[idx_char:]:
                    if next_char in number_s:
                        new_number_string += next_char
                    else:
                        char_restart_at = idx_char + len(new_number_string)
                        break
                # Create int of the new number string and add to new line list
                new_number_int = int(new_number_string)
                new_line.append(new_number_int)
            else:
                new_line.append(char)
        homework.append(new_line)

    print(f'Homework with ints: {homework}')

    added_line = []
    exploded_line = []
    largest_mag = 0

    for idx_line, snail_num in enumerate(homework):
        print(f'idx_line: {idx_line}')

        for adding_num in homework:
            # Addition step

            # Skip the same number so its not being added to itself
            if adding_num == snail_num:
                continue

            added_line = ["["] + snail_num + [","] + adding_num + ["]"]
            print(f'Snail Num: {"".join(str(i) for i in snail_num)}\n'
                  f'Adding this line: {"".join(str(i) for i in adding_num)}')

            print(f'Added line: {"".join(str(i) for i in added_line)}')

            # Loop until no more actions possible/needed
            line_not_finished = True
            line_not_finshed_loop_no = 0
            line = added_line
            while line_not_finished:
                line_not_finshed_loop_no += 1
                #print(f'Line not finished loop #: {line_not_finshed_loop_no}')
                #print('Starting "while line not finished" while loop')
                # Starting with explosion actions
                exploding = True
                new_line_p = []
                exploding_loop_no = 0
                #print('Exploding while loop')
                while exploding:
                    exploding_loop_no += 1
                    #print(f'Exploding loop #: {exploding_loop_no}')

                    finish_len = len(line) - 1

                    list_depth = 1
                    last_num = (-1, -1)
                    new_line_p = []
                    new_line_created = False
                    #print(f'Iterating this line: {line}')
                    #print('Exploding loop')
                    for idx_char, char in enumerate(line):
                        #print(f'Exploding idx_char: {idx_char}')

                        # If list depth is 4, prepare to explode inner pair
                        #print(f'Char this loop ({char}). Index: {idx_char}. List depth: {list_depth}')
                        if list_depth > 5:
                            # Check if this is the inner most pair by checking for the pattern: int , int
                            if (len(line) > idx_char + 2) and (str(char).isdigit()) and (line[idx_char + 1] == ",") and (str(line[idx_char + 2]).isdigit()):
                                # Explode this pair
                                if last_num[0] > -1:
                                    # There is a number to the left. The left number of the exploding pair should be added to it
                                    new_line_p = line[:last_num[1]]
                                    new_line_p.append(last_num[0] + char)
                                    inbetween_chars = line[last_num[1] + 1:idx_char - 1]
                                    new_line_p += inbetween_chars
                                    new_line_p.append(0)
                                else:
                                    # There is no number to the left.
                                    new_line_p = line[:idx_char - 1]
                                    #print(f'New line p: {new_line_p}')
                                    #print(f'Idx char" {idx_char}')
                                    # Add a '0' to replace the pair being exploded
                                    new_line_p.append(0)

                                # Start secondary loop to find the number to the right and finish the explosion process
                                rest_of_line = line[idx_char + 4:].copy()
                                #print(f'Secondary loop: looper over: {rest_of_line}')
                                for idx_nnchar, nn_char in enumerate(rest_of_line):
                                    #print(f'nnchar ({nn_char}) in rest of line: {rest_of_line}')
                                    if str(nn_char).isdigit():
                                        # Add the right number from the exploding pair to this number and add it to the new line
                                        new_line_p.append(line[idx_char + 2] + nn_char)
                                        new_line_p += line[idx_char + 4 + idx_nnchar + 1:]
                                        new_line_created = True
                                        break
                                    else:
                                        new_line_p.append(nn_char)

                        # Break the for loop but not the while loop
                        # Start a new while loop to check if another explosion action is possible
                        if new_line_created:
                            break

                        # Update list depth
                        # (do after list depth check)
                        if char == "[":
                            list_depth += 1
                        elif char == "]":
                            list_depth -= 1

                        # If this is a number set it as the last number for the next round
                        if str(char).isdigit():
                            last_num = (char, idx_char)


                    # If the for loop is finished without a new line being created
                    # that means that no more explosion actions are possible so we move
                    # onto the splitting actions
                    if not new_line_created:
                        exploding = False
                        #print(f'Not new line created. New line p: {new_line_p}')
                        exploded_line = new_line_p.copy()
                    else:
                        line = new_line_p

                    if len(new_line_p) > 0:
                        exploded_line = new_line_p
                    else:
                        exploded_line = line
                    #print("".join(str(i) for i in new_line_p))


                # Do splitting actions
                split_this_round = False
                new_line_p2 = []
                #print(f'Starting splitting actions')
                #print(exploded_line)
                #print('Splitting...')
                #print(f'Exploded line: {exploded_line}')
                for idx_char_sp, char in enumerate(exploded_line):
                    #print(f'Splitting idx_char: {idx_char}')
                    #print(f'Looping: {char}')
                    if str(char).isdigit() and char > 9:
                        # Begin splitting action
                        new_pair = ["[", char // 2, ",", (char + 2 - 1) // 2, "]"]
                        #print(f'Number over ten: {char}. Split into new pair: {new_pair}')
                        # Recreate the line
                        #print(f'Line we are splitting: {"".join(str(i) for i in exploded_line)}')
                        new_line_p2 = exploded_line[:idx_char_sp] + new_pair + exploded_line[idx_char_sp + 1:]
                        line = new_line_p2
                        split_this_round = True
                        exploding = True
                        break

                print("".join(str(i) for i in new_line_p2))

                # Determine if the line has finished adding now
                if (not exploding) and (not split_this_round):
                    line_not_finished = False

                # Debugging
                """if line_not_finshed_loop_no == 3:
                    pass"""

            if len(new_line_p) > 0:
                line_answer = new_line_p
            else:
                line_answer = line
            print(f'\nResults for last finished addition:\n{"".join(str(i) for i in line_answer)}\n')

            """# Debugging
            check_gone = input('Ready to continue? (y = Yes): ')
            if check_gone in ('y', 'Y'):
                pass
            else:
                exit()"""

            print(f'Final result: {"".join(str(i) for i in line_answer)}')

            magnified_number = magnify_number(line_answer)

            if magnified_number > largest_mag:
                largest_mag = magnified_number

    print(f'Largest Magnitude: {largest_mag}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    snail_maths_solver("maths_homework")


