
file_path = "day1/day1_input/"


def count_increases(file_name):
    count = -1  # as first measurement will be more than 0
    prev_no = 0
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        lines = f.readlines()
        for line_txt in lines:
            line_txt = line_txt.rstrip('\n')
            line_as_num = int(line_txt)
            # Check
            print(f'Prev no: {prev_no}')
            print(f'This no: {line_as_num}')
            # Compare and count
            if line_as_num > prev_no:
                count += 1
                print('Result: Increase')
                print(f'Count: {count}')
            else:
                print('Result: No Increase')
                print(f'Count: {count}')
            # Set prev_no for next loop
            prev_no = line_as_num
    print(count)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    count_increases("measurements")


