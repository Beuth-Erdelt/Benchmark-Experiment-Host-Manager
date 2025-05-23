ALTER TABLE "TPCH"."CUSTOMER"
  ADD CONSTRAINT FK_CUSTOMER_REFERENCE_NATION FOREIGN KEY(C_NATIONKEY)
      REFERENCES "TPCH"."NATION" (N_NATIONKEY)
      ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE "TPCH"."LINEITEM"
    ADD CONSTRAINT FK_LINEITEM_REFERENCE_ORDERS FOREIGN KEY(L_ORDERKEY)
      REFERENCES "TPCH"."ORDERS" (O_ORDERKEY)
      ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE "TPCH"."LINEITEM"
    ADD CONSTRAINT FK_LINEITEM_REFERENCE_PART FOREIGN KEY(L_PARTKEY)
      REFERENCES "TPCH"."PART" (P_PARTKEY)
      ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE "TPCH"."LINEITEM"
    ADD CONSTRAINT FK_LINEITEM_REFERENCE_SUPPLIER FOREIGN KEY  (L_SUPPKEY)
      REFERENCES "TPCH"."SUPPLIER" (S_SUPPKEY)
      ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE "TPCH"."NATION"
    ADD CONSTRAINT FK_NATION_REFERENCE_REGION FOREIGN KEY (N_REGIONKEY)
    REFERENCES "TPCH"."REGION" (R_REGIONKEY)
    ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE "TPCH"."ORDERS"
    ADD CONSTRAINT FK_ORDERS_REFERENCE_CUSTOMER FOREIGN KEY  (O_CUSTKEY)
      REFERENCES "TPCH"."CUSTOMER" (C_CUSTKEY)
      ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE "TPCH"."PARTSUPP"
    ADD CONSTRAINT FK_PARTSUPP_REFERENCE_PART FOREIGN KEY  (PS_PARTKEY)
      REFERENCES "TPCH"."PART" (P_PARTKEY)
      ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE "TPCH"."PARTSUPP"
    ADD CONSTRAINT FK_PARTSUPP_REFERENCE_SUPPLIER FOREIGN KEY  (PS_SUPPKEY)
      REFERENCES "TPCH"."SUPPLIER" (S_SUPPKEY)
      ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE "TPCH"."SUPPLIER"
    ADD CONSTRAINT FK_SUPPLIER_REFERENCE_NATION FOREIGN KEY  (S_NATIONKEY)
      REFERENCES "TPCH"."NATION" (N_NATIONKEY)
      ON DELETE RESTRICT ON UPDATE RESTRICT;
