-- https://docs.yugabyte.com/preview/benchmark/ycsb-jdbc
-- https://docs.yugabyte.com/stable/architecture/docdb-sharding/tablet-splitting/#ycsb-workload-with-automatic-tablet-splitting-example
-- https://www.yugabyte.com/blog/optimizing-yugabytedb-memory-tuning-for-ysql/
-- ./bin/yb-ctl --rf=3 create --master_flags "enable_automatic_tablet_splitting=true,tablet_split_low_phase_size_threshold_bytes=30000000" --tserver_flags "memstore_size_mb=10"


-- SELECT 'DROP old usertable' as message;
-- DROP TABLE IF EXISTS public.usertable CASCADE;

-- wait 60 seconds
-- SELECT 'Wait 60 s';
-- select (pg_sleep(60.0::double precision)::text = '')::text as "waiting completed", current_timestamp as "time after waiting";

ALTER DATABASE yugabyte SET temp_file_limit=-1;


-- SELECT "CREATE new usertable";
CREATE TABLE IF NOT EXISTS usertable (
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

SELECT current_timestamp AS "Time after creation";

-- wait 300 seconds
-- SELECT 'Wait 300 s';
-- select (pg_sleep(300.0::double precision)::text = '')::text as "waiting completed", current_timestamp as "time after waiting";

SELECT COUNT(*) AS "Number of rows in usertable" FROM usertable;

