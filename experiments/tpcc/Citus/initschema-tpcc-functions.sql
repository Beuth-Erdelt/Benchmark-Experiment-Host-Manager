-- this is what hammerdb generates for postgresql
-- for citus and benchbase we do not use this, since benchbase runs business logic on the client side




-- DROP FUNCTION public.dbms_random(int4, int4);

CREATE OR REPLACE FUNCTION public.dbms_random(integer, integer)
 RETURNS integer
 LANGUAGE plpgsql
 STRICT
AS $function$
                DECLARE
                start_int ALIAS FOR $1;
                end_int ALIAS FOR $2;
                BEGIN
                RETURN trunc(random() * (end_int-start_int + 1) + start_int);
                END;
                $function$
;

-- DROP FUNCTION public.delivery(int4, int4);

CREATE OR REPLACE FUNCTION public.delivery(integer, integer)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
                DECLARE
                d_w_id		ALIAS FOR $1;
                d_o_carrier_id  ALIAS FOR $2;
                loop_counter	SMALLINT;
                d_id_in_array	SMALLINT[] := ARRAY[1,2,3,4,5,6,7,8,9,10];
                d_id_array		SMALLINT[];
                o_id_array 		INT[];
                c_id_array 		INT[];
                order_count		SMALLINT;
                sum_amounts     NUMERIC[];

                customer_count INT;
                BEGIN
                WITH new_order_delete AS (
                DELETE
                FROM new_order as del_new_order
                USING UNNEST(d_id_in_array) AS d_ids
                WHERE no_d_id = d_ids
                AND no_w_id = d_w_id
                AND del_new_order.no_o_id = (select min (select_new_order.no_o_id)
                from new_order as select_new_order
                where no_d_id = d_ids
                and no_w_id = d_w_id)
                RETURNING del_new_order.no_o_id, del_new_order.no_d_id
                )
                SELECT array_agg(no_o_id), array_agg(no_d_id)
                FROM new_order_delete
                INTO o_id_array, d_id_array;

                UPDATE orders
                SET o_carrier_id = d_o_carrier_id
                FROM UNNEST(o_id_array, d_id_array) AS ids(o_id, d_id)
                WHERE orders.o_id = ids.o_id
                AND o_d_id = ids.d_id
                AND o_w_id = d_w_id;

                WITH order_line_update AS (
                UPDATE order_line
                SET ol_delivery_d = current_timestamp
                FROM UNNEST(o_id_array, d_id_array) AS ids(o_id, d_id)
                WHERE ol_o_id = ids.o_id
                AND ol_d_id = ids.d_id
                AND ol_w_id = d_w_id
                RETURNING ol_d_id, ol_o_id, ol_amount
                )
                SELECT array_agg(ol_d_id), array_agg(c_id), array_agg(sum_amount)
                FROM ( SELECT ol_d_id,
                ( SELECT DISTINCT o_c_id FROM orders WHERE o_id = ol_o_id AND o_d_id = ol_d_id AND o_w_id = d_w_id) AS c_id,
                sum(ol_amount) AS sum_amount
                FROM order_line_update
                GROUP BY ol_d_id, ol_o_id ) AS inner_sum
                INTO d_id_array, c_id_array, sum_amounts;

                UPDATE customer
                SET c_balance = COALESCE(c_balance,0) + ids_and_sums.sum_amounts
                FROM UNNEST(d_id_array, c_id_array, sum_amounts) AS ids_and_sums(d_id, c_id, sum_amounts)
                WHERE customer.c_id = ids_and_sums.c_id
                AND c_d_id = ids_and_sums.d_id
                AND c_w_id = d_w_id;

                RETURN 1;

                EXCEPTION
                WHEN serialization_failure OR deadlock_detected OR no_data_found
                THEN ROLLBACK;
                END;
                $function$
;

-- DROP FUNCTION public.neword(int4, int4, int4, int4, int4, int4);

CREATE OR REPLACE FUNCTION public.neword(integer, integer, integer, integer, integer, integer)
 RETURNS numeric
 LANGUAGE plpgsql
