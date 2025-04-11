
-- warehouse definition

-- Drop table

-- DROP TABLE warehouse;

CREATE TABLE warehouse (
	w_id int4 NOT NULL,
	w_ytd numeric(12, 2) NOT NULL,
	w_tax numeric(4, 4) NOT NULL,
	w_name varchar(10) NOT NULL,
	w_street_1 varchar(20) NOT NULL,
	w_street_2 varchar(20) NOT NULL,
	w_city varchar(20) NOT NULL,
	w_state bpchar(2) NOT NULL,
	w_zip bpchar(9) NOT NULL,
	CONSTRAINT warehouse_pkey PRIMARY KEY (w_id)
);



-- item definition

-- Drop table

-- DROP TABLE item;


CREATE TABLE item (
	i_id int4 NOT NULL,
	i_name varchar(24) NOT NULL,
	i_price numeric(5, 2) NOT NULL,
	i_data varchar(50) NOT NULL,
	i_im_id int4 NOT NULL,
	CONSTRAINT item_pkey PRIMARY KEY (i_id)
);


-- stock definition

-- Drop table

-- DROP TABLE stock;


CREATE TABLE stock (
	s_w_id int4 NOT NULL,
	s_i_id int4 NOT NULL,
	s_quantity int4 NOT NULL,
	s_ytd numeric(8, 2) NOT NULL,
	s_order_cnt int4 NOT NULL,
	s_remote_cnt int4 NOT NULL,
	s_data varchar(50) NOT NULL,
	s_dist_01 bpchar(24) NOT NULL,
	s_dist_02 bpchar(24) NOT NULL,
	s_dist_03 bpchar(24) NOT NULL,
	s_dist_04 bpchar(24) NOT NULL,
	s_dist_05 bpchar(24) NOT NULL,
	s_dist_06 bpchar(24) NOT NULL,
	s_dist_07 bpchar(24) NOT NULL,
	s_dist_08 bpchar(24) NOT NULL,
	s_dist_09 bpchar(24) NOT NULL,
	s_dist_10 bpchar(24) NOT NULL,
	CONSTRAINT stock_pkey PRIMARY KEY (s_w_id HASH, s_i_id ASC),
	CONSTRAINT stock_s_i_id_fkey FOREIGN KEY (s_i_id) REFERENCES item(i_id) ON DELETE CASCADE,
	CONSTRAINT stock_s_w_id_fkey FOREIGN KEY (s_w_id) REFERENCES warehouse(w_id) ON DELETE CASCADE
);



-- district definition

-- Drop table

-- DROP TABLE district;

CREATE TABLE district (
	d_w_id int4 NOT NULL,
	d_id int4 NOT NULL,
	d_ytd numeric(12, 2) NOT NULL,
	d_tax numeric(4, 4) NOT NULL,
	d_next_o_id int4 NOT NULL,
	d_name varchar(10) NOT NULL,
	d_street_1 varchar(20) NOT NULL,
	d_street_2 varchar(20) NOT NULL,
	d_city varchar(20) NOT NULL,
	d_state bpchar(2) NOT NULL,
	d_zip bpchar(9) NOT NULL,
	CONSTRAINT district_pkey PRIMARY KEY ((d_w_id,d_id) HASH),
	CONSTRAINT district_d_w_id_fkey FOREIGN KEY (d_w_id) REFERENCES warehouse(w_id) ON DELETE CASCADE
);


-- customer definition

-- Drop table

-- DROP TABLE customer;

CREATE TABLE customer (
	c_w_id int4 NOT NULL,
	c_d_id int4 NOT NULL,
	c_id int4 NOT NULL,
	c_discount numeric(4, 4) NOT NULL,
	c_credit bpchar(2) NOT NULL,
	c_last varchar(16) NOT NULL,
	c_first varchar(16) NOT NULL,
	c_credit_lim numeric(12, 2) NOT NULL,
	c_balance numeric(12, 2) NOT NULL,
	c_ytd_payment float8 NOT NULL,
	c_payment_cnt int4 NOT NULL,
	c_delivery_cnt int4 NOT NULL,
	c_street_1 varchar(20) NOT NULL,
	c_street_2 varchar(20) NOT NULL,
	c_city varchar(20) NOT NULL,
	c_state bpchar(2) NOT NULL,
	c_zip bpchar(9) NOT NULL,
	c_phone bpchar(16) NOT NULL,
	c_since timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	c_middle bpchar(2) NOT NULL,
	c_data varchar(500) NOT NULL,
	CONSTRAINT customer_pkey PRIMARY KEY ((c_w_id,c_d_id) HASH,c_id),
	CONSTRAINT customer_c_w_id_c_d_id_fkey FOREIGN KEY (c_w_id,c_d_id) REFERENCES district(d_w_id,d_id) ON DELETE CASCADE
);
-- CREATE UNIQUE INDEX customer_i2 ON customer USING lsm (c_w_id, c_d_id, c_last, c_first, c_id);

