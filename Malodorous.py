__author__ = 'Alex'

import pyodbc
import datetime
from os import walk
import time

def InsertAdvancedMask(password, passwordId, connection, cursor):
    cursor.execute("INSERT INTO dbo.AdvancedMask "
                       "(Mask, OriginalPassword) "
                       "VALUES ('" + GetAdvancedMask(password) + "', " + str(passwordId) + ");")
    connection.commit()

def ReplaceSingleQuote(password):
    tempPassword = ""
    for i in range(password.__len__()):
        if(password[i] == "'"):
            tempPassword += "''"
        else:
            tempPassword += password[i]
    return tempPassword

def DropDatabase(connection, cursor):
    file = open("Database/Drop Tables.sql", 'r')
    sql = " ".join(file.readlines())
    cursor.execute(sql)
    connection.commit()

def CreateDatabase(connection, cursor):
    file = open("Database/Create Tables.sql", 'r')
    sql = " ".join(file.readlines())
    cursor.execute(sql)
    connection.commit()

def SetUpCharacterSet(connection, cursor):
    file = open("Database/Insert Into CharacterSet.sql", 'r')
    sql = " ".join(file.readlines())
    cursor.execute(sql)
    connection.commit()

def setUpAvailability(connection, cursor):
    file = open("Database/Insert Into Availability.sql", 'r')
    sql = " ".join(file.readlines())
    cursor.execute(sql)
    connection.commit()

def InsertPassword(password, passwordOrigin, connection, cursor):
    cursor.execute("INSERT INTO dbo.Password (Password, PasswordOrigin, Length, DateAdded, Deleetified) " \
           "VALUES ('" + password + "', '" + str(passwordOrigin) + "', " + str(password.__len__()) + ", '" +
                   str(datetime.datetime.now()) + "', '" + str(False) + "');")
    connection.commit()

def InsertCharacterPlacement(password, passwordId, connection, cursor):
    InsertStatement = "INSERT INTO dbo.CharacterPlacement " \
                      "(Character, Placement, OriginalPassword) VALUES "

    for character in GetCharacterPlacement(password):
        InsertStatement += "('" + character[0] + "', " + character[1] + ", " + str(passwordId) + "),"

    InsertStatement = InsertStatement[:-1]
    cursor.execute(InsertStatement)
    connection.commit()

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

def InsertCharacterSet(password, passwordId, connection, cursor):
    cursor.execute("INSERT INTO dbo.Complexity (CharacterSet, OriginalPassword) VALUES ('" + GetCharacterSet(password) + "', " + str(passwordId) + ")")
    connection.commit

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

def InsertMarkovChain(password, passwordId, connection, cursor):
    InsertStatement = "INSERT INTO dbo.MarkovChain " \
                      "(FirstCharacter, SecondCharacter, OriginalPassword) VALUES "
    for chain in GetMarkovChain(password):
        InsertStatement += "('" + chain[0] + "', '" + chain[1] + "', " + str(passwordId) + "),"
    InsertStatement = InsertStatement[:-1]
    cursor.execute(InsertStatement)
    connection.commit()

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

def InsertNGrams(password, passwordId, connection, cursor):
    InsertStatement = "INSERT INTO dbo.NGrams " \
                      "(Lenth ,NGram ,Placement, Unsigned, OriginalPassword) VALUES "
    for nGram in GetNGrams(password):
        InsertStatement += "(" + str(nGram[0]) + ", '" + nGram[1] + "', " + \
                           str(nGram[2]) + ", " + str(nGram[3]) + ", " + \
                           str(passwordId) + "),"
    InsertStatement = InsertStatement[:-1]
    cursor.execute(InsertStatement)
    connection.commit()