AS $function$
                DECLARE
                no_w_id		        ALIAS FOR $1;
                no_max_w_id	        ALIAS FOR $2;
                no_d_id		        ALIAS FOR $3;
                no_c_id		        ALIAS FOR $4;
                no_o_ol_cnt	        ALIAS FOR $5;
                no_d_next_o_id	    ALIAS FOR $6;
                no_c_discount	    NUMERIC;
                no_c_last			VARCHAR;
                no_c_credit			VARCHAR;
                no_d_tax			NUMERIC;
                no_w_tax			NUMERIC;
                no_s_quantity		NUMERIC;
                no_o_all_local		SMALLINT;
                rbk					SMALLINT;
                item_id_array 		INT[];
                supply_wid_array	INT[];
                quantity_array		SMALLINT[];
                order_line_array	SMALLINT[];
                stock_dist_array	CHAR(24)[];
                s_quantity_array	SMALLINT[];
                price_array			NUMERIC(5,2)[];
                amount_array		NUMERIC(5,2)[];
                BEGIN
                no_o_all_local := 1;
                SELECT c_discount, c_last, c_credit, w_tax
                INTO no_c_discount, no_c_last, no_c_credit, no_w_tax
                FROM customer, warehouse
                WHERE warehouse.w_id = no_w_id AND customer.c_w_id = no_w_id AND customer.c_d_id = no_d_id AND customer.c_id = no_c_id;

                --#2.4.1.4
                rbk := round(DBMS_RANDOM(1,100));
                --#2.4.1.5
                FOR loop_counter IN 1 .. no_o_ol_cnt
                LOOP
                IF ((loop_counter = no_o_ol_cnt) AND (rbk = 1))
                THEN
                item_id_array[loop_counter] := 100001;
                ELSE
                item_id_array[loop_counter] := round(DBMS_RANDOM(1,100000));
                END IF;

                --#2.4.1.5.2
                IF ( round(DBMS_RANDOM(1,100)) > 1 )
                THEN
                supply_wid_array[loop_counter] := no_w_id;
                ELSE
                no_o_all_local := 0;
                supply_wid_array[loop_counter] := 1 + MOD(CAST (no_w_id + round(DBMS_RANDOM(0,no_max_w_id-1)) AS INT), no_max_w_id);
                END IF;

                --#2.4.1.5.3
                quantity_array[loop_counter] := round(DBMS_RANDOM(1,10));
                order_line_array[loop_counter] := loop_counter;
                END LOOP;

                UPDATE district SET d_next_o_id = d_next_o_id + 1 WHERE d_id = no_d_id AND d_w_id = no_w_id RETURNING d_next_o_id - 1, d_tax INTO no_d_next_o_id, no_d_tax;

                INSERT INTO ORDERS (o_id, o_d_id, o_w_id, o_c_id, o_entry_d, o_ol_cnt, o_all_local) VALUES (no_d_next_o_id, no_d_id, no_w_id, no_c_id, current_timestamp, no_o_ol_cnt, no_o_all_local);
                INSERT INTO NEW_ORDER (no_o_id, no_d_id, no_w_id) VALUES (no_d_next_o_id, no_d_id, no_w_id);

                SELECT array_agg ( i_price )
                INTO price_array
                FROM UNNEST(item_id_array) item_id
                LEFT JOIN item ON i_id = item_id;

                IF no_d_id = 1
                THEN
                WITH stock_update AS (
                UPDATE stock
                SET s_quantity = ( CASE WHEN s_quantity < (item_stock.quantity + 10) THEN s_quantity + 91 ELSE s_quantity END) - item_stock.quantity
                FROM UNNEST(item_id_array, supply_wid_array, quantity_array, price_array)
                AS item_stock (item_id, supply_wid, quantity, price)
                WHERE stock.s_i_id = item_stock.item_id
                AND stock.s_w_id = item_stock.supply_wid
                AND stock.s_w_id = ANY(supply_wid_array)
                RETURNING stock.s_dist_01 as s_dist, stock.s_quantity, ( item_stock.quantity + item_stock.price * ( 1 + no_w_tax + no_d_tax ) * ( 1 - no_c_discount ) ) amount
                )
                SELECT array_agg ( s_dist ), array_agg ( s_quantity ), array_agg ( amount )
                FROM stock_update
                INTO stock_dist_array, s_quantity_array, amount_array;
                ELSIF no_d_id = 2
                THEN
                WITH stock_update AS (
                UPDATE stock
                SET s_quantity = ( CASE WHEN s_quantity < (item_stock.quantity + 10) THEN s_quantity + 91 ELSE s_quantity END) - item_stock.quantity
                FROM UNNEST(item_id_array, supply_wid_array, quantity_array, price_array)
                AS item_stock (item_id, supply_wid, quantity, price)
                WHERE stock.s_i_id = item_stock.item_id
                AND stock.s_w_id = item_stock.supply_wid
                AND stock.s_w_id = ANY(supply_wid_array)
                RETURNING stock.s_dist_02 as s_dist, stock.s_quantity, ( item_stock.quantity + item_stock.price * ( 1 + no_w_tax + no_d_tax ) * ( 1 - no_c_discount ) ) amount
                )
                SELECT array_agg ( s_dist ), array_agg ( s_quantity ), array_agg ( amount )
                FROM stock_update
                INTO stock_dist_array, s_quantity_array, amount_array;
                ELSIF no_d_id = 3
                THEN
                WITH stock_update AS (
                UPDATE stock
                SET s_quantity = ( CASE WHEN s_quantity < (item_stock.quantity + 10) THEN s_quantity + 91 ELSE s_quantity END) - item_stock.quantity
                FROM UNNEST(item_id_array, supply_wid_array, quantity_array, price_array)
                AS item_stock (item_id, supply_wid, quantity, price)
                WHERE stock.s_i_id = item_stock.item_id
                AND stock.s_w_id = item_stock.supply_wid
                AND stock.s_w_id = ANY(supply_wid_array)
                RETURNING stock.s_dist_03 as s_dist, stock.s_quantity, ( item_stock.quantity + item_stock.price * ( 1 + no_w_tax + no_d_tax ) * ( 1 - no_c_discount ) ) amount
                )
                SELECT array_agg ( s_dist ), array_agg ( s_quantity ), array_agg ( amount )
                FROM stock_update
                INTO stock_dist_array, s_quantity_array, amount_array;
                ELSIF no_d_id = 4
                THEN
                WITH stock_update AS (
                UPDATE stock
                SET s_quantity = ( CASE WHEN s_quantity < (item_stock.quantity + 10) THEN s_quantity + 91 ELSE s_quantity END) - item_stock.quantity
                FROM UNNEST(item_id_array, supply_wid_array, quantity_array, price_array)
                AS item_stock (item_id, supply_wid, quantity, price)
                WHERE stock.s_i_id = item_stock.item_id
                AND stock.s_w_id = item_stock.supply_wid
                AND stock.s_w_id = ANY(supply_wid_array)
                RETURNING stock.s_dist_04 as s_dist, stock.s_quantity, ( item_stock.quantity + item_stock.price * ( 1 + no_w_tax + no_d_tax ) * ( 1 - no_c_discount ) ) amount
                )
                SELECT array_agg ( s_dist ), array_agg ( s_quantity ), array_agg ( amount )
                FROM stock_update
                INTO stock_dist_array, s_quantity_array, amount_array;
                ELSIF no_d_id = 5
                THEN
                WITH stock_update AS (
                UPDATE stock
                SET s_quantity = ( CASE WHEN s_quantity < (item_stock.quantity + 10) THEN s_quantity + 91 ELSE s_quantity END) - item_stock.quantity
                FROM UNNEST(item_id_array, supply_wid_array, quantity_array, price_array)
                AS item_stock (item_id, supply_wid, quantity, price)
                WHERE stock.s_i_id = item_stock.item_id
                AND stock.s_w_id = item_stock.supply_wid
                AND stock.s_w_id = ANY(supply_wid_array)
                RETURNING stock.s_dist_05 as s_dist, stock.s_quantity, ( item_stock.quantity + item_stock.price * ( 1 + no_w_tax + no_d_tax ) * ( 1 - no_c_discount ) ) amount
                )
                SELECT array_agg ( s_dist ), array_agg ( s_quantity ), array_agg ( amount )
                FROM stock_update
                INTO stock_dist_array, s_quantity_array, amount_array;
                ELSIF no_d_id = 6
                THEN
                WITH stock_update AS (
                UPDATE stock
                SET s_quantity = ( CASE WHEN s_quantity < (item_stock.quantity + 10) THEN s_quantity + 91 ELSE s_quantity END) - item_stock.quantity
                FROM UNNEST(item_id_array, supply_wid_array, quantity_array, price_array)
                AS item_stock (item_id, supply_wid, quantity, price)
                WHERE stock.s_i_id = item_stock.item_id
                AND stock.s_w_id = item_stock.supply_wid
                AND stock.s_w_id = ANY(supply_wid_array)
                RETURNING stock.s_dist_06 as s_dist, stock.s_quantity, ( item_stock.quantity + item_stock.price * ( 1 + no_w_tax + no_d_tax ) * ( 1 - no_c_discount ) ) amount
                )
                SELECT array_agg ( s_dist ), array_agg ( s_quantity ), array_agg ( amount )
                FROM stock_update
                INTO stock_dist_array, s_quantity_array, amount_array;
                ELSIF no_d_id = 7
                THEN
                WITH stock_update AS (
                UPDATE stock
                SET s_quantity = ( CASE WHEN s_quantity < (item_stock.quantity + 10) THEN s_quantity + 91 ELSE s_quantity END) - item_stock.quantity
                FROM UNNEST(item_id_array, supply_wid_array, quantity_array, price_array)
                AS item_stock (item_id, supply_wid, quantity, price)
                WHERE stock.s_i_id = item_stock.item_id
                AND stock.s_w_id = item_stock.supply_wid
                AND stock.s_w_id = ANY(supply_wid_array)
                RETURNING stock.s_dist_07 as s_dist, stock.s_quantity, ( item_stock.quantity + item_stock.price * ( 1 + no_w_tax + no_d_tax ) * ( 1 - no_c_discount ) ) amount
                )
                SELECT array_agg ( s_dist ), array_agg ( s_quantity ), array_agg ( amount )
                FROM stock_update
                INTO stock_dist_array, s_quantity_array, amount_array;
                ELSIF no_d_id = 8
                THEN
                WITH stock_update AS (
                UPDATE stock
                SET s_quantity = ( CASE WHEN s_quantity < (item_stock.quantity + 10) THEN s_quantity + 91 ELSE s_quantity END) - item_stock.quantity
                FROM UNNEST(item_id_array, supply_wid_array, quantity_array, price_array)
                AS item_stock (item_id, supply_wid, quantity, price)
                WHERE stock.s_i_id = item_stock.item_id
                AND stock.s_w_id = item_stock.supply_wid
                AND stock.s_w_id = ANY(supply_wid_array)
                RETURNING stock.s_dist_08 as s_dist, stock.s_quantity, ( item_stock.quantity + item_stock.price * ( 1 + no_w_tax + no_d_tax ) * ( 1 - no_c_discount ) ) amount
                )
                SELECT array_agg ( s_dist ), array_agg ( s_quantity ), array_agg ( amount )
                FROM stock_update
                INTO stock_dist_array, s_quantity_array, amount_array;
                ELSIF no_d_id = 9
                THEN
                WITH stock_update AS (
                UPDATE stock
                SET s_quantity = ( CASE WHEN s_quantity < (item_stock.quantity + 10) THEN s_quantity + 91 ELSE s_quantity END) - item_stock.quantity
                FROM UNNEST(item_id_array, supply_wid_array, quantity_array, price_array)
                AS item_stock (item_id, supply_wid, quantity, price)
                WHERE stock.s_i_id = item_stock.item_id
                AND stock.s_w_id = item_stock.supply_wid
                AND stock.s_w_id = ANY(supply_wid_array)
                RETURNING stock.s_dist_09 as s_dist, stock.s_quantity, ( item_stock.quantity + item_stock.price * ( 1 + no_w_tax + no_d_tax ) * ( 1 - no_c_discount ) ) amount
                )
                SELECT array_agg ( s_dist ), array_agg ( s_quantity ), array_agg ( amount )
                FROM stock_update
                INTO stock_dist_array, s_quantity_array, amount_array;
                ELSIF no_d_id = 10
                THEN
                WITH stock_update AS (
                UPDATE stock
                SET s_quantity = ( CASE WHEN s_quantity < (item_stock.quantity + 10) THEN s_quantity + 91 ELSE s_quantity END) - item_stock.quantity
                FROM UNNEST(item_id_array, supply_wid_array, quantity_array, price_array)
                AS item_stock (item_id, supply_wid, quantity, price)
                WHERE stock.s_i_id = item_stock.item_id
                AND stock.s_w_id = item_stock.supply_wid
                AND stock.s_w_id = ANY(supply_wid_array)
                RETURNING stock.s_dist_10 as s_dist, stock.s_quantity, ( item_stock.quantity + item_stock.price * ( 1 + no_w_tax + no_d_tax ) * ( 1 - no_c_discount ) ) amount
                )
                SELECT array_agg ( s_dist ), array_agg ( s_quantity ), array_agg ( amount )
                FROM stock_update
                INTO stock_dist_array, s_quantity_array, amount_array;
                END IF;

                INSERT INTO order_line (ol_o_id, ol_d_id, ol_w_id, ol_number, ol_i_id, ol_supply_w_id, ol_quantity, ol_amount, ol_dist_info)
                SELECT no_d_next_o_id,
                no_d_id,
                no_w_id,
                data.line_number,
                data.item_id,
                data.supply_wid,
                data.quantity,
                data.amount,
                data.stock_dist
                FROM UNNEST(order_line_array,
                item_id_array,
                supply_wid_array,
                quantity_array,
                amount_array,
                stock_dist_array)
                AS data( line_number, item_id, supply_wid, quantity, amount, stock_dist);

                no_s_quantity := 0;
                FOR loop_counter IN 1 .. no_o_ol_cnt
                LOOP
                no_s_quantity := no_s_quantity + CAST( amount_array[loop_counter] AS NUMERIC);
                END LOOP;

                RETURN no_s_quantity;

                EXCEPTION
                WHEN serialization_failure OR deadlock_detected OR no_data_found
                THEN ROLLBACK;
                END;
                $function$
