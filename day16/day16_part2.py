
import copy

file_path = "day16_input/"


def create_hexadecimal_dict(file_name):
    with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
        data = f.read()

    hexadecimal_dict = {f: v for f, v in [line.split(" = ") for line in data.splitlines()]}

    print(hexadecimal_dict)

    return hexadecimal_dict


def process_literal(psind, binary_str, analysis_string_this_packet, analysis_string_index):
    # Packet type is 'literal value'
    # Group length in packet is 5
    # (char 1 indicates whether this is the final group or not, chars 2:5 are to process)
    packet_not_finished = True
    literal_values = []
    group_no = -1
    letter_codes = {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D',
        4: 'E',
        5: 'F',
        6: 'G',
        7: 'H',
        8: 'I',
        9: 'J',
        10: 'K',
        11: 'L',
        12: 'M',
        13: 'N',
        14: 'O',
        15: 'P',
    }

    # Update analysis string for packet version VVV
    while packet_not_finished:
        group_no += 1
        # Group starting index
        gsind = psind + 6 + (group_no * 5)

        # Update analysis string
        letter = letter_codes[group_no]
        group_analysis_string = ""
        for i in range(1, 6):
            group_analysis_string += letter
        analysis_string_this_packet += group_analysis_string
        analysis_string_index += 5
        # Last group indicator bit
        print(f'Analysing Last Group Indicator bit at: index {gsind}. Char: {binary_str[gsind]}')
        lst_grp_ind = binary_str[gsind]
        data_to_process = binary_str[gsind + 1: gsind + 5]
        print(f'Analysing Literal Value binary string at: index {gsind + 1}: {gsind + 5}. '
              f'\nString: {data_to_process}.')
        literal_values.append(data_to_process)
        #print(f'Literal values update: {literal_values}')
        # End processing if this was the last group in this packet
        if lst_grp_ind == '0':
            packet_not_finished = False

    last_char_index = gsind + 4

    return [literal_values, last_char_index, analysis_string_this_packet, analysis_string_index]


def packet_header_processing(psind, binary_str):
    formatting = "".join([" " for i in range(psind)])
    print(f'Full binary string on top, binary string from start of this packet below:'
          f'\n{binary_str}\n{formatting}{binary_str[psind:]}')
    #print(f'Packet starting index (in packet header processing): {psind}')
    #print(f'Binary string from packet start:\n{formatting}{binary_str[psind:]}')
    print(f'Analysing Packet Version at: index {psind}: {psind + 3}. String: {binary_str[psind:psind + 3]}')
    packet_version = int(binary_str[psind:psind + 3], 2)
    print(f'Analysing Packet Type ID at: index {psind + 3}: {psind + 6}. String: {binary_str[psind + 3:psind + 6]}')
    packet_typeid = str(int(binary_str[psind + 3:psind + 6], 2))

    last_char_index = psind + 5

    return [packet_version, packet_typeid, last_char_index]


