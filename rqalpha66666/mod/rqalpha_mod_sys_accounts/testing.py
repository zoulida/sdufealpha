from rqalpha66666.utils.testing import EnvironmentFixture


class BenchmarkAccountFixture(EnvironmentFixture):
    def __init__(self, *args, **kwargs):
        super(BenchmarkAccountFixture, self).__init__(*args, **kwargs)

        self.benchmark_account_total_cash = 4000
        self.benchmark_account = None

    def init_fixture(self):
        from rqalpha66666.model.base_position import Positions
        from rqalpha66666.mod.rqalpha_mod_sys_accounts.position_model.stock_position import StockPosition
        from rqalpha66666.mod.rqalpha_mod_sys_accounts.account_model import BenchmarkAccount

        super(BenchmarkAccountFixture, self).init_fixture()

        self.benchmark_account = BenchmarkAccount(self.benchmark_account_total_cash,  Positions(StockPosition))
