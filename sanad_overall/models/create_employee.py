import time
from datetime import datetime
import pandas as pd
from xmlrpc.client import ServerProxy

url = "https://sanadbagsfactory-odoo-uat-1-6764251.dev.odoo.com"
db = "sanadbagsfactory-odoo-uat-1-6764251"
username = 'admin'
password = "admin"

common = ServerProxy('{}/xmlrpc/2/common'.format(url))
models = ServerProxy('{}/xmlrpc/2/object'.format(url))

uid = common.login(db, username, password)
print(uid)
var = common.version()

data = pd.read_excel('/home/cognitive/Documents/emp_import.xlsx')
data_rec = data.to_dict('records')
print(data_rec)