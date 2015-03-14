CREATE TABLE dbo.Password (
	PasswordId INT NOT NULL IDENTITY (1, 1),
	Password NVARCHAR(100) NOT NULL,
	PasswordOrigin INT,
	DateAdded DATETIME2,
	Length INT,
	Deleetified BIT NOT NULL,
	OriginalPassword INT,
	PRIMARY KEY (PasswordId)
);

CREATE TABLE dbo.PasswordOrigin (
	OriginId INT NOT NULL IDENTITY (1, 1),
	Origin NVARCHAR(100),
	DateAdded DATETIME2,
	Availability INT,
	PRIMARY KEY (OriginId)
);

CREATE TABLE dbo.Availability (
	AvailabilityId INT NOT NULL IDENTITY (1, 1),
	Description NVARCHAR(100),
	PRIMARY KEY (AvailabilityId)
);

CREATE TABLE dbo.NGrams (
	NGramId INT NOT NULL IDENTITY (1, 1),
	Lenth INT NOT NULL,
	NGram NVARCHAR(50) NOT NULL,
	Placement INT,
	Unsigned BIT,
	OriginalPassword INT NOT NULL,
	PRIMARY KEY (NGramId)
);


CREATE TABLE dbo.CharacterPlacement (
	CharacterId INT NOT NULL IDENTITY (1, 1),
	Character CHAR NOT NULL,
	Placement INT NOT NULL,
	OriginalPassword INT NOT NULL,
	PRIMARY KEY (CharacterId)
);


CREATE TABLE dbo.AdvancedMask (
	MaskId INT NOT NULL IDENTITY (1, 1),
	Mask NVARCHAR(200) NOT NULL,
	OriginalPassword INT NOT NULL,
	PRIMARY KEY (MaskId)
);


CREATE TABLE dbo.BaseWord (
	WordId INT NOT NULL IDENTITY (1, 1),
	Word NVARCHAR(50) NOT NULL,
	Position INT NOT NULL,
	Length INT NOT NULL,
	OriginalPassword INT NOT NULL,
	PRIMARY KEY (WordId)
);

/*
CREATE TABLE dbo.CharacterSet (
	CharacterSetId INT NOT NULL IDENTITY (1, 1),
	CharacterSet NVARCHAR(50) NOT NULL,
	PRIMARY KEY (CharacterSetId)
);
*/

CREATE TABLE dbo.SimpleMask (
	MaskId INT NOT NULL IDENTITY (1, 1),
	Mask NVARCHAR(100) NOT NULL,
	OriginalPassword INT NOT NULL,
	PRIMARY KEY (MaskId)
);


CREATE TABLE dbo.MarkovChain (
	ChainId INT NOT NULL IDENTITY (1,1),
	FirstCharacter CHAR NOT NULL,
	SecondCharacter CHAR NOT NULL,
	OriginalPassword INT NOT NULL,
	PRIMARY KEY (ChainId)
);

CREATE TABLE dbo.Complexity (
	ComplexityId INT NOT NULL IDENTITY (1, 1),
	CharacterSet NVARCHAR(50) NOT NULL,
	OriginalPassword INT NOT NULL,
	PRIMARY KEY (ComplexityId)
);



--Alter tables to add DB constraints
ALTER TABLE Password
ADD FOREIGN KEY (OriginalPassword)
REFERENCES Password (PasswordId);


ALTER TABLE NGrams
ADD FOREIGN KEY (OriginalPassword)
REFERENCES Password (PasswordId);


ALTER TABLE CharacterPlacement
ADD FOREIGN KEY (OriginalPassword)
REFERENCES Password (PasswordId);


ALTER TABLE AdvancedMask
ADD FOREIGN KEY (OriginalPassword)
REFERENCES Password (PasswordId);


ALTER TABLE BaseWord
ADD FOREIGN KEY (OriginalPassword)
REFERENCES Password (PasswordId);


ALTER TABLE SimpleMask
ADD FOREIGN KEY (OriginalPassword)
REFERENCES Password (PasswordId);

ALTER TABLE MarkovChain
ADD FOREIGN KEY (OriginalPassword)
REFERENCES Password (PasswordId);


ALTER TABLE Complexity
ADD FOREIGN KEY (OriginalPassword)
REFERENCES Password (PasswordId);

ALTER TABLE Password
ADD FOREIGN KEY (PasswordOrigin)
REFERENCES PasswordOrigin (OriginId);

ALTER TABLE PasswordOrigin
ADD FOREIGN KEY (Availability)
REFERENCES Availability (AvailabilityId);