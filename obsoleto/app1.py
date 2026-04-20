import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# --- CONFIGURAÇÃO DO ARQUIVO ---
PATH_ARQUIVO = r"P:\PUBLICO\Contenção\Quarentena Controle\2026\controle_lancamento_seguro\REGISTROS_E_ CADASTROS DE PRODUTOS_LANÇAMENTO_SEGURO_CONTENÇÃO 13_02_26.xlsx"

def carregar_dados():
    try:
        # Localiza o cabeçalho onde a coluna "Produto" existe
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
        c_ruim = 'Qtd Ruim'
        c_def_texto = 'Defeito 1' 

        # Limpeza de dados nulos
        df = df.dropna(subset=[c_prod])
        df[c_prod] = df[c_prod].astype(str).str.strip()
        
        # Converte para número (crucial para somar milhares corretamente)
        for col in [c_insp, c_ruim]:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Filtra base de defeitos (apenas linhas com defeito preenchido e qtd_ruim > 0)
        df[c_def_texto] = df[c_def_texto].astype(str).str.strip()
        df_com_defeito = df[
            (df[c_def_texto].str.lower() != 'nan') & 
            (df[c_def_texto] != '') & 
            (df[c_ruim] > 0)
        ].copy()
        
        return df, df_com_defeito, c_prod, c_insp, c_ruim, c_def_texto
    except Exception as e:
        print(f"Erro crítico: {e}")
        return pd.DataFrame(), pd.DataFrame(), None, None, None, None

# --- INICIALIZAÇÃO ---
df_base, df_defs, c_prod, c_insp, c_ruim, c_def_txt = carregar_dados()

app = Dash(__name__)

if df_base.empty:
    app.layout = html.Div([html.H1("Erro ao carregar planilha. Verifique o caminho P:/")])
else:
    lista_produtos = sorted([str(p) for p in df_base[c_prod].unique() if str(p) != 'nan'])

    app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '20px'}, children=[
        html.H1("PRO-METAL - Dashboard de Contenção", style={'textAlign': 'center', 'color': '#003366'}),
        
        # KPIs GERAIS
        html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '20px'}, children=[
            html.Div([
                html.B("TOTAL INSPECIONADO"), 
                html.H2(f"{df_base[c_insp].sum():,.0f}")
            ], style={'textAlign': 'center', 'padding': '20px', 'border': '1px solid #ddd', 'width': '30%', 'backgroundColor': '#f9f9f9'}),
            
            html.Div([
                html.B("TOTAL REFUGO"), 
                html.H2(f"{df_base[c_ruim].sum():,.0f}", style={'color': 'red'})
            ], style={'textAlign': 'center', 'padding': '20px', 'border': '1px solid #ddd', 'width': '30%', 'backgroundColor': '#f9f9f9'}),
            
            html.Div([
                html.B("PPM GERAL"), 
                html.H2(f"{(df_base[c_ruim].sum()/df_base[c_insp].sum()*1000000):,.0f}" if df_base[c_insp].sum() > 0 else "0")
            ], style={'textAlign': 'center', 'padding': '20px', 'border': '1px solid #ddd', 'width': '30%', 'backgroundColor': '#f9f9f9'}),
        ]),

        # GRÁFICO DE DEFEITOS (SOMA DE QUANTIDADES)
        html.Div(style={'backgroundColor': '#f4f7f6', 'padding': '20px', 'borderRadius': '10px', 'border': '1px solid #ddd'}, children=[
            html.H3("Quantidade de Peças por Tipo de Defeito"),
            dcc.Dropdown(
                id='filtro-prod',
                options=[{'label': p, 'value': p} for p in lista_produtos],
                value=lista_produtos[0] if lista_produtos else None,
                clearable=False,
                style={'width': '50%'}
            ),
            dcc.Graph(id='grafico-defeitos-texto')
        ]),

        # GRÁFICO GERAL (TODOS OS PRODUTOS)
        html.H3("Resumo de Volume: Todos os Produtos", style={'marginTop': '40px'}),
        dcc.Graph(
            figure=px.bar(
                df_base.groupby(c_prod)[[c_insp, c_ruim]].sum().reset_index(), # Sem o .head(15)
                x=c_prod, 
                y=[c_insp, c_ruim],
                barmode='group',
                title="Volume Inspecionado vs Quantidade Ruim (Total da Planilha)",
                color_discrete_map={c_insp: '#0055aa', c_ruim: '#cc0000'},
                height=600 # Altura maior para caber todos
            )
        )
    ])

    @app.callback(Output('grafico-defeitos-texto', 'figure'), Input('filtro-prod', 'value'))
    def update_defeitos(prod):
        # Filtra o produto
        df_f = df_defs[df_defs[c_prod] == prod]
        
        # IMPORTANTE: Aqui ele soma a coluna de quantidade ruim, não apenas conta a linha
        contagem = df_f.groupby(c_def_txt)[c_ruim].sum().reset_index()
        contagem.columns = ['Defeito', 'Total_Ruim']
        
        # Ordena para o maior ficar em cima
        contagem = contagem.sort_values('Total_Ruim', ascending=True)
        
        fig = px.bar(
            contagem, 
            x='Total_Ruim', 
            y='Defeito', 
            orientation='h',
            title=f"Total de Peças com Defeito: {prod}",
            text_auto='.0f', 
            color_discrete_sequence=['#cc0000']
        )
        return fig

if __name__ == '__main__':
    # Configuração para rodar no IP da rede e porta 5004
    print("Iniciando servidor em http://192.168.1.241:5004")
    app.run(debug=False, host='0.0.0.0', port=5004)