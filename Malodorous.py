__author__ = 'Alex'

import pyodbc
from os import walk
import time
import datetime
import PasswordAnalysis as Analyse

def InsertAdvancedMask(password, passwordId, connection, cursor):
    cursor.execute("INSERT INTO dbo.AdvancedMask "
                   "(Mask, OriginalPassword) "
                   "VALUES ('" + Analyse.AdvancedMask(password) + "', " +
                   str(passwordId) + ");")
    connection.commit()

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

def SetUpAvailability(connection, cursor):
    file = open("Database/Insert Into Availability.sql", 'r')
    sql = " ".join(file.readlines())
    cursor.execute(sql)
    connection.commit()

def InsertPassword(password, passwordOrigin, connection, cursor):
    cursor.execute("INSERT INTO dbo.Password (Password, PasswordOrigin, Length, DateAdded, Deleetified) " \
           "VALUES (?, '" + str(passwordOrigin) + "', " +
                   str(password.__len__()) + ", '" + str(datetime.datetime.now()) +
                   "', '" + str(False) + "');", (password))
    connection.commit()

def InsertCharacterPlacement(password, passwordId, connection, cursor):
    InsertStatement = "INSERT INTO dbo.CharacterPlacement " \
                      "(Character, Placement, OriginalPassword) VALUES "
    args = []
    for character in Analyse.CharacterPlacement(password):
        InsertStatement += "(?, " + str(character[1]) + ", " + str(passwordId) + "),"
        args.append(character[0])
    cursor.execute(InsertStatement[:-1], args)
    connection.commit()

def InsertCharacterSet(password, passwordId, connection, cursor):
    cursor.execute("INSERT INTO dbo.Complexity (CharacterSet, OriginalPassword) "
                   "VALUES ('" + Analyse.CharacterSet(password) + "', " +
                   str(passwordId) + ")")
    connection.commit

def InsertMarkovChain(password, passwordId, connection, cursor):
    InsertStatement = "INSERT INTO dbo.MarkovChain " \
                      "(FirstCharacter, SecondCharacter, OriginalPassword) VALUES "
    args = []
    for chain in Analyse.MarkovChain(password):
        InsertStatement += "(?, ?, " + str(passwordId) + "),"
        args.append(chain[0])
        args.append(chain[1])
    cursor.execute(InsertStatement[:-1], args)
    connection.commit()

def InsertNGrams(password, passwordId, connection, cursor):
    InsertStatement = "INSERT INTO dbo.NGrams " \
                      "(Length ,NGram ,Placement, Unsigned, IsWord, OriginalPassword) VALUES "
    args = []
    for nGram in Analyse.NGrams(password):
        base = cursor.execute("SELECT COUNT(*) FROM dbo.BaseWord WHERE Word = ?", nGram[1]).fetchone()[0]
        InsertStatement += "(" + str(nGram[0]) + ", ?, " + \
                           str(nGram[2]) + ", " + str(nGram[3]) + ", " + str(base) + ", " + \
                           str(passwordId) + "),"
        args.append(nGram[1])
    cursor.execute(InsertStatement[:-1], args)
    connection.commit()

def InsertNGramUnsigned(password, passwordId, connection, cursor):
    InsertStatement = "INSERT INTO dbo.NGrams " \
                      "(Lenth ,NGram ,Placement, Unsigned, IsWord, OriginalPassword) VALUES "
    args = []
    for nGram in Analyse.NGramsUnsigned(password):
        base = cursor.execute("SELECT COUNT(*) FROM dbo.BaseWord WHERE Word = ?", nGram[1]).fetchone()[0]
        InsertStatement += "(" + str(nGram[0]) + ", ?, " + \
                           str(nGram[2]) + ", " + str(nGram[3]) + ", " + str(base) + ", " + \
                           str(passwordId) + "),"
        args.append(nGram[1])
    cursor.execute(InsertStatement[:-1], args)
    connection.commit()

