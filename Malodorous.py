__author__ = 'Alex'

import pyodbc
import datetime
from os import walk

def InsertPasswordAdvancedMask(password, passwordId, connection, cursor):
    cursor.execute("INSERT INTO dbo.AdvancedMask "
                       "(Mask, OriginalPassword) "
                       "VALUES ('" + GetPasswordAdvancedMask(password) + "', " + str(passwordId) + ");")
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

def InsertPassword(password, connection, cursor):
    cursor.execute("INSERT INTO dbo.Password (Password, Length, DateAdded, Deleetified) " \
           "VALUES ('" + password + "', " + str(password.__len__()) + ", '" +
                   str(datetime.datetime.now()) + "', '" + str(False) + "');")
    connection.commit()

def InsertPasswordCharacterPlacement(password, passwordId, connection, cursor):
    InsertStatement = "INSERT INTO dbo.CharacterPlacement " \
                      "(Character, Placement, OriginalPassword) VALUES "

    for character in GetPasswordCharacterPlacement(password):
        InsertStatement += "('" + character[0] + "', " + character[1] + ", " + str(passwordId) + "),"

    InsertStatement = InsertStatement[:-1]
    cursor.execute(InsertStatement)
    connection.commit()

def GetPasswordCharacterPlacement(password):
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

def GetPasswordAdvancedMask(password):
    advancedMask = ""

    for i in range(password.__len__()):
        if(password[i].islower()):
            advancedMask += "$l"
        elif((password[i]).isupper()):
            advancedMask += "$u"
        elif((password[i]).isdigit()):
            advancedMask += "$d"
        else:
            advancedMask += "$s"

    return advancedMask

def main():
    ##Setup connection to SQL Server
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;'
                          'DATABASE=Malodorous;UID=sa;PWD=password')
    cursor = cnxn.cursor()
    ##Drop and recreate the database
    DropDatabase(cnxn, cursor)
    CreateDatabase(cnxn, cursor)
    SetUpCharacterSet(cnxn, cursor)

    ##Open training password folder
    trainingSetFolder = "Passwords"
    fileList = []
    for (dirpath, dirnames, filenames) in walk(trainingSetFolder + "/"):
        fileList.extend(filenames)
        break

    for files in fileList:
        passwordFileReader = open(trainingSetFolder + "/" + files, 'r')

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
            InsertPassword(escapedPassword, cnxn, cursor)

            ##Get the inserted password ID
            passwordId = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

            ##Add password Advanced Masks
            InsertPasswordAdvancedMask(password, passwordId, cnxn, cursor)

            ##Get password Character Placement
            InsertPasswordCharacterPlacement(password, passwordId, cnxn, cursor)

if __name__ == "__main__":
    main()


