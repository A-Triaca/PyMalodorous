__author__ = 'Alex'

import time
import pyodbc
from os import walk
import datetime
import PasswordAnalysis as Analyse
import DataAccess as Database

def ResetPassword(connection, cursor):
    ##Drop table
    time0 = time.time()
    file = open("Database/Drop Tables Analysis.sql")
    sql = " ".join(file.readlines())
    cursor.execute(sql)
    connection.commit()
    ##Create table
    file = open("Database/Create Tables Analysis.sql")
    sql = " ".join(file.readlines())
    cursor.execute(sql)
    connection.commit()
    print("Database reset and fact table creation took " + str(time.time()-time0))

def InsertAnalysedPassword(connection, cursor, files, word):
    ##Create insert statement
    InsertStatement = "INSERT INTO dbo.PasswordAnalysis " \
                      "(Password, PasswordOrigin, Dictionary, Analysis, Length, Complexity, DateAdded) " \
                      "VALUES (?, ?, ?, "
    ##Analysis
    result = AnalysePassword(word, connection, cursor)
    InsertStatement += "CAST(" + str((1-result)*100) + " AS float), "
    #Length
    InsertStatement += str(len(word)) + ", "
    #Password complexity
    InsertStatement += "'" + Analyse.CharacterSet(word) + "', "
    ##Date added
    InsertStatement += "'" + str(datetime.datetime.now()) + "')"
    cursor.execute(InsertStatement, [word, files, IsPasswordInDictionary(word, connection, cursor)])
    connection.commit()

def IsPasswordInDictionary(password, connection, cursor):
    origin = Database.GetPasswordOrigin(password, connection, cursor)
    if(origin == None):
        return ""
    #print("Password located in dictionary \"" + origin + "\"")
    return origin

def AnalysePasswordLength(password, connection, cursor):
    #Rank length and add rank rather than frequency
    passwordLengthRank = Database.GetPasswordLengthRank(len(password), connection, cursor)
    #print("Password Length Rank = " + str(passwordLengthRank))
    return passwordLengthRank

def AnalyseAdvancedMask(password, connection, cursor):
    advancedMask = Analyse.AdvancedMask(password)
    # advancedMaskCount = Database.GetAdvancedMaskCount(advancedMask, connection, cursor)
    # print("Advanced Mask Count = " + str(advancedMaskCount))
    advancedMaskRank = Database.GetAdvancedMaskRank(advancedMask, connection, cursor)
    #print("Advanced Mask Rank = " + str(advancedMaskRank))
    return (advancedMaskRank)

def AnalyseCharacterPlacement(password, connection, cursor):
    result = 0.0
    length = len(password)
    characters = Analyse.CharacterPlacement(password)
    for character in characters:
        result += Database.GetCharacterPlacementRanking(character[0], character[1], length, connection, cursor)
    #print("Character Placement Ranking = " + str(result/len(password)))
    return result/len(password)

def AnalyseCharacterSet(password, connection, cursor):
    characterSet = Analyse.CharacterSet(password)
    # characterSetCount = Database.GetCharacterSetCount(characterSet, connection, cursor)
    # print("Character Set Count = " + str(characterSetCount))
    characterSetRank = Database.GetCharacterSetRank(characterSet, connection, cursor)
    #print("Character Set Rank = " + str(characterSetRank))
    return (characterSetRank)

def AnalyseMarkovChain(password, connection, cursor):
    result = 0.0
    chains = Analyse.MarkovChain(password)
    for chain in chains:
        result += Database.GetMarkovChainRank(chain[0], chain[1], connection, cursor)
    #print("Markov Chain Ranking = " + str(result/(len(password)-1)))
    return result/(len(password) - 1)

def AnalyseNGrams(password, connection, cursor):
    result = 0.0
    nGrams = Analyse.NGrams(password)
    for nGram in nGrams:
        result += Database.GetNGramRank(nGram[1], connection, cursor)
    #print("NGram Ranking = " + str(result/len(nGrams)))
    return result/len(nGrams)

def AnalyseNGramUnsigned(password, connection, cursor):
    result = 0.0
    nGrams = Analyse.NGramsUnsigned(password)
    for nGram in nGrams:
        result += Database.GetNGramRank(nGram[1], connection, cursor)
    #print("Unsigned NGram Ranking = " + str(result/len(nGrams)))
    return result/len(nGrams)

def AnalyseSimpleMask(password, connection, cursor):
    simpleMask = Analyse.SimpleMask(password)
    # simpleMaskCount = Database.GetSimpleMaskCount(simpleMask, connection, cursor)
    # print("Simple Mask Count = " + str(simpleMaskCount))
    simpleMaskRank = Database.GetSimpleMaskRank(simpleMask, connection, cursor)
    #print("Simple Mask Rank = " + str(simpleMaskRank))
    return (simpleMaskRank)

def AnalysePassword(password, connection, cursor):
    result = 0.0
    numberOfTests = 5
    result += AnalysePasswordLength(password, connection, cursor)
    result += AnalyseAdvancedMask(password, connection, cursor)
    result += AnalyseCharacterPlacement(password, connection, cursor)
    result += AnalyseCharacterSet(password, connection, cursor)
    if(len(password) > 1):
        result += AnalyseMarkovChain(password, connection, cursor)
        numberOfTests += 1
    if(len(password) > 2):
        result += AnalyseNGrams(password, connection, cursor)
        numberOfTests += 1
        if (any(x.isupper() for x in password)):
            result += AnalyseNGramUnsigned(password, connection, cursor)
            numberOfTests += 1
    result += AnalyseSimpleMask(password, connection, cursor)
    print("Password ranking for \"" + password + "\" is " + str((1-(result/numberOfTests))*100) + "%")
    return result/numberOfTests

def main():
    ##Setup connection to SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;'
                          'DATABASE=Malodorous;UID=sa;PWD=password')
    cursor = connection.cursor()

    ##Reset database
    reset = input("Would you like to reset the fact tables?\n"
                  "If yes type 'yes', else leave blank.")
    if(reset == "yes"):
        print("Resetting database and creating fac tables.")
        ResetPassword(connection, cursor)

    ##Read in password or run through Analyse file
    inputPassword = input("Would you like to analyse a single password?\n"
                     "If yes enter the password, else leave blank")

    t0 = time.time()

    if(inputPassword == ""):
        ##Read in passwords and from Analyse folder
        analysisFolder = "Analyse"
        analysedCount = 0
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
                password = password.rstrip("\n")
                if(not password == ""):
                    analysedCount += 1
                    InsertAnalysedPassword(connection, cursor, files, password)

    else:
        ##Analyse single password
        AnalysePassword(inputPassword, connection, cursor)

    t1 = time.time()
    print("Total time taken to analyse: " + str(t1-t0))
    print("Total passwords analysed: " + str(analysedCount))
    print("Average time per password: " + str((t1-t0)/analysedCount))


if __name__ == "__main__":
    main()