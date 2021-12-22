
file_path = "day5_input/"


def count_overlapping_lines(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    """How I would have done it:
        for line in data.splitlines():
        #print(line)
        for line_coords in line.split(' -> '):
            #print(line_coords)
            for point_coords in line_coords.split(','):
                pass
                #print(int(point_coords))"""

    # Adapted from Jay's day 4 solution - maybe need to break into steps for easier reading?
    final_coords = [[[int(coord_point_num) for coord_point_num in line_coords.split(',')] for line_coords in
                     line.split(' -> ')] for line in data.splitlines()]

    print(final_coords)

    # Plot the lines and count the intersections
    # Use nested dictionaries: longer to write but more efficient to run?
    points_dict = {}
    intersects = 0
    for line_coords in final_coords:
        x1 = line_coords[0][0]
        x2 = line_coords[1][0]
        y1 = line_coords[0][1]
        y2 = line_coords[1][1]
        print(line_coords)
        if x1 == x2:
            print('Vertical Line')
            max_y = max(y1, y2)
            min_y = min(y1, y2)
            print(f'Max y: {max_y}')
            print(f'Min y: {min_y}')
            # Check if there's an entry for this x already, if not add it
            if x1 not in points_dict:
                points_dict[x1] = {}
            for y in range(min_y, max_y+1):
                # Check if there's an entry for this y already
                if y in points_dict[x1]:
                    # Check the count of lines crossing this point
                    if points_dict[x1][y] == 1:
                        # This is the second line to cross this point so increase intersect counter by 1
                        intersects += 1
                        # And increase the counter by 1
                        points_dict[x1][y] += 1
                    else:
                        # There's already two lines crossing here so just increase the counter,
                        # not the intersects count
                        points_dict[x1][y] += 1
                else:
                    # Add the y entry and set value to 1
                    points_dict[x1][y] = 1

        elif y1 == y2:
            print('Horizontal Line')
            max_x = max(x1, x2)
            min_x = min(x1, x2)
            print(f'Max x: {max_x}')
            print(f'Min x: {min_x}')
            # Loop through x points for this horizontal line
            for x in range(min_x, max_x + 1):
                # Check if there's an entry for this x already and if not, add it
                if x not in points_dict:
                    points_dict[x] = {}
                    # Set y dict inside with count value 1
                    points_dict[x][y1] = 1
                else:
                    # Check if there's already an entry for the y of this point
                    if y1 in points_dict[x]:
                        if points_dict[x][y1] == 1:
                            # This is the second line to cross this point so increase intersect counter by 1
                            intersects += 1
                            # And increase the counter by 1
                            points_dict[x][y1] += 1
                        else:
                            # There's already two lines crossing here so just increase the counter,
                            # not the intersects count
                            points_dict[x][y1] += 1
                    else:
                        # Add entry for this y and set to 1
                        points_dict[x][y1] = 1
        else:
            print('Diagonal Line')
            max_x = max(x1, x2)
            min_x = min(x1, x2)
            print(f'Max x: {max_x}')
            print(f'Min x: {min_x}')

            # Determine if line slopes positively or negatively
            if (x1 == min_x and y2 > y1) or (x2 == min_x and y1 > y2):
                # Line slopes down - y & x increase with each step
                slope = 'down'
            elif (x1 == min_x and y1 > y2) or (x2 == min_x and y2 > y1):
                # Line slopes up - x increases & y decreases with each step
                slope = 'up'

            # Set xp and yp
            if x1 == min_x:
                xp = x1
                yp = y1
                stop_y = y2
            elif x2 == min_x:
                xp = x2
                yp = y2
                stop_y = y1
            # Step along the line until the max/min y is reached
            finished = False
            step_x = 0
            step_y = 0
            test = 0
            while not finished:
                print(f'Plotting: x: {xp} and y: {yp}')
                print(f'Stop y: {stop_y}')
                # Check if x entry exists and add it if not
                if xp not in points_dict:
                    points_dict[xp] = {}
                    # Set y dict inside with count value 1
                    points_dict[xp][yp] = 1
                else:
                    # Check if the y entry exists
                    if yp in points_dict[xp]:
                        # If the count is 1 then this is the first intersect to increase the count by 1
                        if points_dict[xp][yp] == 1:
                            intersects += 1
                            # Also add one to the count
                            points_dict[xp][yp] += 1
                        else:
                            points_dict[xp][yp] += 1
                    else:
                        # Add the y entry and set count value to 1
                        points_dict[xp][yp] = 1
                # Change step
                # Check if we're finished now
                if yp == stop_y:
                    finished = True
                # Advance step by 1, according to slope type
                if slope == 'down':
                    xp += 1
                    yp += 1
                elif slope == 'up':
                    xp += 1
                    yp -= 1

    print(f'Total Intersects: {intersects}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    count_overlapping_lines("vent_lines")

