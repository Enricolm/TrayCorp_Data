# %%
# %%
import requests as re
import json
import pandas as pd
from datetime import datetime,timedelta

# %%
data = datetime.now().date()
ontem = data - timedelta(1)
menos_uma_semana = ontem - timedelta(60)
ontem = datetime.strftime(ontem, '%Y-%m-%d')
menos_uma_semana = datetime.strftime(menos_uma_semana, '%Y-%m-%d')

# %%
pag = 1 
df = pd.DataFrame()
iterador = True

headers = {
    "accept": "application/json",
    "Authorization": "Basic ##############"
}

url2 = 'https://api.fbits.net/formasPagamento'
resposta_pagamentos = re.get(url2,headers=headers)
resposta_pagamentos = resposta_pagamentos.json()
lista_pagamento = {}
for k in range(len(resposta_pagamentos)):
    id_pagamento = resposta_pagamentos[k]['formaPagamentoId']
    Forma = resposta_pagamentos[k]['nomeExibicao']
    lista_pagamento[id_pagamento] = Forma
    
while iterador == True:
    url1 = f"https://api.fbits.net/pedidos?dataInicial={menos_uma_semana}&dataFinal={ontem}&pagina={pag}&valido=true"
    
    response1 = re.get(url1, headers=headers)
    response1 = response1.json()
    for i in range(len(response1)):
        pedidoId = response1[i]['pedidoId']
        data = response1[i]['data']
        data = data.split('T')[0]
        formaPagamento = response1[i]['pagamento'][0]['formaPagamentoId']
        if formaPagamento in lista_pagamento.keys():
            formaPagamento = lista_pagamento[int(formaPagamento)]
        df1 = pd.DataFrame(data= {'Data do Pedido' : data,'Id do Pedido' : pedidoId,'Forma de Pagamento' : formaPagamento}, index=[0] )
        if len(response1) != 50:
            iterador = False
        
        df = pd.concat([df,df1], ignore_index=True)
    pag += 1
        
df.to_csv('Data_Pedido X Forma_Pagamento.csv', sep=';',index=False)


# %%