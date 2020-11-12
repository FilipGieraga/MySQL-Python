DROP DATABASE IF EXISTS my_store;
CREATE DATABASE my_store;

USE my_store; 


CREATE TABLE accounts (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(32) UNIQUE NOT NULL,
    email Varchar(50) NOT NULL
);


CREATE TABLE account_details (
    id INTEGER,
    address VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    zip_code varchar(6) NOT NULL,
    phone INT(9) NOT NULL,
    INDEX AD_id (id),
	FOREIGN KEY (id)
        REFERENCES Accounts(id)
        ON DELETE CASCADE
);


CREATE TABLE orders (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    order_date datetime default now(),
    total_price float default null,
    comment varchar(200) default null ,
    order_rating int,
    account_id INT,
    INDEX A_id (account_id),
	FOREIGN KEY (account_id)
        REFERENCES Accounts(id)
        ON DELETE CASCADE
);

CREATE TABLE Products (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    Product_name varchar(250),
    Brand varchar(30),
    Unit_price float not null
);

CREATE TABLE Order_Products(
	Order_ID int,
    Product_ID int,
    Amount int,
    Total Float Default Null,
    INDEX O_id (Order_ID),
    INDEX P_id (Product_ID),
    FOREIGN KEY (Order_ID)
        REFERENCES Orders(id)
        ON DELETE CASCADE,
	FOREIGN KEY (Product_ID)
        REFERENCES Products(id)
        ON DELETE CASCADE);


CREATE TABLE Product_ratings(
	Product_ID int,
    Account_ID int,
    Rating int,
    INDEX A_id (Account_ID),
    INDEX P_id (Product_ID),
	FOREIGN KEY (Account_ID)
        REFERENCES Accounts(id)
        ON DELETE CASCADE,
	FOREIGN KEY (Product_ID)
        REFERENCES Products(id)
        ON DELETE CASCADE);
    
    
    
    
    
    
    
 
 
 
 
 
 
 
 
 
 
 
 
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    