import pandas as pd 
import tabula
import matplotlib.pyplot as plt
import numpy as np

##Url del Plan Estratégico y Financiero 2021-2025 del Infonavit
url="https://portalmx.infonavit.org.mx/wps/wcm/connect/67e528e7-f13d-4dbf-a668-b29a594351c3/Plan_Estrategico_y_Financiero_2020-2024.pdf?MOD=AJPERES&CVID=mYkHiU3"

###Importar únicamente la página 116 del documento
df=tabula.read_pdf(url,pages="116")

###Dado que se importa como lista, se debe transformar a dataframe

df = pd.DataFrame(np.array(df).reshape(35,6))


##Tirar las dos primeras filas y la última, la cual contiene los totales

df=df.tail(-2)
df=df[:-1]

##Solo nos interesan las dos primeras columnas con el nombre de la entidad y el número de créditos de vivienda nueva
df = df.iloc[:, 0:2]

##Renombrar columnas
df=df.rename(columns={0: "nom_ent", 
                1: "credvivn"})


##convertir los números de string a entero
df['credvivn'] = df['credvivn'].str.replace(',', '').astype(int)

##Corregir nombres de entidades

df['nom_ent'] = df['nom_ent'].replace(['Quintan Roo'],'Quintana Roo')

##Salvar en csv
df.to_csv (r'C:/Users/ALIENWARE/Documents/canadevi/infonavit2021.csv',
 index = False, header=True,encoding='utf-8-sig')

##Segunda parte: Gráfico
##Se calcularán los porcentajes que representan cada estado del total y se graficará


##Calcular porcentaje del total
df["pct"]=df["credvivn"]/sum(df["credvivn"])*100

#Ordenamos de mayor a menor de acuerdo al porcentaje
df.sort_values('pct',inplace=True)

##Gráfica
df.plot(kind="barh",figsize=(19, 7),color="#feb24c",
x="nom_ent",y="pct")
#Título
plt.title('Infonavit. Distribución de las metas de crédito para adquisición de vivienda nueva por entidad federativa, 2021 \n (%)',
fontsize=14,fontweight="bold", loc="left")
plt.legend("",frameon=False)
plt.xlabel('Porcentaje del total de créditos para adquisición de vivienda nueva\nFuente: @claudiodanielpc con información de INFONAVIT. Plan Estratégico y Financiero 2021-2025')
plt.ylabel("Entidad federativa")
##Guardar y mostrar la gráfica
plt.savefig("infonavitnueva.png",format="png",dpi=600,transparent=False)
plt.show()
