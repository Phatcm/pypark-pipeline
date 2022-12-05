import os                           #A portable way of using operating system dependent functionality
from logging import error, info     #Logging progress
from sys import exit                #To gracefully exit out of Python application upon error
import glob                         #Finds all the pathnames matching a specified pattern
import psycopg2                     #PostgreSQL database adapter for the Python
import pandas as pd                 #High-performance, easy-to-use data structures and data analysis tools for Python 
from sql_queries import staging_retail_table_insert, stocks_table_insert, date_table_insert, invoices_table_insert, country_table_insert, online_retail_table_insert

def extract_to_staging(cur, filepath):
    # open file
    try:
        retail = pd.read_csv(filepath)
        info("OnlineRetail data files read complete")
    except Exception as e:
        error(f"Error reading OnlineRetail data files: {e}")
        exit()
    
    # cleaning data
    try:
        # .0 at the end of customerID
        retail['CustomerID'] = retail['CustomerID'].astype(str).str.replace('.0', '', regex=False)
        # format datetime
        retail['InvoiceDate'] = pd.to_datetime(retail['InvoiceDate']).dt.normalize()
        # Delete row with null data
        retail_clean = retail.dropna().reset_index(drop=True)
        # CustomerID can't be null
        indexnan = retail_clean[ (retail_clean['CustomerID'] == 'nan')].index
        retail_clean.drop(indexnan , inplace=True)
    except Exception as e:
        error(f"Error creating table DataFrame: {e}")
        exit()
    
    try:
        for i,row in retail_clean.iterrows():
            cur.execute(staging_retail_table_insert, list(row))
        info("Successfully executed staging_retail table INSERT statement")
    except Exception as e:
        error(f"Error executing staging_retail table INSERT statement: {e}")
        exit()

def tranform_and_load(cur):
    # core.stocks
    try:
        query=("""SELECT DISTINCT StockCode, Description FROM staging.retail""")
        cur.execute(query)
        stocks = cur.fetchall()
        
        df = pd.DataFrame(stocks, columns= ["stock_code", "stock_name"])
    except Exception as e:
        error(f"Error executing core_stock queries: {e}")
        exit()
    
    try:
        for i,row in df.iterrows():
            cur.execute(stocks_table_insert, list(row))
    except Exception as e:
        error(f"Error executing core_stock table INSERT statement: {e}")
        exit()
    
    # core.date
    try:
        query=("""SELECT DISTINCT InvoiceDate,
                       EXTRACT(year from InvoiceDate)*10000 + EXTRACT('month' from InvoiceDate)*100+EXTRACT('day' from InvoiceDate)as date_id            
       FROM staging.retail
       ORDER BY date_id ASC""")
        cur.execute(query)
        date = cur.fetchall()
        
        
        dft = pd.DataFrame(date, columns= ["invoice_date", "date_id"])
        dft= dft.loc[:,['date_id','invoice_date']]
    except Exception as e:
        error(f"Error executing core_date queries: {e}")
        exit()
    
    try:
        for i,row in dft.iterrows():
            cur.execute(date_table_insert, list(row))
    except Exception as e:
        error(f"Error executing core_date table INSERT statement: {e}")
        exit()
    
    #core.invoices
    try:
        query=("""SELECT DISTINCT InvoiceNo FROM staging.retail""")
        cur.execute(query)
        invoices = cur.fetchall()
        
        df = pd.DataFrame(invoices, columns= ["invoice_no"])
    except Exception as e:
        error(f"Error executing core_invoices queries: {e}")
        exit()
    
    try:
        for i,row in df.iterrows():
            cur.execute(invoices_table_insert, list(row))
    except Exception as e:
        error(f"Error executing core_invoices table INSERT statement: {e}")
        exit()
    
    #core.country
    try:
        query=("""SELECT DISTINCT Country FROM staging.retail""")
        cur.execute(query)
        country = cur.fetchall()
        
        df = pd.DataFrame(country, columns= ["country_name"])
    except Exception as e:
        error(f"Error executing core_country queries: {e}")
        exit()
    
    try:
        for i,row in df.iterrows():
            cur.execute(country_table_insert, list(row))
    except Exception as e:
        error(f"Error executing core_country table INSERT statement: {e}")
        exit()
    
    #core.OnlineRetail
    try:
        query=(""" SELECT
                s.stock_id as stock_id_FK,
                i.invoice_id as invoice_id_FK,
                d.date_id as date_id_FK,
                c.country_id as country_id_FK,
                customerid,
                quantity,
                unitprice
            FROM staging.retail r 
            JOIN core.stocks s ON s.stock_code = r.stockcode 
            JOIN core.invoices i ON i.invoice_no = r.invoiceno
            JOIN core.date d ON d.invoice_date = r.invoicedate
            JOIN core.country c ON c.country_name = r.country
            ORDER BY date_id_FK ASC""")
        cur.execute(query)
        result = cur.fetchall()
        df = pd.DataFrame(result, columns= ["stock_id_FK", "invoice_id_FK", "date_id_FK" ,"country_id_FK", "customerid", "quantity", "unitprice"])
    except Exception as e:
        error(f"Error executing core_OnlineRetail queries: {e}")
        exit()
    
    try:
        for i,row in df.iterrows():
            cur.execute(online_retail_table_insert, list(row))
    except Exception as e:
        error(f"Error executing core_OnlineRetail table INSERT statement: {e}")
        exit()
        
def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    try:
        for root, dirs, files in os.walk(filepath):
            files = glob.glob(os.path.join(root,'*.csv'))

            for f in files :
                all_files.append(os.path.abspath(f))
        info("Creating the list of data file path complete successfully")
    except Exception as e:
        error(f"Error creating list of data file path: {e}")
        exit()
    # get total number of files found
    num_files = len(all_files)
    info(f"{num_files} files found in {filepath}")
    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        info(f"{i}/{num_files} files processed")






def main():
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=indeedjobs user=postgres password=243278")
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        info("Successfully connected to Sparkify DB and retrived associated connection and cursor")
    except Exception as e:
        error(f"Error connecting to Sparkify DB: {e}")
        exit()
    
    process_data(cur, conn, filepath='data/', func=extract_to_staging)
    tranform_and_load(cur)
    conn.close()


if __name__ == "__main__":
    main()
    
    