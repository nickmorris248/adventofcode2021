
file_path = "day1/day1_input/"


def count_increases(file_name):
    numbers = []
    count_of_increases = 0
    numbers_in_this_running_total = 0
    this_running_total = 0
    prev_running_total = 0
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        lines = f.readlines()
        for line_txt in lines:
            line_txt = line_txt.rstrip('\n')
            line_as_num = int(line_txt)
            numbers.append(line_as_num)
        # Set first running total
        prev_running_total = numbers[0] + numbers[1] + numbers[2]
        # Start at 3rd number of second running count
        this_num_index = 3
        for number in numbers[3:]:
            this_running_total = number + numbers[this_num_index - 1] + numbers[this_num_index - 2]
            # Check
            print(f'This running total: {this_running_total}')
            print(f'Prev. running total: {prev_running_total}')
            # Compare running totals
            if this_running_total > prev_running_total:
                count_of_increases += 1
                print('Result: Increase')
            else:
                print('Result: Non Increase')
            # Pass value of running total
            prev_running_total = this_running_total
            # Increase number index value
            this_num_index += 1

        print(count_of_increases)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    count_increases("measurements")


