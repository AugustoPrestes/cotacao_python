# Importações para o projeto
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.grid import grid

import numpy as np
import pandas as pd
from datetime import datetime 

import yfinance as yf

import plotly.express as px





# Função para construir o side bar
def build_sidebar():
    # Decoração do sidebar
    st.image('imagem/grafico.png')

    # Buscando o nome do papel
    tickers_list = pd.read_csv('tickers.csv', index_col=0)

    # Seleção do papel
    tickers = st.multiselect(label="Selecione o Papel", options=tickers_list)
    tickers = [t+".SA" for t in tickers]    # Colocando dentro do padrão da API

    # print(tickers_list.columns)
    # Escolha do intervalo do Pape
    start_date = st.date_input("De", format='DD/MM/YYYY', value=datetime(2023,1,1))
    end_date = st.date_input("Até", format='DD/MM/YYYY', value="today")

    if tickers:
        prices = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
        if len(tickers) == 1:
            prices = prices.to_frame()
            prices.columns = [tickers[0].rstrip(".SA")]

        prices.columns = prices.columns.str.rstrip(".SA")
        prices['IBOV'] = yf.download("^BVSP", start=start_date, end=end_date)['Adj Close']
        return tickers, prices 
    
    return None, None
    



# Função para construir o corpo da pagina
def build_main(tickers, prices):
    weights = np.ones(len(tickers))/len(tickers)
    prices['portfolio'] = prices.drop("IBOV", axis=1) @ weights 

    # normalizando os valores para à criação do gráfico
    norm_prices = 100 * prices / prices.iloc[0]
    returns = prices.pct_change()[1:]

    # Volatilidade do portifólio
    vol = returns.std()*np.sqrt(252)
    rets = (norm_prices.iloc[-1] - 100) / 100

    # Grid com o nome dos ativos
    mygrid = grid(5, 5, 5, 5, 5, 5, vertical_align='top')

    for t in prices.columns:
        container = mygrid.container(border=True)
        container.subheader(t, divider='red')

        # Divisores do container
        colA, colB, colC = container.columns(3)
        if t == "portfolio":
            colA.image("imagem/grafico.png")
        elif t == "IBOV":
            colA.image("images/pie-chart-svgrepo-com.svg")
        else:
            colA.image(f'https://raw.githubusercontent.com/thefintz/icones-b3/main/icones/{t}.png', width=85)

        colB.metric(label="Retorno", value=f"{rets[t]:.0%}")
        colC.metric(label="Volatilidade", value=f"{vol[t]:.0%}")

        style_metric_cards(background_color='rga(255,255,255, 0)')

    # Criando os gráficos
    col1, col2 = st.columns(2, gap='large')
    
    with col1:
        st.subheader('Desempenho Relativo')
        st.line_chart(norm_prices, height=600)

    with col2:
        st.subheader('Risco x Retorno')
        fig = px.scatter(
            x = vol, 
            y=rets,
            text=vol.index,
            color= rets/vol,
            color_continuous_scale=px.colors.sequential.Bluered_r
        )

        fig.update_traces(
            textfont_color = 'white',
            marker=dict(size=45),
            textfont_size=10
        )
        fig.layout.yaxis.title = 'Retorno Total'
        fig.layout.xaxis.title = 'Volatilidade (anualizada)'
        fig.layout.height = 600
        fig.layout.xaxis.tickformat = ".0%"
        fig.layout.yaxis.tickformat = ".0%"        
        fig.layout.coloraxis.colorbar.title = 'Sharpe'

        st.plotly_chart(fig, use_container_width=True)


    # Tabela com os papeis e o portifólio
    st.subheader('Tabela de fechamento')
    st.dataframe(prices)


# Configurando o Layout da pagina
# st.set_page_config(layout='wide')


with st.sidebar:
   tickers, prices = build_sidebar()


st.title("Investindo com Python")
if tickers:
    build_main(tickers, prices)