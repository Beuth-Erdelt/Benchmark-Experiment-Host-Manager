SELECT COUNT(*) FROM tpch.customer FORCE INDEX(c_n);
SELECT COUNT(*) FROM tpch.nation FORCE INDEX(n_r);
SELECT COUNT(*) FROM tpch.supplier FORCE INDEX(s_n);
SELECT COUNT(*) FROM tpch.partsupp FORCE INDEX(ps_s);
SELECT COUNT(*) FROM tpch.partsupp FORCE INDEX(ps_p);
SELECT COUNT(*) FROM tpch.orders FORCE INDEX(o_c);
SELECT COUNT(*) FROM tpch.lineitem FORCE INDEX(l_o);
SELECT COUNT(*) FROM tpch.lineitem FORCE INDEX(l_ps);

SELECT COUNT(*) FROM tpch.customer;
SELECT COUNT(*) FROM tpch.lineitem;
SELECT COUNT(*) FROM tpch.nation;
SELECT COUNT(*) FROM tpch.supplier;
SELECT COUNT(*) FROM tpch.partsupp;
SELECT COUNT(*) FROM tpch.orders;
SELECT COUNT(*) FROM tpch.region;
SELECT COUNT(*) FROM tpch.part;
