import tabula
import pandas as pd

servidores_pcd = pd.read_csv('lista_pcds.txt', header=0)
servidores_pcd = servidores_pcd['nome'].str.upper()
#print(servidores_pcd)

salarios = pd.read_csv('folhamg022024.csv', sep=';', low_memory=False, encoding = "ISO-8859-1")
#salarios = salarios.drop(salarios['nmefet'] != 'AUDITOR FISCAL DA RECEITA ESTADUAL')
#df[df['Age'] >= 25]
salarios = salarios[salarios['nmefet']== 'AUDITOR FISCAL DA RECEITA ESTADUAL']
salarios['nome'] = salarios['nome'].str.upper()
#print(salarios)
#print(salarios.info())

lista = pd.merge(salarios, servidores_pcd, on='nome')
print(lista)
lista.to_csv('rem_pcds_022024.csv', sep=';', index=False)