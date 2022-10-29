import pandas
import pandas as pd
from pandasql import sqldf
import sqlite3
from ftp_connection import *
from extracter import *


if __name__ == "__main__":
    #download('task.rar')
    #extract('files/task.rar')
    data = pd.read_csv('files/data.csv', sep=';', decimal=',')
    deposit = pd.read_csv('files/deposit.csv', sep=';', decimal=',')
    price = pd.read_csv('files/price.csv', sep=';', decimal=',')
    quantity = pd.read_csv('files/quantity.csv', sep=';', decimal=',')
    weight = pd.read_csv('files/weight.txt', sep='/t', engine='python', decimal=',')
    
    querry = '''
    
    SELECT
        data.main_part_number,
        data.manufacturer,
        data.category,
        data.origin,
        IFNULL(deposit.deposit, 0) AS deposit,
        price.price,
        quantity.quantity,
        IFNULL(price + deposit.deposit, price) AS total

    FROM
        data
            INNER JOIN
        price ON data.part_number = price.part_number
            LEFT JOIN
        deposit ON data.part_number = deposit.part_number
            LEFT JOIN
        quantity ON data.part_number = quantity.part_number
    WHERE 
        quantity.warehouse = 'A'
        OR quantity.warehouse = 'H'
        OR quantity.warehouse = 'J'
        OR quantity.warehouse = '3'
        OR quantity.warehouse = '9'
        AND (price + deposit.deposit) > 2
        
                
    '''

    df = sqldf(querry)
    df.to_csv('export.csv', sep=';')

    conn = sqlite3.connect("database1.db")
    df.to_sql("df", conn, if_exists="replace")

    export_querry = '''
    
    SELECT 
        main_part_number,
        manufacturer,
        category,
        origin,
        CAST (quantity AS INTEGER),
        ROUND (total, 2) AS price 
    FROM 
        df WHERE quantity > 0

    '''
    export = pandas.read_sql(export_querry, conn)
    export.to_csv('export.csv', sep=';', index=False)
