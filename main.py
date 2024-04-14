import numpy as np
import pandas as pd
from IPython import display

teto_previdencia = 7507.49
df_final = pd.DataFrame
servidores_df = pd.read_csv('~/Downloads/dados_serv_202402.csv', low_memory=False, sep=';', encoding = "ISO-8859-1")

for x in range(1,13):
    print("O ano é 2023. O mês é:", x)
    if(x <10):
        pdf_path = '~/Downloads/ServidoresMG_0'+ str(x) +'23.csv'
    else:
        pdf_path = '~/Downloads/ServidoresMG_'+ str(x) +'23.csv'
    df = pd.read_csv(pdf_path, sep=';', encoding = "ISO-8859-1", low_memory=False, decimal = ',', dtype = {'remuner':np.float64,'ir': np.float64, 'prev':np.float64})
    print("Contagem do dataframe df antes de tratar: ", df.count())
    df = df.drop(['nome','descsitser','nmefet','tem_apost','desccomi','descinst','descunid','carga_hora','teto','judic','ferias','decter','premio','rem_pos', 'feriasprem','jetons','eventual','bdmg','cemig','codemig','cohab','copasa','emater','epamig','funpemg','gasmig','mgi','mgs','prodemge','prominas','emip','codemge','emc'], axis=1)
    print("Contagem do dataframe df antes de tratar e após exclluir colunas: ", df.count())
    df = df[df['remuner'] > teto_previdencia]
    print("Contagem do dataframe df após excluir remunerações abaixo do teto ", df.count())
    df = df[df['prev'] > 900]
    print("Contagem do dataframe df após excluir contribuições menores que 900: ", df.count())
    df['anomes'] = "2023" + str(x)
    if(x<5):
        #calculo ir até abril
        df['bc_ir_prev'] = (df['ir'] + 884.96) / 0.275 
    else:
        #calculo ir a partir de maio
        df['bc_ir_prev'] = (df['ir'] + 896) / 0.275
    if(x == 1):
        df_final = df
    else:
        df_final = pd.concat([df_final, df], ignore_index = True)
    print("Contagem DF", df.count())
    print("Contagem df_final", df_final.count())
    print("\n")

#a partir daqui escrever as condições de filtros
#a primeira é eliminar aqueles cuja remuneração seja inferior ao teto
#df_final = df_final[df_final['remuner'] > teto_previdencia]
#relação estimada é de até 0,130823548752514
print("Contagem df_final antes da alíquota:", df_final.count())
df_final['aliquota_pss_efetiva'] = df_final['prev'] / df_final['remuner']
teto_aliquota_previsto = 0.130823548752514
df_final = df_final[df_final['aliquota_pss_efetiva'] < teto_aliquota_previsto]

#criar coluna para base de cálculo do IR
df_final['bc_ir'] = df_final['remuner'] - df_final['prev']

print("Contagem df_final depois da alíquota:", df_final.count())

#Filtrar as contribuições previdenciárias que sejam superiores ao valor aplicável ao teto (verificar)
#Após, filtrar dentre todas estas aquelas que a relação entre a contrição e remuneração seja menor que a aplicável ao teto. 

#deduzir o IR cobrado
#fazer isto criando uma tabela base de cálculo do IR. Verificar se há correlação entre a diferença e número de dependentes (bc_ir_pres - bc_ir)

#Lembrar que pode haver dedução por dependentes. Tentar identificar isto. 
df_final = df_final.sort_values(by=['prev'], ascending=True)



df_final.info()

df_final = df_final.round(2)
#df_final.to_csv('dffinal_teste.csv', mode='a', index=False)

df = pd.merge(df_final, servidores_df, on='masp', how='left')
print(df.head(5))
print(df.tail(5))
df.info()
df.to_csv('tabela_merge.csv', mode='a', index=False)

"""
for tabela in df:
    print(tabela)
    tabela.to_csv('tabela.csv', sep=';', mode='a')
"""
# convert PDF into CSV
#tabula.convert_into(pdf_path, "output.csv", stream=True, output_format="csv", pages='210-211')
#tabula.convert_into(pdf_path2, "output2.csv", stream=True, output_format="csv", pages='203')
#tabula.convert_into(pdf_path3, "output3.csv", stream=True, output_format="csv", pages='203')