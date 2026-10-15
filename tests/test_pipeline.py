import csv
import sqlite3
import tempfile
import unittest
from pathlib import Path
from scripts.prepare_data import clean

class PipelineTest(unittest.TestCase):
    def test_cleaning_and_revenue(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            raw, clean_csv, db = [base / x for x in ('raw.csv','clean.csv','test.db')]
            with raw.open('w',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['order_id','order_date','customer_id','segment','region','channel','product','category','quantity','unit_price_eur','discount_pct','status'])
                writer.writerow(['1','2025-01-02','A','PME','Paris','Web','Product','Software',2,100,10,'Completed'])
                writer.writerow(['2','2025-01-03','A','PME','Paris','Web','Product','Software',2,100,10,'Cancelled'])
                writer.writerow(['2','2025-01-03','A','PME','Paris','Web','Product','Software',2,100,10,'Cancelled'])
            self.assertEqual(clean(raw,clean_csv,db),(2,1))
            with sqlite3.connect(db) as conn:
                self.assertEqual(conn.execute('SELECT SUM(revenue_eur) FROM sales').fetchone()[0],180)

if __name__ == '__main__': unittest.main()
