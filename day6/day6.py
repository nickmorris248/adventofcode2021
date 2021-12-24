
file_path = "day6_input/"


def simulate_fish_ages(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    fish_list = [int(i) for i in data.split(',')]

    print(fish_list)

    for day in range(80):
        # Cycle through simulated fish and do something based on their internal timer state
        new_fish_today = []
        for index, fish_intv in enumerate(fish_list):
            if fish_intv == 0:
                # Add new fish with interval timer 8
                new_fish_today.append(8)
                # Reset this fish's timer to 6
                fish_list[index] = 6
            else:
                # Reduce interval timer by 1
                fish_list[index] -= 1
        # Add the new fish for today onto the end of the list
        fish_list += new_fish_today

    answer = len(fish_list)

    print(answer)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    simulate_fish_ages("fish_ages")

