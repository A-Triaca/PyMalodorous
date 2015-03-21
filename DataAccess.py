__author__ = 'Alex'

def GetAdvancedMaskCount(mask, connection, cursor):
    result =  cursor.execute("SELECT "
                                "(SELECT CAST(COUNT(*) AS float) "
                                "FROM dbo.AdvancedMask "
                                "WHERE Mask = '" + mask + "')/CAST(COUNT(*) AS float) "
                            "FROM dbo.AdvancedMask").fetchone()
    if(result == None):
        return 0
    return result[0]

def GetAdvancedMaskRank(mask, connection, cursor):
    result = cursor.execute("DECLARE @MaxRank INT "
                            "SELECT @MaxRank=DENSE_RANK() OVER (ORDER BY COUNT(*)) "
                                    "FROM dbo.AdvancedMask GROUP BY Mask "
                            "SELECT CAST(R.Rank AS float)/CAST(@MaxRank AS float) FROM "
                                "(SELECT Mask, DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank "
                                "FROM dbo.AdvancedMask GROUP BY Mask) AS R "
                            "WHERE R.Mask = '" + mask + "'").fetchone()
    if(result == None):
        return 0
    return result[0]

def GetCharacterSetCount(characterSet, connection, cursor):
    result =  cursor.execute("SELECT "
                                "(SELECT CAST(COUNT(*) AS float) "
                                "FROM dbo.Complexity "
                                "WHERE CharacterSet = '" + characterSet + "')/CAST(COUNT(*) AS float) "
                            "FROM dbo.Complexity").fetchone()
    if(result == None):
        return 0
    return result[0]

def GetCharacterSetRank(characterSet, connection, cursor):
    result =  cursor.execute("DECLARE @MaxRank INT "
                            "SELECT @MaxRank=DENSE_RANK() OVER (ORDER BY COUNT(*)) "
                                    "FROM dbo.Complexity GROUP BY CharacterSet "
                            "SELECT CAST(R.Rank AS float)/CAST(@MaxRank AS float) FROM "
                                "(SELECT CharacterSet, DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank "
                                "FROM dbo.Complexity GROUP BY CharacterSet) AS R "
                            "WHERE R.CharacterSet = '" + characterSet + "'").fetchone()
    if(result == None):
        return 0
    return result[0]