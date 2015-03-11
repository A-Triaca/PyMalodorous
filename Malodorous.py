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
        ##Trim password
        password = password.strip()
        ##Insert password into DB and commit
        ######ESCAPE SPECIAL CHARACTERS
        cursor.execute("INSERT INTO dbo.Password (Password, Length, DateAdded, Deleetified) VALUES ('" + password + "', " + str(password.__len__()) + ", '" + str(datetime.datetime.now()) + "', '" + str(False) + "');")
        cnxn.commit()
        ##Get the inserted password ID
        passordId = cursor.execute("SELECT @@IDENTITY").fetchone()[0]


if __name__ == "__main__":
    main()