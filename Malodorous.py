__author__ = 'Alex'

import pyodbc
import datetime

def main():
    ##Setup connection to SQL Server
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=Malodorous;UID=sa;PWD=password')
    cursor = cnxn.cursor()
    ##Open training password file
    passwordFile = open('10kMostCommon.txt', 'r')
    ##Loop through passwords in file and break them down and add to DB
    for password in passwordFile:
        ##Insert password into DB and commit
        cursor.execute("INSERT INTO Password VALUES (" + password + ", " + password.__len__() + ", " + datetime.datetime + ", " + False + ");")
        cnxn.commit()
        ##Get the inserted password ID
        passordId = cursor.execute("SELECT @@IDENTITY")
        print(passordId)


if __name__ == "__main__":
    main()