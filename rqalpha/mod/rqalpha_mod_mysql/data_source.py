# -*- coding: utf-8 -*-
#
# Copyright 2017 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import six
import tushare as ts
from datetime import date
from dateutil.relativedelta import relativedelta
from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.utils.py2 import lru_cache


class MysqlDayDataSource(BaseDataSource):
    def __init__(self, path):
        super(MysqlDayDataSource, self).__init__(path)

    def getMysqlResult(self, code, index, start, end):
        #return ts.get_k_data(code, index=index, start=start, end=end)
        from .mysqlCache import MysqlCache
        tc = MysqlCache()
        result = tc.getCacheData(code, index, start, end)
        return result
    #@lru_cache(None)
    #@staticmethod
    #@lru_cache(None)
    def get_mysql_k_data(self, instrument, start_dt, end_dt):
        order_book_id = instrument.order_book_id
        code = order_book_id.split(".")[0]

        if instrument.type == 'CS':
            index = False
        elif instrument.type == 'INDX':
            index = True
        else:
            return None
        start = start_dt.strftime('%Y-%m-%d')
        end = end_dt.strftime('%Y-%m-%d')
        tushareData = self.getMysqlResult(code, index, start, end)
        return tushareData  #ts.get_k_data(code, index=index, start=start_dt.strftime('%Y-%m-%d'), end=end_dt.strftime('%Y-%m-%d'))

    def get_bar(self, instrument, dt, frequency):
        if frequency != '1d':
            return super(MysqlDayDataSource, self).get_bar(instrument, dt, frequency)
        #self.get_tushare_k_data( instrument, dt, dt)
        bar_data = self.get_mysql_k_data(instrument, dt, dt)

        if bar_data is None or bar_data.empty:
            return super(MysqlDayDataSource, self).get_bar(instrument, dt, frequency)
        else:
            return bar_data.iloc[0].to_dict()

    def history_bars(self, instrument, bar_count, frequency, fields, dt, skip_suspended=True, include_now=False,
                     adjust_type='pre', adjust_orig=None):
        if frequency != '1d' or not skip_suspended:
            return super(MysqlDayDataSource, self).history_bars(instrument, bar_count, frequency, fields, dt, skip_suspended)

        start_dt_loc = self.get_trading_calendar().get_loc(dt.replace(hour=0, minute=0, second=0, microsecond=0)) - bar_count + 1
        start_dt = self.get_trading_calendar()[start_dt_loc]

        bar_data = self.get_mysql_k_data(instrument, start_dt, dt)

        if bar_data is None or bar_data.empty:
            return super(MysqlDayDataSource, self).get_bar(instrument, dt, frequency)
        else:
            if isinstance(fields, six.string_types):
                fields = [fields]
            fields = [field for field in fields if field in bar_data.columns]

            #return bar_data[fields].as_matrix()
            tt = bar_data[fields].as_matrix()
            matrixdata = bar_data[fields].as_matrix().flatten()
            return bar_data[fields].as_matrix().flatten()

    def available_data_range(self, frequency):
        return date(2005, 1, 1), date.today() - relativedelta(days=1)
