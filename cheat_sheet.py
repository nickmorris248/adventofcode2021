

# https://github.com/PythonForForex/advent-of-code-2021/blob/main/day3.py
for i in range(len(input[0])):
    all_bits = [b[i] for b in input]
    zeros = all_bits.count('0')
    ones = all_bits.count('1')


# https://github.com/PythonForForex/advent-of-code-2021/blob/main/day3.py
    if zeros == ones:
        raise AssertionError('Unexpected result')

# Python One Line For Loop
# https://blog.finxter.com/python-one-line-for-loop-a-simple-tutorial/

# https://github.com/PythonForForex/advent-of-code-2021/blob/main/day3.py
revised_input = [b for b in revised_input if b[i] == idx_key]
# https://github.com/PythonForForex/advent-of-code-2021/blob/main/day4.py
all_boards = [i.splitlines() for i in raw_input]
boards_array = [
    [[int(i) for i in board.split()] for board in boards] for boards in all_boards

# https://github.com/PythonForForex/advent-of-code-2021/blob/main/day6.py
input_dict = {i: 0 for i in range(-1, 9)}


# Enumerate
for idx, board in enumerate(boards_array):

# all()
# The all() function returns True if all items in an iterable are true, otherwise it returns False.
# If the iterable object is empty, the all() function also returns True.
# https://www.w3schools.com/python/ref_func_all.asp
if all([i in numbers for i in horizontal]) or all(
                [i in numbers for i in vertical]


# The count() method returns the number of elements with the specified value.
    # https://www.w3schools.com/python/ref_list_count.asp

    for val in input:
        input_dict[val] = input.count(val)
        #print(f'Val in input is {val} and input.count(val) is {input.count(val)}')

    # A Pandas DataFrame is a 2 dimensional data structure,
    # like a 2 dimensional array, or a table with rows and columns.
    # https://www.w3schools.com/python/pandas/pandas_dataframes.asp

    df = pd.DataFrame(input_dict.items())

    # The items() method returns a view object. The view object contains
    # the key-value pairs of the dictionary, as tuples in a list.
    # The view object will reflect any changes done to the dictionary
    # https://www.w3schools.com/python/ref_dictionary_items.asp







    # numpy.sum(arr, axis, dtype, out) :
    # This function returns the sum of array elements over the specified axis.
    # https://www.geeksforgeeks.org/numpy-sum-in-python/
    print(int(df[1].sum()))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    code_sample = input('Code Sample Name: ')

    if code_sample == '':
        pass
