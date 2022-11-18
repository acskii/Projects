# Made by Andrew Sameh
# Finished on : 6:23 PM GMT+2 ~ 16/11/2022 ! (DD/MM/YY)
# Last Updated on : 5:30 PM GMT+2 ~ 18/11/2022 | (DD/MM/YY)

# Flags that can be used:
# [1] -->   maxsl={int}   
#     -->   Limits the program to output only to a specified sub-directory, 0 being only the files and folders in the directory chosen

# [2] -->   count={files/folders}   OR  count=({files/folders}, {files/folders})
#     -->   Keeps count of the number of files/folders
#     -->   The () means that you will be listing elements, one wanting to count both files and folders would write count=(files, folders)

# [3] -->   filetype={FILE TYPE}  OR  filetype=({FILE TYPE}, {FILE TYPE}, ...)
#     -->   Limits the program to only output files with the specified file extension, FOLDERS WILL BE OUTPUT NORMALLY
#     -->   The () means that you will be listing elements, e.g. filetype=(py, txt, png, pdf)

# Lines of Code : 166

import os, re, math, sys, time, threading, codecs
from pathlib import Path

byte_sizes=[
	["bytes", 0],
	["KB", 1000],
	["MB", 1000000],
	["GB", 1000000000],
]

SaveFile = str(Path.home())+"\\Desktop\\dirlist.log"
MegaList = []
ShowSizes = True
ShowPrints = True
Level = 0

def defineSize(num):
    for Count in range(0, len(byte_sizes)-1):
        if num > byte_sizes[Count][1] and num < byte_sizes[Count+1][1]:
            Pack = byte_sizes[Count]
        elif num == byte_sizes[Count][1]:
            Pack = byte_sizes[Count]
    if num >= byte_sizes[len(byte_sizes)-1][1]:
        Pack = byte_sizes[len(byte_sizes)-1]

    if Pack[0] != "bytes":
        First = str(math.floor(num/Pack[1]))
        if re.match(f"^{First}", str(num)):
            EndIndex = len(str(First))-1
            AfterDot = str(num)[EndIndex+1] + str(num)[EndIndex+2]
            return First+"."+AfterDot+" "+Pack[0]
    else: return str(num) + " bytes"

def recogniseCmd(text):
    Cmds = {
        "Sub-levels": 999,
        "Count-Folders": False,
        "Count-Files": False,
        "Specified-Type": ["All"],
    }
    if re.match("[\s\S]*maxsl=\S+\s*", text):
        try:
            Cmds["Sub-levels"] = int(re.findall("[\s\S]*maxsl=(\S+)\s*", text)[0])
        except:
            print("[LOG]: Attempt to enter non-integer value in flag 'maxsl' of ", re.findall("[\s\S]*maxsl=(\S+)\s*", text)[0])
            Cmds["Sub-levels"] = None
    if re.match("[\s\S]*count=.+\s*", text):
        Items = re.findall("[\s\S]*count=(.+)\s*", text)[0]
        if re.match("\(.+\)", Items):
            Items = str(Items).replace("(", "")
            Items = str(Items).replace(")", "")
            ls = re.findall("\s*([^,]+)[,]*\s*", Items)
            for i in ls:
                if i == "files":  Cmds["Count-Files"] = True
                elif i == "folders": Cmds["Count-Folders"] = True
        else:
            if re.match("files", Items): Cmds["Count-Files"] = True
            elif re.match("folders", Items): Cmds["Count-Folders"] = True
    if re.match("[\s\S]*filetype=.+\s*", text):
        Items = re.findall("[\s\S]*filetype=(.+)\s*", text)[0]
        if re.match("\(.+\)", Items):
            Items = str(Items).replace("(", "")
            Items = str(Items).replace(")", "")
            ls = re.findall("\s*([^,]+)[,]*\s*", Items)
            Cmds["Specified-Type"] = []
            for i in ls:
                Cmds["Specified-Type"].append(i)
        else:
            Cmds["Specified-Type"] = [Items]

    return Cmds
