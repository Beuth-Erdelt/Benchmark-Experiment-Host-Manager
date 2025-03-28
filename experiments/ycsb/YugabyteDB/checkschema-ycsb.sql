select 'yb_table_properties.usertable' as msg;
SELECT * FROM yb_table_properties('usertable'::regclass);

select 'yb_servers' as msg;
SELECT * -- public_ip, yb_local_tablets.*
FROM yb_servers()
JOIN yb_local_tablets ON true;

SELECT COUNT(*) AS "Number of rows in usertable" FROM usertable;