;

-- DROP FUNCTION public.ostat(int4, int4, int4, int4, varchar);

CREATE OR REPLACE FUNCTION public.ostat(integer, integer, integer, integer, character varying)
 RETURNS SETOF record
 LANGUAGE plpgsql
AS $function$
                DECLARE
                os_w_id		ALIAS FOR $1;
                os_d_id		ALIAS FOR $2;
                os_c_id	 	ALIAS FOR $3;
                byname		ALIAS FOR $4;
                os_c_last	ALIAS FOR $5;
                out_os_c_id	INTEGER;
                out_os_c_last	VARCHAR;
                os_c_first	VARCHAR;
                os_c_middle	VARCHAR;
                os_c_balance	NUMERIC;
                os_o_id		INTEGER;
                os_entdate	TIMESTAMP;
                os_o_carrier_id	INTEGER;
                os_ol 		RECORD;
                namecnt		INTEGER;
                c_name CURSOR FOR
                SELECT c_balance, c_first, c_middle, c_id
                FROM customer
                WHERE c_last = os_c_last AND c_d_id = os_d_id AND c_w_id = os_w_id
                ORDER BY c_first;
                BEGIN
                IF ( byname = 1 )
                THEN
                SELECT count(c_id) INTO namecnt
                FROM customer
                WHERE c_last = os_c_last AND c_d_id = os_d_id AND c_w_id = os_w_id;
                IF ( MOD (namecnt, 2) = 1 )
                THEN
                namecnt := (namecnt + 1);
                END IF;
                OPEN c_name;
                FOR loop_counter IN 0 .. cast((namecnt/2) AS INTEGER)
                LOOP
                FETCH c_name
                INTO os_c_balance, os_c_first, os_c_middle, os_c_id;
                END LOOP;
                close c_name;
                ELSE
                SELECT c_balance, c_first, c_middle, c_last
                INTO os_c_balance, os_c_first, os_c_middle, os_c_last
                FROM customer
                WHERE c_id = os_c_id AND c_d_id = os_d_id AND c_w_id = os_w_id;
                END IF;
                SELECT o_id, o_carrier_id, o_entry_d
                INTO os_o_id, os_o_carrier_id, os_entdate
                FROM
                (SELECT o_id, o_carrier_id, o_entry_d
                FROM orders where o_d_id = os_d_id AND o_w_id = os_w_id and o_c_id=os_c_id
                ORDER BY o_id DESC) AS SUBQUERY
                LIMIT 1;
                FOR os_ol IN
                SELECT ol_i_id, ol_supply_w_id, ol_quantity, ol_amount, ol_delivery_d, out_os_c_id, out_os_c_last, os_c_first, os_c_middle, os_c_balance, os_o_id, os_entdate, os_o_carrier_id
                FROM order_line
                WHERE ol_o_id = os_o_id AND ol_d_id = os_d_id AND ol_w_id = os_w_id
                LOOP
                RETURN NEXT os_ol;
                END LOOP;
                EXCEPTION
                WHEN serialization_failure OR deadlock_detected OR no_data_found
                THEN ROLLBACK;
                END;
                $function$
