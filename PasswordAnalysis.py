__author__ = 'Alex'

def ReplaceSingleQuote(password):
    tempPassword = ""
    for i in range(password.__len__()):
        if(password[i] == "'"):
            tempPassword += "''"
        else:
            tempPassword += password[i]
    return tempPassword

def CharacterPlacement(password):
    characterList = []
    for i in range(password.__len__()):
        characterList.append((password[i], i))
    return characterList

def AdvancedMask(password):
    advancedMask = ""

    for character in password:
        if(character.islower()):
            advancedMask += "$l"
        elif(character.isupper()):
            advancedMask += "$u"
        elif(character.isdigit()):
            advancedMask += "$d"
        else:
            advancedMask += "$s"

    return advancedMask

def CharacterSet(password):
    characterSet = ""
    lower = upper = digit = special = False

    for character in password:
        if (character.islower()):
            lower = True
        elif (character.isupper()):
            upper = True
        elif (character.isdigit()):
            digit = True
        else:
            special = True

    if (lower and upper):
        characterSet += "Alpha"
    elif(lower):
        characterSet += "Loweralpha"
    elif(upper):
        characterSet += "Upperalpha"

    if (digit):
        characterSet += "Numeric"
    if (special):
        characterSet += "Special"

    return characterSet

def MarkovChain(password):
    chain = []
    for i in range(len(password)-1):
        chain.append((password[i], password[i+1]))
    return chain

def NGrams(password):
    nGram = []
    for i in range(2, len(password)):
        for j in range(len(password)-i + 1):
            nGram.append((i, password[j:j+i], j, 0))
    return  nGram

def NGramsUnsigned(password):
    nGram = []
    password = password.lower()
    for i in range(2, len(password)):
        for j in range(len(password)-i + 1):
            nGram.append((i, password[j:j+i], j, 1))
    return  nGram

def SimpleMask(password):
    prev = mask = ""
    for i in range(len(password)):
        curr = TypeOfCharacter(password[i])
        if (curr != prev):
            prev = curr
            mask += curr
    return mask

def TypeOfCharacter(character):
    if (character.islower()):
        return "$l"
    elif (character.isupper()):
        return "$u"
    elif (character.isdigit()):
        return "$d"
    else:
        return "$s"

