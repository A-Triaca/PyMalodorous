__author__ = 'Alex'

import pyodbc


connection = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;'
                          'DATABASE=Malodorous;UID=sa;PWD=password')
cursor = connection.cursor()

def GetAdvancedMaskCount(mask):
    result =  cursor.execute("SELECT COUNT(*) "
                          "FROM dbo.AdvancedMask "
                          "WHERE Mask = '" + mask + "'").fetchone()
    if(result == None):
        return 0
    return result[0]

def GetAdvancedMaskRank(mask):
    result = cursor.execute("SELECT R.Rank FROM "
                          "(SELECT Mask, DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank "
                          "FROM dbo.AdvancedMask GROUP BY Mask) AS R "
                          "WHERE R.Mask = '" + mask + "'").fetchone()
    if(result == None):
        return 0
    return result[0]

def GetCharacterSetCount(characterSet):
    result =  cursor.execute("SELECT COUNT(*) "
                             "FROM dbo.Complexity "
                             "WHERE CharacterSet = '" + characterSet + "'").fetchone()
    if(result == None):
        return 0
    return result[0]

def GetCharacterSetRank(characterSet):
    result =  cursor.execute("SELECT R.Rank "
                             "FROM "
                             "(SELECT CharacterSet, DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank "
                             "FROM dbo.Complexity GROUP BY CharacterSet) AS R "
                             "WHERE R.CharacterSet = '" + characterSet + "'").fetchone()
    if(result == None):
        return 0
    return result[0]