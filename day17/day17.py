
# Part 1 & 2

def trick_shot_aimer(data):

    # target area: x=20..30, y=-10..-5

    target_area = [[j.split("=") for j in i.split('..')] for i in data.split(": ")[1].split(',')]

    print(target_area)

    x_min, x_max = sorted([int(target_area[0][0][1]), int(target_area[0][1][0])])

    print(f'x min: {x_min}, x max: {x_max}')

    y_min, y_max = sorted([int(target_area[1][0][1]), int(target_area[1][1][0])])

    print(f'y min: {y_min}, y max: {y_max}')

    # Due to drag, the probe's x velocity changes by 1 toward
    # the value 0; that is, it decreases by 1 if it is greater
    # than 0, increases by 1 if it is less than 0, or does not
    # change if it is already 0.
    # Due to gravity, the probe's y velocity decreases by 1.

    # Start by finding the range of x values that result in
    # the probe reaching the x_min value and not exceeding the x_max value

    x_range = []
    for x_start in range(1, x_max + 1):
        step_exploring = True
        x_pos = 0
        x_velocity = x_start
        while step_exploring:

            if (abs(x_max) >= abs(x_pos)) and (abs(x_pos) >= abs(x_min)):
                #print(f'{x_max} >= {x_pos} >= {x_min}')
                if x_start not in x_range:
                    x_range.append(x_start)

            if x_pos > abs(x_max):
                step_exploring = False

            if x_velocity == 0:
                step_exploring = False

            x_pos += abs(x_velocity)

            if x_velocity > 0:
                x_velocity -= 1
            elif x_velocity < 0:
                x_velocity += 1
            else:
                x_velocity = 0

    print(f'X Range: {x_range}')




    # Now find the y values that will reach the target area for each x value in the range
    # and determine the maximum height reached amongst them
    successful_launch_stats = []
    attempt_no = 0
    successful_ys = []
    loops_since_last_unique_y = 1
    for x_start in x_range:
        # Max range for y value arbitrarily set at 1000 originally and was
        # successful at getting the right answers but further analysis revealed
        # the maximum y is 1 less than the absolute of the lowest y value in the
        # target area
        for y_start in range(y_min, abs(y_min) + 1):
            # but analysis suggests
            attempt_no += 1
            attempt = [x_start, y_start]

            stepping = True
            step_no = 0
            x_vel = attempt[0]
            y_vel = attempt[1]
            probe_position = [0, 0]
            max_height = 0
            mh_step = 0
            mh_probe_position = [0, 0]
            mh_starting_velocity = attempt
            #print(f'\nNew Attempt from {probe_position}. Initial Velocity: {attempt}')
            last_position = []
            while stepping:
                step_no += 1

                # Adjust probe position for this step
                probe_position[0] += x_vel
                probe_position[1] += y_vel

                # Print current position
                #print(f'Probe Position After Step #{step_no}: {probe_position} (Starting Velocity: {attempt})')

                # Update max height stats
                if probe_position[1] > max_height:
                    max_height = probe_position[1]
                    mh_step = step_no
                    mh_probe_position = probe_position.copy()
                    mh_starting_velocity = attempt

                # If the probe position is already past the target area, break the loop
                # Keep track of the position before termination as well
                if (probe_position[1] < y_min) or (abs(probe_position[0]) > abs(x_max)):
                    stepping = False
                    #print(f'Attempt from {attempt} terminated at position: {probe_position} (previous: {last_position}).\n'
                    #      f'Max height: {max_height}. Step Number: {step_no}\n')

                # Update last position for next round
                last_position = probe_position.copy()

                # Check if the probe is in the target area
                if ((probe_position[0] >= x_min) and (probe_position[0] <= x_max)) or ((probe_position[0] <= x_min) and (probe_position[0] >= x_max)):
                    if ((probe_position[1] >= y_min) and (probe_position[1] <= y_max)) or ((probe_position[1] <= y_min) and (probe_position[1] >= y_max)):
                        #print(f'\nTarget area hit at position: {probe_position}')


                        if y_start not in successful_ys:
                            successful_ys.append(y_start)
                        else:
                            loops_since_last_unique_y += 1
                        print(f'Success at Y value: {y_start} (total: {len(successful_ys)})\n'
                              f'Loops since last unique y: {loops_since_last_unique_y}')

                        # Records stats for ths successful launch
                        this_launch = [max_height, mh_step, mh_probe_position, mh_starting_velocity]
                        successful_launch_stats.append(this_launch)

                # Apply drag and gravity to x/y values for the next step
                if x_vel > 0:
                    x_vel -= 1
                elif x_vel < 0:
                    x_vel += 1
                else:
                    x_vel = 0

                y_vel -= 1

                if step_no == 100000:
                    stepping = False

    # Print summary stats
    print(f'\n\nSuccessful Launch Stats: ')
    print(successful_launch_stats)

    print(sorted(successful_launch_stats))

    highest_launch = 0
    unique_starting_positions = []
    for launch in successful_launch_stats:
        if launch[0] > highest_launch:
            highest_launch = launch[0]
        if launch[3] not in unique_starting_positions:
            unique_starting_positions.append(launch[3])

    print(highest_launch)

    print(f'\nNumber of initial starting values: {len(unique_starting_positions)}')

    print(f'Highest successful Y: {max(successful_ys)}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    trick_shot_aimer("target area: x=153..199, y=-114..-75")

# Input strings:
# Example: target area: x=20..30, y=-10..-5
# Actual: target area: x=153..199, y=-114..-75
