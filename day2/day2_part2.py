
file_path = "day2_input/"


def determine_location(file_name):
    horiz_pos = 0
    aim = 0
    depth = 0
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        lines = f.readlines()
        for line_txt in lines:
            line_txt = line_txt.rstrip('\n')
            # Determine the word at the front of the line
            word = ''
            num_txt = ''
            detecting_word = True
            for char in line_txt:
                if detecting_word:
                    if char != " ":
                        word += char
                    else:
                        # Reaching a space means the word is complete
                        detecting_word = False
                else:
                    # Switch to detecting number
                    num_txt += char

            # Convert number text into int
            num_int = int(num_txt)

            # Checking
            print(f'Word detected: {word}')
            print(f'Number detected: {num_int}')

            # Adjust horizontal position and depth based on detected direction word and number
            if word == 'forward':
                horiz_pos += num_int
                depth += (aim * num_int)
                print('Detected Forward')
            elif word == 'down':
                aim += num_int
                print('Detected Down')
            elif word == 'up':
                aim -= num_int
                print('Detected Up')

            # Reset number int
            num_int = 0

            print(f'Overall Horizontal: {horiz_pos}')
            print(f'Overall Depth: {depth}')
            print(f'Overall Aim: {aim}')

        # Multiple end values to get final answer
        answer = horiz_pos * depth

        print(answer)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    determine_location("course")


