file_path = "day14_input/"

# Attempted analysis of the data to find patterns but ended up using a much simpler method


def polymer_generator(file_name, steps):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    # Extracting and formatting data
    page_contents = data.split('\n\n')
    template_list = [i for i in page_contents[0]]
    print(template_list)
    print(f'Template: {"".join(template_list)}')
    rules_list = [[i for i in line.split(' -> ')] for line in page_contents[1].splitlines()]
    rules_dict = {k: v for k, v in rules_list}
    # d = {i: True for i in [1,2,3]}
    # mydict = {k: v for k, v in iterable}

    #print(rules_dict)

    # Analysis Stage
    analysis_stage = True
    if analysis_stage:
        # Run through 5 steps with each of the letter pairs from the rules as the starting template and look for patterns
        analysis = rules_dict.keys()
        analysis_template_list = [[char for char in pair] for pair in analysis]
        print(analysis_template_list)
    else:
        analysis_template_list = [1]

    for starting_pair in analysis_template_list:
        if analysis_stage:
            template_list = starting_pair
            print(f'Analysing Pair: {"".join(starting_pair)}')
        current_template_list = template_list
        rules_applied_this_starting_pair = []
        strings_generated = []
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
                        if this_pair not in rules_applied_this_starting_pair:
                            rules_applied_this_starting_pair.append(this_pair)
                        #print(f'New template list AFTER adding: {new_template_list}')

            current_template_list = new_template_list
            #print(current_template_list)
            current = "".join(current_template_list)
            if current not in strings_generated:
                strings_generated.append(current)
            else:
                print('String repeat found!')
            print(f'After Step {step + 1}: {current} (Length: {len(current)})')
            print(f'Applied {len(rules_applied_this_starting_pair)} rules this step:'
                  f' {rules_applied_this_starting_pair}')
            # Calculate answer
            letter_counts = {}
            for val in current_template_list:
                if val not in letter_counts:
                    letter_counts[val] = current_template_list.count(val)

            print(f'{letter_counts}\n')

    max_value = max(letter_counts.values())
    min_value = min(letter_counts.values())

    answer = max_value - min_value

    print(answer)

    # Findings
    # Total number of letters is double the previous number minus 1: (len_prev x 2) -1
    # Letters counts after 10 steps (real data):
    # {'C': 998, 'O': 3092, 'B': 3003, 'F': 2099, 'S': 2668, 'P': 1717, 'H': 1919, 'N': 2034, 'V': 717, 'K': 1210}
    # Example data:
    # {'N': 865, 'B': 1749, 'C': 298, 'H': 161}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    polymer_generator("test", 8)
