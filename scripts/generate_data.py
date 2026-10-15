"""Generate deterministic fictitious sales transactions for the portfolio demo."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
random.seed(2026)
segments = ['PME', 'Grand compte', 'Particulier']
regions = ['Île-de-France', 'Auvergne-Rhône-Alpes', 'Occitanie', 'Nouvelle-Aquitaine', 'PACA', 'Hauts-de-France']
products = [('Logiciel CRM', 'Logiciels', 89), ('Abonnement BI', 'Logiciels', 149), ('Audit data', 'Conseil', 690), ('Formation Excel', 'Formation', 220), ('Automatisation', 'Conseil', 450), ('Formation Power BI', 'Formation', 320)]
channels = ['Web', 'Partenaire', 'Commercial direct']
start = date(2024, 1, 1)
end = date(2025, 12, 31)
with (ROOT / 'data/raw/ventes_brutes.csv').open('w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['order_id','order_date','customer_id','segment','region','channel','product','category','quantity','unit_price_eur','discount_pct','status'])
    for i in range(1, 2401):
        day = start + timedelta(days=random.randrange((end - start).days + 1))
        p, cat, price = random.choice(products)
        qty = random.choices([1,2,3,4,5], weights=[40,30,17,9,4])[0]
        price = round(price * random.uniform(.88, 1.13), 2)
        discount = random.choice([0,0,0,5,10,15,20])
        status = random.choices(['Completed','Cancelled','Refunded'],weights=[91,6,3])[0]
        writer.writerow([f'CMD-{i:05}',day.isoformat(),f'CL-{random.randint(1,480):04}',random.choice(segments),random.choice(regions),random.choice(channels),p,cat,qty,f'{price:.2f}',discount,status])
print('Generated 2400 fictitious orders')
