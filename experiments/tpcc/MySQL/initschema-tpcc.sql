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


-- set max MEMORY engine size
SET GLOBAL tmp_table_size = 1024 * 1024 * 1024 * 32;
SET GLOBAL max_heap_table_size = 1024 * 1024 * 1024 * 32;
