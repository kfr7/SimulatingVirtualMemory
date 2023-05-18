



if __name__ == "__main__":
    PM = [0] * 524288
    D = [[0] * 512] * 1024
    
    print(len(PM))
    print(len(D))
    print(len(D[0]))


    with open("first.txt", "r") as first_file:
        for triplet_commands in first_file:
            # get commands without extra spaces on either side
            triplet_commands = triplet_commands.strip()
            # parse commands into list of strings
            triplet_commands = triplet_commands.split()
            # flag of which line we are on
            first_line = True
            # iterate through list using triple indices
            first = 0
            second = 1
            third = 2
            while first < len(triplet_commands):
                if first_line:
                    # triplets of (segment, length, frame)
                    segment = int(triplet_commands[first])
                    length = int(triplet_commands[second])
                    frame = int(triplet_commands[third])
                    # print(f"DEBUG: S:{segment}, L:{length}, F:{frame}")
                else:
                    # triplets of (segment, page, frame)
                    segment = int(triplet_commands[first])
                    page = int(triplet_commands[second])
                    frame = int(triplet_commands[third])
                    # print(f"DEBUG: S:{segment}, P:{page}, F:{frame}")

                # shift all indicies right three times
                first += 3
                second += 3
                third += 3
                # indicate first line is done
                if first_line:
                    first_line = False
                
            