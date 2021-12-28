file_path = "day8_input/"


def unscramble_digits(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    count = 0
    observation_lengths = [[[len(i) for i in segment.split(' ')] for segment in line.split(' | ')]
                           for line in data.splitlines()]

    print(observation_lengths)

    ob_letters = [[[letters for letters in segment.split(' ')] for segment in line.split(' | ')]
                  for line in data.splitlines()]

    print(ob_letters)

    running_total = 0
    for obs_line in ob_letters:

        # Keep track of obs corresponding to different numbers (for this set)
        zero_l = []
        one_l = []
        two_l = []
        three_l = []
        four_l = []
        five_l = []
        six_l = []
        seven_l = []
        eight_l = []
        nine_l = []
        zero69 = []
        two35 = []

        # Keep track of the obs strings corresponding to different numbers (for this set)
        one = ''
        two = ''
        three = ''
        four = ''
        five = ''
        six = ''
        seven = ''
        eight = ''
        nine = ''
        zero = ''

        # Keep track of the letters (abcdef) corresponding to each display segment (for this set)
        top_seg = ''
        mid_seg = ''
        bot_seg = ''
        tleft = ''
        bleft = ''
        tright = ''
        bright = ''

        # Round 1 is analysis and round 2 is decoding
        decoding = False
        for obs_set in obs_line:
            digit = ''
            for obs in obs_set:
                # Identify number options based on obs string length
                if not decoding:
                    if len(obs) == 2:
                        one_l.append(obs)
                    elif len(obs) == 4:
                        four_l.append(obs)
                    elif len(obs) == 3:
                        seven_l.append(obs)
                    elif len(obs) == 7:
                        eight_l.append(obs)
                    elif len(obs) == 6:
                        zero69.append(obs)
                    elif len(obs) == 5:
                        two35.append(obs)
                    else:
                        print("Unknown length")
                elif decoding:
                    print(f'Evaluating: {sorted(obs)} against d0 ({sorted(d0)})')
                    print(f'Evaluating: {sorted(obs)} against d1 ({sorted(d1)})')
                    print(f'Evaluating: {sorted(obs)} against d2 ({sorted(d2)})')
                    print(f'Evaluating: {sorted(obs)} against d3 ({sorted(d3)})')
                    print(f'Evaluating: {sorted(obs)} against d4 ({sorted(d4)})')
                    print(f'Evaluating: {sorted(obs)} against d5 ({sorted(d5)})')
                    print(f'Evaluating: {sorted(obs)} against d6 ({sorted(d6)})')
                    print(f'Evaluating: {sorted(obs)} against d7 ({sorted(d7)})')
                    print(f'Evaluating: {sorted(obs)} against d8 ({sorted(d8)})')
                    print(f'Evaluating: {sorted(obs)} against d9 ({sorted(d9)})')

                    # Decoding the observation strings into digits
                    if sorted(obs) == sorted(d0):
                        digit += '0'
                    elif sorted(obs) == sorted(d1):
                        digit += '1'
                    elif sorted(obs) == sorted(d2):
                        digit += '2'
                    elif sorted(obs) == sorted(d3):
                        digit += '3'
                    elif sorted(obs) == sorted(d4):
                        digit += '4'
                    elif sorted(obs) == sorted(d5):
                        digit += '5'
                    elif sorted(obs) == sorted(d6):
                        digit += '6'
                    elif sorted(obs) == sorted(d7):
                        digit += '7'
                    elif sorted(obs) == sorted(d8):
                        digit += '8'
                    elif sorted(obs) == sorted(d9):
                        digit += '9'
                    else:
                        print(f'Decode error: Unknown digit: {obs}')

                if decoding:
                    print(f'Decoded Digit: {digit}')
            if decoding:
                running_total += int(digit)

            if not decoding:
                # Frequency analysis of observations in this set
                # If the observations don't include some numbers or there's multiples of other numbers
                # that will be revealed here and modifications will be required for the analysis to work
                print(f'\n--New Obs Set for Analysis--\nOnes in this set: {len(one_l)} ({one_l})')
                if len(one_l) == 1:
                    one = one_l[0]
                print(f'Two35s in this set: {len(two35)} ({two35})')
                print(f'Fours in this set: {len(four_l)} ({four_l})')
                if len(four_l) == 1:
                    four = four_l[0]
                print(f'Zero69s in this set: {len(zero69)} ({zero69})')
                print(f'Sevens in this set: {len(seven_l)} ({seven_l})')
                if len(seven_l) == 1:
                    seven = seven_l[0]
                print(f'Eights in this set: {len(eight_l)} ({eight_l})')
                if len(eight_l) == 1:
                    eight = eight_l[0]

                # The unique segment between 1s and 7s is the top segment
                top_seg_set = set(seven) - set(one)
                # If you take the segments in 4 plus the top segment away from 9 there will be one segment left
                # which is the bottom segment
                for num in zero69:
                    #print(f'zero69 check: for num in  zero69: Num = {num} | set(four) = {set(four)} | top_set = {top_seg_set}')
                    left = set(num) - set(four) - top_seg_set
                    #print(f'Left: {left}')
                    if len(left) == 1:
                        # This obs is a 9
                        nine = num
                        # The remaining letter is the bottom segment
                        bot_seg_set = left
                # If you take the segments of 1 and the top and bot segments away from 3 there will be one segment
                # left which will be the middle segment
                for num in two35:
                    left = set(num) - set(one) - top_seg_set - bot_seg_set
                    if len(left) == 1:
                        # This obs is a 3
                        three = num
                        # The remaining letter is the middle segment
                        mid_seg_set = left
                        #print(f'Mid seg check: {mid_seg_set}\nLeft: {left}')
                #print(f'Middle Segment: {sorted(mid_seg)[0]}')
                # The 0 is the only number in the 069 group that doesn't have the middle segment
                for num in zero69:
                    #print(f'Zero check: Checking {num} in {zero69}')
                    if sorted(mid_seg_set)[0] not in list(num):
                        #print(f'If mid_seg_set {mid_seg_set} not in list(num) {list(num)}')
                        # This number is zero
                        zero = num
                # The last unknown number in the 069 group is 6
                six = sorted(set(zero69) - {zero} - {nine})[0]
                #print(f'Six check: {six}')
                # If you remove the segments of nine from zero you are left with the bottom left segment
                bleft_set = set(zero) - set(nine)
                # The segments of 1 minus the segments of 6 leaves segment top right
                tright_set = set(one) - set(six)
                #print(f'Tright check: {tright_set} from set(one): {set(one)} less set(six): {set(six)}')
                # The remaining segment of 1 is the bottom right
                bright_set = set(one) - tright_set
                #print(f'Bright check: {bright_set}: Set(one) = {set(one)}, tright = {tright_set}')
                # The segments of 4 minus the segments of 3 leaves the segment top left
                tleft_set = set(four) - set(three)

                # Convert segment sets to individual letters
                top_seg = list(top_seg_set)[0]
                mid_seg = list(mid_seg_set)[0]
                bot_seg = list(bot_seg_set)[0]
                tleft = list(tleft_set)[0]
                tright = list(tright_set)[0]
                bleft = list(bleft_set)[0]
                bright = list(bright_set)[0]

                # Print results for reference
                print('\n*Analysis Results*\n')
                print(f'Top Segment: {sorted(top_seg)[0]}')
                print(f'Middle Segment: {sorted(mid_seg)[0]}')
                print(f'Bottom Segment: {sorted(bot_seg)[0]}')
                print(f'Top Left Segment: {sorted(tleft)[0]}')
                print(f'Top Right Segment: {sorted(tright)[0]}')
                print(f'Bottom Left Segment: {sorted(bleft)[0]}')
                print(f'Bottom Right Segment: {sorted(bright)[0]}')

                # Move to round 2: Decoding
                print('\n*Start Decoding*\n')
                decoding = True
                # Build decoding references for each number (d0, d1, d2 etc.) from the
                # segments that make up that number
                d0 = [top_seg, tright, bright, bot_seg, bleft, tleft]
                d1 = [tright, bright]
                d2 = [top_seg, tright, mid_seg, bleft, bot_seg]
                d3 = [top_seg, tright, mid_seg, bright, bot_seg]
                d4 = [tleft, tright, mid_seg, bright]
                d5 = [top_seg, mid_seg, bright, bot_seg, tleft]
                d6 = [top_seg, mid_seg, bright, bot_seg, bleft, tleft]
                d7 = [top_seg, tright, bright]
                d8 = [top_seg, tright, mid_seg, bright, bot_seg, bleft, tleft]
                d9 = [top_seg, tright, mid_seg, bright, bot_seg, tleft]

    print(f'\n\nAnswer is: {running_total}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    unscramble_digits("display_observations")
