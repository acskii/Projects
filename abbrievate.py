# Made by : Andrew Sameh
# Finished on 11:12 PM GMT+2 ~ 28/8/2021 (DD/MM/YY)

# Info:
# A program that abbrievates any number in three different formats that is within a 33 numeric character limit
# All abbrievations are below beside variable abbevs 

# Formats:
# (1) Spaces : ex : 1 000 000
# (2) Commas : ex : 1,000,000
# (3) Normal : ex : 1000000

# Lines of Code : 145

import re

message = "Here are all you need to use my program:\n    ***Just type in a number, and the program will abbrievate it***\n    Some formats to look for:\n      (1) Spaces : ex : 1 000 000\n      (2) Normal : ex : 1000000\n      (3) Commas : ex : 1,000,000\n    As always, type 'done' if you wish to exit the program.\nMade by : Andrew Sameh"

# abbevs --> Abbrievation , Number of digits, Number of commas
abbevs = [
    ("K", 4, 1),
    ("M", 7, 2),
    ("B", 10, 3),
    ("T", 13, 4),
    ("Qa", 16, 5),
    ("Qn", 19, 6),
    ("Qd", 21, 7),
    ("Sx", 24, 8),
    ("Sp", 27, 9),
    ("Quad", 30, 10)
]

def abbrievate(number, abbrev) :
    number = int(number)
    dn = 0
    count = 0
    formatted = ""
    
    for char in str(number) :
        count = count + 1
  
    if count > 32 :
        print("Number too big to abbrievate!!")
    else:
        for ab, digits, _ in abbevs :
            if count >= digits and count < digits+3 :
                dn = digits
                abbrev = ab
            else :
                continue
    
        rounded = round(float(number))

        if abbrev != "" :
            formatted = "{0:.1f}".format(rounded / 10**(dn-1)) + abbrev
        else :
            formatted = str(float(number))

    return formatted

def check(answer) :
    send = False
    response, _ = recognise(answer)

    if not re.search("%\?", answer) :
        try :
            if int(float(response)) >= 0 :
                send = True
        except :
            if len(response) > 33 :
                send = False
                print("Number too big to abbrievate!!")
            send = False
    else :
        send = True
        
    return send
    
def recognise(answer) :
    ab = ""
    number = ""
    
    try:
        if re.search("[,]+", answer) :
            if "." in answer :
                number = ""
                ab = ""
            else :
                commas = len(re.findall("[,]+", answer))
                    
                for abv, _, cm in abbevs :
                    if commas == cm :
                        ab = abv
                    else :
                        continue
                    
                filtered = "".join( answer.split(",") ) 
                number = filtered
            
        elif " " in answer :
            if "." in answer :
                number = ""
                ab = ""
            else :
                digits = 0
                number = "".join( answer.split() )
                    
                for entry in answer.split() :
                    for char in entry :
                        digits = digits + 1
                  
                for abv, dn, _ in abbevs :
                    if digits >= dn and digits < dn+3:
                        ab = abv
                    else :
                        continue
                            
        elif re.search("[0-9]*", answer) :
            if "." in answer :
                dots = len(re.findall("\.+", answer))
                
                if dots == 1 :
                    number = str(int(float(answer)))
                    digits = len( re.findall("([0-9]+)\.", answer)[0] )
                    
                    for abv, dn, _ in abbevs :
                        if digits >= dn and digits < dn+3 :
                            ab = abv
                        else :
                            continue
                      
                else :
                    number = ""
                    ab = ""
            else :
                number = str(int(answer))
                digits = len(str(int(answer)))
                
                for abv, dn, _ in abbevs :
                    if digits >= dn and digits < dn+3 :
                        ab = abv
                    else :
                        continue
                
                            
        elif re.search("%\?", answer) :
            number = ""
            ab = ""
    except:
        number = ""
        ab = ""
    
    return number, ab

if __name__ == "__main__" :
    answer = ""
    print("Abbrievater by Andrew Sameh.\ntype '%?' if you need help.")
    
    while answer != "done" :
        print("---------------------")
        answer = input("Enter Number Here: ")
        
        if answer != "done" :
            if check(answer) :
                number, abbev = recognise(answer)
                
                if answer == "%?":
                    print(message)
                else:
                    print(abbrievate(number, abbev))
            else :
                print("Can't abbrievate.\nPlease make sure you input numeric characters only OR follow our formatting rules")
                continue    
            