def loading():
    if not ShowPrints:
        stages=["\\\\", "||", "//", "--"]
        while ShowPrints == False:
            for stage in stages:
                sys.stdout.write("Waiting for Completion.. {0}\r".format(stage))
                time.sleep(.1)
                sys.stdout.flush()
        time.sleep(1)
        sys.stdout.flush()
        sys.stdout.write("\n")
        print("Process Completion: DONE.\n")
        time.sleep(2)

ParentDir = input("Enter Directory:  ")
while os.path.exists(ParentDir) != True:
    ParentDir = input("Enter Directory:  ")
if len(re.findall("$.*(\\\)", ParentDir)) == 0: ParentDir = ParentDir + "\\"


# remove/comment out code below if the default values are to your liking and you never intend to let the user change them
#----------------------------------------------------------------------------------------------------------------------------
Ask = input("Would you like to show file sizes (Y/N)? ")
while  Ask != "Y" and Ask != "N":
    Ask = input("Would you like to show file sizes (Y/N)? ")
if Ask == "Y": ShowSizes = True 
else: ShowSizes = False
Ask = input("Would you like to show printing process (Y/N)? ")
while  Ask != "Y" and Ask != "N":
    Ask = input("Would you like to show printing process (Y/N)? ")
if Ask == "Y": ShowPrints = True 
else: ShowPrints = False
#----------------------------------------------------------------------------------------------------------------------------
cmds = recogniseCmd(input("Enter desired flags here (press ENTER to dimiss):  "))
Folders = 0
Files = 0

q = threading.Thread(target=loading)
q.start()
for (dirpath, dirnames, filenames) in os.walk(ParentDir):
    try:
        # Finding which level I am in
        Level = (dirpath.count("\\")-ParentDir.count("\\"))

        # Printing the directory name
        if (len(dirnames) + len(filenames)) > 0: 
            if os.path.basename(dirpath) != os.path.basename(ParentDir):
                if (Level) <= cmds["Sub-levels"]:
                    if cmds["Count-Folders"] == True: Folders += 1
                    MegaList.append(("  "*(Level))+f"[{os.path.basename(dirpath)}]: \n")
                    if ShowPrints: print(("  "*(Level))+f"[{os.path.basename(dirpath)}]: ")    
        else: 
            if (Level) <= cmds["Sub-levels"]:
                if cmds["Count-Folders"] == True: Folders += 1
                MegaList.append(("  "*(Level))+f"[{os.path.basename(dirpath)}]: EMPTY \n")
                if ShowPrints: print(("  "*(Level))+f"[{os.path.basename(dirpath)}]: EMPTY")
            

        # Printing the files within the current directory
        for file in filenames:
            Level = (os.path.join(dirpath, file).count("\\")-ParentDir.count("\\"))
            if (Level) <= cmds["Sub-levels"]:
                if ShowSizes: Extra = f"  --// {defineSize(os.stat(os.path.join(dirpath, file)).st_size)}"
                else: Extra = ""

                if cmds["Specified-Type"][0] == "All":
                    if cmds["Count-Files"] == True: Files += 1
                    MegaList.append(("  "*(Level))+"--> "+file+Extra+"\n")
                    if ShowPrints: print(("  "*(Level))+"--> "+file)
                else:
                    for t in cmds["Specified-Type"]:
                        if file.lower().endswith(f".{t}"):
                            if cmds["Count-Files"] == True: Files += 1
                            MegaList.append(("  "*(Level))+"--> "+file+Extra+"\n")
                            if ShowPrints: print(("  "*(Level))+"--> "+file)

    except FileNotFoundError:
        print("[LOG]: Couldn't be found: ", dirpath)
        continue

with codecs.open(SaveFile, "w", encoding="utf-8") as savefile:
    for entry in MegaList:
        try:
            savefile.writelines([entry])
        except:
            print("[ERROR]: error occured while trying to save file entry of: ", entry)
            savefile.writelines(["--------------------------------------------//ENTRY REDACTED FOR CAUSING ERROR\\\\--------------------------------------------\n"])
            continue
print("Saved all valid entries in file: ", SaveFile)
if cmds["Count-Folders"]: print("FOLDERS FOUND: ", Folders)
if cmds["Count-Files"]: print("FILES FOUND: ", Files)
ShowPrints = True
MegaList = []
time.sleep(2)
input("::Press ENTER to close program::")