-- CREATE INDEX idx_customer_name ON customer USING lsm (c_w_id, c_d_id, c_last, c_first);



-- history definition

-- Drop table

-- DROP TABLE history;


CREATE TABLE history (
	h_c_id int4 NOT NULL,
	h_c_d_id int4 NOT NULL,
	h_c_w_id int4 NOT NULL,
	h_d_id int4 NOT NULL,
	h_w_id int4 NOT NULL,
	h_date timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	h_amount numeric(6, 2) NOT NULL,
	h_data varchar(24) NOT NULL,
	CONSTRAINT history_h_c_w_id_h_c_d_id_h_c_id_fkey FOREIGN KEY (h_c_w_id,h_c_d_id,h_c_id) REFERENCES customer(c_w_id,c_d_id,c_id) ON DELETE CASCADE,
	CONSTRAINT history_h_w_id_h_d_id_fkey FOREIGN KEY (h_w_id,h_d_id) REFERENCES district(d_w_id,d_id) ON DELETE CASCADE
);




-- oorder definition

-- Drop table

-- DROP TABLE oorder;


CREATE TABLE oorder (
	o_w_id int4 NOT NULL,
	o_d_id int4 NOT NULL,
	o_id int4 NOT NULL,
	o_c_id int4 NOT NULL,
	o_carrier_id int4 NULL DEFAULT NULL,
	o_ol_cnt int4 NOT NULL,
	o_all_local int4 NOT NULL,
	o_entry_d timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT oorder_o_w_id_o_d_id_o_c_id_o_id_key UNIQUE (o_w_id, o_d_id, o_c_id, o_id),
	CONSTRAINT oorder_pkey PRIMARY KEY ((o_w_id,o_d_id) HASH,o_id),
	CONSTRAINT oorder_o_w_id_o_d_id_o_c_id_fkey FOREIGN KEY (o_w_id,o_d_id,o_c_id) REFERENCES customer(c_w_id,c_d_id,c_id) ON DELETE CASCADE
);
-- CREATE UNIQUE INDEX oorder_i2 ON oorder USING lsm (o_w_id, o_d_id, o_c_id, o_id);



-- new_order definition

-- Drop table

-- DROP TABLE new_order;


CREATE TABLE new_order (
	no_w_id int4 NOT NULL,
	no_d_id int4 NOT NULL,
	no_o_id int4 NOT NULL,
	CONSTRAINT new_order_pkey PRIMARY KEY ((no_w_id,no_d_id) HASH,no_o_id),
	CONSTRAINT new_order_no_w_id_no_d_id_no_o_id_fkey FOREIGN KEY (no_w_id,no_d_id,no_o_id) REFERENCES oorder(o_w_id,o_d_id,o_id) ON DELETE CASCADE
);


-- order_line definition

-- Drop table

-- DROP TABLE order_line;


CREATE TABLE order_line (
	ol_w_id int4 NOT NULL,
	ol_d_id int4 NOT NULL,
	ol_o_id int4 NOT NULL,
	ol_number int4 NOT NULL,
	ol_i_id int4 NOT NULL,
	ol_delivery_d timestamp NULL DEFAULT NULL,
	ol_amount numeric(6, 2) NOT NULL,
	ol_supply_w_id int4 NOT NULL,
	ol_quantity numeric(6, 2) NOT NULL,
	ol_dist_info bpchar(24) NOT NULL,
	CONSTRAINT order_line_pkey PRIMARY KEY ((ol_w_id,ol_d_id) HASH, ol_o_id,ol_number),
	CONSTRAINT order_line_ol_supply_w_id_ol_i_id_fkey FOREIGN KEY (ol_supply_w_id,ol_i_id) REFERENCES stock(s_w_id,s_i_id) ON DELETE CASCADE,
	CONSTRAINT order_line_ol_w_id_ol_d_id_ol_o_id_fkey FOREIGN KEY (ol_w_id,ol_d_id,ol_o_id) REFERENCES oorder(o_w_id,o_d_id,o_id) ON DELETE CASCADE
);





SELECT pg_sleep(30);
