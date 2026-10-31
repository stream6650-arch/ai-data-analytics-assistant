"""Allowlisted metrics and deterministic bilingual question routing."""
import re

METRICS = {'revenue': '營收', 'cost': '成本', 'gross_profit': '毛利'}
DIMENSIONS = {'product': '產品', 'region': '地區', 'month': '月份'}


def route_question(question):
    text = question.strip().lower()
    if not text:
        return None
    # Reject unsupported dimensions/metrics instead of inventing an answer.
    if re.search(r'客戶|顧客|預測|明年|庫存|淨利|customer|forecast|predict|inventory|net profit', text):
        return None
    metric = ('gross_profit' if re.search(r'毛利|gross profit|profitability', text)
              else 'cost' if re.search(r'成本|cost', text)
              else 'revenue' if re.search(r'營收|銷售|營業額|收入|revenue|sales', text)
              else None)
    dimension = ('month' if re.search(r'月|趨勢|month|trend', text)
                 else 'region' if re.search(r'地區|區域|region', text)
                 else 'product' if re.search(r'產品|商品|product', text)
                 else None)
    return (metric, dimension) if metric and dimension else None


def aggregate(frame, metric, dimension):
    if metric not in METRICS or dimension not in DIMENSIONS:
        raise ValueError('Unsupported metric or dimension')
    result = frame.groupby(dimension, as_index=False)[metric].sum()
    return result.sort_values(dimension if dimension == 'month' else metric,
                              ascending=dimension == 'month').reset_index(drop=True)
