file_path = "day16_input/"


def create_hexadecimal_dict(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    hexadecimal_dict = {f: v for f, v in [line.split(" = ") for line in data.splitlines()]}

    print(hexadecimal_dict)

    return hexadecimal_dict


def process_literal(psind, binary_str):
    # Packet type is 'literal value'
    # Group length in packet is 5
    # (char 1 indicates whether this is the final group or not, chars 2:5 are to process)
    packet_not_finished = True
    literal_values = []
    group_no = -1
    while packet_not_finished:
        group_no += 1
        # Group starting index
        gsind = psind + 6 + (group_no * 5)
        # Last group indicator bit
        print(f'Analysing Last Group Indicator bit at: index {gsind}. Char: {binary_str[gsind]}')
        lst_grp_ind = binary_str[gsind]
        data_to_process = binary_str[gsind + 1: gsind + 5]
        print(f'Analysing Literal Value binary string at: index {gsind + 1}: {gsind + 5}. '
              f'\nString: {data_to_process}')
        # print(data_to_process)
        literal_values.append(data_to_process)
        print(f'Literal values update: {literal_values}')
        # End processing if this was the last group in this packet
        if lst_grp_ind == '0':
            packet_not_finished = False

    last_char_index = gsind + 4

    return [literal_values, last_char_index]


def packet_header_processing(psind, binary_str):
    formatting = "".join([" " for i in range(psind)])
    print(f'Full binary string on top, binary string from start of this packet below:'
          f'\n{binary_str}\n{formatting}{binary_str[psind:]}')
    print(f'Packet starting index (in packet header processing): {psind}')
    #print(f'Binary string from packet start:\n{formatting}{binary_str[psind:]}')
    print(f'Analysing Packet Version at: index {psind}: {psind + 3}. String: {binary_str[psind:psind + 3]}')
    packet_version = int(binary_str[psind:psind + 3], 2)
    print(f'Analysing Packet Type ID at: index {psind + 3}: {psind + 6}. String: {binary_str[psind + 3:psind + 6]}')
    packet_typeid = int(binary_str[psind + 3:psind + 6], 2)

    last_char_index = psind + 5

    return [packet_version, packet_typeid, last_char_index]


def transmission_decoder(file_name, hexadecimal_dict):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    #testing
    #data = 'A0016C880162017C3686B18A3D4780'

    print(f'Hexadecimal string: {data}')

    # Create hexadecimal dict
    hexadecimal_dict = create_hexadecimal_dict(hexadecimal_dict)

    # Extracting hexadecimal and convert into binary string
    binary_str = "".join([hexadecimal_dict[i] for i in data])
    print(binary_str)

    # Results dict
    packet_results = {}

    counting_sub_packets = False
    sub_packets_count = 0
    sum_of_version_no = 0
    # Start processing bit string
    string_still_processing = True
    # Packet starting index
    psind = 0
    packet_id = 0
    processing_sub_packets = False
    ending_index = 0
    ending_sub_packet = 0
    analysis_string = ''
    while string_still_processing:
        packet_id += 1
        print('\nNew Packet')
        print(f'Packet starting index (top of new packet loop): {psind}')
        php_results = packet_header_processing(psind, binary_str)
        packet_version = php_results[0]
        analysis_string += 'VVV'
        packet_typeid = php_results[1]
        analysis_string += 'TTT'

        if processing_sub_packets:
            # Mark packet id as a sub-packet under its parent
            packet_results[packet_id] = ['sub', packet_id - 1, 'ongoing']
        else:
            packet_results[packet_id] = ['primary', 'n/a', 'ongoing']

        print(f'Packet results dict update: {packet_results}')


        sum_of_version_no += packet_version

        print(f'Packet Version: {packet_version}\nPacket Type ID: {packet_typeid}')

        print(f'Checking psind: {psind}')
        # Do packet processing according to packet type
        if packet_typeid == 4:
            print(f'--Packet Type: Literal Value--')
            print(f'Packet starting index (top of Literal value processing): {psind}')
            # Packet type is 'Literal Value'
            # Group length in packet is 5
            # (char 1 indicates whether this is the final group or not, chars 2:5 are to process)
            litv_result = process_literal(psind, binary_str)
            literal_values = litv_result[0]

            num_of_lv = len(literal_values)

            # Update packet starting index for the next round
            psind = litv_result[1] + 1
            print(f'Packet starting index for next round: {psind}')
            # Mark this packet as done. Format: packet_results[packet_id] = ['primary', 'n/a', 'ongoing']
            packet_results[packet_id][2] = 'done'
            print(f'Updated packet results dict: {packet_results}')

            # Print results
            final_lit_value = int("".join(literal_values), 2)
            print(f'Literal Value: {final_lit_value}')
            #string_still_processing = False

        else:
            print(f'Packet starting index (top of Operator processing): {psind}')
            # Packet type is 'Operator'
            # Determine length type
            length_type_id = binary_str[psind + 6]
            print(f'Length Type ID (0 or 1): {length_type_id}')
            # Process according to length id
            if length_type_id == '0':
                formatting = "".join([" " for i in range(psind)])
                print(f'Packet starting index (top Length ID 0 processing): {psind}')
                print(f'Full binary string on top, binary string from start of this packet below:'
                      f'\n{binary_str}\n{formatting}{binary_str[psind:]}')
                print(f'Packet starting index (in packet header processing): {psind}')
                # Next 15 bits are a number that represents the total length
                # in bits of the sub-packets contained by this packet
                len_of_subpackets_bin = binary_str[psind + 7: psind + 22]
                print(f'15 bit binary string: {len_of_subpackets_bin}')
                print(f'Len of 15 bit binary string: {len(len_of_subpackets_bin)}')
                len_of_subpackets_dec = int(len_of_subpackets_bin, 2)
                print(f'Length of Sub-packets: {len_of_subpackets_dec}')
                subpackets_to_process_bin = binary_str[psind + 23: psind + 23 + len_of_subpackets_dec + 1]
                processing_sub_packets = True
                if processing_sub_packets:
                    ending_index = psind + 23 + len_of_subpackets_dec

                # Update packet starting index for the next round
                psind = psind + 21 + 1

            else:
                print(f'Packet starting index (top Length ID 1 processing): {psind}')
                # Next 11 bits are a number that represents the number of
                # sub-packets immediately contained by this packet
                print(f'Checking psind: {psind}')
                num_of_subpackets_bin = binary_str[psind + 7: psind + 18]
                print(f'Number of Sub-packets binary string: {num_of_subpackets_bin}')
                num_of_subpackets_dec = int(num_of_subpackets_bin, 2)
                print(f'Number of Sub-packets: {num_of_subpackets_dec}')
                subpackets_to_process_bin = binary_str[psind + 18: psind + 18 + num_of_subpackets_dec + 1]
                counting_sub_packets = True
                processing_sub_packets = True
                if processing_sub_packets:
                    ending_sub_packet = num_of_subpackets_dec

                # Update packet starting index for the next round
                psind = psind + 17 + 1
                print(f'Updated psind for next round: {psind}')

            #string_still_processing = False
        if processing_sub_packets:
            # Have we reached the ending index yet
            print(f'Checking: psind: {psind} | ending index: {ending_index}')
            if psind == ending_index + 1:
                processing_sub_packets = False
        if counting_sub_packets:
            sub_packets_count += 1
            print(f'Checking: Sub packet count: {sub_packets_count} | ending count: {ending_sub_packet}')
            if sub_packets_count == ending_sub_packet:
                counting_sub_packets = False
                sub_packets_count = 0


        # Determine if this is the end of the string
        print(f'Bits yet to process: {len(binary_str[psind:])}')
        if len(binary_str[psind:]) < 8:
            print(f'Bits yet to process: {len(binary_str[psind:])}')
            string_still_processing = False

    # Answer
    print(f'Answer: {sum_of_version_no}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    transmission_decoder("transmission_hexadecimal", "hexadecimal")


