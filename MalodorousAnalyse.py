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
    result = AnalysePassword(word)
    InsertStatement += str(result) + ", "
    ##Date added
    InsertStatement += "'" + str(datetime.datetime.now()) + "')"
    cursor.execute(InsertStatement)
    connection.commit()

def AnalysePasswordMakeup(password):
    result = 0.0
    #Rank length and add rank rather than frequency
    #If in dictionary print that it is and print dictionary
    return result

def AnalyseAdvancedMask(password):
    advancedMask = Analyse.AdvancedMask(password)
    advancedMaskCount = Database.GetAdvancedMaskCount(advancedMask)
    print("Advanced Mask Count = " + str(advancedMaskCount))
    advancedMaskRank = Database.GetAdvancedMaskRank(advancedMask)
    print("Advanced Mask Rank = " + str(advancedMaskRank))
    return (advancedMaskRank * advancedMaskCount)

def AnalyseCharacterPlacement(password):
    result = 0.0

    return result

def AnalyseCharacterSet(password):
    characterSet = Analyse.CharacterSet(password)
    characterSetCount = Database.GetCharacterSetCount(characterSet)
    print("Character Set Count = " + str(characterSetCount))
    characterSetRank = Database.GetCharacterSetRank(characterSet)
    print("Character Set Rank = " + str(characterSetRank))
    return (characterSetCount * characterSetRank)

def AnalyseMarkovChain(password):
    result = 0.0

    return result

def AnalyseNGrams(password):
    result = 0.0

    return result

def AnalyseNGramUnsigned(password):
    result = 0.0

    return result

def AnalyseSimpleMask(password):
    result = 0.0

    return result

def AnalysePassword(password):
    result = 0.0
    result += AnalysePasswordMakeup(password)
    result += AnalyseAdvancedMask(password)
    result += AnalyseCharacterPlacement(password)
    result += AnalyseCharacterSet(password)
    result += AnalyseMarkovChain(password)
    result += AnalyseNGrams(password)
    result += AnalyseNGramUnsigned(password)
    result += AnalyseSimpleMask(password)
    return result

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
        print("Result for " + inputPassword + " is " + str(AnalysePassword(inputPassword)))

    t1 = time.time()
    print("Total time taken to analyse: " + str(t1-t0))


if __name__ == "__main__":
    main()