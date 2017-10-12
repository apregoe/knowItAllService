DROP DATABASE if exists knowItAll;
CREATE DATABASE knowItAll;

USE knowItAll;

-- 1 of the 4: Academic, Entertainment, Social, Location
CREATE TABLE Category (
    categoryId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    categoryName VARCHAR(20) NOT NULL,
);

-- Ex. CSCI 310, Prof. Michael Schindler
CREATE TABLE Topic (
    topicId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    categoryId INT(11) NOT NULL,
    title VARCHAR(50) NOT NULL,
    FOREIGN KEY (categoryId)
        REFERENCES Category (categoryId)
);

CREATE TABLE User (
    userId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    password VARCHAR(50) NOT NULL,
    uscEmail VARCHAR(50) NOT NULL,
    verified INT(1)
);

-- A UserReview is created every time a user reviews an Item.
CREATE TABLE Review (
    reviewId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    userId INT(11) NOT NULL,
    topicId INT(11) NOT NULL,
    rating INT(1) NOT NULL,
    comment VARCHAR(256),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID)
        REFERENCES User (userId),
    FOREIGN KEY (topicId)
        REFERENCES Topic (topicId)
);


CREATE TABLE Poll (
    pollId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    userID INT(11) NOT NULL,
    openForever INT(1)
    endTime TIMESTAMP,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    text VARCHAR(64) NOT NULL,
    FOREIGN KEY (userID)
        REFERENCES User (userID)
);

CREATE TABLE PollChoice (
    pollChoiceId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    pollId INT(11) NOT NULL,
    text VARCHAR(64) NOT NULL,
    FOREIGN KEY (pollId)
        REFERENCES Poll (pollId)
);

CREATE TABLE Vote (
    voteId INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    pollChoiceId INT(11) NOT NULL,
    userId INT(11) NOT NULL,
    FOREIGN KEY (pollChoiceId)
        REFERENCES PollChoice (pollChoiceId)
    FOREIGN KEY (userID)
        REFERENCES User (userId),
);

- Create the 4 Main Categories that are always needed.
INSERT INTO Topic (topicName)
    VALUES ('Academic');
INSERT INTO Topic (topicName)
    VALUES ('Food');
INSERT INTO Topic (topicName)
    VALUES ('Entertainment');
INSERT INTO Topic (topicName)
    VALUES ('Locations'); 
  
