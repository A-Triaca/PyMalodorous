CREATE TABLE dbo.PasswordAnalysis (
	PasswordId INT NOT NULL IDENTITY (1, 1),
	Password NVARCHAR(100) NOT NULL,
	PasswordOrigin NVARCHAR(100),
	Analysis numeric(38,30),
	DateAdded DATETIME2 DEFAULT GETDATE(),
	PRIMARY KEY (PasswordId)
);

CREATE TABLE fac.NGram(
NGram NVARCHAR(100),
Rank INT,
Unsigned BIT,
Length INT);

INSERT INTO fac.NGram
SELECT NGram, DENSE_RANK() OVER (ORDER BY COUNT(*)) AS Rank, Unsigned, Lenth
FROM dbo.NGrams
GROUP BY NGram, Unsigned, Lenth
