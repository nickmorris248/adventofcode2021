file_path = "day11_input/"


def print_map(map_dict):
    print('\n')
    this_row = ''
    index = 0
    for ref in map_dict:
        index += 1
        energy = map_dict[ref][0]
        this_row += str(energy)
        if index == 10:
            print(this_row)
            this_row = ''
            index = 0
    print('\n')


def octopus_flash_simulator(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    octo_map = [[int(i) for i in line] for line in data.splitlines()]

    print(octo_map)

    map_dict = {}

    # Give each octopus a reference number (1 - 100)
    oct_ref = 0
    for row in octo_map:
        for col in row:
            # Increment ref
            oct_ref += 1
            # Determine the refs of the adjacent octopuses (clockwise from 12)
            twelve = oct_ref - 10
            one30 = oct_ref - 9
            three = oct_ref + 1
            four30 = oct_ref + 11
            six = oct_ref + 10
            seven30 = oct_ref + 9
            nine = oct_ref - 1
            ten30 = oct_ref - 11

            # Put them in a list. Skip refs on edges and corners as appropriate
            # Top left corner
            if oct_ref == 1:
                adj_list = [three, four30, six]
            # Top right corner
            elif oct_ref == 10:
                adj_list = [six, seven30, nine]
            # Bottom right corner
            elif oct_ref == 100:
                adj_list = [twelve, nine, ten30]
            # Bottom left corner
            elif oct_ref == 91:
                adj_list = [twelve, one30, three]
            # Left column (not corner)
            elif (oct_ref + 10) % 10 == 1:
                adj_list = [twelve, one30, three, four30, six]
            # Right column (not corner)
            elif oct_ref % 10 == 0:
                adj_list = [twelve, six, seven30, nine, ten30]
            # Top row (not corner)
            elif oct_ref < 10:
                adj_list = [three, four30, six, seven30, nine]
            # Bottom row (not corner)
            elif oct_ref > 90:
                adj_list = [twelve, one30, three, nine, ten30]
            else:
                adj_list = [twelve, one30, three, four30, six, seven30, nine, ten30]

            step_last_flash = 0
            map_dict[oct_ref] = [col, step_last_flash, adj_list]

    print(map_dict)

    flash_counter = 0
    # Loop through 100 steps
    flashes_after_last_step = 0
    step = 0
    simult_flash = False
    simult_flash_step = 0
    while not simult_flash:
        step += 1
        octos_flashed_this_step = []
        print(f'\nStep #{step}: Part 1 - Increment energy of each octo by 1')
        # Increment energy of each octopus by 1
        for octopus in map_dict:
            map_dict[octopus][0] += 1
            # If this takes them to 10, add to the flashed list
            if (map_dict[octopus][0] == 10) and (octopus not in octos_flashed_this_step):
                octos_flashed_this_step.append(octopus)
        # Loop through those who have flashed this step

        print(f'\nStep #{step}: Part 2')
        for octopus in octos_flashed_this_step:
            print(f'Step #{step}: Checking Octopus #{octopus} in:')
            print(f'Octos flashed this step: {octos_flashed_this_step}')
            if (map_dict[octopus][0] > 9) and map_dict[octopus][1] != step:
                # print_map(map_dict)
                # Increment flash counter
                flash_counter += 1
                # Change the 'step last flash' reference to this step
                map_dict[octopus][1] = step
                # Set the energy value back to 0
                map_dict[octopus][0] = 0
                # Increment the energy values of each adjacent octopus by 1
                for adj_oct in map_dict[octopus][2]:
                    if adj_oct not in octos_flashed_this_step:
                        map_dict[adj_oct][0] += 1
                        # If this increases their energy to 10, add to the end of the flashed this step list
                        if (map_dict[adj_oct][0] > 9) and (adj_oct not in octos_flashed_this_step):
                            octos_flashed_this_step.append(adj_oct)

        flashes_this_step = flash_counter - flashes_after_last_step
        print(f'Step #{step}: {flashes_this_step} flashes')
        flashes_after_last_step = flash_counter

        # Did they all flash at the same time?
        if flashes_this_step == 100:
            simult_flash_step = step
            simult_flash = True

        print_map(map_dict)

        print(map_dict)

    if simult_flash:
        print(f'All Octopuses flashed on Step #{simult_flash_step}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    octopus_flash_simulator("octopuses")
