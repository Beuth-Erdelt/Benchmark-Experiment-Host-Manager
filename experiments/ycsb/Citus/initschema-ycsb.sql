CREATE TABLE public.usertable (
  YCSB_KEY varchar(255) NOT NULL,
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
  PRIMARY KEY (YCSB_KEY)
);

SELECT create_distributed_table('usertable', 'YCSB_KEY');

ALTER TABLE usertable SET (replication_factor = {num_worker_replicas});

