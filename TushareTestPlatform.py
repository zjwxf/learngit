
import multiprocessing
import os
import pandas as pd
import time
import tushare as ts


def log(text):
    print('-' * 15)
    print(text)


def set_tushare(token):
    ts.set_token(token='0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
    pro = ts.pro_api('0a9d3308245c51f14e45b0c6d9166ffcc4fbd13d3438222f99f675f7')
    return pro


def set_done_code():
    work_dir = os.getcwd()
    file_path = os.path.join(work_dir, 'done_code.csv')
    flag = 0
    if not os.path.exists(file_path):
        # 如果不存在记录文件则创建
        done_code = pd.DataFrame(dict(done_code=[]))
        done_code.to_csv('done_code.csv')
        log('创建：done_code.csv')
    else:
        done_code = pd.read_csv(file_path, index_col=[0])
        if not done_code.empty:
            flag = input('是否继续上次未加载股票？确认1否认0：')
            if flag == 0:
                done_code = pd.DataFrame(dict(done_code=[]))
                done_code.to_csv('done_code.csv')
                log('已重置：done_code.csv')
        else:
            pass
    assert flag == 0 or 1
    return flag, list(done_code['done_code'])


def set_mkdir(dir_name):
    work_dir = os.getcwd()
    if not os.path.isdir(os.path.join(work_dir, dir_name)):
        os.mkdir(dir_name)
        log(f'已创建：{dir_name}')
    else:
        log(f'已存在：{dir_name}')


def record_done_code(stock_code):
    done_code = pd.read_csv('done_code.csv', index_col=[0])
    d_code = pd.DataFrame(dict(done_code=stock_code), index=[0])
    done_code.append(d_code, ignore_index=True)
    done_code.to_csv('done_code.csv')


def Get_stock_basicinfo():
    stock_basicinfo = pro.stock_basic(list_status='L')
    return stock_basicinfo


def Get_Data(stock_code):
    try:
        # ---获取数据---
        df = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date='20000101')
        # ---存入数据---
        df.to_csv(os.path.join('stock_hfq', f'{stock_code}.csv'))
        # 记录已获取股票
        record_done_code(stock_code)
        time.sleep(1)
        print(df.head(3))
    except:
        print(f'未能获取数据：{stock_code}')
        pass


if __name__ == '__main__':
    set_mkdir('stock_hfq')
    # 设置token
    pro = set_tushare('你的token 可以从tushare网站获取')
    # 获取股票基本数据
    stock_basic_info = Get_stock_basicinfo()
    # 设置股票池
    flag, done_code = set_done_code()
    stock_list = list(stock_basic_info['ts_code'])
    # 如果flag==0则直接使用stock_list 否则使用stock_list与done_code的差集即未完成的股票
    code = stock_list if flag == 0 else stock_list.remove(done_code)
    # 设置进程池
    p = multiprocessing.Pool(8)
    b = p.map(Get_Data, code)
    p.close()
    p.join()
    p = multiprocessing.Pool()