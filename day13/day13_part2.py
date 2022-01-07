file_path = "day13_input/"


def counting_dots(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    page_contents = data.split('\n\n')

    #print(page_contents[1])

    dots = [[int(i) for i in line.split(',')] for line in page_contents[0].splitlines()]

    print(dots)

    part2 = [line.strip('fold along') for line in page_contents[1].splitlines()]

    print(part2)

    fold_ins = [line.split('=') for line in part2]

    print(fold_ins)

    new_dots_list = []
    num_dots = 0
    # Loop through fold instructions
    for instruction in fold_ins:

        # Determine fold location
        fold_loc = int(instruction[1])

        # Loop through coordinates and modify based on fold instruction
        for dot in dots:
            x = dot[0]
            y = dot[1]

            # Determine fold direction
            if instruction[0] == 'y':
                # We're folding up
                loc = y
                y_shift = (loc - fold_loc) * 2
                x_shift = 0
            elif instruction[0] == 'x':
                # Folding left
                loc = x
                y_shift = 0
                x_shift = (loc - fold_loc) * 2
            else:
                loc = ''
                x_shift = ''
                y_shift = ''
                raise AssertionError(f'Invalid fold axis: {instruction[0]}')

            # Dot will shift if it's x or y coord number is higher than the fold location
            # (putting it below the fold for y and to the right of the fold for x)
            if loc < fold_loc:
                # Dot is above the fold and stays where it is. Add to new list
                add_dot = dot
            elif loc > fold_loc:
                add_dot = [x - x_shift, y - y_shift]
            else:
                add_dot = []
                raise AssertionError(f'Dot ({dot}) on fold line: {fold_loc}')

            # Add dot
            if add_dot not in new_dots_list:
                new_dots_list.append(add_dot)

        # Number of dots now
        num_dots = len(new_dots_list)
        dots = new_dots_list

    print(num_dots)
    #print(sorted(new_dots_list))

    # Print dots on page
    print('print stage')
    matrix_dots = []
    for final_dot in new_dots_list:
        x_value = final_dot[0]
        y_value = final_dot[1]
        if y_value > len(matrix_dots):
            # Strings to add
            add_lines = ['' for i in range(y_value - len(matrix_dots) + 1)]
            matrix_dots += add_lines
            print(add_lines)

        print(f'Checking: y_value: {y_value}, len(matrix_dots): {len(matrix_dots)}')
        if x_value > len(matrix_dots[y_value]):
            extension = "".join([' ' for i in range(x_value - len(matrix_dots[y_value]))])
            extension += '#'
            matrix_dots[y_value] += extension
        else:
            new_line = matrix_dots[y_value][:x_value] + '#' + matrix_dots[y_value][x_value + 1:]
            matrix_dots[y_value] = new_line
            #print(extension)

    for line in matrix_dots[:100]:
        print(line[:100])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    counting_dots("manual_page")
