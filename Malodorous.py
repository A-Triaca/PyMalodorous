__author__ = 'Alex'

import pyodbc
import datetime

def passwordAdvancedMask(password):

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

def replaceSingleQuote(password):
    tempPassword = ""
    for i in range(password.__len__()):
        if(password[i] == "'"):
            tempPassword += "''"
        else:
            tempPassword += password[i]
    return tempPassword

def main():
    ##Setup connection to SQL Server
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;'
                          'DATABASE=Malodorous;UID=sa;PWD=password')
    cursor = cnxn.cursor()
    ##Open training password file
    passwordFile = open('10kMostCommon.txt', 'r')
    ##Loop through passwords in file and break them down and add to DB
    for password in passwordFile:
        ##Trim password
        password = password.rstrip("\n")
        ##Escape single quotes
        if(password.__contains__("'")):
            password = replaceSingleQuote(password)
        ##Insert password into DB and commit
        cursor.execute("INSERT INTO dbo.Password "
                       "(Password, Length, DateAdded, Deleetified) "
                       "VALUES ('" + password + "', " + str(password.__len__()) +
                       ", '" + str(datetime.datetime.now()) + "', '" + str(False) + "');")
        cnxn.commit()
        ##Get the inserted password ID
        passordId = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
        ##Get password Advanced Mask
        advancedMask = passwordAdvancedMask(password)
        cursor.execute("INSERT INTO dbo.AdvancedMask "
                       "(Mask, OriginalPassword) "
                       "VALUES ('" + advancedMask + "', " + str(passordId) + ");")
        cnxn.commit()


if __name__ == "__main__":
    main()


