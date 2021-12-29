file_path = "day10_input/"


def syntax_scoring(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    syntax_lines = data.splitlines()

    print(syntax_lines)

    # Loop through characters in the line and add the open characters to a list
    # When coming across a closing character, it should match the last opening character
    # If it doesn't it means that is the corrupting character for the line

    # Scoring
    scoring = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }

    opening_chars = ['(', '[', '{', '<']
    closing_chars = [')', ']', '}', '>']

    # Corresponding characters
    corr = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }

    line_completion_scores = []

    # Loop through the characters
    for line in syntax_lines:
        oc_list = []
        line_corrupted = False
        for ind, char in enumerate(line):
            #print(f'Index this char: {ind}')
            #print(f'This char: {char}')
            if char in opening_chars:
                oc_list.append(char)
            elif char in closing_chars:
                if char != corr[oc_list[-1]]:
                    # Line is corrupted - skip it
                    line_corrupted = True
                    break
                elif char == corr[oc_list[-1]]:
                    # Remove that item from the list
                    oc_list.pop()

            else:
                print('Unknown character')

        # Now at the end of the line
        #print('End of line found')
        # End of the line
        # If the list of opening tags isn't empty the line is incomplete
        if not line_corrupted and (len(oc_list) != 0):
            #print(f'Incomplete string: {line}')
            #print(f'Length of oc_list: {len(oc_list)}')
            # Create new completion string score
            completion_score = 0
            completion_string_list = []
            # Loop backwards through the oc list and add the closing tags
            #print(f'oc_list: {oc_list}')
            for open_char in reversed(oc_list):
                #print(f'Last char in oc_list: {open_char}')
                # Multiple current score by 5
                completion_score *= 5
                # Add the value for the completing character
                this_char_score = scoring[corr[open_char]]
                completion_score += this_char_score
                # Add closing char to the list
                completion_string_list.append(corr[open_char])
            # Add the completion score for this line to the list of scores
            line_completion_scores.append(completion_score)
            #print(f'Completion string: {completion_string_list} - Score: {completion_score}')

    # Find the middle score
    median_index = (len(line_completion_scores) // 2)
    print(f'Median index: {median_index}')
    print(f'Sorted scores: {sorted(line_completion_scores)}')
    answer = sorted(line_completion_scores)[median_index]
    print(f'The answer is: {answer}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    syntax_scoring("navigation_subsystem")