def InsertNGramUnsigned(password, passwordId, connection, cursor):
    InsertStatement = "INSERT INTO dbo.NGrams " \
                      "(Lenth ,NGram ,Placement, Unsigned, OriginalPassword) VALUES "
    for nGram in GetNGramsUnsigned(password):
        InsertStatement += "(" + str(nGram[0]) + ", '" + nGram[1] + "', " + \
                           str(nGram[2]) + ", " + str(nGram[3]) + ", " + \
                           str(passwordId) + "),"
    InsertStatement = InsertStatement[:-1]
    cursor.execute(InsertStatement)
    connection.commit()

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

def InsertSimpleMask(password, passwordId, connection, cursor):
    InsertStatement = "INSERT INTO dbo.SimpleMask " \
                      "(Mask, OriginalPassword) VALUES "
    InsertStatement += "('" + GetSimpleMask(password) + "', " + str(passwordId) + ")"
    cursor.execute(InsertStatement)
    connection.commit()

def GetAvailability(connection, cursor):
    message = "What is the difficulty of obtaining the database?\n"
    catagories = cursor.execute("SELECT * FROM dbo.Availability")
    for option in catagories:
        message += str(option[0]) + " - " + option[1] + "\n"
    availability = input(message)
    catagory = cursor.execute("SELECT * FROM dbo.Availability WHERE AvailabilityId = " + availability).fetchone()[1]
    print("You have chosen: " + catagory)
    return availability

def AddPasswordOriginToDatabase(file, connection, cursor):
    availability = GetAvailability(connection, cursor)
    cursor.execute("INSERT INTO PasswordOrigin (Origin, Availability, DateAdded) VALUES ('" + file + "', '" + availability + "', '" + str(datetime.datetime.now()) + "')")
    connection.commit()


def main():
    ##Setup connection to SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;'
                          'DATABASE=Malodorous;UID=sa;PWD=password')
    cursor = connection.cursor()
    ##Drop and recreate the database
    DropDatabase(connection, cursor)
    CreateDatabase(connection, cursor)
    setUpAvailability(connection, cursor)
    #SetUpCharacterSet(connection, cursor)

    ##Open training password folder
    trainingSetFolder = "Passwords"
    fileList = []
    for (dirpath, dirnames, filenames) in walk(trainingSetFolder + "/"):
        fileList.extend(filenames)
        break

    for files in fileList:
        passwordFileReader = open(trainingSetFolder + "/" + files, 'r')

        ##Add password origin to database
        AddPasswordOriginToDatabase(files, connection, cursor)
        originId = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

        t0 = time.time()

        ##Loop through passwords in file and break them down and add to DB
        for password in passwordFileReader:

            ##Trim password
            password = password.rstrip("\n")

            ##Remove blank passwords
            if(password == ""):
                continue

            ##Escape single quotes
            escapedPassword = password
            if(password.__contains__("'")):
                escapedPassword = ReplaceSingleQuote(password)

            ##Insert password into DB and commit
            InsertPassword(escapedPassword, originId, connection, cursor)

            ##Get the inserted password ID
            passwordId = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

            ##Add password Advanced Masks
            InsertAdvancedMask(password, passwordId, connection, cursor)

            ##Get password Character Placement
            InsertCharacterPlacement(password, passwordId, connection, cursor)

            ##Get password Complexity
            InsertCharacterSet(password, passwordId, connection, cursor)

            ##Insert Markov Chain
            if(len(password) > 1):
                InsertMarkovChain(password, passwordId, connection, cursor)

            if(len(password) > 2):
            ##Insert NGrams
                InsertNGrams(password, passwordId, connection, cursor)

            ##If password contains capitals insert Unsigned Ngrams
                if (any(x.isupper() for x in password)):
                    InsertNGramUnsigned(password, passwordId, connection, cursor)

            ##Insert Simple Mask
            InsertSimpleMask(password, passwordId, connection, cursor)

            ##TODO Insert deleetified password

            ##TODO Find base words in password

        t1 = time.time()
        print("Total time for file = " + str(t1 - t0))
        print("Average time for file = " + str((t1 - t0)/10000))
        print("Average number of inserts per second = " + str(1/((t1 - t0)/10000)))

if __name__ == "__main__":
    main()


