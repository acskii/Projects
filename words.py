

# Made by Andrew Sameh
# Finished on : 6:31 PM GMT+2 ~ 23/8/2021 ! (DD/MM/YY)
# Updated on : 7:26 AM GMT+2 _ 1/10/2021 | (DD/MM/YY)

# Info:
# Asks for file (.txt) location and lists top 10 common words
# Option to add a flags to filter results
# flags are down below / must be seperated from file location by space
# ex : plans.txt %l=9       --> this will list top 9 most common words inside file given

#Flag Info:
#   %l={num}    --> Set top ranks from 1 to inf
#   %m={num}    --> Set Maximum word repeats to be shown
#   $r          --> Ignore true rank of words
#   %s={format} --> Save results in log file with format you set in same directory   
#   $p          --> Doesn't show results
#   %?          --> Help

# Lines of Code : 110

import re

flags = [
    ("%l=", "[0-9]+"),
    ("%s=", ".+"),
    ("%m=", "[0-9]+"),
    ("$r", ""),
    ("$p", ""),
    ("%?", ""),
    ("%s", "")
]

message = "Here is all help you need:\nWhen prompted, type in the file location/directory you want the program to use.\n***This program ranks by default the top 10 most common words in the file you specify***\nRECOMMENDED FILE TYPE: .txt\nFlags:\n\tsearch:{pattern}: --> Searches for pattern given and returns number of times it was seen. \n\t<<<<<NO OTHER FLAGS WILL RUN IF THIS IS TYPED: THIS MUST BE TYPED AS FIRST FLAG!<<<<< \n\n\t%l={num} --> Set top ranks from 1 to inf\n\t%m={num} --> Set Maximum word repeats to be shown\n\t$r       --> Ignore true rank of words\n\t$p       --> Doesn't show results\n\t%s={format} --> Saves results in log file with format you set in same directory\n\t%s --> Saves results in a .txt format in the same directory\n\t%?       --> Help\n\nPROGRAM IGNORES WRONG FLAGS\nTo exit program: type 'done'.\nMade by : Andrew Sameh"

def sort(fileName) :
    try :
        handle = open(fileName)
        gram = {}
        
        for line in handle :
            line = line.rstrip()
            for word in line.split() :
                gram[word] = gram.get(word, 0) + 1
        
        return sorted( [ (v,k) for k,v in gram.items() ] , reverse=True)
        
    except :
        print("Can't read file, please check your spelling and/or directory.\n If you added a flag, make sure you have a space between location and flag.\ntype '%?' if you need help.")
        return []


def filter(answer) :
    num = 0
    format = "txt"
    max = 0
    save = False
    rank = False
    p = True
    search_For = ""
    line = answer
    help = False
    
    if re.search("search:", line):
        try :
            search_For = re.findall("search:(.+):", line)[0]
            
            if re.search("%[s]", line) :
                save = True
        except :
            search_For = ""
    else:
        for flag, value in flags :
            if flag == "%l=" :
                try:
                    num = int(re.findall(f"{flag}({value})", line)[0])
                except:
                    num = 0
            elif flag == "%s=" :
                if re.search("%[s]=", line) :
                    save = True
                    
                    try :
                        format = "".join(re.findall(f"{flag}({value})", line)[0])
                    except :
                        format = "txt"
            elif flag == "%s" :
                if re.search("%[s]", line) :
                    save = True
                    
            elif flag == "%m=" :
                try:
                    max = int(re.findall(f"{flag}({value})", line)[0])
                except:
                    max = 0
            elif flag == "$r" :
                if re.search("\$r", line) :
                    rank = True
            elif flag == "$p" :
                if re.search("\$p", line) :
                    p = False
            elif flag == "%?" :
                if re.search("%\?", line) :
                    help = True
    
    if line != "done" :
        line = "".join( re.findall(".+\.txt", line) )
        
    return {
        "save": save,
        "num": num,
        "format": format,
        "line": line,
        "max": max,
        "ranks": rank,
        "search": search_For,
        "print": p,
        "help": help
    }


if __name__ == "__main__" :
    answer = ""
    
    print("Common Word Lister by Andrew Sameh.\n type '%?' if you need help.")
    while answer != "done" :
        data = filter(input("FileLocation: "))
        answer = data["line"]
        log = []
        
        if answer != "done" :
            if data["help"] : 
                print(message)
                continue
            else:
                if data["search"] == "" :
                    log = []
                    if data["num"] == 0 : data["num"] = 10
                    if data["max"] == 0 : data["max"] = None
                    print("-----------------------------")
                    rank = 0
                    for value, key in sort(answer)[:data["num"]] :
                        if not data["ranks"] : rank = rank + 1
                        if data["max"] is None or value <= data["max"]:
                            if data["ranks"] : rank = rank + 1
                            if data["print"] : print(f"[{rank}]: {key} :[{value}]")
                            if data["save"] :
                                log.append(f"[{rank}]: {key} :[{value}]\n")
                else :
                    print("-----------------------------")
                    
                    #try:
                    handle = open(answer)
                    gram = {}
                    index = 0
                                
                    for line in handle:
                        index = index + 1
                        line = line.rstrip()
                            
                        if re.search(f"{data['search'].lower()}", line.lower()):
                            amount = len(re.findall(f"{data['search'].lower()}", line.lower()))
                            patterns = re.findall(f"(\S*?{data['search'].lower()}\S*?)\s", line.lower())
                            log.append(f"Line[{index}]: {amount} :{patterns}\n")
                            if data["print"] : print(f"Line[{index}]: {patterns} :Found {amount} time(s).\n")
                            #re.findall(f"{data['search'].lower()}", line.lower())
                            gram[data['search']] = gram.get(data['search'], 0) + amount
                                 
                    try:
                        print(f"Total times found: {gram[data['search']]}")
                    except:
                        print("Search submitted is not found")
                    #except:
                    #    print("Can't read file, please check your spelling and/or directory.\n If you added a flag, make sure you have a space between location and flag.\ntype '%?' if you need help.")
                            
                        
                    
                if data["save"] :
                    with open(f'log.{data["format"]}', "w+") as l :
                        l.write("".join(log))
                    print(f"Saved results in a .{data['format']} log file")
