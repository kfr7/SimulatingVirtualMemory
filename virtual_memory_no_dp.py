# virtual_memory_no_dp.py

def decode_virtual_address(virtual_address: int) -> tuple((int, int, int, int)):
    """
    Use bitwise operations to derive 
    segment number s, page number p,
    word number w, and page word offset number pw

    :param virtual_address: number of the virtual address number to be translated
    :return: tuple of (s, p, w, pw)
    """
    s = virtual_address >> 18
    p = (virtual_address >> 9) & 511
    w = 511 & virtual_address
    pw = 262143 & virtual_address
    return (s, p, w, pw)


if __name__ == "__main__":
    PM = [0] * 524288
    # D = [[0] * 512] * 1024    # don't need disk for this version

    with open("first.txt", "r") as first_file:
        # flag of which line we are on
        first_line = True
        for triplet_commands in first_file:
            # get commands without extra spaces on either side
            triplet_commands = triplet_commands.strip()
            # parse commands into list of strings
            triplet_commands = triplet_commands.split()
            # iterate through list using triple indices
            first = 0
            second = 1
            third = 2
            while first < len(triplet_commands):
                if first_line:
                    # triplets of (segment, length, frame/block(negative))
                    segment = int(triplet_commands[first])
                    length = int(triplet_commands[second])
                    frame_block = int(triplet_commands[third])
                    # store entry information for segment table
                    PM[2*segment] = length
                    PM[2*segment+1] = frame_block
                    # print(f"DEBUG: S:{segment}, L:{length}, F/B:{frame_block}")
            
                else:
                    # triplets of (segment, page, frame/block(negative))
                    segment = int(triplet_commands[first])
                    page = int(triplet_commands[second])
                    frame_block = int(triplet_commands[third])
                    # store entry information for page table
                    PM[PM[2*segment+1]*512+page] = frame_block
                    # print(f"DEBUG: S:{segment}, P:{page}, F/B:{frame_block}")

                # shift all indicies right three times
                first += 3
                second += 3
                third += 3

            # indicate first line is done
            if first_line:
                first_line = False

    with open("second.txt", "r") as first_file:
        for virtual_addresses in first_file:
            # get commands without extra spaces on either side
            virtual_addresses = virtual_addresses.strip()
            # parse commands into list of strings
            virtual_addresses = virtual_addresses.split()

            for virtual_address in virtual_addresses:
                s, p, w, pw = decode_virtual_address(int(virtual_address))
                # print("DEBUG (s, p, w, pw):", s, p, w, pw)
                # print("DEBUG PM[2*s]", PM[2*s])
                # before anything, must do error checks
                if s < 0 or s >= 512:
                    # segment does not exist
                    print(-1, end=" ")
                elif PM[2*s] == 0 and PM[2*s+1] == 0:
                    # the segment is not being used
                    print(-1, end=" ")
                elif pw >= PM[2*s]:
                    # access is out of bounds so error
                    print(-1, end=" ")
                else:
                    # now get the frame of page table
                    frame_of_pt = PM[2*s+1]
                    if frame_of_pt < 0:
                        # MAYBE DELETE THIS IF STATEMENT
                        # checks if that page was initialized with some block 
                        # (this version is without blocks though so say it's an error)
                        print(-1, end=" ")
                        continue

                    # now get the frame of the page
                    frame_of_p = PM[frame_of_pt*512+p]
                    if frame_of_p == 0:
                        # MAYBE DELETE THIS IF STATEMENT
                        # checks if that page was initialized with some frame or not
                        print(-1, end=" ")
                        continue
                    elif frame_of_p < 0:
                        # MAYBE DELETE THIS IF STATEMENT
                        # checks if that page was initialized with some block 
                        # (this version is without blocks though so say it's an error)
                        print(-1, end=" ")
                        continue

                    # now we can print the address
                    print(frame_of_p*512+w, end=" ")
    