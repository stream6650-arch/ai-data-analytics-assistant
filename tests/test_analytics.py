import unittest
import pandas as pd
from src.analytics import aggregate, route_question
from src.generate_sales import generate_sales


class AnalyticsTests(unittest.TestCase):
    def test_generation(self):
        data = generate_sales()
        self.assertEqual(len(data), 1800)
        pd.testing.assert_frame_equal(data, generate_sales())
        self.assertTrue((data.revenue == data.quantity * data.unit_price).all())
        self.assertTrue((data.gross_profit == data.revenue - data.cost).all())
        self.assertEqual(data.date.dt.year.unique().tolist(), [2025])

    def test_known_totals(self):
        data = pd.DataFrame({'product': ['A', 'B', 'A'], 'revenue': [10, 50, 20]})
        result = aggregate(data, 'revenue', 'product')
        self.assertEqual(result.to_dict('records'), [{'product': 'B', 'revenue': 50}, {'product': 'A', 'revenue': 30}])
        with self.assertRaises(ValueError):
            aggregate(data, 'unknown', 'product')

    def test_routing(self):
        cases = {'哪個產品營收最高？': ('revenue', 'product'),
                 'Show revenue by region': ('revenue', 'region'),
                 'Show monthly sales trend': ('revenue', 'month'),
                 'Which product has the highest gross profit?': ('gross_profit', 'product'),
                 '每月成本': ('cost', 'month')}
        for question, expected in cases.items():
            self.assertEqual(route_question(question), expected)
        for question in ['', 'hello', '預測明年產品營收', 'customer revenue']:
            self.assertIsNone(route_question(question))

    def test_filters_and_month_order(self):
        data = generate_sales()
        filtered = data[(data['product'] == 'Laptop') & (data.date.dt.month <= 3)]
        result = aggregate(filtered, 'revenue', 'month')
        self.assertEqual(result.month.tolist(), ['2025-01', '2025-02', '2025-03'])
        self.assertEqual(result.revenue.sum(), filtered.revenue.sum())


if __name__ == '__main__':
    unittest.main()
