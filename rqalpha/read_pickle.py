__author__ = 'zoulida'
import pandas as pd

result_dict = pd.read_pickle('result.pkl')

result_dict.keys()
print(result_dict)
# [out]dict_keys(['total_portfolios', 'summary', 'benchmark_portfolios', 'benchmark_positions', 'stock_positions', 'trades', 'stock_portfolios'])
