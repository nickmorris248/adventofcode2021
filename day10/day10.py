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
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    score = 0

    opening_chars = ['(', '[', '{', '<']
    closing_chars = [')', ']', '}', '>']

    # Corresponding characters
    corr = {
        ')': '(',
        ']': '[',
        '}': '{',
        '>': '<'
    }

    # Loop through the characters
    for line in syntax_lines:
        oc_list = []
        for char in line:
            if char in opening_chars:
                oc_list.append(char)
            elif char in closing_chars:
                if corr[char] != oc_list[-1]:
                    # Line is corrupted
                    # Add to score
                    score += scoring[char]
                    break
                elif char == '\n':
                    # End of the line
                    pass
                elif corr[char] == oc_list[-1]:
                    # Remove that item from the list
                    oc_list.pop()
                else:
                    print('Unknown character')

    print(f'The answer is: {score}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    syntax_scoring("navigation_subsystem")
