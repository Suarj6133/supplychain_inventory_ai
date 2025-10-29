import sqlite3
import pandas as pd

DB_PATH = 'grocery_data.db'

#definig db path and geting files into the DB

def load_csv_to_sqlite():
    conn = sqlite3.connect(DB_PATH)

    #converting excel data into dataframe
    df1 = pd.read_excel("grocery_data.xlsx")
    #moving this df1 as report and feeting into sqlite
    df1.to_sql("report", conn, if_exists="replace", index=False)

    conn.close()
    print("excel loaded into database")

if __name__ == "__main__":
    load_csv_to_sqlite()