;

-- DROP FUNCTION public.payment(int4, int4, int4, int4, int4, int4, numeric, varchar, varchar, numeric);

CREATE OR REPLACE FUNCTION public.payment(integer, integer, integer, integer, integer, integer, numeric, character varying, character varying, numeric)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
                DECLARE
                p_w_id			ALIAS FOR $1;
                p_d_id			ALIAS FOR $2;
                p_c_w_id		ALIAS FOR $3;
                p_c_d_id		ALIAS FOR $4;
                p_c_id_in		ALIAS FOR $5;
                byname			ALIAS FOR $6;
                p_h_amount		ALIAS FOR $7;
                p_c_last_in		ALIAS FOR $8;
                p_c_credit_in	ALIAS FOR $9;
                p_c_balance_in	ALIAS FOR $10;
                p_c_balance     NUMERIC(12, 2);
                p_c_credit      CHAR(2);
                p_c_last		VARCHAR(16);
                p_c_id			INTEGER;
                p_w_street_1            VARCHAR(20);
                p_w_street_2            VARCHAR(20);
                p_w_city                VARCHAR(20);
                p_w_state               CHAR(2);
                p_w_zip                 CHAR(9);
                p_d_street_1            VARCHAR(20);
                p_d_street_2            VARCHAR(20);
                p_d_city                VARCHAR(20);
                p_d_state               CHAR(2);
                p_d_zip                 CHAR(9);
                p_c_first               VARCHAR(16);
                p_c_middle              CHAR(2);
                p_c_street_1            VARCHAR(20);
                p_c_street_2            VARCHAR(20);
                p_c_city                VARCHAR(20);
                p_c_state               CHAR(2);
                p_c_zip                 CHAR(9);
                p_c_phone               CHAR(16);
                p_c_since				TIMESTAMP;
                p_c_credit_lim          NUMERIC(12, 2);
                p_c_discount            NUMERIC(4, 4);
                tstamp					TIMESTAMP;
                p_d_name				VARCHAR(11);
                p_w_name				VARCHAR(11);
                p_c_new_data			VARCHAR(500);

                name_count SMALLINT;

                c_byname CURSOR FOR
                SELECT c_first, c_middle, c_id,
                c_street_1, c_street_2, c_city, c_state, c_zip,
                c_phone, c_credit, c_credit_lim,
                c_discount, c_balance, c_since
                FROM customer
                WHERE c_w_id = p_c_w_id AND c_d_id = p_c_d_id AND c_last = p_c_last
                ORDER BY c_first;
                BEGIN
                tstamp := current_timestamp;
                p_c_id := p_c_id_in;
                p_c_balance := p_c_balance_in;
                p_c_last := p_c_last_in;
                p_c_credit := p_c_credit_in;

                UPDATE warehouse
                SET w_ytd = w_ytd + p_h_amount
                WHERE w_id = p_w_id
                RETURNING w_street_1, w_street_2, w_city, w_state, w_zip, w_name
                INTO p_w_street_1, p_w_street_2, p_w_city, p_w_state, p_w_zip, p_w_name;

                UPDATE district
                SET d_ytd = d_ytd + p_h_amount
                WHERE d_w_id = p_w_id AND d_id = p_d_id
                RETURNING d_street_1, d_street_2, d_city, d_state, d_zip, d_name
                INTO p_d_street_1, p_d_street_2, p_d_city, p_d_state, p_d_zip, p_d_name;

                IF ( byname = 1 )
                THEN
                SELECT count(c_last) INTO name_count
                FROM customer
                WHERE c_last = p_c_last AND c_d_id = p_c_d_id AND c_w_id = p_c_w_id;
                OPEN c_byname;
                FOR loop_counter IN 1 .. cast( name_count/2 AS INT)
                LOOP
                FETCH c_byname
                INTO p_c_first, p_c_middle, p_c_id, p_c_street_1, p_c_street_2, p_c_city, p_c_state, p_c_zip, p_c_phone, p_c_credit, p_c_credit_lim, p_c_discount, p_c_balance, p_c_since;
                END LOOP;
                CLOSE c_byname;
                ELSE
                SELECT c_first, c_middle, c_last,
                c_street_1, c_street_2, c_city, c_state, c_zip,
                c_phone, c_credit, c_credit_lim,
                c_discount, c_balance, c_since
                INTO p_c_first, p_c_middle, p_c_last,
                p_c_street_1, p_c_street_2, p_c_city, p_c_state, p_c_zip,
                p_c_phone, p_c_credit, p_c_credit_lim,
                p_c_discount, p_c_balance, p_c_since
                FROM customer
                WHERE c_w_id = p_c_w_id AND c_d_id = p_c_d_id AND c_id = p_c_id;
                END IF;

                IF p_c_credit = 'BC'
                THEN
                UPDATE customer
                SET c_balance = p_c_balance - p_h_amount,
                c_data = substr ((p_c_id || ' ' ||
                p_c_d_id || ' ' ||
                p_c_w_id || ' ' ||
                p_d_id || ' ' ||
                p_w_id || ' ' ||
                to_char (p_h_amount, '9999.99') || ' | ') || c_data, 1, 500)
                WHERE c_w_id = p_c_w_id AND c_d_id = p_c_d_id AND c_id = p_c_id
                RETURNING c_balance, c_data INTO p_c_balance, p_c_new_data;
                ELSE
                UPDATE customer
                SET c_balance = p_c_balance - p_h_amount
                WHERE c_w_id = p_c_w_id AND c_d_id = p_c_d_id AND c_id = p_c_id
                RETURNING c_balance, ' ' INTO p_c_balance, p_c_new_data;
                END IF;

                INSERT INTO history (h_c_d_id, h_c_w_id, h_c_id, h_d_id,h_w_id, h_date, h_amount, h_data)
                VALUES (p_c_d_id, p_c_w_id, p_c_id, p_d_id,	p_w_id, tstamp, p_h_amount, p_w_name || ' ' || p_d_name);

                RETURN p_c_id;

                EXCEPTION
                WHEN serialization_failure OR deadlock_detected OR no_data_found
                THEN ROLLBACK;
                END;
                $function$
;

-- DROP FUNCTION public.slev(int4, int4, int4);

CREATE OR REPLACE FUNCTION public.slev(integer, integer, integer)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
                DECLARE
                st_w_id			ALIAS FOR $1;
                st_d_id			ALIAS FOR $2;
                threshold		ALIAS FOR $3;
                stock_count		INTEGER;
                BEGIN
                SELECT COUNT(DISTINCT (s_i_id)) INTO stock_count
                FROM order_line, stock, district
                WHERE ol_w_id = st_w_id
                AND ol_d_id = st_d_id
                AND d_w_id=st_w_id
                AND d_id=st_d_id
                AND (ol_o_id < d_next_o_id)
                AND ol_o_id >= (d_next_o_id - 20)
                AND s_w_id = st_w_id
                AND s_i_id = ol_i_id
                AND s_quantity < threshold;

                RETURN stock_count;
                EXCEPTION
                WHEN serialization_failure OR deadlock_detected OR no_data_found
                THEN ROLLBACK;
                END;
                $function$
;