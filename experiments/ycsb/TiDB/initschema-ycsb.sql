-- Switch to or create a database
-- CREATE DATABASE ycsb;
-- USE ycsb;

-- Create table with hash sharding for better distribution
CREATE TABLE usertable (
  YCSB_KEY VARCHAR(255) PRIMARY KEY,
  FIELD0 TEXT,
  FIELD1 TEXT,
  FIELD2 TEXT,
  FIELD3 TEXT,
  FIELD4 TEXT,
  FIELD5 TEXT,
  FIELD6 TEXT,
  FIELD7 TEXT,
  FIELD8 TEXT,
  FIELD9 TEXT
) SHARD_ROW_ID_BITS = 4;
