"""Generate reproducible demo data; optionally export it as a CSV."""
from pathlib import Path
import numpy as np
import pandas as pd


def generate_sales(rows=1800, seed=7):
    rng = np.random.default_rng(seed)
    products = np.array(['Laptop', 'Monitor', 'Headset', 'Keyboard'])
    index = rng.integers(0, len(products), rows)
    frame = pd.DataFrame({
        'date': pd.Timestamp('2025-01-01') + pd.to_timedelta(rng.integers(0, 365, rows), unit='D'),
        'product': products[index],
        'region': rng.choice(['North', 'South', 'East', 'West'], rows),
        'quantity': rng.integers(1, 6, rows),
        'unit_price': np.array([1200, 350, 120, 80])[index],
        'unit_cost': np.array([850, 230, 65, 40])[index],
    })
    frame['revenue'] = frame.quantity * frame.unit_price
    frame['cost'] = frame.quantity * frame.unit_cost
    frame['gross_profit'] = frame.revenue - frame.cost
    frame['month'] = frame.date.dt.strftime('%Y-%m')
    return frame.sort_values('date').reset_index(drop=True)


if __name__ == '__main__':
    path = Path(__file__).resolve().parents[1] / 'data' / 'sales.csv'
    path.parent.mkdir(exist_ok=True)
    generate_sales().to_csv(path, index=False)
    print(f'Wrote {path}')
