__author__ = 'zoulida'
import bcolz

data = bcolz.open(rootdir="/root/.rqalpha/bundle/stocks.bcolz", mode="a" )
save = data.todataframe()
save.to_csv('stockszld.csv')