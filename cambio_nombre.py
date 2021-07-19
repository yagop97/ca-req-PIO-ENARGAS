import re
import shutil
import os

url_docs = r"G:\Proveedores\AUDITORIA PIO 2017AL2020\CGP\1er entrega\20003_2018_02_UNP-21-01-18_0"
folders = os.listdir(url_docs)
try:
    folders.remove("Thumbs.db")
    folders.remove("Renombrados")
except:
    pass

regex_soc = re.compile(r"[\\](\d{5})")
regex_cod = re.compile(r"[\\](\d{5}_\d{4}.*)")

num_soc = re.findall(regex_soc,url_docs)[0]
cod_proy = re.findall(regex_cod,url_docs)[0]

n = 0
for x in folders:
    url_src = os.path.join(url_docs, x, "{}.pdf".format("Binder1"))
    nuevo_nombre = str(num_soc + "_0_PIO-CAD_2021-06_20210618~" + cod_proy + "~LP~" + x + ".pdf")
    url_out = os.path.join(url_docs, "Renombrados", "{}".format(nuevo_nombre))
    try:
        os.mkdir(os.path.join(url_docs, "Renombrados"))
        shutil.copy(url_src, url_out)
    except:
        shutil.copy(url_src, url_out)
    n += 1
    print("Done {} of {}".format(n, len(folders)))
        



            