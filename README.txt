Requerimiento PIO

1. Configuración del espacio de trabajo

    1.1 Descargar y agregar al PATH del sistema python
    1.2 Instalar las librerias incluidas en requirements.txt (pip install -r requirements.txt)

2. Uso del programa

    2.1 Archivos y carpetas necesarias
        a) Files\DOCS.xlsx
            Contiene los documentos a presentar en el requerimiento
                Columnas del excel = SOCIEDAD	SOC	PROYECTO	OP	FECHAOP	PROVEEDOR	TIPO_DOC	NRO_DOC
        b) Files\FBL1N.xlsx
            Contiene los datos de SAP de los documentos a presentar
            Se utiliza para obtener datos del documento necesarios para obtener la URL donde esta guardado el documento
        c ) Files\OP\ 
            Contiene los archivos PDF detallados en la columna OP de Files\DOCS.xlsx
            El nombre de los archivos es el que baja de SAP: OPaabbbbbbbbbbcccc
            Donde:
                aa: es el codigo de sociedad: 01 para CGP y 02 para CGS
                bbbbbbbbbb: es el numero de OP
                cccc: es el año de emision de la OP

    2.2 Workflow
        a) facturas.py 
            Toma los archivos excel requeridos, busca los PDF de los documentos en las carpetas del disco y las copia en la carpeta:
            \Output\[cod sociedad]\[cod proyecto]\[numero_OP]
            devolviendo una carpeta por cada OP que contiene cada archivo pdf requerido, en caso de haber sido encontrado
            Tambien devuelve el archivo docs_expand.xlsx que detalla los documentos que no tienen PDF asociado
        b) OP.py
            Toma los archivos PDF que hay en la carpeta requerida y los copia en las carpetas creadas en a)
            Luego de este paso, las carpetas creadas en el paso anterior tienen archivos pdf de documentos y de la OP
        c) Completar la informacion faltante
            - remitos y certificados
            - documentos sin PDF asociado
        d) Agrupar los documentos de la carpeta en un solo PDF utilizando adobe acrobat
            En cada carpeta creada en a) seleccionar todos los documentos pdf a unificar -> click derecho mouse -> seleccionar "Combine archivos en Acrobat..."
            En abode organizar paginas para que quede OP como primer pagina
            Guardar en la misma carpeta con el nombre por defecto "Binder1"
        d) cambio_nombre.py
            Busca en cada carpeta el archivo PDF llamado "Binder1" y lo guarda en una nueva carpeta llamada "Renombrados"
