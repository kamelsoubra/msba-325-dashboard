"""Aggregate the source CSV using Python's standard library only."""
import csv
import json
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    groups = defaultdict(lambda: [Decimal('0'), 0])
    ids = set()
    with (ROOT / 'data' / 'Coffee Shop Sales.csv').open(encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            date = datetime.strptime(row['transaction_date'], '%m/%d/%y')
            hour = int(row['transaction_time'].split(':')[0])
            assert date.year == 2023 and 1 <= date.month <= 6
            assert 6 <= hour <= 20
            assert row['transaction_id'] not in ids, 'Duplicate transaction ID'
            ids.add(row['transaction_id'])
            key = (date.month, row['store_location'], row['product_category'], hour)
            groups[key][0] += Decimal(row['transaction_qty']) * Decimal(row['unit_price'])
            groups[key][1] += 1
    total = sum((v[0] for v in groups.values()), Decimal('0'))
    print(f'Total revenue: ${total:,.2f}')
    assert total == Decimal('698812.33'), f'Unexpected revenue: {total}'
    assert len(ids) == 149116, f'Unexpected transaction count: {len(ids)}'
    assert len(groups) == 2156, f'Unexpected aggregate count: {len(groups)}'
    rows = [dict(m=m, store_location=s, product_category=c, h=h,
                 r=float(r.quantize(Decimal('0.01'))), t=t)
            for (m, s, c, h), (r, t) in sorted(groups.items())]
    (ROOT / 'public').mkdir(exist_ok=True)
    (ROOT / 'public' / 'agg.json').write_text(json.dumps(rows, separators=(',', ':')), encoding='utf-8')
    print(f'{len(ids):,} transactions; {len(rows):,} aggregate rows written to public/agg.json')

if __name__ == '__main__':
    main()
