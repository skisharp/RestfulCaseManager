# -*- coding: utf-8 -*-
import cx_Oracle


def tes_tmain():
    oracle_connecton = cx_Oracle.connect('polar', 'polardev33', 'm1-erp-appdev3.m1.baidu.com:8551/PLDEV3')
    cursor = oracle_connecton.cursor()
    # res = oracle_connecton.cursor.callproc
    res = cursor.callfunc('a_test', cx_Oracle.NUMBER, (20,))
    print res

    res1 = cursor.callfunc('get_dept_count', cx_Oracle.NUMBER, (136167,))
    print res1

    # 中文乱码
    res2 = cursor.callfunc('cux_mt_recommend_pkg.get_bg_name', cx_Oracle.STRING, (0, 'ZHS'))
    print res2

     # 中文乱码
    res3 = cursor.callfunc('cux_mt_recommend_pkg.get_bg_name', cx_Oracle.STRING, (0, 'ZHS'))
    print res3

    oracle_connecton.close()

if __name__ == '__main__':
    tes_tmain()
