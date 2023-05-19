# virtual_memory_with_dp.py

from queue import PriorityQueue    # maintains free frame list

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

def read_block(block: int, frame: int) -> None:
    """
    Copy content of block (512 words/integers) int
    specified frame (512 words/integers)

    :param block: block number of disk to read from
    :param frame: frame number of physical memory to copy into
    """
    disk_index = block*512
    physical_index = frame*512
    for _ in range(512):
        PM[physical_index] = D[disk_index]
        disk_index += 1
        physical_index += 1


if __name__ == "__main__":
    PM = [0] * 524288   # physical memory
    D = [0] * 524288    # disk (logical/virtual memory)
    FF = PriorityQueue(0)   # initialize free frames AFTER filling memory hierarchy
    frames_allocated = set()    # keep track of which ones we used to not add it
                                # into initial free frame list
    frames_used_for_page_faults = set()

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
                    # indicate that the frame for the segment table is now being used
                    if frame_block >= 0:    # if frame is positive
                        # add the frame that is being used for the page table for this segment
                        frames_allocated.add(frame_block)
                    # print(f"DEBUG: S:{segment}, L:{length}, F/B:{frame_block}")

                else:
                    # triplets of (segment, page, frame/block(negative))
                    segment = int(triplet_commands[first])
                    page = int(triplet_commands[second])
                    frame_block = int(triplet_commands[third])
                    # store entry information for page table
                    # two cases, 
                    if PM[2*segment+1] < 0:
                        # 1) frame where page table begins is negative (on disk)
                        D[abs(PM[2*segment+1])*512+page] = frame_block
                    else:
                        # 2) frame where page table begins is positive (on physical memory)
                        PM[PM[2*segment+1]*512+page] = frame_block
                    # if frame is positive then that is the one that is now used
                    if frame_block >= 0:    # if frame is positive
                        frames_allocated.add(frame_block)

                    # print(f"DEBUG: S:{segment}, P:{page}, F/B:{frame_block}")

                # shift all indicies right three times
                first += 3
                second += 3
                third += 3

            # indicate first line is done
            if first_line:
                first_line = False

    # fill free frames without including ones used above in input
    for i in range(2, 1024):
        if i not in frames_allocated:
            FF.put(i)

    with open("second.txt", "r") as first_file:
        for virtual_addresses in first_file:
            # get commands without extra spaces on either side
            virtual_addresses = virtual_addresses.strip()
            # parse commands into list of strings
            virtual_addresses = virtual_addresses.split()

            for virtual_address in virtual_addresses:
                s, p, w, pw = decode_virtual_address(int(virtual_address))
                # print()
                # print(f"DEBUG for {virtual_address} (s={s}, p={p}, w={w}, pw={pw})")
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
                    # check if it is a frame or block (positive or negative)
                    if frame_of_pt < 0:
                        # if negative, then we need to retrieve that block and put it into 
                        # the first free frame
                        smallest_free_frame = FF.get()  # get and remove smallest free frame
                        frames_used_for_page_faults.add(smallest_free_frame)   # for debug purposes
                        # copy block content of page table into frame of physical memory
                        read_block(abs(frame_of_pt), smallest_free_frame)
                        # update segment table frame entry with new frame in 
                        # which page table resides for that segment
                        PM[2*s+1] = smallest_free_frame
                        # continue translation with new updated frame_of_pt
                        frame_of_pt = smallest_free_frame
                        
                    # now get the frame of the page
                    frame_of_p = PM[frame_of_pt*512+p]
                    # check if it is a frame or block (positive or negative)
                    if frame_of_p == 0:
                        # MAYBE DELETE THIS IF STATEMENT
                        # checks if that page was initialized with some frame or not
                        print(-1, end=" ")
                        continue
                    elif frame_of_p < 0:
                        # if negative, then we need to retrieve that block and put it into 
                        # the first free frame
                        smallest_free_frame = FF.get()  # get and remove smallest free frame
                        frames_used_for_page_faults.add(smallest_free_frame)   # for debug purposes
                        # copy block content of page table into frame of physical memory
                        read_block(abs(frame_of_p), smallest_free_frame)
                        # update page table entry with new update frame
                        # that contains the specified page
                        PM[frame_of_pt*512+p] = smallest_free_frame
                        # continue translation with new updated frame_of_p
                        frame_of_p = smallest_free_frame
                    # now we can print the address
                    print(frame_of_p*512+w, end=" ")
    # print()
    # print("DEBUG")
    # print(f"Frames used when getting input:")
    # print(frames_allocated)
    # print(f"Frames used when dealing with page faults:")
    # print(frames_used_for_page_faults)
    