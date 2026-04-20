import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

PATH_ARQUIVO = r"P:\PUBLICO\Contenção\Quarentena Controle\2026\controle_lancamento_seguro\REGISTROS_E_ CADASTROS DE PRODUTOS_LANÇAMENTO_SEGURO_CONTENÇÃO 13_02_26.xlsx"

def carregar_dados_reais():
    try:
        # 1. Localiza o cabeçalho
        df_raw = pd.read_excel(PATH_ARQUIVO)
        header_row = 0
        for i, row in df_raw.iterrows():
            if "Produto" in [str(v).strip() for v in row.values]:
                header_row = i + 1
                break
        
        df = pd.read_excel(PATH_ARQUIVO, skiprows=header_row)
        df.columns = [str(c).replace('\n', ' ').strip() for c in df.columns]
        
        c_prod = 'Produto'
        c_insp = 'Qtd Inspecionada'
        c_ruim_total = 'Qtd Ruim'
        
        df = df.dropna(subset=[c_prod])
        df[c_prod] = df[c_prod].astype(str).str.strip()
        
        # Converte colunas principais para número
        for c in [c_insp, c_ruim_total]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

        # 2. LÓGICA DOS PARES (Defeito X -> Qtd Defeito X)
        lista_defeitos = []
        # Percorremos os pares de 1 a 4 conforme a imagem
        for i in range(1, 5):
            col_nome = f'Defeito {i}'
            col_qtd = f'Qtd Defeito {i}'
            
            if col_nome in df.columns and col_qtd in df.columns:
                # Garantir que a coluna de quantidade do defeito seja numérica
                df[col_qtd] = pd.to_numeric(df[col_qtd], errors='coerce').fillna(0)
                
                # Filtrar apenas linhas onde o defeito existe e tem quantidade > 0
                for _, linha in df.iterrows():
                    nome_v = str(linha[col_nome]).strip()
                    qtd_v = linha[col_qtd]
                    
                    if nome_v.lower() != 'nan' and nome_v != '' and qtd_v > 0:
                        # Limpa o ".0" caso o defeito seja um código numérico
                        if nome_v.endswith('.0'): nome_v = nome_v[:-2]
                        
                        lista_defeitos.append({
                            'Produto': linha[c_prod],
                            'Descricao': nome_v,
                            'Quantidade': qtd_v
                        })
        
        return df, pd.DataFrame(lista_defeitos)
    except Exception as e:
        print(f"Erro na leitura: {e}")
        return None, None

app = Dash(__name__)

app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '20px'}, children=[
    dcc.Interval(id='intervalo', interval=300000, n_intervals=0), # 5 min
    
    html.H1("PRO-METAL - Safety Lauching", style={'textAlign': 'center', 'color': '#003366'}),
    html.Div(id='txt-update', style={'textAlign': 'right', 'color': 'gray'}),

    # Bloco de KPIs
    html.Div(id='kpis-content'),

    # Gráfico Detalhado
    html.Div(style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px', 'border': '1px solid #ddd'}, children=[
        html.H3("Quebra de Defeitos (Quantidade por Tipo)"),
        dcc.Dropdown(id='dropdown-prod', clearable=False, style={'width': '50%'}),
        dcc.Graph(id='grafico-detalhe')
    ]),

    # Gráfico Geral
    html.H3("Volume Geral por Produto", style={'marginTop': '40px'}),
    dcc.Graph(id='grafico-geral')
])

@app.callback(
    [Output('kpis-content', 'children'),
     Output('dropdown-prod', 'options'),
     Output('dropdown-prod', 'value'),
     Output('grafico-geral', 'figure'),
     Output('txt-update', 'children')],
    [Input('intervalo', 'n_intervals')],
    [Input('dropdown-prod', 'value')]
)
def atualizar_pagina(n, prod_sel):
    df, df_def = carregar_dados_reais()
    if df is None: return html.Div("Erro"), [], None, px.bar(), "Erro"
    
    # KPIs
    t_insp = df['Qtd Inspecionada'].sum()
    t_ruim = df['Qtd Ruim'].sum()
    
    kpis = html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '20px'}, children=[
        html.Div([html.B("INSPECIONADO"), html.H2(f"{t_insp:,.0f}")], style={'textAlign': 'center'}),
        html.Div([html.B("REFUGO TOTAL"), html.H2(f"{t_ruim:,.0f}", style={'color': 'red'})], style={'textAlign': 'center'}),
    ])
    
    prods = sorted(df['Produto'].unique())
    opcoes = [{'label': p, 'value': p} for p in prods]
    val = prod_sel if prod_sel in prods else prods[0]
    
    fig_g = px.bar(df.groupby('Produto')[['Qtd Inspecionada', 'Qtd Ruim']].sum().reset_index(),
                   x='Produto', y=['Qtd Inspecionada', 'Qtd Ruim'], barmode='group',
                   color_discrete_map={'Qtd Inspecionada': '#0055aa', 'Qtd Ruim': '#cc0000'})
    
    return kpis, opcoes, val, fig_g, f"Sincronizado: {pd.Timestamp.now().strftime('%H:%M:%S')}"

@app.callback(
    Output('grafico-detalhe', 'figure'),
    [Input('dropdown-prod', 'value'),
     Input('intervalo', 'n_intervals')]
)
def atualizar_defeitos(prod, n):
    df, df_def = carregar_dados_reais()
    if df_def is None or df_def.empty or not prod: return px.bar()
    
    # Pega o total do refugo para a barra de comparação
    total_refugo = df[df['Produto'] == prod]['Qtd Ruim'].sum()
    
    # Filtra e agrupa os defeitos capturados pela lógica de pares
    df_f = df_def[df_def['Produto'] == prod]
    df_agrup = df_f.groupby('Descricao', as_index=False)['Quantidade'].sum()
    
    # Cria o DataFrame para o gráfico
    df_plot = pd.concat([
        pd.DataFrame([{'Descricao': 'TOTAL GERAL', 'Quantidade': total_refugo}]),
        df_agrup.sort_values('Quantidade', ascending=True)
    ], ignore_index=True)

    fig = px.bar(df_plot, x='Quantidade', y='Descricao', orientation='h',
                 text='Quantidade', color='Descricao',
                 color_discrete_map={'TOTAL GERAL': '#333333'},
                 color_discrete_sequence=['#cc0000'])
    
    fig.update_layout(
        showlegend=False,
        yaxis={'type': 'category', 'autorange': 'reversed', 'title': ''},
        margin=dict(l=200)
    )
    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    
    return fig

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5004)