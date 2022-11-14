from datetime import date
import sqlite3
from time import time
import requests
import pandas as pd
import io
import glob 


dbname = "TWStock.db"

db = sqlite3.connect(dbname)

pd.read_excel("number.xlsx").iloc[:,1:].to_sql("number.xlsx".replace('.xlsx', ''), db, if_exists='replace')