def update_litv_parent_packet(packet_results, packet_id, final_lit_value, final_index, ids_of_open_packets,
                         analysis_string_this_packet):
    # If this is a sub packet, update the parent packet as well
    packet = packet_results[packet_id]['parentpacketid']
    print(f'Evaluating parent packets for Literal Value Packet')
    print(f'\nThis is a sub-packet (ID {packet_id}) of parent packet ID: {packet}')
    # Add literal value from this packet to the parent packet record
    if len(final_lit_value) > 0:
        for value in final_lit_value:
            packet_results[packet]['literal_values'].append(value)

    # Check if this completes the parent packet
    closed_this_packet = []
    # Determine parent packet's length type
    ppl_type = packet_results[packet]['length_typeid']
    if ppl_type == '0':
        # Extract index that the parent packet ends on
        end_ind = packet_results[packet]['subpackets_ending_index']
        print(f'Parent packet ends on index: {end_ind}. Current on index: {final_index}')
        # If the parent packet ending index matches this packet index, end the parent packet
        if end_ind == final_index:
            packet_results[packet]['open'] = False
            # Remove from open ids list
            packet_popped = ids_of_open_packets.pop()
            if packet_popped != packet:
                raise AssertionError("Mismatched packet closure (parent of LitV)")
            closed_this_packet.append(packet)
            print(f' Closed parent packet ID {packet} based on reaching index {final_index}')
            analysis_string_this_packet += f' (Closed parent packet ID {packet} based on reaching index ' \
                                           f'{final_index}) IDs still open: {ids_of_open_packets}'

    elif ppl_type == '1':
        # Extract number of sub packets in this parent packet
        no_subpackets = packet_results[packet]['subpackets_number']
        subpackets_currently_associated = packet_results[packet]['subpacketids']
        no_values_added = len(packet_results[packet]['literal_values'])

        print(f'Parent packet ends after: {no_subpackets} sub-packets. '
              f'\nCurrently have: {no_values_added}')

        # Check if this number matches the number of sub packets associated with this parent
        if no_values_added == no_subpackets:
            packet_results[packet]['open'] = False
            # Remove from open ids list
            packet_popped = ids_of_open_packets.pop()
            if packet_popped != packet:
                raise AssertionError("Mismatched packet closure (parent of LitV)")
            closed_this_packet.append(packet)
            print(f'Closed parent packet ID {packet} based on reaching {no_values_added} sub-packets')
            analysis_string_this_packet += f' (Closed parent packet id # {packet} based on reaching ' \
                                           f'{no_values_added} sub-packets) IDs still ' \
                                           f'open: {ids_of_open_packets}'

    return [packet_results, ids_of_open_packets, analysis_string_this_packet, closed_this_packet]


def update_operator_parent_packet(packet_results, packet_id, final_index, ids_of_open_packets,
                         analysis_string_this_packet):
    # If this is a sub packet, update the parent packet as well
    completed_primary_packets = []
    operator_packets = [packet_id]
    for op_packet in operator_packets:
        # Do calculation for this packet
        print(f'\nDoing calculation for ID{op_packet}. Current list {operator_packets}')
        typeid = packet_results[op_packet]['typeid']
        values = packet_results[op_packet]['literal_values']
        calc_result = evaluate_packet_calculation(typeid, values)  # return [result, result_reached]
        if calc_result[1]:
            result = calc_result[0]
        else:
            raise AssertionError(f"Packet ID{op_packet} Calculation error: {calc_result[0]} from input values: "
                                 f"{values} & Typeid: {typeid}")

        packet_results[op_packet]['final_result'] = result

        # Check if this is a sub-packet
        is_subpacket = packet_results[op_packet]['sub-packet']
        if is_subpacket:
            # Add the final result from this packet to the parent packet's 'literal values'
            parent_packet_id = packet_results[op_packet]['parentpacketid']
            print(f'\nCurrently open packets: {ids_of_open_packets}')
            print(f'This is a sub-packet (ID {op_packet}) of parent packet ID: {parent_packet_id}')
            packet_results[parent_packet_id]['literal_values'].append(result)
            print(f'Added final result ({result}) to parent packet (ID {parent_packet_id}) of packet ID: {op_packet}')

            # Check if the parent packet is now complete
            # Determine parent packet's length type
            ppl_type = packet_results[parent_packet_id]['length_typeid']
            if ppl_type == '0':
                # Extract index that the parent packet ends on
                end_ind = packet_results[parent_packet_id]['subpackets_ending_index']
                print(f'Parent packet ends on index: {end_ind}. Current on index: {final_index}')
                # If the parent packet ending index matches this packet index, end the parent packet
                if end_ind == final_index:
                    packet_results[parent_packet_id]['open'] = False
                    # Remove from open ids list
                    packet_popped = ids_of_open_packets.pop()
                    if packet_popped != parent_packet_id:
                        raise AssertionError("Mismatched packet closure (parent of Op Len Type 0)")
                    print(f' Closed parent packet ID {parent_packet_id} based on reaching index {final_index}')
                    analysis_string_this_packet += f' (Closed parent packet ID {parent_packet_id} based on reaching index ' \
                                                f'{final_index}) IDs still open: {ids_of_open_packets}'

                    # Add this packet to the list to be evaluated too
                    operator_packets.append(parent_packet_id)

            elif ppl_type == '1':
                # Extract number of sub packets in this parent packet
                no_subpackets = packet_results[parent_packet_id]['subpackets_number']
                subpackets_currently_associated = packet_results[parent_packet_id]['subpacketids']
                no_values_added = len(packet_results[parent_packet_id]['literal_values'])

                print(f'Parent packet ends after: {no_subpackets} sub-packets. '
                      f'\nCurrently have: {no_values_added}')
                # Check if this number matches the number of sub packets associated with this parent
                if no_values_added == no_subpackets:
                    packet_results[parent_packet_id]['open'] = False
                    # Remove from open ids list
                    packet_popped = ids_of_open_packets.pop()
                    if packet_popped != parent_packet_id:
                        raise AssertionError("Mismatched packet closure (parent of Op Len Type 1)")
                    print(f'Closed parent packet ID {parent_packet_id} based on reaching {no_values_added} sub-packets')
                    analysis_string_this_packet += f' (Closed parent packet id # {parent_packet_id} based on reaching ' \
                                                   f'{no_values_added} sub-packets) IDs still ' \
                                                   f'open: {ids_of_open_packets}'

                    # Add this packet to the list to be evaluated too
                    operator_packets.append(parent_packet_id)

        else:
            # This should be the final packet
            completed_primary_packets.append(result)

    return [packet_results, ids_of_open_packets, analysis_string_this_packet, completed_primary_packets]


