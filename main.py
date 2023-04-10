# %%
import requests as re
import json
import pandas as pd
from datetime import datetime,timedelta

# %%
data = datetime.now().date()
ontem = data - timedelta(1)
menos_uma_semana = ontem - timedelta(7)
ontem = datetime.strftime(ontem, '%Y-%m-%d')
menos_uma_semana = datetime.strftime(menos_uma_semana, '%Y-%m-%d')

# %%
situacaoPedido = 11
url1 = f"https://api.fbits.net/pedidos/situacaoPedido/{situacaoPedido}?dataInicial={menos_uma_semana}&dataFinal={ontem}"
headers = {
    "accept": "application/json",
    "Authorization": "Basic ##############"
}

response1 = re.get(url1, headers=headers)
response1 = response1.json()
response1

# %%
df = pd.DataFrame()
for i in range (len(response1)):
    df1 = pd.DataFrame(data={'Id Transação' : response1[i - 1]['transacaoId'],'Valor Gasto' : response1[i -1]['itens'][0]['precoVenda'], 'Quantidade' : response1[i -1]['itens'][0]['quantidade']}, index=[0])
    df = pd.concat([df,df1],ignore_index=True)



# %%
df_antiga = pd.read_csv('Dados.csv', sep=';')
df = pd.concat([df,df_antiga])
df.to_csv('Dados.csv', sep=';', index=False)

# %%

