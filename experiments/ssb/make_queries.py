"""
Generate the SSB query files of this folder (normal/flat x spec/random, plus
empty and profiling). The random files embed parameter tables (e.g. every city
with the other cities of its nation), so they are generated, not written by hand.

usage (from the repository root): python experiments/ssb/make_queries.py [output folder]

Authors: Patrick K. Erdelt
Copyright (C) 2026 Patrick K. Erdelt
SPDX-License-Identifier: AGPL-3.0-or-later
See LICENSE for details.
"""
import datetime
import os
import random
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

# Date literal in the flat queries; checked against PostgreSQL, MonetDB, ClickHouse
DATE = "date '{}'"

#: Regions and nations of dbgen's dists.dss
regions = {
    'AFRICA': ['ALGERIA', 'ETHIOPIA', 'KENYA', 'MOROCCO', 'MOZAMBIQUE'],
    'AMERICA': ['ARGENTINA', 'BRAZIL', 'CANADA', 'PERU', 'UNITED STATES'],
    'ASIA': ['CHINA', 'INDIA', 'INDONESIA', 'JAPAN', 'VIETNAM'],
    'EUROPE': ['FRANCE', 'GERMANY', 'ROMANIA', 'RUSSIA', 'UNITED KINGDOM'],
    'MIDDLE EAST': ['EGYPT', 'IRAN', 'IRAQ', 'JORDAN', 'SAUDI ARABIA'],
}
# dbgen gen_city(): first 9 characters of the nation, blank-padded, plus a digit 0-9
cities = {n: [n[:9].ljust(9) + str(d) for d in range(10)] for ns in regions.values() for n in ns}
assert len(cities) == 25 and sum(len(v) for v in cities.values()) == 250 and len(regions) == 5
REGIONS = sorted(regions)
NATIONS = sorted(cities)
CATEGORIES = [f"{m}{c}" for m in range(1, 6) for c in range(1, 6)]
YEARS_FULL = list(range(1992, 1998))     # 1998 holds orders only until 1998-08-02

# --------------------------------------------------------------------- parameter tables
def p_int(lo, hi, size=1):
    p = {'type': "integer", 'range': [lo, hi]}
    if size > 1:
        p['size'] = size
    return p

def p_list(values):
    return {'type': "list", 'range': values}

def p_dict(d):
    return {'type': "dict", 'range': d}

def iso(d):
    return d.strftime('%Y-%m-%d')

def week_bounds(year, week):
    # dbgen: d_weeknuminyear = d_daynuminyear/7 + 1, so week w holds days 7(w-1) .. 7w-1
    first = datetime.date(year, 1, 1) + datetime.timedelta(days=7 * (week - 1) - 1)
    return first, first + datetime.timedelta(days=6)

P_DISCOUNT = p_int(2, 9)        # lo_discount between D-1 and D+1 (spec, Q1 template)
P_QUANTITY_LT = p_int(24, 25)   # lo_quantity < Q (spec, Q1 template)
P_QUANTITY_RANGE = p_int(1, 41)  # lo_quantity between Q and Q+9 (width as in Q1.2/Q1.3)
P_REGION = p_list(REGIONS)
P_NATION = p_list(NATIONS)
P_CATEGORY = p_list(CATEGORIES)
# first and last brand of 8 consecutive brands within one decade: brands are not
# zero-padded ('MFGR#222' is brand 2), so a range crossing a decade catches a 1-digit brand
P_BRAND_RANGE = p_dict({str(b): [str(b + 7)] for b in (10, 11, 12, 20, 21, 22, 30, 31, 32)})
P_BRAND = p_int(1, 40)
# two distinct cities of the same nation: key = first city, values = the other cities
P_CITY_PAIR = p_dict({c: [o for o in cities[n] if o != c] for n in NATIONS for c in cities[n]})
P_REGION_NATION = p_dict({r: sorted(regions[r]) for r in REGIONS})
P_MFGR_PAIR = p_int(1, 5, size=2)

