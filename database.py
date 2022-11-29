import psycopg2
import pandas as pd                                                   
from sql_queries import create_table_queries, drop_table_queries    
from logging import error, info                                     
from sys import exit                                               


def create_database():
    conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=243278")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    #Create specific db
    cur.execute("DROP DATABASE indeedjobs")
    cur.execute("CREATE DATABASE indeedjobs")
    
    conn.close()
    
    #Connect to new one
    conn = psycopg2.connect("host=127.0.0.1 dbname=indeedjobs user=postgres password=243278")
    cur = conn.cursor()
    
    return cur,conn

def drop_tables(cur,conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
        
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def main():

    try:
        cur, conn = create_database()
        info("Successfully created database and retrieved associated connection and cursor")
    except Exception as e:
        error(f"Error creating database or retrieving associated connection and cursor: {e}")
        exit()
    
    try:
        create_tables(cur, conn)
        info("CREATE TABLE queries execution complete")
    except Exception as e:
        error(f"Error executing CREATE TABLE queries: {e}")
        exit()

    conn.close()

if __name__ == "__main__":
    main()