__author__ = 'zoulida'
import pymysql
import pandas as pd
from DBUtils.PooledDB import PooledDB


# 数据库名称和密码
name = 'root'
password = 'root'  # 替换为自己的账户名和密码
pool = PooledDB(pymysql, 5, host='202.194.246.167' ,user = name, passwd = password, db = 'stockDataBase', port = 3306) #5为连接池里的最少连接数

def queryMySQL_plot_stock_market(code1, startdate = '2017-12-09', enddate = '2018-12-09'):#不使用连接池
    ###########################查询刚才操作的成果##################################

    # 重新建立数据库连接
    db = pymysql.connect('localhost', name, password, 'stockDataBase')
    cursor = db.cursor()
    # 查询数据库并打印内容
    #cursor.execute('select * from stock_600016 where timestamp = 977155200')
    #str = 'select * from stock_600016 where 日期 between %s' % startdata + 'and %s' % enddata
    #print(str)
    code = 'stock_'+code1
    #print(code)
    cursor.execute('select * from %s where 日期 between \'%s\'' % (code , startdate) + ' and \'%s\'' % enddate)
    #cursor.execute('select * from stock_600016 where 收盘价 = 18.56')
    results = cursor.fetchall()
    df = pd.DataFrame(list(results))
    #df2 = df.rename(columns={'0': 'timestamp', '1': 'data', '4': 'close', '5': 'price', '6': 'e'} , inplace=True)
    df.rename(columns={1:'date', 4: 'close', 5:'high', 6:'low', 7:'open'} , inplace=True)
    #df2 = df.set_index(['date'])
    #print(df)
    #print(df.columns.values.tolist())
    #print(df2)
    #for row in results:
    #    print(row)
    # 关闭
    cursor.close()
    db.commit()
    db.close()
    return df

def queryMySQL_getLast(code1):#使用连接池
    '''import datetime
    now = datetime.now()
    before = datetime.timedelta(days=-100)'''
    try:
        # 调用连接池
        conn = pool.connection()
        cur = conn.cursor()
        code = 'stock_'+code1
        #sql = 'select * from %s where 日期 between \'%s\'' % (code , startdate) + ' and \'%s\'' % enddate
        sql = 'SELECT * FROM %s where 日期 in(select max(日期) from %s)' % (code, code)
        #print(sql)
        cur.execute(sql)
        results = cur.fetchall()
        df = pd.DataFrame(list(results))
        df.rename(columns={0:'Stamp', 1:'Date',2:'Code', 3:'Name', 4: 'Close', 5:'High', 6:'Low', 7:'Open', 8:'Lcose'
                           , 9:'涨跌额', 10:'涨跌幅', 11:'换手率', 12:'Volume', 13:'成交金额', 14:'总市值', 15:'流通市值'} , inplace=True)
        #print(df)

    except IOError:
        conn.rollback() # 出现异常 回滚事件
        print("Error: Function happen Error: test()")
    finally:
        print("释放资源，数据库连接池")
        cur.close()
        conn.close()
        #查询表结构语句为desc stock_000016
        return  df

def queryMySQL_plot_stock_market(code1, startdate = '2017-12-09', enddate = '2018-12-09'):#使用连接池

    try:
        # 调用连接池
        conn = pool.connection()
        cur = conn.cursor()
        code = 'stock_'+code1
        sql = 'select * from %s where 日期 between \'%s\'' % (code , startdate) + ' and \'%s\'' % enddate
        #print(sql)
        cur.execute(sql)
        results = cur.fetchall()
        df = pd.DataFrame(list(results))
        df.rename(columns={0:'Stamp', 1:'Date',2:'Code', 3:'Name', 4: 'Close', 5:'High', 6:'Low', 7:'Open', 8:'Lcose'
                           , 9:'涨跌额', 10:'涨跌幅', 11:'换手率', 12:'Volume', 13:'成交金额', 14:'总市值', 15:'流通市值'} , inplace=True)
        #print(df)

    except IOError:
        conn.rollback() # 出现异常 回滚事件
        print("Error: Function happen Error: test()")
    finally:
        print("释放资源，数据库连接池")
        cur.close()
        conn.close()
        #查询表结构语句为desc stock_000016
        return  df

def test(project_name):
    try:
        # 调用连接池
        conn = pool.connection()
        cur = conn.cursor()
        sql = "select * from stock_600016 "
        cur.execute(sql)
        results = cur.fetchall()
        df = pd.DataFrame(list(results))
        print(df)
    except IOError:
        conn.rollback() # 出现异常 回滚事件
        print("Error: Function happen Error: test()")
    finally:
        print("释放资源，test，"+project_name)
        cur.close()
        conn.close()


if __name__ == "__main__":
    startdate  = '2017-12-09'
    enddate  = '2018-12-13'
    print(startdate)
    code = '600016'
    df2 = queryMySQL_plot_stock_market(code, startdate, enddate)
    print(df2)
#test('test')
'''conn = pool.connection()  #以后每次需要数据库连接就是用connection（）函数获取连接就好了
cur=conn.cursor()
SQL='select * from stock_600016 '
r = cur.execute(SQL)
results = cur.fetchall()
df = pd.DataFrame(list(results))
print(df)
cur.close()
conn.close()'''