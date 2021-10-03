

# Made by Andrew Sameh
# Finished on : 6:31 PM GMT+2 ~ 23/8/2021 ! (DD/MM/YY)
# Updated on : 8:22 AM GMT+2 ~ 1/10/2021 | (DD/MM/YY)

# Info:
# Asks for file (.txt) location and lists top 10 common words
# Option to add a flags to filter results
# flags are down below / must be seperated from file location by space
# ex : plans.txt %l=9       --> this will list top 9 most common words inside file given

#Flag Info:
#   search:{pattern}: --> Searches for all patterns that match the pattern you provide.
#   a:{word}:   --> Finds all words that are EXACT replicas of the word you provide. (case-sensitive)
#   %l={num}    --> Set top ranks from 1 to inf.
#   %m={num}    --> Set Maximum word repeats to be shown.
#   $r          --> Ignore true rank of words.
#   %s={format} --> Save results in log file with format you set in same directory .  
#   $p          --> Doesn't print results.
#   %?          --> Help.

# Lines of Code : 188

import re

flags = [
    ("%l=", "[0-9]+"),
    ("%s=", "\S*"),
    ("%m=", "[0-9]+"),
    ("$r", ""),
    ("$p", ""),
    ("%?", ""),
    ("%s", "")
]

message = "--------------------------------\n\n***This program ranks by default the top 10 most common words in the file you specify***\nWhen prompted, type in the file location/directory you want the program to use.\n\nRECOMMENDED FILE TYPE: .txt\nFlags:\n\n\tsearch:{pattern}: --> Searches for pattern given and returns which line it was found, and number of times it was seen.\n\n\ta:{word}: --> Searches for the SAME word you type and returns results\n\t\n\t\t**NO OTHER FLAG WILL RUN IF ANY OF THE ABOVE IS TYPED** \n\n\t%l={num} --> Edits top ranks from 1 to inf\n\n\t%m={num} --> Set Maximum word repeats to be shown\n\n\t$r       --> Ignore true rank of words\n\n\t$p       --> Doesn't print results\n\n\t%s={format} --> Saves results in log file with format you set in same directory\n\n\t%s       --> Saves results in a .txt format in the same directory\n\n\t%?       --> Help\n\nPROGRAM IGNORES WRONG FLAGS\n\nTo exit program: type 'done'.\nMade by : Andrew Sameh\n-------------------------------\n"

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
        print("Can't read file, please check your spelling and/or directory.\nIf you added a flag, make sure you have a space between location and flag.\ntype '%?' if you need help.")
        return []


def filter(answer) :
    num = 0
    format = "txt"
    max = 0
    save = False
    rank = False
    p = True
    search_For = ""
    absolute = ""
    line = answer
    help = False
    
    if re.search("search:.+:", line) or re.search("a:.+:", line):
        try :
            if re.search("a:.+:", line):
                absolute = re.findall("a:(.+):", line)[0]
            elif re.search("search:.+:", line):
                search_For = re.findall("search:(.+):", line)[0]

            if re.search("%[s]=", line) :   
                try :
                    format = "".join(re.findall("%s=(\S*)", line)[0])
                except :
                    format = "txt"
            if re.search("%[s]", line) :
                save = True
            if re.search("\$p", line) :
                p = False
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
    
    if line.lower() != "done" :
        line = "".join( re.findall(".+\.txt", line) )
        
    return {
        "save": save,
        "num": num,
        "format": format,
        "line": line,
        "max": max,
        "absolute_search": absolute,
        "ranks": rank,
        "search": search_For,
        "print": p,
        "help": help
    }


if __name__ == "__main__" :
    answer = ""
    
    print("Common Word Lister by Andrew Sameh.\n type '%?' if you need help.")
    while answer.lower() != "done" :
        data = filter(input("FileLocation: "))
        answer = data["line"]
        log = []
        
        if answer.lower() != "done" :
            if data["help"] : 
                print(message)
                continue
            else:
                if data["search"] == "" and data["absolute_search"] == "":
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
                    
                    try:
                        handle = open(answer)
                        gram = {}
                        index = 0
                                    
                        if data["search"] != "":
                            print("## All results are lower-cased, this ONLY looks for PATTERNS not words.. ##")
                        elif data["absolute_search"] != "":
                            print("## This search is case-sensitive, results are more accurate than 'search' flag, looks for WORDS ONLY ##")
                                    
                        for line in handle:
                            index = index + 1
                            line = line.rstrip()
                            
                            if data["absolute_search"] == "":
                                if re.search(f"{data['search'].lower()}", line.lower()):
                                    amount = len(re.findall(f"{data['search'].lower()}", line.lower()))
                                    patterns = re.findall(f"(\S*?{data['search'].lower()}\S*?)\s", line.lower())
                                    if amount > 0 and len(patterns) > 0:
                                        log.append(f"Line[{index}]: {amount} :{patterns}\n")
                                        if data["print"] : print(f"Line[{index}]: {patterns} :Found {amount} time(s).\n")
                                        #re.findall(f"{data['search'].lower()}", line.lower())
                                        gram[data['search']] = gram.get(data['search'], 0) + amount
                            else:
                                if re.search(f"{data['absolute_search']}", line):
                                    amount = len(re.findall(f"\s{data['absolute_search']}\s", line))
                                    words = re.findall(f"\s({data['absolute_search']})\s", line)
                                    if amount > 0 and len(patterns) > 0:
                                        log.append(f"Line[{index}]: {amount} :{words}\n")
                                        if data["print"] : print(f"Line[{index}]: {words} :Found {amount} time(s).\n")
                                        gram[data['absolute_search']] = gram.get(data['absolute_search'], 0) + amount
                        try:
                            if data["absolute_search"] == "":
                                print(f"Total times found: {gram[data['search']]}")
                            else:
                                print(f"Total times found: {gram[data['absolute_search']]}")
                        except:
                            print("Search submitted is not found")
                    except:
                        print("Can't read file, please check your spelling and/or directory.\n If you added a flag, make sure you have a space between location and flag.\ntype '%?' if you need help.")
                            
                        
                    
                if data["save"] :
                    with open(f'log.{data["format"]}', "w+") as l :
                        l.write("".join(log))
                    print(f"Saved results in a .{data['format']} log file")
