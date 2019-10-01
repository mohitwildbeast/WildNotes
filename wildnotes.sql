CREATE DATABASE IF NOT EXISTS `wildnotes` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `wildnotes`;

CREATE TABLE IF NOT EXISTS `users` (
	`id` int(10) NOT NULL AUTO_INCREMENT,
    `email` varchar(100) NOT NULL,
    `password` varchar(255) NOT NULL,
    `name` varchar(100) NOT NULL,
    PRIMARY KEY(`id`)
	) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
    