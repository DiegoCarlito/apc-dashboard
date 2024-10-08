import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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

# Função para filtrar o ano do gráfico de matrículas
def filtrar_ano(df, ano_escolhido):
    return df[df['Ano'] == ano_escolhido].copy()

# Função para o gráfico de matrículas
def gerar_grafico_matriculas(ano_escolhido):
    df = pd.read_csv('./data/matriculas.csv')

    # Configurações do gráfico
    configuracoes = {"title": {"text": f"Matrículas escolares em {ano_escolhido}"}}

    fig = px.bar(filtrar_ano(df, ano_escolhido), x="Estado", y="Alunos", title=configuracoes["title"]["text"])

    fig.update_layout(margin=dict(l=50, r=50, t=50, b=50), title_x=0.5)
    return fig

# Função para gerar gráficos de despesas
def gerar_grafico_despesas(tipo_grafico):
    df = pd.read_csv('./data/despesas_inep.csv')

    # Converter os valores para o formato numérico, removendo vírgulas e pontos
    df['Valor Empenhado'] = df['Valor Empenhado'].replace({r"[.,]": ""}, regex=True).astype(float)
    df['Valor Pago'] = df['Valor Pago'].replace({r"[.,]": ""}, regex=True).astype(float)

    # Extrair o ano (apenas os últimos dois dígitos) da coluna 'Mês Ano'
    df['Ano'] = df['Mês Ano'].str[-2:]

    # Agrupar os valores empenhados e pagos por ano
    despesas_por_ano = df.groupby('Ano').agg({
        'Valor Empenhado': 'sum',
        'Valor Pago': 'sum'
    }).reset_index()

    # Ordenar os anos em ordem crescente
    despesas_por_ano = despesas_por_ano.sort_values(by='Ano')

    fig = go.Figure()

    if tipo_grafico == '1':  # Gráfico combinado
        fig.add_trace(go.Scatter(x=despesas_por_ano['Ano'], y=despesas_por_ano['Valor Pago'], mode='lines+markers', name='Valor Pago'))
        fig.add_trace(go.Scatter(x=despesas_por_ano['Ano'], y=despesas_por_ano['Valor Empenhado'], mode='lines+markers', name='Valor Empenhado'))
        titulo = 'Valores Pagos e Empenhados por Ano'
    
    elif tipo_grafico == '2':  # Apenas valor pago
        fig.add_trace(go.Scatter(x=despesas_por_ano['Ano'], y=despesas_por_ano['Valor Pago'], mode='lines+markers', name='Valor Pago'))
        titulo = 'Valores Pagos por Ano'

    elif tipo_grafico == '3':  # Apenas valor empenhado
        fig.add_trace(go.Scatter(x=despesas_por_ano['Ano'], y=despesas_por_ano['Valor Empenhado'], mode='lines+markers', name='Valor Empenhado'))
        titulo = 'Valores Empenhados por Ano'

    fig.update_yaxes(title='Valores (R$)', showgrid=True, gridwidth=1, gridcolor='lightgrey', showline=True, linewidth=1, linecolor='black')
    fig.update_xaxes(title='Anos', showgrid=True, gridwidth=1, gridcolor='lightgrey', showline=True, linewidth=1, linecolor='black')
    fig.update_layout(
        title=titulo,
        autosize=False,
        width=1200,
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_x=0.5)

    return fig

# Função para gerar gráfico da taxa de aprovação
def gerar_grafico_aprovacao():
    df = pd.read_csv('./data/aprovados.csv')

    # Converter colunas de aprovação em valores numéricos
    df[['1 Série', '2 Série', '3 Série', '4 Serie']] = df[['1 Série', '2 Série', '3 Série', '4 Serie']].apply(pd.to_numeric, errors='coerce')

    # Filtrar apenas as linhas do Brasil
    df_brasil = df[df['Unidade geográfica'] == 'Brasil']

    # Calcular a média de cada ano (média das quatro séries)
    df_brasil['Média Anual'] = df_brasil[['1 Série', '2 Série', '3 Série', '4 Serie']].mean(axis=1)

    # Criar o gráfico de pizza
    fig = go.Figure()

    fig.add_trace(go.Pie(labels=df_brasil['Ano'], values=df_brasil['Média Anual'], 
                        hoverinfo='label+percent', textinfo='value+percent'))

    fig.update_layout(
        title='Taxa de Aprovação no Ensino Médio (Média Anual - 2017 a 2021)',
        autosize=False,
        width=800,
        height=600,
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

    html.Div(
        dcc.Graph(id='grafico-enem'),
        style={'display': 'flex', 'justify-content': 'center'}
    ),

    html.Hr(),

    html.Div(
        dcc.Graph(id='grafico-pisa'),
        style={'display': 'flex', 'justify-content': 'center'}
    ),

    html.Hr(),

    dcc.Dropdown(
        id='opcao-ano',
        options=[
            {'label': '2019', 'value': 2019},
            {'label': '2022', 'value': 2022}
        ],
        value=2019
    ),

    html.Div(
        dcc.Graph(id='grafico-evasao'),
        style={'display': 'flex', 'justify-content': 'center'}
    ),

    html.Hr(),

    dcc.Dropdown(
        id='opcao-despesas',
        options=[
            {'label': 'Valores Pagos e Empenhados', 'value': '1'},
            {'label': 'Somente Valor Pago', 'value': '2'},
            {'label': 'Somente Valor Empenhado', 'value': '3'}
        ],
        value='1'
    ),

    html.Div(
        dcc.Graph(id='grafico-despesas'),
        style={'display': 'flex', 'justify-content': 'center'}
    ),

    html.Hr(),

    html.Div(
        dcc.Graph(id='grafico-aprovados'),
        style={'display': 'flex', 'justify-content': 'center'}
    )
])

@app.callback(
    Output('grafico-enem', 'figure'),
    [Input('opcao-grafico-enem', 'value')]
)
def update_grafico_enem(opcao):
    return grafico_enem_por_opcao(opcao)

@app.callback(
    Output('grafico-pisa', 'figure'),
    [Input('grafico-pisa', 'id')]
)
def update_grafico_pisa(_):
    return gerar_grafico_pisa()

@app.callback(
    Output('grafico-evasao', 'figure'),
    [Input('opcao-ano', 'value')]
)
def update_grafico_matriculas(opcao):
    return gerar_grafico_matriculas(opcao)

@app.callback(
    Output('grafico-despesas', 'figure'),
    [Input('opcao-despesas', 'value')]
)
def update_grafico_despesas(opcao):
    return gerar_grafico_despesas(opcao)

@app.callback(
    Output('grafico-aprovados', 'figure'),
    [Input('grafico-aprovados', 'id')]
)
def update_grafico_aprovados(_):
    return gerar_grafico_aprovacao()

if __name__ == '__main__':
    app.run_server(debug=True)