def InsertSimpleMask(password, passwordId, connection, cursor):
    InsertStatement = "INSERT INTO dbo.SimpleMask " \
                      "(Mask, OriginalPassword) VALUES "
    InsertStatement += "('" + Analyse.SimpleMask(password) + "', " + str(passwordId) + ")"
    cursor.execute(InsertStatement)
    connection.commit()

def GetAvailability(cursor):
    message = "What is the difficulty of obtaining the database?\n"
    catagories = cursor.execute("SELECT * FROM dbo.Availability")
    for option in catagories:
        message += str(option[0]) + " - " + option[1] + "\n"
    availability = input(message)
    catagory = cursor.execute("SELECT * FROM dbo.Availability WHERE AvailabilityId = " + availability).fetchone()[1]
    print("You have chosen: " + catagory)
    return availability

def AddPasswordOriginToDatabase(file, connection, cursor):
    availability = GetAvailability(cursor)
    cursor.execute("INSERT INTO PasswordOrigin (Origin, Availability) "
                   "VALUES ('" + file + "', " + str(availability) + ")")
    connection.commit()

def ResetDictionaries(connection, cursor):
    cursor.execute("DROP TABLE dbo.BaseWord")
    connection.commit()
    cursor.execute("CREATE TABLE dbo.BaseWord "
                   "(Word NVARCHAR(50) NOT NULL, Length INT NOT NULL, PRIMARY KEY (Word));")
    connection.commit()

def LoadDictionaries(connection, cursor):
    dictionaryFolder = "Dictionaries"
    fileList = []
    count = 0
    t0 = time.time()

    for (dirpath, dirnames, filenames) in walk(dictionaryFolder + "/"):
        fileList.extend(filenames)
        break

    for files in fileList:
        dictionaryFileReader = open(dictionaryFolder + "/" + files, 'r', encoding="utf-8-sig")
        for word in dictionaryFileReader:
            count += 1
            word = word.rstrip("\n")
            if(word == "" or word.startswith("#") or len(word) < 3):
                continue
            if(word.__contains__("'")):
                word = Analyse.ReplaceSingleQuote(word)
            if(cursor.execute("SELECT COUNT(*) FROM dbo.BaseWord "
                              "WHERE Word = '" + word + "'").fetchone()[0] == 0):
                insertStatement = "INSERT INTO dbo.BaseWord (Word, Length) VALUES " \
                              "('" + word + "', " + str(len(word)) + ")"
                cursor.execute(insertStatement)
                connection.commit()

    t1 = time.time()
    print("Total words loaded = " + str(count))
    print("Total time for file = " + str(time.time() - t0))
    print("Average time for file = " + str((t1 - t0)/count))
    print("Average number of inserts per second = " + str(1/((t1 - t0)/count)))

def main():
    ##Setup connection to SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;'
                          'DATABASE=Malodorous;UID=sa;PWD=password')
    cursor = connection.cursor()
    ##Drop and recreate the database
    DropDatabase(connection, cursor)
    CreateDatabase(connection, cursor)
    SetUpAvailability(connection, cursor)
    #SetUpCharacterSet(connection, cursor)

    ##Reset dictionaries, drop tables and recreate
    if(input("Would you like to drop the dictionaries?('yes'/'no')") == "yes"):
        ResetDictionaries(connection, cursor)

    ##Load dictionaries for base word compare (note that this method only loads unique words and will not create duplicates.
    if(input("Would you like to load the dictionaries?('yes'/'no')") == "yes"):
        LoadDictionaries(connection, cursor)

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
        count = 0
        ##Loop through passwords in file and break them down and add to DB
        for password in passwordFileReader:

            count += 1

            ##Trim password
            password = password.rstrip("\n")
            password = password.lstrip()

            ##Remove blank passwords
            if(password == ""):
                continue

            ##Insert password into DB and commit
            InsertPassword(password, originId, connection, cursor)

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

        t1 = time.time()
        print("Total words loaded = " + str(count))
        print("Total time for file = " + str(t1 - t0))
        print("Average time for file = " + str((t1 - t0)/count))
        print("Average number of inserts per second = " + str(1/((t1 - t0)/count)))

if __name__ == "__main__":
    main()


