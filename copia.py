import shutil
import pandas as pd
import os
import re

df = pd.read_excel("copia.xlsx")
base = "G:\Proveedores\AUDITORIA PIO 2017AL2020\Proyectos a Presentar\CGP\Entrega 4\{}\Renombrados\\20004_2_PIO-CAD_2021-02_20210212~{}~LP~{}.pdf"
df["carpeta"] = df["SubproyectoId"]
df["SubproyectoId"] =[re.sub("2000(3)","20004",x) for index, x in df["SubproyectoId"].items()] 
URL =[]
for x in range(df.shape[0]):
    proy = df["SubproyectoId"][x]
    carpeta = df["carpeta"][x]
    OP = df["OPNumero"][x]
    URL.append(os.path.abspath(base.format(carpeta,proy, OP)))

n=0
errors = []
for x in URL:
    n += 1
    print("copying {} of {}".format(n,len(URL)))
    try:
        url_dest = r"G:\Proveedores\AUDITORIA PIO 2017AL2020\Proyectos a Presentar\CGP\Entrega 4\Rectificativas"
        shutil.copy(x,url_dest)
    except:
        errors.append(x)
        pd.Series(errors).to_excel("errors.xlsx")