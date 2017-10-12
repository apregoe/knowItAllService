DROP DATABASE if exists knowItAll;
CREATE DATABASE knowItAll;

USE knowItAll;

-- Topic which is one of Academic, Food, Entertainment, Locations 
CREATE TABLE Topic (
    topicId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    topicName VARCHAR(50) NOT NULL
);

-- Category within a Topic, e.g. 'Food Truck', 'Movie Theater', Park, Class
CREATE TABLE Category (
    categoryId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    topicId INT(11) NOT NULL,
    categoryName VARCHAR(50) NOT NULL,
    FOREIGN KEY (topicId)
        REFERENCES Topic (topicId),
);

-- An member of a Category, e.g. CSCI103, 'Blaze Pizza', 
CREATE TABLE CategoryMember (
    categoryMemberId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    categoryId INT(11) NOT NULL,
    categoryMemberName VARCHAR(50) NOT NULL,
    FOREIGN KEY (categoryId)
        REFERENCES Category (categoryId),
);

CREATE TABLE User (
    userId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Token VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    uscEmail VARCHAR(50) NOT NULL,
    verified INT(1)
);

CREATE TABLE UserRating (
    userRatingId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    userId INT(11) NOT NULL,
    categoryMemberId INT(11) NOT NULL,
    rating INT(11) NOT NULL,
    FOREIGN KEY (userID)
        REFERENCES User (userId),
    FOREIGN KEY (categoryMemberId)
        REFERENCES CategoryMember (categoryMemberId)
);


CREATE TABLE Poll (
    packageID INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    userID INT(11) NOT NULL,
    title VARCHAR(64) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (userID)
        REFERENCES LinkItUser (userID)
);

- Create Topics
INSERT INTO Topic (topicName)
    VALUES ('Academic');
INSERT INTO Topic (topicName)
    VALUES ('Food');
INSERT INTO Topic (topicName)
    VALUES ('Entertainment');
INSERT INTO Topic (topicName)
    VALUES ('Locations'); 

