
file_path = "day3_input/"


def calc_life_support_rating(file_name):
    binary_1s = 0
    binary_0s = 0
    # lists of binary strings, filtered down over time
    ogr_str_lst = []  # oxygen generator rating list of binary strings
    csr_str_lst = []  # CO2 scrubber rating list of binary strings
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        it_lst = f.readlines()

    print(f'Total Records: {len(it_lst)}')

    # Finding the Oxygen Generator Rating
    char_index = 0
    while len(ogr_str_lst) != 1:
        wkg_lst_1s = []
        wkg_lst_0s = []
        for line_txt in it_lst:
            line_txt = line_txt.rstrip('\n')
            if line_txt[char_index] == '1':
                wkg_lst_1s.append(line_txt)
            else:
                wkg_lst_0s.append(line_txt)

        # Determine which list to proceed with
        if len(wkg_lst_1s) >= len(wkg_lst_0s):
            it_lst = wkg_lst_1s
            # If this is the first char, set the first filtered list for CO2 scubbing ratings
            if char_index == 0:
                csr_str_lst = wkg_lst_0s
        else:
            it_lst = wkg_lst_0s
            if char_index == 0:
                csr_str_lst = wkg_lst_1s

        # Update master list for accurate size determination in while loop
        ogr_str_lst = it_lst

        # Iterate char index
        char_index += 1

        # Checking
        print(f'Filtering Round #{char_index}, Records Left: {len(ogr_str_lst)}')
        print(f'Records: {ogr_str_lst}')

    ogr_bin_str = ogr_str_lst[0]
    print(f'Final OGR Rating Binary: {ogr_bin_str}')
    ogr_int = int(ogr_bin_str, 2)
    print(f'Final OGR Rating Int: {ogr_int}\n\n\n')

    # Finding the CO2 Scrubber Rating
    char_index = 1  # We already did the first round above so starting at 2nd char
    it_lst = csr_str_lst
    while len(csr_str_lst) != 1:
        wkg_lst_1s = []
        wkg_lst_0s = []
        for line_txt in it_lst:
            line_txt = line_txt.rstrip('\n')
            if line_txt[char_index] == '1':
                wkg_lst_1s.append(line_txt)
            else:
                wkg_lst_0s.append(line_txt)

        # Determine which list to proceed with
        print(f'Working list 1s: {wkg_lst_1s}')
        print(f'Working list 0s: {wkg_lst_0s}')
        if len(wkg_lst_1s) >= len(wkg_lst_0s):
            it_lst = wkg_lst_0s
            #print(f'Len 1s > Len 0s')
        else:
            it_lst = wkg_lst_1s
            #print(f'Len 1s > Len 0s')

        # Update master list for accurate size determination in while loop
        csr_str_lst = it_lst

        # Iterate char index
        char_index += 1

        # Checking
        # Checking
        print(f'Filtering Round #{char_index}, Records Left: {len(csr_str_lst)}')
        print(f'Records: {csr_str_lst}\n')

    csr_bin_str = csr_str_lst[0]
    print(f'Final OGR Rating Binary: {csr_bin_str}')
    csr_int = int(csr_bin_str, 2)
    print(f'Final OGR Rating Int: {csr_int}')

    # Calculate life support rating
    print(f'\n\nLife Support Rating: {ogr_int * csr_int}')

#[489, 493, 504, 517, 513, 485, 521, 479, 502, 506, 480, 507]
#[511, 507, 496, 483, 487, 515, 479, 521, 498, 494, 520, 493]
#[0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1]
#[1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0]
#2967914


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    calc_life_support_rating("diagnostic")


