DROP DATABASE IF EXISTS AIdb;
CREATE DATABASE AIdb
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;

USE AIdb;
GRANT ALL PRIVILEGES ON AIdb.* TO 'AIUser'@'localhost' IDENTIFIED BY 'Na8JDfVTV3vUglx'
WITH GRANT OPTION ;
FLUSH PRIVILEGES ;