CREATE TABLE dbo.PasswordAnalysis (
	PasswordId INT NOT NULL IDENTITY (1, 1),
	Password NVARCHAR(100) NOT NULL,
	PasswordOrigin NVARCHAR(100),
	Analysis numeric(38,30),
	DateAdded DATETIME2 DEFAULT GETDATE(),
	PRIMARY KEY (PasswordId)
);
