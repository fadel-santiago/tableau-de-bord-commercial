"""Validate orders, clean records, derive revenue, write analytics-ready CSV and SQLite."""
import csv
import sqlite3
import sys
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/raw/ventes_brutes.csv'
TARGET = ROOT / 'data/processed/ventes_nettoyees.csv'
DATABASE = ROOT / 'data/processed/commercial.sqlite'
FIELDS = ['order_id','order_date','year','month','customer_id','segment','region','channel','product','category','quantity','unit_price_eur','discount_pct','status','revenue_eur']

def clean(source=SOURCE, target=TARGET, database=DATABASE):
    records, rejects, seen = [], [], set()
    with Path(source).open(newline='', encoding='utf-8-sig') as f:
        for row_number, row in enumerate(csv.DictReader(f), start=2):
            try:
                order_id = row['order_id'].strip()
                if not order_id or order_id in seen:
                    raise ValueError('empty or duplicate order_id')
                order_date = date.fromisoformat(row['order_date'].strip())
                qty = int(row['quantity'])
                price = Decimal(row['unit_price_eur'])
                discount = Decimal(row['discount_pct'])
                if qty <= 0 or price < 0 or not 0 <= discount <= 100:
                    raise ValueError('out-of-range numeric field')
                if row['status'] not in ('Completed','Cancelled','Refunded'):
                    raise ValueError('invalid status')
                required = ('customer_id','segment','region','channel','product','category')
                if any(not row[k].strip() for k in required):
                    raise ValueError('missing mandatory field')
                revenue = (price * qty * (Decimal('1') - discount / 100)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP) if row['status'] == 'Completed' else Decimal('0.00')
                record = {'order_id':order_id,'order_date':order_date.isoformat(),'year':order_date.year,'month':order_date.strftime('%Y-%m'),'customer_id':row['customer_id'].strip(),'segment':row['segment'].strip(),'region':row['region'].strip(),'channel':row['channel'].strip(),'product':row['product'].strip(),'category':row['category'].strip(),'quantity':qty,'unit_price_eur':f'{price:.2f}','discount_pct':str(discount),'status':row['status'],'revenue_eur':f'{revenue:.2f}'}
                records.append(record)
                seen.add(order_id)
            except (KeyError, ValueError, InvalidOperation) as e:
                rejects.append((row_number, str(e)))
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    with Path(target).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)
    with sqlite3.connect(database) as conn:
        conn.execute('DROP TABLE IF EXISTS sales')
        conn.execute('''CREATE TABLE sales (order_id TEXT PRIMARY KEY, order_date TEXT NOT NULL, year INTEGER, month TEXT, customer_id TEXT, segment TEXT, region TEXT, channel TEXT, product TEXT, category TEXT, quantity INTEGER, unit_price_eur REAL, discount_pct REAL, status TEXT, revenue_eur REAL)''')
        conn.executemany('INSERT INTO sales VALUES (' + ','.join(['?']*len(FIELDS)) + ')', [tuple(r[k] for k in FIELDS) for r in records])
        conn.execute('CREATE INDEX idx_sales_month ON sales(month)')
        conn.execute('CREATE INDEX idx_sales_region ON sales(region)')
    print(f'Cleaned {len(records)} orders. Rejected {len(rejects)}. DB: {database}')
    for n, e in rejects[:10]: print(f'  row {n}: {e}', file=sys.stderr)
    return len(records), len(rejects)

if __name__ == '__main__': clean()
