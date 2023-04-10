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
while iterador == True:
    url1 = f"https://api.fbits.net/pedidos?dataInicial={menos_uma_semana}&dataFinal={ontem}&pagina={pag}&valido=true"
    headers = {
        "accept": "application/json",
        "Authorization": "Basic ########"
    }

    response1 = re.get(url1, headers=headers)
    response1 = response1.json()
    for i in range(len(response1)):
        pedidoId = response1[i]['pedidoId']
        data = response1[i]['data']
        data = data.split('T')[0]
        dataPagamento = response1[i]['dataPagamento']
        try:
            dataPagamento = dataPagamento.split('T')[0]
        except:
            dataPagamento = '0000-00-00'
        Situacao = response1[i]['situacaoPedidoId']
        situacoes_pedidos = {
            
            1:"Pago",
            2: "Aguardando Pagamento",
            3: "Cancelado",
            4: "Cancelado",
            5: "Cancelado",
            6: "Cancelado",
            7: "Cancelado",
            8: "Cancelado",
            9: "Pedido Enviado",
            10: "Pedido Autorizado",
            11: "Em Preparação",
            12: "Pedido Devolvido",
            13: "Documentos Para Compra",
            14: "Pedido Aprovado Análise",
            15: "Recebido",
            16: "Separado",
            17 : 'Encomendado',
            18 : 'Entregue',
            19 : 'Aguardando troca de Pagamento',
            20 : 'Pedido Conferido',
            21 : 'Retirar na loja',
            22 : 'Pagamento Negado',
            23 : 'Entregue (Lista de Eventos)'
        }

        if Situacao in situacoes_pedidos.keys():
            Situacao = situacoes_pedidos[int(Situacao)]

        df1 = pd.DataFrame(data= {'Data do Pedido' : data,'Data de Pagamento' : dataPagamento,'Id do Pedido' : pedidoId,'Situação' : Situacao}, index=[0] )
        if len(response1) != 50:
            iterador = False
        
        df = pd.concat([df,df1], ignore_index=True)
    pag += 1
        
df.to_csv('Data_pagamento X Situação.csv', sep=';',index=False)

