__author__ = 'Alex'

import time
import pyodbc
from os import walk
import datetime
import PasswordAnalysis as Analyse
import DataAccess as Database

def ResetPassword(connection, cursor):
    ##Drop table
    file = open("Database/Drop Tables Analysis.sql")
    sql = " ".join(file.readlines())
    cursor.execute(sql)
    connection.commit()
    ##Create table
    file = open("Database/Create Tables Analysis.sql")
    sql = " ".join(file.readlines())
    cursor.execute(sql)
    connection.commit()

def InsertAnalysedPassword(connection, cursor, files, word):
    ##Create insert statement
    InsertStatement = "INSERT INTO dbo.PasswordAnalysis " \
                      "(Password, PasswordOrigin, Analysis, DateAdded) " \
                      "VALUES ("
    ##Password
    InsertStatement += "'" + word + "', "
    ##File origin
    InsertStatement += "'" + files + "', "
    ##Analysis
    result = AnalysePassword(word, connection, cursor)
    InsertStatement += "CAST(" + str(result) + " AS float), "
    ##Date added
    InsertStatement += "'" + str(datetime.datetime.now()) + "')"
    cursor.execute(InsertStatement)
    connection.commit()

def IsPasswordInDictionary(password, connection, cursor):
    origin = Database.GetPasswordOrigin(password, connection, cursor)
    if(not origin == None):
        print("Password located in dictionary \"" + origin + "\"")

def AnalysePasswordLength(password, connection, cursor):
    #Rank length and add rank rather than frequency
    passwordLengthRank = Database.GetPasswordLengthRank(len(password), connection, cursor)
    print("Password Length Rank = " + str(passwordLengthRank))
    return passwordLengthRank

def AnalyseAdvancedMask(password, connection, cursor):
    advancedMask = Analyse.AdvancedMask(password)
    advancedMaskCount = Database.GetAdvancedMaskCount(advancedMask, connection, cursor)
    print("Advanced Mask Count = " + str(advancedMaskCount))
    advancedMaskRank = Database.GetAdvancedMaskRank(advancedMask, connection, cursor)
    print("Advanced Mask Rank = " + str(advancedMaskRank))
    return (advancedMaskRank + advancedMaskCount)/2

def AnalyseCharacterPlacement(password, connection, cursor):
    result = 0.0
    characters = Analyse.CharacterPlacement(password)
    for character in characters:
        result += Database.GetCharacterPlacementRanking(character[0], character[1], connection, cursor)
    print("Character Placement Ranking = " + str(result/len(password)))
    return result/len(password)

def AnalyseCharacterSet(password, connection, cursor):
    characterSet = Analyse.CharacterSet(password)
    characterSetCount = Database.GetCharacterSetCount(characterSet, connection, cursor)
    print("Character Set Count = " + str(characterSetCount))
    characterSetRank = Database.GetCharacterSetRank(characterSet, connection, cursor)
    print("Character Set Rank = " + str(characterSetRank))
    return (characterSetCount + characterSetRank)/2

def AnalyseMarkovChain(password, connection, cursor):
    result = 0.0
    chains = Analyse.MarkovChain(password)
    for chain in chains:
        result += Database.GetMarkovChainRank(chain[0], chain[1], connection, cursor)
    print("Markov Chain Ranking = " + str(result/len(password)))
    return result/(len(password) - 1)

def AnalyseNGrams(password, connection, cursor):
    result = 1.0

    return result

def AnalyseNGramUnsigned(password, connection, cursor):
    result = 1.0

    return result

def AnalyseSimpleMask(password, connection, cursor):
    simpleMask = Analyse.SimpleMask(password)
    simpleMaskCount = Database.GetSimpleMaskCount(simpleMask, connection, cursor)
    print("Simple Mask Count = " + str(simpleMaskCount))
    simpleMaskRank = Database.GetSimpleMaskRank(simpleMask, connection, cursor)
    print("Simple Mask Rank = " + str(simpleMaskRank))
    return (simpleMaskRank + simpleMaskCount)/2

def AnalysePassword(password, connection, cursor):
    result = 0.0
    numberOfTests = 8
    IsPasswordInDictionary(password, connection, cursor)
    result += AnalysePasswordLength(password, connection, cursor)
    result += AnalyseAdvancedMask(password, connection, cursor)
    result += AnalyseCharacterPlacement(password, connection, cursor)
    result += AnalyseCharacterSet(password, connection, cursor)
    result += AnalyseMarkovChain(password, connection, cursor)#
    result += AnalyseNGrams(password, connection, cursor)#
    result += AnalyseNGramUnsigned(password, connection, cursor)#
    result += AnalyseSimpleMask(password, connection, cursor)
    print("Password ranking for \"" + password + "\" is " + str(result/numberOfTests))
    return result/numberOfTests

def main():
    ##Setup connection to SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;'
                          'DATABASE=Malodorous;UID=sa;PWD=password')
    cursor = connection.cursor()

    ##Reset database
    ResetPassword(connection, cursor)

    ##Read in password or run through Analyse file
    inputPassword = input("Would you like to analyse a single password?\n"
                     "If yes enter the password, else leave blank")

    t0 = time.time()

    if(inputPassword == ""):
        ##Read in passwords and from Analyse folder
        analysisFolder = "Analyse"
        fileList = []
        for (dirpath, dirnames, filenames) in walk(analysisFolder + "/"):
            fileList.extend(filenames)
            break
        ##Run through folder and read in all files
        for files in fileList:
            passwordFileReader = open(analysisFolder + "/" + files)
            ##Run through each file and read in each word
            for password in passwordFileReader:
                ##Analyse password
                if(not password == ""):
                    InsertAnalysedPassword(connection, cursor, files, password)

    else:
        ##Analyse single password
        print("Result for " + inputPassword + " is " + str(AnalysePassword(inputPassword, connection, cursor)))

    t1 = time.time()
    print("Total time taken to analyse: " + str(t1-t0))


if __name__ == "__main__":
    main()