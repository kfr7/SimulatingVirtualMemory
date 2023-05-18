# SimulatingVirtualMemory
Simulate interaction between physical memory and virtual memory.

HOW TO RUN:
(Program uses Python so it will be needed to be downloaded
on the system)
1) Place both of the commands text files in the same directory as "virtual_memory.py"
2) Name the first text file: "first.txt"
3) Name the second text file (one with VM addresses): "second.txt"
4) In terminal, change directories into the directory 
    which contains both files, and 
    enter "python3 virtual_memory_no_dp.py" or 
    "python3 virtual_memory_with_dp.py" (preferred since this file has demand paging implemented)
    Depending on your machine, you might be able to just put "python" instead of "python3"
    To redirect to a file, just add " > output.txt" to the end of the commands mentioned above

LIST OF FILES IN ZIP:
1) "virtual_memory_no_dp.py": main python file that has ALL the code
    needed to compute physical memory addresses given
    virtual memory addresses but does not use demand paging.
2) "virtual_memory_with_dp.py": main python file that has ALL the code
    needed to compute physical memory addresses given
    virtual memory addresses and IMPLEMENTS demand paging.
2) "README.md": describes how to run and list of files in zip.