def evaluate_packet_calculation(typeid, values):
    result_reached = False

    result = 'n/a'
    if len(values) == 0:
        result_reached = False
    elif typeid == '0':
        result = sum(values)
        result_reached = True
        print(f'Typeid 0 means sum the values')
    elif typeid == '1':
        print(f'Typeid 1 means multiply the values together')
        if len(values) == 1:
            result = values[0]
            result_reached = True
        else:
            result = values[0]
            for num in values[1:]:
                print(f'{result} * {num} = ')
                result *= num
                print(f'{result}')
            result_reached = True
    elif typeid == '2':
        result = min(values)
        print(f'Typeid 2 means find the minimum of the values')
        result_reached = True
    elif typeid == '3':
        result = max(values)
        print(f'Typeid 3 means find the maximum of the values')
        result_reached = True
    elif typeid in ('5', '6', '7') and len(values) != 2:
        print(f'Typeids 5, 6 & 7 need 2 values but currently we only have {len(values)}')
    elif typeid == '5':
        print(f'Typeid 5 means return a 1 if the first value is greater than the second (must be 2 total)')
        if values[0] > values[1]:
            result = 1
            result_reached = True
        else:
            result = 0
            result_reached = True
    elif typeid == '6':
        print(f'Typeid 6 means return a 1 if the first value is less than the second (must be 2 total)')
        if values[0] < values[1]:
            result = 1
            result_reached = True
        else:
            result = 0
            result_reached = True
    elif typeid == '7':
        print(f'Typeid 7 means return a 1 if the first value is equal to the second (must be 2 total)')
        if values[0] == values[1]:
            result = 1
            result_reached = True
        else:
            result = 0
            result_reached = True
    elif typeid == '4':
        print(f'Typeid 4 means the value has already been evaluated and added to the parent '
              f'packet so nothing more needed here')
        result_reached = False
    else:
        raise AssertionError(f"Invalid type id ({typeid}) detected at calculation stage")

    return [result, result_reached]


