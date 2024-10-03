import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output

# Função para gerar gráficos do ENEM
def gerar_grafico_enem(df, colunas, titulo):
    fig = go.Figure()
    for coluna in colunas:
        fig.add_trace(go.Bar(x=df['Ano'], y=df[coluna], name=coluna))

    fig.update_yaxes(title='Média', showgrid=True, gridcolor='lightgrey', showline=True, linecolor='black')
    fig.update_xaxes(title='Anos', showgrid=True, gridcolor='lightgrey', showline=True, linecolor='black')
    fig.update_layout(
        title=titulo,
        autosize=False,
        width=800,
        height=500,
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white',
        barmode='group',
        title_x=0.5,
    )
    
    return fig

# Função principal para seleção dos gráficos do ENEM
def grafico_enem_por_opcao(opcao):
    df = pd.read_csv('./data/enem.csv')
    opcoes = {
        '1': gerar_grafico_enem(df, ['Média Ling.', 'Média C.H.', 'Média C.N.', 'Média Mat.', 'Média Red.', 'Total'], 'Média Geral do ENEM'),
        '2': gerar_grafico_enem(df, ['Média Ling.'], 'Média de Linguagens no ENEM'),
        '3': gerar_grafico_enem(df, ['Média C.H.'], 'Média de Ciências Humanas no ENEM'),
        '4': gerar_grafico_enem(df, ['Média C.N.'], 'Média de Ciências da Natureza no ENEM'),
        '5': gerar_grafico_enem(df, ['Média Mat.'], 'Média de Matemática no ENEM'),
        '6': gerar_grafico_enem(df, ['Média Red.'], 'Média de Redação no ENEM'),
        '7': gerar_grafico_enem(df, ['Total'], 'Média Total no ENEM')
    }
    return opcoes.get(opcao, gerar_grafico_enem(df, ['Total'], 'Média Total no ENEM'))

# Função para o gráfico PISA
def gerar_grafico_pisa():
    df = pd.read_csv('./data/pisa.csv')
    anos = ['PISA 2006', 'PISA 2009', 'PISA 2012', 'PISA 2015', 'PISA 2018']

    # Garantindo que os valores estão nas colunas corretas
    leitura = df[df['Competência'] == 'Leitura'].iloc[0, 1:].values
    matematica = df[df['Competência'] == 'Matemática'].iloc[0, 1:].values
    ciencia = df[df['Competência'] == 'Ciência'].iloc[0, 1:].values

    fig = go.Figure()

    fig.add_trace(go.Bar(x=anos, y=leitura, name='Leitura'))
    fig.add_trace(go.Bar(x=anos, y=matematica, name='Matemática'))
    fig.add_trace(go.Bar(x=anos, y=ciencia, name='Ciência'))

    fig.update_yaxes(title='Performance', showgrid=True, gridcolor='lightgrey', showline=True, linecolor='black')
    fig.update_xaxes(title='Anos', showgrid=True, gridcolor='lightgrey', showline=True, linecolor='black')
    fig.update_layout(
        title='Desempenho no PISA (2006 a 2018)', 
        autosize=False, 
        width=800, 
        height=500, 
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white',
        barmode='group',
        title_x=0.5)
    
    return fig

# App Dash
app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Dropdown(
        id='opcao-grafico-enem',
        options=[
            {'label': 'Média Geral', 'value': '1'},
            {'label': 'Linguagens', 'value': '2'},
            {'label': 'Ciências Humanas', 'value': '3'},
            {'label': 'Ciências da Natureza', 'value': '4'},
            {'label': 'Matemática', 'value': '5'},
            {'label': 'Redação', 'value': '6'},
            {'label': 'Total', 'value': '7'},
        ],
        value='1'
    ),
    dcc.Graph(id='grafico-enem'),
    
    html.Hr(),

    dcc.Graph(id='grafico-pisa')
])

@app.callback(
    Output('grafico-enem', 'figure'),
    [Input('opcao-grafico-enem', 'value')]
)
def update_grafico(opcao):
    return grafico_enem_por_opcao(opcao)

@app.callback(
    Output('grafico-pisa', 'figure'),
    [Input('grafico-pisa', 'id')]
)
def update_grafico_pisa(_):
    return gerar_grafico_pisa()

if __name__ == '__main__':
    app.run_server(debug=True)
