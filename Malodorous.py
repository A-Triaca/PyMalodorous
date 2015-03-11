__author__ = 'Alex'

import pyodbc
import datetime

def passwordAdvancedMask(password):
    lowerChars = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', \
                 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', \
                 'u', 'v', 'w', 'x', 'y', 'z'}
    upperChars = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', \
                 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', \
                 'U', 'V', 'W', 'X', 'Y', 'Z'}
    numbers = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}

    advancedMask = ""

    for i in range(password.__len__()):
        if(lowerChars.__contains__(password[i])):
            advancedMask += "$l"
        elif(upperChars.__contains__(password[i])):
            advancedMask += "$u"
        elif(numbers.__contains__(password[i])):
            advancedMask += "$d"
        else:
            advancedMask += "$s"

    return advancedMask

def main():
    ##Setup connection to SQL Server
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=Malodorous;UID=sa;PWD=password')
    cursor = cnxn.cursor()
    ##Open training password file
    passwordFile = open('10kMostCommon.txt', 'r')
    ##Loop through passwords in file and break them down and add to DB
    for password in passwordFile:
        ##Trim password
        password = password.rstrip("\n")
        ##Insert password into DB and commit
        cursor.execute("INSERT INTO dbo.Password (Password, Length, DateAdded, Deleetified) VALUES ('" + password + "', " + str(password.__len__()) + ", '" + str(datetime.datetime.now()) + "', '" + str(False) + "');")
        cnxn.commit()
        ##Get the inserted password ID
        passordId = cursor.execute("SELECT @@IDENTITY").fetchone()[0]
        passwordAdvancedMask(password)


if __name__ == "__main__":
    main()