# normal (date dimension) and flat (lo_orderdate) forms of the date parameters
P_YEAR_Q1 = p_int(1993, 1997)
P_YEAR_Q1_FLAT = p_dict({str(y): [str(y + 1)] for y in range(1993, 1998)})
P_YEARMONTHNUM = p_list([y * 100 + m for y in YEARS_FULL for m in range(1, 13)])
P_MONTH_FLAT = p_dict({iso(datetime.date(y, m, 1)): [iso(datetime.date(y + m // 12, m % 12 + 1, 1))]
                       for y in YEARS_FULL for m in range(1, 13)})
P_YEARMONTH = p_list([datetime.date(y, m, 1).strftime('%b') + str(y) for y in YEARS_FULL for m in range(1, 13)])
# weeks 2..52: week 1 has 6 days, week 53 one or two
P_WEEK = p_dict({str(y): list(range(2, 53)) for y in YEARS_FULL})
P_WEEK_FLAT = p_dict({iso(week_bounds(y, w)[0]): [iso(week_bounds(y, w)[1])] for y in YEARS_FULL for w in range(2, 53)})
P_YEAR_PAIR = p_int(1992, 1997)
P_YEAR_PAIR_FLAT = p_dict({str(y): [str(y + 2)] for y in range(1992, 1998)})

assert week_bounds(1994, 6) == (datetime.date(1994, 2, 4), datetime.date(1994, 2, 10))

# --------------------------------------------------------------------- queries
JOIN_D = "lo_orderdate = d_datekey"
YEAR_FLAT = "cast(extract(year from lo_orderdate) as integer)"
# MySQL has no CAST(... AS INTEGER); its EXTRACT already returns an integer. DBMS-Benchmarker
# picks the variant by dialect or connection name, so MariaDB (dialect MySQL) runs it too.
YEAR_FLAT_DBMS = {'MySQL': "extract(year from lo_orderdate)"}

def flat_range(lo, hi_excl):
    return f"lo_orderdate >= {DATE.format(lo)} and lo_orderdate < {DATE.format(hi_excl)}"

def flat_between(lo, hi):
    return f"lo_orderdate between {DATE.format(lo)} and {DATE.format(hi)}"

# Each entry: title, normal spec, normal random (sql, params), flat spec, flat random (sql, params)
Q = []

def q1(title, normal_where, flat_where, normal_where_r, flat_where_r, params_r, params_rf):
    sel = "select sum(lo_extendedprice*lo_discount) as revenue"
    Q.append({
        'title': title,
        'normal': f"{sel}\nfrom lineorder, dates\nwhere {JOIN_D}\nand {normal_where}",
        'normal_r': (f"{sel}\nfrom lineorder, dates\nwhere {JOIN_D}\nand {normal_where_r}", params_r),
        'flat': f"{sel}\nfrom lineorder_flat\nwhere {flat_where}",
        'flat_r': (f"{sel}\nfrom lineorder_flat\nwhere {flat_where_r}", params_rf),
    })

DISC_R = "lo_discount between {DISCOUNT} - 1 and {DISCOUNT} + 1"
q1("Q1.1: Revenue increase from eliminating discounts in a year (SSB Q1.1)",
   "d_year = 1993\nand lo_discount between 1 and 3\nand lo_quantity < 25",
   f"{flat_range('1993-01-01', '1994-01-01')}\nand lo_discount between 1 and 3\nand lo_quantity < 25",
   f"d_year = {{YEAR}}\nand {DISC_R}\nand lo_quantity < {{QUANTITY}}",
   f"{flat_range('{YEAR1}-01-01', '{YEAR2}-01-01')}\nand {DISC_R}\nand lo_quantity < {{QUANTITY}}",
   {'YEAR': P_YEAR_Q1, 'DISCOUNT': P_DISCOUNT, 'QUANTITY': P_QUANTITY_LT},
   {'YEAR': P_YEAR_Q1_FLAT, 'DISCOUNT': P_DISCOUNT, 'QUANTITY': P_QUANTITY_LT})
QTY_R = "lo_quantity between {QUANTITY} and {QUANTITY} + 9"
q1("Q1.2: Revenue increase from eliminating discounts in a month (SSB Q1.2)",
   "d_yearmonthnum = 199401\nand lo_discount between 4 and 6\nand lo_quantity between 26 and 35",
   f"{flat_range('1994-01-01', '1994-02-01')}\nand lo_discount between 4 and 6\nand lo_quantity between 26 and 35",
   f"d_yearmonthnum = {{YEARMONTHNUM}}\nand {DISC_R}\nand {QTY_R}",
   f"{flat_range('{MONTH1}', '{MONTH2}')}\nand {DISC_R}\nand {QTY_R}",
   {'YEARMONTHNUM': P_YEARMONTHNUM, 'DISCOUNT': P_DISCOUNT, 'QUANTITY': P_QUANTITY_RANGE},
   {'MONTH': P_MONTH_FLAT, 'DISCOUNT': P_DISCOUNT, 'QUANTITY': P_QUANTITY_RANGE})
q1("Q1.3: Revenue increase from eliminating discounts in a week (SSB Q1.3)",
   "d_weeknuminyear = 6\nand d_year = 1994\nand lo_discount between 5 and 7\nand lo_quantity between 26 and 35",
   f"{flat_between('1994-02-04', '1994-02-10')}\nand lo_discount between 5 and 7\nand lo_quantity between 26 and 35",
   f"d_weeknuminyear = {{WEEK2}}\nand d_year = {{WEEK1}}\nand {DISC_R}\nand {QTY_R}",
   f"{flat_between('{WEEK1}', '{WEEK2}')}\nand {DISC_R}\nand {QTY_R}",
   {'WEEK': P_WEEK, 'DISCOUNT': P_DISCOUNT, 'QUANTITY': P_QUANTITY_RANGE},
   {'WEEK': P_WEEK_FLAT, 'DISCOUNT': P_DISCOUNT, 'QUANTITY': P_QUANTITY_RANGE})

def q2(title, part_where, region, part_where_r, params_r):
    sel_n = "select sum(lo_revenue) as revenue, d_year, p_brand1"
    sel_f = f"select sum(lo_revenue) as revenue, {YEAR_FLAT} as d_year, p_brand1"
    from_n = "from lineorder, dates, part, supplier\nwhere lo_orderdate = d_datekey\nand lo_partkey = p_partkey\nand lo_suppkey = s_suppkey"
    tail_n = "group by d_year, p_brand1\norder by d_year, p_brand1"
    tail_f = f"group by {YEAR_FLAT}, p_brand1\norder by d_year, p_brand1"
    Q.append({
        'title': title,
        'normal': f"{sel_n}\n{from_n}\nand {part_where}\nand s_region = '{region}'\n{tail_n}",
        'normal_r': (f"{sel_n}\n{from_n}\nand {part_where_r}\nand s_region = '{{REGION}}'\n{tail_n}", params_r),
        'flat': f"{sel_f}\nfrom lineorder_flat\nwhere {part_where}\nand s_region = '{region}'\n{tail_f}",
        'flat_r': (f"{sel_f}\nfrom lineorder_flat\nwhere {part_where_r}\nand s_region = '{{REGION}}'\n{tail_f}", params_r),
    })

q2("Q2.1: Revenue by year and brand for a product category and supplier region (SSB Q2.1)",
   "p_category = 'MFGR#12'", "AMERICA", "p_category = 'MFGR#{CATEGORY}'",
   {'CATEGORY': P_CATEGORY, 'REGION': P_REGION})
q2("Q2.2: Revenue by year and brand for a brand range and supplier region (SSB Q2.2)",
   "p_brand1 between 'MFGR#2221' and 'MFGR#2228'", "ASIA",
   "p_brand1 between 'MFGR#{CATEGORY}{BRAND1}' and 'MFGR#{CATEGORY}{BRAND2}'",
   {'CATEGORY': P_CATEGORY, 'BRAND': P_BRAND_RANGE, 'REGION': P_REGION})
q2("Q2.3: Revenue by year for one brand and supplier region (SSB Q2.3)",
   "p_brand1 = 'MFGR#2239'", "EUROPE", "p_brand1 = 'MFGR#{CATEGORY}{BRAND}'",
   {'CATEGORY': P_CATEGORY, 'BRAND': P_BRAND, 'REGION': P_REGION})

def q3(title, cols, where, years, where_r, params_r, flat_dates_r=None, flat_params_r=None):
    # years: (normal predicate, flat predicate) on the date
    c1, c2 = cols
    sel_n = f"select {c1}, {c2}, d_year, sum(lo_revenue) as revenue"
    sel_f = f"select {c1}, {c2}, {YEAR_FLAT} as d_year, sum(lo_revenue) as revenue"
    from_n = "from customer, lineorder, supplier, dates\nwhere lo_custkey = c_custkey\nand lo_suppkey = s_suppkey\nand lo_orderdate = d_datekey"
    tail_n = f"group by {c1}, {c2}, d_year\norder by d_year asc, revenue desc"
    tail_f = f"group by {c1}, {c2}, {YEAR_FLAT}\norder by d_year asc, revenue desc"
    years_n, years_f = years
    years_n_r, years_f_r = (years if flat_dates_r is None else flat_dates_r)
    Q.append({
        'title': title,
        'normal': f"{sel_n}\n{from_n}\nand {where}\nand {years_n}\n{tail_n}",
        'normal_r': (f"{sel_n}\n{from_n}\nand {where_r}\nand {years_n_r}\n{tail_n}", params_r),
        'flat': f"{sel_f}\nfrom lineorder_flat\nwhere {where}\nand {years_f}\n{tail_f}",
        'flat_r': (f"{sel_f}\nfrom lineorder_flat\nwhere {where_r}\nand {years_f_r}\n{tail_f}",
                   params_r if flat_params_r is None else flat_params_r),
    })

YEARS_9297 = ("d_year >= 1992 and d_year <= 1997", flat_range('1992-01-01', '1998-01-01'))
q3("Q3.1: Revenue by customer and supplier nation and year within a region (SSB Q3.1)",
   ("c_nation", "s_nation"), "c_region = 'ASIA'\nand s_region = 'ASIA'", YEARS_9297,
   "c_region = '{REGION}'\nand s_region = '{REGION}'", {'REGION': P_REGION})
q3("Q3.2: Revenue by customer and supplier city and year within a nation (SSB Q3.2)",
   ("c_city", "s_city"), "c_nation = 'UNITED STATES'\nand s_nation = 'UNITED STATES'", YEARS_9297,
   "c_nation = '{NATION}'\nand s_nation = '{NATION}'", {'NATION': P_NATION})
CITIES_SPEC = "(c_city = 'UNITED KI1' or c_city = 'UNITED KI5')\nand (s_city = 'UNITED KI1' or s_city = 'UNITED KI5')"
CITIES_R = "(c_city = '{CITY1}' or c_city = '{CITY2}')\nand (s_city = '{CITY1}' or s_city = '{CITY2}')"
q3("Q3.3: Revenue by customer and supplier city and year for two cities (SSB Q3.3)",
   ("c_city", "s_city"), CITIES_SPEC, YEARS_9297, CITIES_R, {'CITY': P_CITY_PAIR})
q3("Q3.4: Revenue by customer and supplier city for two cities in one month (SSB Q3.4)",
   ("c_city", "s_city"), CITIES_SPEC,
   ("d_yearmonth = 'Dec1997'", flat_range('1997-12-01', '1998-01-01')),
   CITIES_R, {'CITY': P_CITY_PAIR, 'YEARMONTH': P_YEARMONTH},
   flat_dates_r=("d_yearmonth = '{YEARMONTH}'", flat_range('{MONTH1}', '{MONTH2}')),
   flat_params_r={'CITY': P_CITY_PAIR, 'MONTH': P_MONTH_FLAT})

def q4(title, cols, where, where_r, params_r, years=None, years_r=None, flat_params_r=None):
    profit = "sum(lo_revenue - lo_supplycost) as profit"
    sel_n = "select d_year, " + ", ".join(cols) + f", {profit}"
    sel_f = f"select {YEAR_FLAT} as d_year, " + ", ".join(cols) + f", {profit}"
    from_n = ("from dates, customer, supplier, part, lineorder\nwhere lo_custkey = c_custkey\n"
              "and lo_suppkey = s_suppkey\nand lo_partkey = p_partkey\nand lo_orderdate = d_datekey")
    g = ", ".join(cols)
    tail_n = f"group by d_year, {g}\norder by d_year, {g}"
    tail_f = f"group by {YEAR_FLAT}, {g}\norder by d_year, {g}"
    yn, yf = years if years else ("", "")
    yn_r, yf_r = years_r if years_r else ("", "")
    add = lambda s: f"\nand {s}" if s else ""
    Q.append({
        'title': title,
        'normal': f"{sel_n}\n{from_n}\nand {where}{add(yn)}\n{tail_n}",
        'normal_r': (f"{sel_n}\n{from_n}\nand {where_r}{add(yn_r)}\n{tail_n}", params_r),
        'flat': f"{sel_f}\nfrom lineorder_flat\nwhere {where}{add(yf)}\n{tail_f}",
        'flat_r': (f"{sel_f}\nfrom lineorder_flat\nwhere {where_r}{add(yf_r)}\n{tail_f}",
                   params_r if flat_params_r is None else flat_params_r),
    })

MFGR_SPEC = "(p_mfgr = 'MFGR#1' or p_mfgr = 'MFGR#2')"
MFGR_R = "(p_mfgr = 'MFGR#{MFGR1}' or p_mfgr = 'MFGR#{MFGR2}')"
YEARS_9798 = ("(d_year = 1997 or d_year = 1998)", flat_range('1997-01-01', '1999-01-01'))
YEARS_R = ("(d_year = {YEAR} or d_year = {YEAR} + 1)", flat_range('{YEAR1}-01-01', '{YEAR2}-01-01'))
q4("Q4.1: Profit by year and customer nation for a region and two manufacturers (SSB Q4.1)",
   ["c_nation"], f"c_region = 'AMERICA'\nand s_region = 'AMERICA'\nand {MFGR_SPEC}",
   f"c_region = '{{REGION}}'\nand s_region = '{{REGION}}'\nand {MFGR_R}",
   {'REGION': P_REGION, 'MFGR': P_MFGR_PAIR})
q4("Q4.2: Profit by year, supplier nation and category for two years (SSB Q4.2)",
   ["s_nation", "p_category"], f"c_region = 'AMERICA'\nand s_region = 'AMERICA'\nand {MFGR_SPEC}",
   f"c_region = '{{REGION}}'\nand s_region = '{{REGION}}'\nand {MFGR_R}",
   {'REGION': P_REGION, 'MFGR': P_MFGR_PAIR, 'YEAR': P_YEAR_PAIR}, YEARS_9798, YEARS_R,
   {'REGION': P_REGION, 'MFGR': P_MFGR_PAIR, 'YEAR': P_YEAR_PAIR_FLAT})
q4("Q4.3: Profit by year, supplier city and brand for a nation and category (SSB Q4.3)",
   ["s_city", "p_brand1"], "c_region = 'AMERICA'\nand s_nation = 'UNITED STATES'\nand p_category = 'MFGR#14'",
   "c_region = '{NATION1}'\nand s_nation = '{NATION2}'\nand p_category = 'MFGR#{CATEGORY}'",
   {'NATION': P_REGION_NATION, 'CATEGORY': P_CATEGORY, 'YEAR': P_YEAR_PAIR}, YEARS_9798, YEARS_R,
   {'NATION': P_REGION_NATION, 'CATEGORY': P_CATEGORY, 'YEAR': P_YEAR_PAIR_FLAT})
assert len(Q) == 13

# --------------------------------------------------------------------- writing
rng = random.Random(348)
STREAMS = {}
for s in range(1, 41):
    order = list(range(1, 14))
    rng.shuffle(order)
    STREAMS[s] = order

TIMER = """			'active': True,
			'numWarmup': 0,
			'numCooldown': 0,
			'numRun': 1,
			'timer':
			{
				'datatransfer':
				{
					'active': True,
					'sorted': True,
					'compare': 'result',
					'store': [],
					'precision': 0,
				},
				'connection':
				{
					'active': True,
				}
			}
"""

def header(name, intro, streams=True):
    s = "{\n"
    s += f"\t'name': {name!r},\n"
    s += f"\t'intro': {intro!r},\n"
    s += "\t'factor': 'mean',\n"
    s += "\t'connectionmanagement': {\n\t\t'timeout': 1200,\n\t\t'numProcesses': 1,\n\t\t'runsPerConnection': 0,\n\t\t'singleConnection': True\n\t},\n"
    if streams:
        s += f"\t'stream_ordering': {STREAMS!r},\n"
    s += "\t'queries':\n\t[\n"
    return s

def entry(title, sql, params=None):
    assert '"""' not in sql
    s = "\t\t{\n"
    s += f"\t\t\t'title': {title!r},\n"
    s += f'\t\t\t\'query\': """{sql}""",\n'
    if YEAR_FLAT in sql:
        # DBMS-specific variants (YEAR_FLAT_DBMS)
        s += "\t\t\t'DBMS': {\n"
        for dbms, year in YEAR_FLAT_DBMS.items():
            s += f'\t\t\t\t{dbms!r}: """{sql.replace(YEAR_FLAT, year)}""",\n'
        s += "\t\t\t},\n"
    if params:
        s += "\t\t\t'parameter': {\n"
        for k, v in params.items():
            s += f"\t\t\t\t{k!r}: {v!r},\n"
        s += "\t\t\t},\n"
    s += TIMER
    s += "\t\t},\n"
    return s

def write(filename, name, intro, key, randomized):
    s = header(name, intro)
    for q in Q:
        if randomized:
            sql, params = q[key]
            if '{' not in sql:
                params = None
            s += entry(q['title'], sql, params)
        else:
            assert '{' not in q[key], q['title']
            s += entry(q['title'], q[key])
    s += "\t]\n}\n"
    with open(f"{OUT}/{filename}", 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)

SPEC_INTRO = ("This includes the 13 queries of the Star Schema Benchmark (O'Neil et al., revision 3, 2009) "
              "with the constants of the specification (Q2.3: brand 'MFGR#2239', as used by ClickHouse and Doris; "
              "the specification's text and SQL disagree there).")
RANDOM_INTRO = ("This includes the 13 queries of the Star Schema Benchmark as templates with random parameters "
                "(generalization after Rabl et al., ICPE 2013): every predicate picks a random member of its "
                "hierarchy level or moves its range, so each query keeps the filter factor of the specification.")
FLAT_NOTE = " The queries read the denormalized table lineorder_flat; year, month and week come from lo_orderdate."
write('queries-ssb.config', "The SSB Queries", SPEC_INTRO, 'normal', False)
write('queries-ssb-random.config', "The SSB Queries (random parameters)", RANDOM_INTRO, 'normal_r', True)
write('queries-ssb-flat.config', "The SSB Queries (flat)", SPEC_INTRO + FLAT_NOTE, 'flat', False)
write('queries-ssb-flat-random.config', "The SSB Queries (flat, random parameters)", RANDOM_INTRO + FLAT_NOTE, 'flat_r', True)

# empty: one dummy query
s = header("The SSB Dummy Queries", "This only includes a dummy query.", streams=False)
s += entry("Select constant 1 (Q1)", "select 1")
s += "\t]\n}\n"
open(f"{OUT}/queries-ssb-empty.config", 'w', encoding='utf-8', newline='\n').write(s)

# profiling: row count, distinct keys, min/max of the key and date columns per table,
# one file per schema variant (a query on a table of the other variant would fail)
LO_COLUMNS = ['lo_orderkey', 'lo_custkey', 'lo_partkey', 'lo_suppkey', 'lo_orderdate', 'lo_commitdate']
PROFILES = {
    'queries-ssb-profiling.config': ("Data Profiling SSB", [
        ('customer', ['c_custkey']), ('supplier', ['s_suppkey']), ('part', ['p_partkey']),
        ('dates', ['d_datekey']), ('lineorder', LO_COLUMNS)]),
    'queries-ssb-flat-profiling.config': ("Data Profiling SSB (flat)", [('lineorder_flat', LO_COLUMNS)]),
}
for filename, (name, profile) in PROFILES.items():
    s = header(name, "Row count, count distinct, minimum and maximum of the key and date columns of each table.",
               streams=False)
    for table, cols in profile:
        for c in cols:
            s += entry(f"stats about {table}.{c}",
                       f"select count(*) as co, count(distinct {c}) as di, min({c}) as mi, max({c}) as ma from {table}")
    s += "\t]\n}\n"
    open(f"{OUT}/{filename}", 'w', encoding='utf-8', newline='\n').write(s)
print("written to", OUT)
