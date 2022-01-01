file_path = "day14_input/"


def polymer_generator(file_name, steps):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    # Extracting and formatting data
    page_contents = data.split('\n\n')
    template_list = [i for i in page_contents[0]]
    print(template_list)
    rules_list = [[i for i in line.split(' -> ')] for line in page_contents[1].splitlines()]
    rules_dict = {k: v for k, v in rules_list}
    # d = {i: True for i in [1,2,3]}
    # mydict = {k: v for k, v in iterable}

    print(rules_dict)
    current_template_list = template_list
    for step in range(steps):
        new_template_list = []
        for idx, singular in enumerate(current_template_list):
            if idx == len(current_template_list) - 1:
                new_template_list += [singular]
                break
            else:
                char0 = current_template_list[idx]
                char1 = current_template_list[idx + 1]
                #print(f'Char0: {char0}, Char01: {char1}')
                this_pair = "".join([char0, char1])
                #print(f'Joined pair: {this_pair}')
                if this_pair in rules_dict:
                    #print(f'New template list before adding: {new_template_list}')
                    new_template_list += [char0, rules_dict[this_pair]]
                    #print(f'New template list AFTER adding: {new_template_list}')

        current_template_list = new_template_list
        #print(current_template_list)

    # Calculate answer
    letter_counts = {}
    for val in current_template_list:
        if val not in letter_counts:
            letter_counts[val] = current_template_list.count(val)

    print(letter_counts)

    max_value = max(letter_counts.values())
    min_value = min(letter_counts.values())

    answer = max_value - min_value

    print(answer)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    polymer_generator("example", 10)
