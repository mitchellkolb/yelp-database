
--SQL script file containing all CREATE TABLE statements. Name this file “<your-name>_RELATIONS_v2.sql”



CREATE TABLE Businesses(
	address VARCHAR (20),
	state VARCHAR (20),
	city VARCHAR (20),
	lat_long_cords VARCHAR (20),
	businessID CHAR (20),
	business_name VARCHAR (20),
	business_details VARCHAR (300),
	PRIMARY KEY (businessID)
);

CREATE TABLE Checkin(
	date_ DATE,
	amounr_of_checkins Integer,
	businessID CHAR (20),
	PRIMARY KEY (date_, businessID),
	FOREIGN KEY (businessID) REFERENCES Businesses(businessID)
);

CREATE TABLE Categories(
	nameCat VARCHAR(20),
	typesCat VARCHAR(100),
	businessID CHAR (20),
	PRIMARY KEY (nameCat, businessID),
	FOREIGN KEY (businessID) REFERENCES Businesses(businessID)
);

CREATE TABLE Attributes(
	nameAtt VARCHAR(20),
	valueAtt Integer,
	businessID CHAR (20),
	PRIMARY KEY (nameAtt, businessID),
	FOREIGN KEY (businessID) REFERENCES Businesses(businessID)
);

CREATE TABLE Users(
	income Integer,
	userID VARCHAR (20),
	username VARCHAR (20),
	userfriends VARCHAR (200),
	userdetails VARCHAR (200),
	PRIMARY KEY (userID)
);


CREATE TABLE located_in(
	zipcode Integer,
	businessID CHAR (20),
	userID VARCHAR (20),
	FOREIGN KEY (businessID) REFERENCES Businesses(businessID),
	FOREIGN KEY (userID) REFERENCES Users(userID)
);


CREATE TABLE Review(
	date_ DATE,
	reviewScore Integer,
	starRating Integer,
	content_of_review VARCHAR (1000),
	reviewID VARCHAR (20),
	userID VARCHAR (20),
	PRIMARY KEY (reviewID),
	FOREIGN KEY (userID) REFERENCES Users(userID)
);


CREATE TABLE matched_with(
	businessID CHAR (20),
	reviewID VARCHAR (20),
	FOREIGN KEY (businessID) REFERENCES Businesses(businessID),
	FOREIGN KEY (reviewID) REFERENCES Review(reviewID)
);


CREATE TABLE Writes(
	reviewID VARCHAR (20),
	userID VARCHAR (20),
	FOREIGN KEY (reviewID) REFERENCES Review(reviewID),
	FOREIGN KEY (userID) REFERENCES Users(userID)
);