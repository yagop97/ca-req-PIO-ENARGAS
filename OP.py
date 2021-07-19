import shutil
import os
import pandas as pd
import numpy as np
import re

docs = pd.read_excel(r"C:\Users\ypajarino\Projects\2021.01.20 REQ PIO\Files\DOCS.xlsx")
url = r"C:\Users\ypajarino\Projects\2021.01.20 REQ PIO\Files\OP"
ops = os.listdir(url)
reg = re.compile("OP0\d{1}(\d{10})")
soc = str(docs.iloc[0,0])
op_url = r"C:\Users\ypajarino\Projects\2021.01.20 REQ PIO\Output"
nitems = len(ops)

n=0
for x in ops:
    n += 1
    print("Copying {} of {}".format(n, nitems))
    op = re.findall(reg, x)[0]
    proy = docs.loc[docs["OP"] == int(op),"PROYECTO"].unique()
    src_url = os.path.join(url, x)
    for y in proy:
        dest_url = os.path.join(op_url, soc, y, op, x)
        try:
            os.mkdir(os.path.dirname(dest_url))
            shutil.copy(src_url, dest_url)
        except:
            shutil.copy(src_url, dest_url)