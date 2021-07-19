import shutil
import os
import pandas as pd
import numpy as np


docs = pd.read_excel(r'C:\Users\ypajarino\Projects\2021.01.20 REQ PIO\Files\DOCS.xlsx', converters={"PROVEEDOR":str})
FBL1N = pd.read_excel(r'C:\Users\ypajarino\Projects\2021.01.20 REQ PIO\Files\FBL1N.xlsx',converters={"Acreedor":str,"Clave de referencia":str})

nitems = docs.shape[0]

# Modificaciones al dataset
to_replace = {
    "KR":"FC",
    "KH":"NC",
    "KJ":"ND",
    "KE":"FC",
    "K5":"FC",
    "KC":"NC",
    "K2":"FC",
    "K0":"NC",
    "K4":"ND",
    "K3":"NC",
    "KB":"FC"
}
FI = ["KH","KE","KJ"]
FBL1N["Clase de documento"] = FBL1N["Clase de documento"].replace(to_replace)
docs["key"] = docs["PROVEEDOR"].astype(str) + docs["TIPO_DOC"] + docs["NRO_DOC"].astype(str)
FBL1N["key"] = FBL1N["Acreedor"].astype(str) + FBL1N["Clase de documento"] + FBL1N["Referencia"]
docs["FECHAOP"] = docs["FECHAOP"].astype(str)
docs["KEY_OP"] = docs["OP"].astype(str) + docs["FECHAOP"][:4]

# Ciclo para obtener: el número de doc asociado en la URL del disco y el año de contabilización. Datos de la FBL1N
# Para Nro documento mayor a 1600000000 (contabilizados por MM) se obtiene el campo clave referencia, para menores se obtiene el nro de documento SAP
# Se almacenan en las columnas URL_DOC y URL_YEAR
SAP_docs = []
years = []
for x in range(nitems):
    count = 0
    key = docs["key"][x]
    for y in range(FBL1N.shape[0]):
        if FBL1N["key"][y] == key:
            if FBL1N.loc[FBL1N["key"]==key,"Nro documento"].values[0] > 1600000000:
                SAP_docs.append(FBL1N["Clave de referencia"][y][:-4])    
            else:
                SAP_docs.append(FBL1N["Nro documento"][y])
            years.append(FBL1N["Fe.contabilización"][y].year)
            count += 1
    if count == 0:
        SAP_docs.append(key)
        years.append(key)
m = np.asarray(SAP_docs)
n = np.asarray(years)
docs["URL_DOC"] = m
docs["URL_YEAR"] = n

# Creación de columna URL con el formato de ruta de URL guardada en disco
url_root = r'\\arfile01\buegadministracion\proveedores\facturas digitalizadas proveedores'
docs["URL_END"] = docs["PROVEEDOR"].astype(str) + "-" + docs["URL_DOC"] + "-" + docs["URL_YEAR"].astype(str)
docs["URL"] = url_root + "\\" + docs["SOC"] + "\\" + docs["URL_END"] + ".pdf"
#docs.to_excel(r"C:\Users\ypajarino\Projects\2021.01.20 REQ PIO\prueba.xlsx")

#Función que prueba la existencia de PDF asociado a la ruta, guarda en una lista los que tienen PDF asociado y en otra los que no
def get_dirs(serie):
    print("Revisando existencia de PDF asociado")
    sin_pdf = []
    con_pdf = []
    for index, value in serie.items():
        if os.path.exists(value) == False:
            sin_pdf.append(value)
        else:
            con_pdf.append(value)
    return sin_pdf, con_pdf

sin_pdf, con_pdf = get_dirs(docs["URL"])

pdf = []
for y in range(nitems):
    n = 0
    for x in sin_pdf:
        if x == docs["URL"][y]:
            pdf.append("No tiene PDF asociado")
            n += 1
            break
    if n == 0:
        pdf.append("Tiene PDF asociado")
        

pdf = np.asarray(pdf)
docs["PDF"] = pdf
print("Docs sin PDF asociado: {}".format(len(sin_pdf)))
docs.to_excel((r"C:\Users\ypajarino\Projects\2021.01.20 REQ PIO\docs_expand.xlsx"))

# Copiado de documentos PDF en carpeta sociedad\proyecto\OP
for x in range(nitems):
    if docs["URL"][x] in con_pdf:
        print("doing {} of {}".format(x + 1, nitems))
        prov = docs["PROVEEDOR"][x]
        doc = docs["NRO_DOC"][x]
        year = docs["URL_YEAR"][x]
        dest_fpath = os.path.join(r"C:\Users\ypajarino\Projects\2021.01.20 REQ PIO\Output",docs["SOCIEDAD"][x].astype(str),docs["PROYECTO"][x],docs["OP"][x].astype(str),f"{prov}-{doc}-{year}.pdf")
        try:
            shutil.copy(docs["URL"][x], dest_fpath)
        except:
            os.makedirs(os.path.dirname(dest_fpath))
            shutil.copy(docs["URL"][x], dest_fpath)
    else:
        print("doing {} of {} - no tiene PDF asociado".format(x + 1, nitems))

 