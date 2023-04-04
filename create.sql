DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS ItemCategory;
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS Member;

CREATE TABLE Item(
    	item_id INTEGER PRIMARY KEY,
    	name VARCHAR(255),
    	currently DOUBLE,
    	first_bid DOUBLE,
    	number_of_bids INTEGER,
    	started SMALLDATETIME,
    	ends SMALLDATETIME,
    	description TEXT,
    	buy_price DOUBLE,
    	seller_id VARCHAR(255),
    	FOREIGN KEY(seller_id) REFERENCES Member(user_id));

CREATE TABLE Bid(
    	item_id INTEGER,
	bidder_id VARCHAR(255),
    	time SMALLDATETIME,
    	amount DOUBLE,
    	PRIMARY KEY(item_id, bidder_id, time),
    	FOREIGN KEY(bidder_id) REFERENCES Member(user_id),
    	FOREIGN KEY(item_id) REFERENCES Item(item_id));

CREATE TABLE Category(
    	name VARCHAR(255) PRIMARY KEY);

CREATE TABLE Member(
    	user_id VARCHAR(255) PRIMARY KEY,
    	rating INTEGER,
	location VARCHAR(255),
	country VARCHAR(50));

CREATE TABLE ItemCategory(
    	item_id INTEGER,
    	category_name VARCHAR(255),
    	PRIMARY KEY(item_id, category_name),
    	FOREIGN KEY(item_id) REFERENCES Item(item_id),
    	FOREIGN KEY(category_name) REFERENCES Category(name));