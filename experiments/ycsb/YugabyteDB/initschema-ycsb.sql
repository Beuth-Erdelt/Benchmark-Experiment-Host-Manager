DROP TABLE IF EXISTS public.usertable CASCADE;


alter database yugabyte SET temp_file_limit=-1;


CREATE TABLE public.usertable (
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

  -- https://docs.yugabyte.com/preview/benchmark/ycsb-jdbc