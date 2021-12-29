file_path = "day12_input/"


def path_finder(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    cave_connections = [[i for i in line.split('-')] for line in data.splitlines()]

    print(cave_connections)

    # Map connections in a dict
    map_con = {}
    for connection in cave_connections:
        for cave in connection:
            other_cave = connection.copy()
            other_cave.remove(cave)
            #print(f'Other cave: {other_cave}')
            if cave not in map_con:
                map_con[cave] = other_cave
            elif cave in map_con:
                if other_cave[0] not in map_con[cave]:
                    map_con[cave].append(other_cave[0])
            else:
                print('Strange result')

    print(map_con)

    paths = {}
    # Try to build paths. Refer to dict for possible next cave to visit
    # First cave is always the start
    searching = True
    # Start off the paths dict
    paths['start'] = []
    for cave in map_con['start']:
        paths['start'].append(cave)
    paths_list = ['start']
    #print(f'Paths dict: {paths}')
    #print(f'Paths list: {paths_list}')
    for path in paths_list:
        # Add each branch from this path as a new path in the dict
        for cave in paths[path]:
            new_path = path
            # Check that cave is not already in this path
            # If cave letter is uppercase it can be repeated in the path
            if (cave not in new_path) or (cave.isupper()):
                # Add cave to the path
                new_path += cave
                # Add new path to paths dict
                if new_path not in paths:
                    if cave == 'end':
                        paths[new_path] = 'end'
                    else:
                        paths[new_path] = map_con[cave]
                        paths_list.append(new_path)
                # If this is the end cave, break this path
                if cave == 'end':
                    continue
            #print(f'Paths dict: {paths}')
            #print(f'Paths list: {paths_list}')

    # Count paths
    count = 0
    for path in paths:
        if paths[path] == 'end':
            count += 1

    print(f'Answer is: {count}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path_finder("cave_connections")
