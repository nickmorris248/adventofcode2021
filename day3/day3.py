
file_path = "day3_input/"


def calc_power_consumption(file_name):
    binary_1s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    binary_0s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        lines = f.readlines()

    for line_txt in lines:
        line_txt = line_txt.rstrip('\n')
        # Loop through characters in line
        char_index = -1
        for char in line_txt:
            char_index += 1
            if char == '1':
                binary_1s[char_index] += 1
            elif char == '0':
                binary_0s[char_index] += 1

    print(binary_1s)
    print(binary_0s)

    gamma_lst = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    epsilon_lst = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Compare totals and create lists to represent gamma and epsilon
    char_index = -1
    for a, b in zip(binary_1s, binary_0s):
        char_index += 1
        if a > b:
            gamma_lst[char_index] = 1
            epsilon_lst[char_index] = 0
        elif b > a:
            gamma_lst[char_index] = 0
            epsilon_lst[char_index] = 1

    print(gamma_lst)
    print(epsilon_lst)

    # Join lists into strings then convert to binary then convert to int
    gamma_str = "".join(map(str, gamma_lst))
    gamma_int = int(gamma_str, 2)

    epsilon_lst = "".join(map(str, epsilon_lst))
    epsilon_int = int(epsilon_lst, 2)

    # Calculate answer
    print(gamma_int * epsilon_int)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    calc_power_consumption("diagnostic")


