# SimulatingVirtualMemory
Simulate interaction between physical memory and virtual memory.

HOW TO RUN:
(Program uses Python so it will be needed to be downloaded on the machine)
1) Place both of the command files (initialization and input) in the same directory as "virtual_memory_*.py"
2) Name the init text file: "first.txt"
3) Name the input text file (one with VM addresses): "second.txt"
4) In terminal, change directories into the directory which contains both files, and 
    enter "python3 virtual_memory_no_dp.py" or "python3 virtual_memory_with_dp.py" (preferred - demand paging)
    Depending on your machine, you might be able to just put "python" instead of "python3"
    To redirect to a file, just add " > output.txt" to the end of the commands mentioned above

LIST OF FILES IN ZIP:
1) "virtual_memory_no_dp.py": main python file that has ALL the code
    needed to compute physical memory addresses given
    virtual memory addresses but does not use demand paging.
2) "virtual_memory_with_dp.py": main python file that has ALL the code
    needed to compute physical memory addresses given
    virtual memory addresses and does implement demand paging.
3) "README.md": describes how to run and list of files in zip.
4) "output-dp.txt" is the output file using demand paging
5) "output-no-dp.txt" is the output file without demand paging

Remember: 
Name the folder that you are going to compress into a zip file: project2_Kian_Ranjbar
and the zip file should be named the same thing but with project2_Kian_Ranjbar.zip (zip extension)
