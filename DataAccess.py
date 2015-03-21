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

def GetSimpleMaskCount(mask, connection, cursor):
    result =  cursor.execute("SELECT "
                                "(SELECT CAST(COUNT(*) AS float) "
                                "FROM dbo.SimpleMask "
                                "WHERE Mask = '" + mask + "')/CAST(COUNT(*) AS float) "
                            "FROM dbo.SimpleMask").fetchone()
    if(result == None):
        return 0
    return result[0]

def GetSimpleMaskRank(mask, connection, cursor):
    result = cursor.execute("DECLARE @MaxRank INT "
                            "SELECT @MaxRank=DENSE_RANK() OVER (ORDER BY COUNT(*)) "
                                    "FROM dbo.SimpleMask GROUP BY Mask "
                            "SELECT CAST(R.Rank AS float)/CAST(@MaxRank AS float) FROM "
                                "(SELECT Mask, DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank "
                                "FROM dbo.SimpleMask GROUP BY Mask) AS R "
                            "WHERE R.Mask = '" + mask + "'").fetchone()
    if(result == None):
        return 0
    return result[0]

def GetPasswordLengthRank(length, connection, cursor):
    result = cursor.execute("DECLARE @MaxRank INT "
                            "SELECT @MaxRank=DENSE_RANK() OVER (ORDER BY COUNT(*)) "
                                    "FROM dbo.Password GROUP BY Length "
                            "SELECT CAST(R.Rank AS float)/CAST(@MaxRank AS float) FROM "
                                "(SELECT Length, DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank "
                                "FROM dbo.Password GROUP BY Length) AS R "
                            "WHERE R.Length = " + str(length) + "").fetchone()
    if(result == None):
        return 0
    return result[0]

def GetPasswordOrigin(password, connection, cursor):
    result = cursor.execute("SELECT po.Origin "
                            "FROM dbo.Password as P INNER JOIN dbo.PasswordOrigin AS po "
                            "ON p.PasswordOrigin = po.OriginId "
                            "WHERE Password = ?", password).fetchone()
    if(result == None):
        return None
    return result[0]

def GetCharacterPlacementRanking(character, placement, connection, cursor):
    result = cursor.execute("DECLARE @MaxRank INT "
                            "SELECT @MaxRank=DENSE_RANK() OVER (ORDER BY COUNT(*)) "
                            "FROM dbo.CharacterPlacement INNER JOIN dbo.Password  "
                                "ON dbo.CharacterPlacement.OriginalPassword=dbo.Password.PasswordId "
                            "WHERE dbo.Password.Length >= " + str(placement) + " "
                            "GROUP BY Character, Placement "
                            "SELECT CAST(R.Rank AS float)/CAST(@MaxRank AS float) FROM "
                            "(SELECT Character, Placement, DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank "
                            "FROM dbo.CharacterPlacement INNER JOIN dbo.Password "
                                "ON dbo.CharacterPlacement.OriginalPassword = dbo.Password.PasswordId "
                            "WHERE dbo.Password.Length >= " + str(placement) + " "
                            "GROUP BY Character, Placement) AS R "
                            "WHERE R.Character = ? AND R.Placement = " + str(placement), character).fetchone()
    if(result == None):
        return None
    return result[0]

def GetMarkovChainRank(firstCharacter, secondCharacter, connection, cursor):
    result = cursor.execute("DECLARE @MaxRank INT "
                            "SELECT @MaxRank=DENSE_RANK() OVER (ORDER BY COUNT(*)) "
                            "FROM dbo.MarkovChain "
                            "GROUP BY FirstCharacter, SecondCharacter  "
                            "SELECT CAST(R.Rank AS float)/CAST(@MaxRank AS float) FROM "
                            "(SELECT FirstCharacter, SecondCharacter, DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank "
                            "FROM dbo.MarkovChain "
                            "GROUP BY FirstCharacter, SecondCharacter) AS R "
                            "WHERE R.FirstCharacter = ? AND R.SecondCharacter = ?", firstCharacter, secondCharacter).fetchone()
    if(result == None):
        return None
    return result[0]

def GetNGramRank(nGram, connection, cursor):
    result = cursor.execute("DECLARE @MaxRank INT "
                            "SELECT @MaxRank=DENSE_RANK() OVER (ORDER BY COUNT(*)) "
                            "FROM dbo.NGrams "
                            "WHERE Unsigned = 0 "
                            "GROUP BY NGram "
                            "SELECT CAST(R.Rank AS float)/CAST(@MaxRank AS float) FROM "
                            "(SELECT NGram, DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank "
                            "FROM dbo.NGrams "
                            "WHERE Unsigned = 0 "
                            "GROUP BY NGram) AS R "
                            "WHERE R.NGram = ?", nGram).fetchone()
    if(result == None):
        return None
    return result[0]

def GetNGramUnsignedRank(nGram, connection, cursor):
    result = cursor.execute("DECLARE @MaxRank INT "
                            "SELECT @MaxRank=DENSE_RANK() OVER (ORDER BY COUNT(*)) "
                            "FROM dbo.NGrams "
                            "WHERE Unsigned = 1 "
                            "GROUP BY NGram "
                            "SELECT CAST(R.Rank AS float)/CAST(@MaxRank AS float) FROM "
                            "(SELECT NGram, DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank "
                            "FROM dbo.NGrams "
                            "WHERE Unsigned = 1 "
                            "GROUP BY NGram) AS R "
                            "WHERE R.NGram = ?", nGram).fetchone()
    if(result == None):
        return None
    return result[0]