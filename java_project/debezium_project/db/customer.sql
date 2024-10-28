CREATE DATABASE IF NOT EXISTS customerdb;

USE customerdb;

DROP TABLE IF EXISTS `customer`;

CREATE TABLE `customer` (
   `id` int not null,
   `fullname` varchar(255) default null,
   `email` varchar(255) default null,
   PRIMARY KEY (`id`)
);

INSERT INTO customerdb.customer VALUES (1, 'John Doe', 'jd@example.com');