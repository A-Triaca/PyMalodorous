__author__ = 'Alex'

import datetime
import pyodbc
from os import walk


def AnalysePassword(word):
    pass


def main():
    t0 = datetime.now()

    ##Setup connection to SQL Server
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;'
                          'DATABASE=Malodorous;UID=sa;PWD=password')
    cursor = connection.cursor()

    password = input("Would you like to analyse a single password?\n"
                     "If yes enter the password, else leave blank")
    if(password == ""):
        ##Read in passwords and from Analyse folder
        analysisFolder = "Analyse"
        fileList = []
        for (dirpath, dirnames, filenames) in walk(analysisFolder + "/"):
            fileList.extend(filenames)
            break

        for files in fileList:
            wordFileReader = open(analysisFolder + "/" + files, 'r')

        for word in files:
            AnalysePassword(word)

    else:
        ##Analyse single password
        AnalysePassword(password)

    t1 = datetime.now()
    print("Total time taken to analyse: " + str(t1-t0))


if __name__ == "__main__":
    main()