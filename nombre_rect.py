import shutil
import os
import re
import pandas as pd

base = r"G:\Proveedores\AUDITORIA PIO 2017AL2020\Proyectos a Presentar\CGP\Entrega 4\CGP rectificativas"
dirs = os.listdir(base)
errors = []
n=0
for x in dirs:
    n += 1
    print("Doing {} of {}".format(n,len(dirs)))
    try:
        url = os.path.join(base, x)
        x = re.sub("20004","20003",x)
        x = re.sub("_20210212~","_20210218~",x)
        x = re.sub("_4_","_3_",x)
        dest_url = os.path.join(base, "Renombrados", x)
        shutil.copy(url, dest_url)
    except:
        errors.append(x)

pd.Series(errors).to_excel("ren_errors.xlsx")
