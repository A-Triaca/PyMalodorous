__author__ = 'Alex'

def ReplaceSingleQuote(password):
    tempPassword = ""
    for i in range(password.__len__()):
        if(password[i] == "'"):
            tempPassword += "''"
        else:
            tempPassword += password[i]
    return tempPassword

def GetCharacterPlacement(password):
    characterList = []
    if(not password.__contains__("'")):
        for i in range(password.__len__()):
            characterList.append((password[i], str(i)))
    else:
        for i in range(password.__len__()):
            if(password[i] == "'"):
                characterList.append(("''", str(i)))
            else:
                characterList.append((password[i], str(i)))
    return characterList

def GetAdvancedMask(password):
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

def GetCharacterSet(password):
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

def GetMarkovChain(password):
    chain = []
    if(not password.__contains__("'")):
        for i in range(len(password)-1):
            chain.append((password[i], password[i+1]))
    else:
        for i in range(len(password)-1):
            if(password[i] == "'" and password[i+1]):
                chain.append(("''", "''"))
            elif(password[i] == "'"):
                chain.append(("''", password[i+1]))
            elif(password[i+1] + "'"):
                chain.append((password[i], "''"))
            else:
                chain.append((password[i], password[i+1]))
    return chain

def GetNGrams(password):
    nGram = []
    if(not password.__contains__("'")):
        for i in range(2, len(password)):
            for j in range(len(password)-i + 1):
                nGram.append((i, password[j:j+i], j, 0))
    else:
        for i in range(2, len(password)):
            for j in range(len(password)-i + 1):
                nGram.append((i, ReplaceSingleQuote(password[j:j+i]), j, 0))
    return  nGram

def GetNGramsUnsigned(password):
    nGram = []
    password = password.lower()
    if(not password.__contains__("'")):
        for i in range(2, len(password)):
            for j in range(len(password)-i + 1):
                nGram.append((i, password[j:j+i], j, 1))
    else:
        for i in range(2, len(password)):
            for j in range(len(password)-i + 1):
                nGram.append((i, ReplaceSingleQuote(password[j:j+i]), j, 1))
    return  nGram

def GetSimpleMask(password):
    prev = mask = ""
    for i in range(len(password)):
        curr = GetTypeOfCharacter(password[i])
        if (curr != prev):
            prev = curr
            mask += curr
    return mask

def GetTypeOfCharacter(character):
    if (character.islower()):
        return "$l"
    elif (character.isupper()):
        return "$u"
    elif (character.isdigit()):
        return "$d"
    else:
        return "$s"

