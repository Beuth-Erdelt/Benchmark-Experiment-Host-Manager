CREATE DATABASE ycsb;

-- CREATE TABLE ycsb.usertable (

CREATE ROWSTORE TABLE ycsb.usertable (
  YCSB_KEY varchar(255) PRIMARY KEY,
  FIELD0 text,
  FIELD1 text,
  FIELD2 text,
  FIELD3 text,
  FIELD4 text,
  FIELD5 text,
  FIELD6 text,
  FIELD7 text,
  FIELD8 text,
  FIELD9 text
);

USE ycsb;

SHOW TABLES EXTENDED;

SHOW DATABASES EXTENDED;

SHOW TABLES IN ycsb EXTENDED;

