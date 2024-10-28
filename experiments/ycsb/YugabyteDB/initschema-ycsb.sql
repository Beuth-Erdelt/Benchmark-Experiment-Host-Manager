SELECT 'DROP old usertable' as message;
-- DROP TABLE IF EXISTS public.usertable CASCADE;

-- wait 60 seconds
SELECT 'Wait 60 s';
-- select (pg_sleep(60.0::double precision)::text = '')::text;

alter database yugabyte SET temp_file_limit=-1;


SELECT 'CREATE new usertable';
CREATE TABLE usertable (
           YCSB_KEY VARCHAR(255) PRIMARY KEY,
           FIELD0 TEXT, FIELD1 TEXT, FIELD2 TEXT, FIELD3 TEXT,
           FIELD4 TEXT, FIELD5 TEXT, FIELD6 TEXT, FIELD7 TEXT,
           FIELD8 TEXT, FIELD9 TEXT);

/*
CREATE TABLE usertable (
  YCSB_KEY varchar(255),
  FIELD0 text,
  FIELD1 text,
  FIELD2 text,
  FIELD3 text,
  FIELD4 text,
  FIELD5 text,
  FIELD6 text,
  FIELD7 text,
  FIELD8 text,
  FIELD9 text,
  PRIMARY KEY (YCSB_KEY ASC))
  SPLIT AT VALUES (('user10'),('user14'),('user18'),
  ('user22'),('user26'),('user30'),('user34'),('user38'),
  ('user42'),('user46'),('user50'),('user54'),('user58'),
  ('user62'),('user66'),('user70'),('user74'),('user78'),
  ('user82'),('user86'),('user90'),('user94'),('user98')
);
*/

SELECT 'Time after creation';
select current_timestamp;

-- wait 300 seconds
SELECT 'Wait 300 s';
-- select (pg_sleep(300.0::double precision)::text = '')::text;

SELECT 'Time after waiting';
select current_timestamp;

SELECT COUNT(*) AS "number of rows in usertable" FROM usertable;

-- https://docs.yugabyte.com/preview/benchmark/ycsb-jdbc
