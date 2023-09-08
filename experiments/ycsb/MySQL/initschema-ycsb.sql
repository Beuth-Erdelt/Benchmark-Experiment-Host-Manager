DROP USER 'root'@'%';
FLUSH PRIVILEGES;

CREATE USER 'root'@'%';
ALTER USER 'root'@'%' IDENTIFIED BY 'root';

 -- SET PASSWORD FOR root@'172.17.0.3' = PASSWORD('root');

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

-- allow load local in file
SET GLOBAL local_infile = 1;

-- allow zero date
SET sql_mode='';
SET GLOBAL sql_mode='';

-- speed up import
SET GLOBAL innodb_buffer_pool_size = 32*1024*1024*1024;
SET GLOBAL innodb_log_buffer_size = 16*1024*1024*1024;
SET GLOBAL innodb_flush_log_at_trx_commit =0;

CREATE DATABASE ycsb;

CREATE TABLE ycsb.usertable (
  `YCSB_KEY` varchar(255) NOT NULL,
  `FIELD0` text,
  `FIELD1` text,
  `FIELD2` text,
  `FIELD3` text,
  `FIELD4` text,
  `FIELD5` text,
  `FIELD6` text,
  `FIELD7` text,
  `FIELD8` text,
  `FIELD9` text,
  PRIMARY KEY (`YCSB_KEY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