def transmission_decoder(input_type, input_source, hexadecimal_dict):

    if input_type == 'string':
        data = input_source
    elif input_type == 'file':
        file_name = input_source
        with open(f'{file_path}{file_name}.txt', encoding='utf8') as f:
            data = f.read()

    print(f'Hexadecimal string: {data}')

    # Create hexadecimal dict
    hexadecimal_dict = create_hexadecimal_dict(hexadecimal_dict)

    # Extracting hexadecimal and convert into binary string
    binary_str = "".join([hexadecimal_dict[i] for i in data])
    print(binary_str)

    # Results dict
    packet_results = {}

    sum_of_version_no = 0
    # Start processing bit string
    string_still_processing = True
    # Packet starting index
    psind = 0
    packet_id = 0
    new_packet = {
        'open': True,
        'sub-packet': False,
        'parentpacketid': '',
        'starting_index': '',
        'version': '',
        'typeid': '',
        'typename': '',
        'length_typeid': '',
        'literal_values': [],
        'subpacketids': [],
        'subpackets_ending_index': 0,
        'subpackets_number': 0,
        'final_result': 'n/a'
    }

    ids_of_open_packets = []

    loop_counter = 0
    analysis_string_this_packet = ''
    analysis_string_index = 0
    analysis_strings = {0: f"000: {binary_str}"}
    formatting = "".join([" " for i in range(psind)])
    print(f'Full binary string on top, binary string from start of this packet below:'
          f'\n{binary_str}\n{formatting}{binary_str[psind:]}')
    print(f'Packet starting index (in packet header processing): {psind}')
    print(f'Binary string from packet start:\n{formatting}{binary_str[psind:]}')

    completed_primary_packets = []

    while string_still_processing:

        # Debugging by restricting loops
        loop_counter += 1
        if loop_counter % 10000000000000 == 0:
            cont = input("\nContinue? (y = yes): ")
            if cont == 'y':
                pass

        print(f'Packet id start of loop: {packet_id}')
        packet_id += 1
        print(f'Packet id after incrementing: {packet_id}')
        print(f'\n\nSearching for next packet...')
        print(f'Ids of open packets (before assessing sub packet): {ids_of_open_packets}')

        # Add new packet record to results dict
        packet_results[packet_id] = copy.deepcopy(new_packet)

        # Updating Analysis String
        if len(str(packet_id)) == 1:
            pi_string = '00' + str(packet_id) + ': '
        elif len(str(packet_id)) == 2:
            pi_string = '0' + str(packet_id) + ': '
        elif len(str(packet_id)) == 3:
            pi_string = str(packet_id) + ': '
        else:
            raise AssertionError("Packet ID length greater than 3")

        # Add space to indent string under the the correct part of binary string
        print(f'Analysis string index: {analysis_string_index}')
        indent_space_len = analysis_string_index
        indent_space = "".join([" " for i in range(indent_space_len)])
        analysis_string_this_packet = pi_string + indent_space

        if len(ids_of_open_packets) > 0:
            # Mark packet id as a sub-packet under its parent
            # The parent packet is the last packet opened that is still open
            parent_packet_id = ids_of_open_packets[-1]
            packet_results[packet_id]['sub-packet'] = True
            packet_results[packet_id]['parentpacketid'] = parent_packet_id
            packet_results[parent_packet_id]['subpacketids'].append(packet_id)

        ids_of_open_packets.append(packet_id)

        print(f'Ids of open packets (after sub packet assessment): {ids_of_open_packets}')

        print('\n=~=~=New Packet=~=~=')
        print(f'Packet starting index (top of new packet loop): {psind}')
        php_results = packet_header_processing(psind, binary_str)
        packet_version = php_results[0]
        packet_typeid = php_results[1]

        # Update analysis string for packet version VVV
        analysis_string_this_packet += 'VVV'
        analysis_string_index += 3
        # Update analysis string for packet id TTT
        analysis_string_this_packet += 'TTT'
        analysis_string_index += 3

        # Update dict record for this packet
        packet_results[packet_id]['starting_index'] = psind
        packet_results[packet_id]['version'] = packet_version
        packet_results[packet_id]['typeid'] = packet_typeid

        sum_of_version_no += packet_version

        print(f'Packet Version: {packet_version}\nPacket Type ID: {packet_typeid}')

        # Do packet processing according to packet type
        if packet_typeid == '4':

            # Packet type is 'Literal Value'
            print(f'--Packet Type: Literal Value--')
            packet_results[packet_id]['typename'] = "Literal Value"

            # Processing Packet
            litv_result = process_literal(psind, binary_str, analysis_string_this_packet, analysis_string_index)
            literal_value_results = litv_result[0]
            analysis_string_this_packet = litv_result[2]

            # Print results
            final_lit_value = int("".join(literal_value_results), 2)
            print(f'Literal Value Binary Strings: {literal_value_results}'
                  f'\nLiteral Value Decimal: {final_lit_value}')

            # Add results to results dict
            packet_results[packet_id]['literal_values'].append(final_lit_value)
            packet_results[packet_id]['final_result'] = final_lit_value

            # Mark this packet as done
            packet_results[packet_id]['open'] = False

            # Remove packet id from open packets list (should be the last id added)
            ids_of_open_packets.pop()

            # If this is a sub packet, update the parent packet as well
            if packet_results[packet_id]['sub-packet']:

                final_index = litv_result[1]
                update_results = update_litv_parent_packet(packet_results, packet_id, [final_lit_value],
                                                      final_index, ids_of_open_packets, analysis_string_this_packet)

                packet_results = update_results[0]
                ids_of_open_packets = update_results[1]
                analysis_string_this_packet = update_results[2]

                # If the parent packet is now completed, check if the parent of that packet is also now completed
                if len(update_results[3]) == 1:
                    parent_pack_id = update_results[3][0]
                    pp_update_results = update_operator_parent_packet(packet_results, parent_pack_id,
                                                      final_index, ids_of_open_packets, analysis_string_this_packet)

                    packet_results = pp_update_results[0]
                    ids_of_open_packets = pp_update_results[1]
                    analysis_string_this_packet = pp_update_results[2]
                    completed_primary_packets = pp_update_results[3]

                elif len(update_results[3]) > 1:
                    raise AssertionError("LitV closed more than one parent packet")

            # Update analysis string index
            analysis_string_index = litv_result[3]

            # Update packet starting index for the next round
            psind = litv_result[1] + 1
            print(f'Packet starting index for next round: {psind}')

        else:
            # Packet type is 'Operator'
            print(f'--Packet Type: Operator--')
            print(f'Packet starting index (top of Operator processing): {psind}')
            packet_results[packet_id]['typename'] = "Operator"

            # Determine length type
            length_type_id = binary_str[psind + 6]
            print(f'Length Type ID (0 or 1): {length_type_id}')
            packet_results[packet_id]['length_typeid'] = length_type_id

            # Update analysis string for length type 'Z'
            analysis_string_this_packet += "Z"
            analysis_string_index += 1

            # Process packet according to length id
            if length_type_id == '0':
                formatting = "".join([" " for i in range(psind)])

                # Next 15 bits are a number that represents the total length
                # in bits of the sub-packets contained by this packet
                len_of_subpackets_bin = binary_str[psind + 7: psind + 22]
                print(f'15 bit binary string: {len_of_subpackets_bin}')
                print(f'Len of 15 bit binary string: {len(len_of_subpackets_bin)}')

                # Update analysis string for 15 bit length code 'YYYYYYYYYYYYYYY'
                analysis_string_this_packet += 'YYYYYYYYYYYYYYY'
                analysis_string_index += 15

                len_of_subpackets_dec = int(len_of_subpackets_bin, 2)
                ending_index = psind + 21 + len_of_subpackets_dec
                packet_results[packet_id]['subpackets_ending_index'] = ending_index
                print(f'Length of Sub-packets: {len_of_subpackets_dec}')

                # Update analysis string with codes corresponding to bit length of subpackets
                codes_for_sub_packets = "".join(["A" for i in range(len_of_subpackets_dec)])
                analysis_string_this_packet += codes_for_sub_packets

                # Update packet starting index for the next round
                psind = psind + 21 + 1

            else:
                print(f'Packet starting index (top Length ID 1 processing): {psind}')
                # Next 11 bits are a number that represents the number of
                # sub-packets immediately contained by this packet
                print(f'Checking psind: {psind}')
                num_of_subpackets_bin = binary_str[psind + 7: psind + 18]

                # Update analysis string for 15 bit subpacket number code 'XXXXXXXXXXX'
                analysis_string_this_packet += 'XXXXXXXXXXX'
                analysis_string_index += 11

                print(f'Number of Sub-packets binary string: {num_of_subpackets_bin}')
                num_of_subpackets_dec = int(num_of_subpackets_bin, 2)
                print(f'Number of Sub-packets: {num_of_subpackets_dec}')
                packet_results[packet_id]['subpackets_number'] = num_of_subpackets_dec

                # Update analysis string with codes corresponding to the number of subpackets
                analysis_string_this_packet += f" UNKNOWN CHAR LEN ({num_of_subpackets_dec} packets)"

                # Update packet starting index for the next round
                psind = psind + 17 + 1
                print(f'Updated psind for next round: {psind}')

        # Print analysis strings results so far
        for k, v in analysis_strings.items():
            print(v)

        # Add this string to the string dict
        analysis_string_this_packet += f' (packet id {packet_id}) (parent packet ids still open: {ids_of_open_packets})'
        analysis_strings[packet_id] = analysis_string_this_packet

        # Print results from this round
        print(f'\nResults so far for Packet ID {packet_id}')
        for k, v in packet_results[packet_id].items():
            print(f'{k}: {v}')

        # Determine if this is the end of the string
        print('\n====Check if this is the end of the string====')
        print(f'Bits yet to process: {len(binary_str[psind:])}')
        if len(binary_str[psind:]) < 8:
            print(f'Bits yet to process: {len(binary_str[psind:])}')
            string_still_processing = False

        #checking packet id
        print(f'Packet id at end of loop: {packet_id}')

    # Final packet results
    print('\n====Final Results===')
    for packet_entry in packet_results:
        # Print results so far
        print(f'\nFinal results for Packet ID {packet_entry}')
        for k, v in packet_results[packet_entry].items():
            print(f'{k}: {v}')

    # Sum of version numbers answer (from part 1)
    print(f'\nSum of Version Numbers: {sum_of_version_no}\n\n')

    # Print results of packets net yet resolved (debugging)
    print(f'Results of non resolved packets')
    for packet_id_reviewing in packet_results:
        if packet_results[packet_id_reviewing]['final_result'] == 'n/a':
            print(f'\nCurrent Results for Packet ID {packet_id_reviewing}')
            for k, v in packet_results[packet_id_reviewing].items():
                print(f'{k}: {v}')

    for k, v in analysis_strings.items():
        print(v)

    # Final result
    final_result = packet_results[1]['final_result']
    print(f'\nFinal result: {final_result}')

    print(f'\nCompleted Primary Packets (should match the above and only be one result): \n'
          f'{completed_primary_packets}\n\n')

    # Further debugging
    still_debugging = True
    while still_debugging:
        id_to_inspect = int(input("Packet ID to Inspect: "))

        # Collect analysis strings
        debug_strings = [0, id_to_inspect]
        if len(packet_results[id_to_inspect]['subpacketids']) > 0:
            debug_strings += packet_results[id_to_inspect]['subpacketids']

        print(f'\nDebugging Packet ID: {id_to_inspect}')
        for inspected_id in debug_strings:
            print(analysis_strings[inspected_id])

        # Final results of debugging packet
        print(f'\nPacket records to date')
        for inspected_id_2 in debug_strings:
            print(f'\nResults for ID" {inspected_id_2}')
            if inspected_id_2 == 0:
                continue
            else:
                for k, v in packet_results[inspected_id_2].items():
                    print(f'{k}: {v}')

        # Get input regarding continuing debugging or not
        still_debug = input("More debugging (y = Yes, n = No): ")
        if still_debug == 'n':
            still_debugging = False


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Format (input_type, input_source, hexadecimal_dict_source_file_name)
    # input type: 'string' means the input source will be a hexadecimal string
    # input type 'file' means the input source will be a file name of a txt file that has a hexadecimal string in it
    # input source: either the hexadecimal string or the file name of the string, according to input type
    transmission_decoder("file", "transmission_hexadecimal", "hexadecimal")

    # Final result: 1392637195518

    # Testing strings:
    # Literal Value: D2FE28
    # Operator Packet - length type id 0: 38006F45291200
    # Operator Packet - length type id 1: EE00D40C823060

    """Here are a few more examples of hexadecimal-encoded transmissions:

8A004A801A8002F478 represents an operator packet (version 4) which contains 
an operator packet (version 1) which contains an operator packet (version 5) 
which contains a literal value (version 6); this packet has a version sum of 16.

620080001611562C8802118E34 represents an operator packet (version 3) which 
contains two sub-packets; each sub-packet is an operator packet that contains 
two literal values. This packet has a version sum of 12.

C0015000016115A2E0802F182340 has the same structure as the previous example, 
but the outermost packet uses a different length type ID. This packet has a 
version sum of 23.

A0016C880162017C3686B18A3D4780 is an operator packet that contains an 
operator packet that contains an operator packet that contains five literal 
values; it has a version sum of 31.
"""


