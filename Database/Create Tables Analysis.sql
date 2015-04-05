CREATE TABLE dbo.PasswordAnalysis (
	PasswordId INT NOT NULL IDENTITY (1, 1),
	Password NVARCHAR(100) NOT NULL,
	PasswordOrigin NVARCHAR(100),
	Analysis numeric(38,30),
	Length INT,
	Complexity NVARCHAR(20),
	DateAdded DATETIME2 DEFAULT GETDATE(),
	PRIMARY KEY (PasswordId)
);

CREATE TABLE fac.NGram(
    NGram NVARCHAR(100),
    Rank INT,
    Unsigned BIT,
    Length INT
);

INSERT INTO fac.NGram
    SELECT
        NGram,
        DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank,
        Unsigned,
        Lenth
    FROM dbo.NGrams
    GROUP BY
        NGram,
        Unsigned,
        Lenth;

CREATE TABLE fac.PasswordOrigin(
    Origin NVARCHAR(100),
    Password NVARCHAR(100)
);

INSERT INTO fac.PasswordOrigin
SELECT po.Origin, p.Password
FROM dbo.Password as P INNER JOIN dbo.PasswordOrigin AS po
ON p.PasswordOrigin = po.OriginId;