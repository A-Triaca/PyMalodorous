__author__ = 'Alex'

import time
import pyodbc
from os import walk
import datetime
import Malodorous
import PasswordAnalysis

def ResetPassword(connection, cursor):
    ##Drop table
    file = open("Database/Drop Tables Analysis.sql", 'r')
    sql = " ".join(file.readlines())
    cursor.execute(sql)
    connection.commit()
    ##Create table
    file = open("Database/Create Tables Analysis.sql", 'r')
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

def AnaylseAdvancedMask(password):
    result = 0.0
    advancedMask = PasswordAnalysis.GetAdvancedMask(password)
    return result

def AnalyseCharacterPlacement(password):
    result = 0.0

    return result

def AnalyseCharacterSet(password):
    result = 0.0

    return result

def AnalyseMarkovChain(password):
    result = 0.0

    return result

def AnaylseNGrams(password):
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
    result += AnaylseAdvancedMask(password)
    result += AnalyseCharacterPlacement(password)
    result += AnalyseCharacterSet(password)
    result += AnalyseMarkovChain(password)
    result += AnaylseNGrams(password)
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
            wordFileReader = open(analysisFolder + "/" + files, 'r')
            ##Run through each file and read in each word
            for password in files:
                ##Analyse password
                if(not password == ""):
                    InsertAnalysedPassword(connection, cursor, files, password)

    else:
        ##Analyse single password
        print("Result for " + inputPassword + " is " + AnalysePassword(inputPassword))

    t1 = time.time()
    print("Total time taken to analyse: " + str(t1-t0))


if __name__ == "__main__":
    main()