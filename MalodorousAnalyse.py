__author__ = 'Alex'

import datetime
import pyodbc
from os import walk


def AnalysePassword(word):
    pass


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


def main():
    t0 = datetime.now()

    ##Setup connection to SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;'
                          'DATABASE=Malodorous;UID=sa;PWD=password')
    cursor = connection.cursor()

    ##Reset database
    ResetPassword(connection, cursor)

    ##Read in password or run through Analyse file
    password = input("Would you like to analyse a single password?\n"
                     "If yes enter the password, else leave blank")

    if(password == ""):
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
            for word in files:
                ##Analyse password
                if(not word == ""):
                    result = AnalysePassword(word)

    else:
        ##Analyse single password
        print("Result for " + password + " is " + AnalysePassword(password))

    t1 = datetime.now()
    print("Total time taken to analyse: " + str(t1-t0))


if __name__ == "__main__":
    main()