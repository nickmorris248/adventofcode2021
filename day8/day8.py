file_path = "day8_input/"


def unscramble_digits(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    count = 0
    observations = [[[len(i) for i in segment.split(' ')] for segment in line.split(' | ')]
                    for line in data.splitlines()]

    print(observations)

    # count += 1 if obs in [2, 3, 4, 7] for obs in obs_set in observations

    for obs_set in observations:
        for obs in obs_set[1]:
            if obs in [2, 3, 4, 7]:
                count += 1

    print(f'Answer is: {count}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    unscramble_digits("display_observations")
