__author__ = 'zoulida'
from rqalpha import run
config = {
    "base": {
        "strategy_file": "examples/golden_cross.py",#""./examples/buy_and_hold.py",
        "start_date": "2016-01-01",
        "end_date": "2016-12-31",
        "frequency": "1d",
        "accounts": {
            "stock": 100000
        },
        "benchmark":"000300.XSHG"
    },
    "mod": {
        "sys_analyser": {
            "enabled": True,
            "plot": True
        }
    }
}
run(config)