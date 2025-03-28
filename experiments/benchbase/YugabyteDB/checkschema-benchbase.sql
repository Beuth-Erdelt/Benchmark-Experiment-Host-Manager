select 'yb_servers' as msg;
SELECT * -- public_ip, yb_local_tablets.*
FROM yb_servers()
JOIN yb_local_tablets ON true;

