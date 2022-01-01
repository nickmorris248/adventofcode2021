file_path = "day14_input/"


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
    # First value of [0, 0] records the pairs to be processed today, the second value is for pairs to be
    # processed tomorrow
    processing_dict = {k: [0, 0] for k, v in rules_list}
    letter_counts = {}
    #print(processing_dict)
    current_template_list = template_list
    # Preload processing dict
    for idx, singular in enumerate(template_list):
        # Add to the letter counts dict
        if singular not in letter_counts:
            letter_counts[singular] = 1
        else:
            letter_counts[singular] += 1

        # Create the letter pairs
        if idx == len(current_template_list) - 1:
            break
        else:
            char0 = current_template_list[idx]
            char1 = current_template_list[idx + 1]
            this_pair = "".join([char0, char1])
            if this_pair in processing_dict:
                processing_dict[this_pair][0] += 1

    print(processing_dict)

    for step in range(1, steps + 1):

        # Loop through processing dict
        for rule in processing_dict:
            # Check if there's any letter pairs to process
            this_step_tally = processing_dict[rule][0]
            if this_step_tally > 0:
                insert_char = rules_dict[rule]
                result1 = rule[0] + insert_char
                result2 = insert_char + rule[1]
                # Add 1 to the 'next step' tally for each of the resulting pairs from this operation
                if result1 in processing_dict:
                    processing_dict[result1][1] += this_step_tally
                if result2 in processing_dict:
                    processing_dict[result2][1] += this_step_tally

                # Increase the letters tally
                if insert_char not in letter_counts:
                    letter_counts[insert_char] = this_step_tally
                else:
                    letter_counts[insert_char] += this_step_tally

                # Reset this step's tallies to zero
                processing_dict[rule][0] = 0

        # Once all rules have been done for today, shift tomorrow's tallies to today for the next loop
        for rule in processing_dict:
            processing_dict[rule][0] = processing_dict[rule][1]

            # Reset tomorrow's tally to 0
            processing_dict[rule][1] = 0

        #print(f'After Step #{step}:\n{processing_dict}')

    print(letter_counts)

    max_value = max(letter_counts.values())
    min_value = min(letter_counts.values())

    answer = max_value - min_value

    print(answer)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    polymer_generator("polymer_instructions", 40)
