from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import shutil
import os
import pandas as pd
import numpy as np
import re

# directory = r"C:\Users\ypajarino\Projects\2021.01.20 REQ PIO\Output\20003\20003_2018_04_MAQUINARIAS_1"
directory = input("Ingreses carpeta de acrhivos (sin comillas): ")
#print(dirs)

docs = []
for file in os.listdir(directory):
    folder = os.path.join(directory,file)
    f_docs = os.listdir(folder)
    m = []
    print("Unificando OP: {}".format(file),end="")
    output = PdfFileMerger()
    try:
        f_docs.remove("Binder1.pdf")
    except:
        pass
    
    try:
        for item in f_docs:
            pdf= PdfFileReader(open(os.path.join(folder,item), "rb"),strict=False)
            if item[:2] == "OP":
                output.merge(0,pdf)
            else:
                output.append(pdf)
        outputStream = open(os.path.join(folder,"Binder1.pdf"), "wb")
        output.write(outputStream)
        outputStream.close()
        print()
    except:
        print(" Error")

