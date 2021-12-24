
file_path = "day6_input/"


def simulate_fish_ages(file_name, days):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    fish_list = [int(i) for i in data.split(',')]

    print(fish_list)

    # Keep track of number of fish at each interval
    interval_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # Loop through fish at the beginning and count the number at each interval
    for interval in fish_list:
        interval_counts[interval] += 1

    # Now loop through days and keep track of number of fish at each interval
    for day in range(days):
        # Next day counts
        next_day = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        # Interval 8
        next_day[0] = interval_counts[1]
        next_day[1] = interval_counts[2]
        next_day[2] = interval_counts[3]
        next_day[3] = interval_counts[4]
        next_day[4] = interval_counts[5]
        next_day[5] = interval_counts[6]
        next_day[6] = interval_counts[7] + interval_counts[0]
        next_day[7] = interval_counts[8]
        next_day[8] = interval_counts[0]

        # Set the interval counts for next day
        interval_counts = next_day

    answer = sum(interval_counts)

    print(f'Answer: {answer}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    simulate_fish_ages("fish_ages", 256)

