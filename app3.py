import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output

# Caminho do seu arquivo
PATH_ARQUIVO = r"P:\PUBLICO\Contenção\Quarentena Controle\2026\controle_lancamento_seguro\REGISTROS_E_ CADASTROS DE PRODUTOS_LANÇAMENTO_SEGURO_CONTENÇÃO 13_02_26.xlsx"


def carregar_dados_reais():
    try:
        df_raw = pd.read_excel(PATH_ARQUIVO)
        header_row = 0
        for i, row in df_raw.iterrows():
            if "Produto" in [str(v).strip() for v in row.values]:
                header_row = i + 1
                break

        df = pd.read_excel(PATH_ARQUIVO, skiprows=header_row)
        df.columns = [str(c).replace("\n", " ").strip() for c in df.columns]

        c_prod, c_insp, c_ruim_total, c_data = "Produto", "Qtd Inspecionada", "Qtd Ruim", "Data"

        df = df.dropna(subset=[c_prod])
        df[c_prod] = df[c_prod].astype(str).str.strip()
        df[c_data] = pd.to_datetime(df[c_data], errors="coerce")

        for c in [c_insp, c_ruim_total]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        lista_defeitos = []
        for i in range(1, 5):
            col_n, col_q = f"Defeito {i}", f"Qtd Defeito {i}"
            if col_n in df.columns and col_q in df.columns:
                df[col_q] = pd.to_numeric(df[col_q], errors="coerce").fillna(0)
                for _, linha in df.iterrows():
                    nome_v, qtd_v = str(linha[col_n]).strip(), linha[col_q]
                    if nome_v.lower() != "nan" and nome_v != "" and qtd_v > 0:
                        if nome_v.endswith(".0"):
                            nome_v = nome_v[:-2]
                        lista_defeitos.append(
                            {"Produto": linha[c_prod], "Descricao": nome_v, "Quantidade": qtd_v}
                        )

        return df, pd.DataFrame(lista_defeitos)
    except Exception as e:
        print(f"Erro na leitura: {e}")
        return None, None


app = Dash(__name__)
app.title = "PRO-METAL - Safety Launch"

CORES = {
    "azul_escuro": "#0c2340",
    "azul": "#0f4c81",
    "azul_claro": "#2d78c4",
    "card": "#ffffff",
    "borda": "#d6e0ea",
    "texto": "#17212b",
    "texto_suave": "#5e6b78",
    "vermelho": "#d62828",
    "verde": "#2e8b57",
    "laranja": "#ff8c00",
}

ESTILO_CARD = {
    "backgroundColor": CORES["card"],
    "borderRadius": "18px",
    "padding": "22px",
    "border": f"1px solid {CORES['borda']}",
    "boxShadow": "0 10px 30px rgba(12, 35, 64, 0.08)",
}

app.layout = html.Div(
    style={
        "fontFamily": '"Segoe UI", Tahoma, sans-serif',
        "background": "linear-gradient(180deg, #f7fafc 0%, #eef3f8 45%, #e6edf5 100%)",
        "minHeight": "100vh",
        "padding": "24px",
    },
    children=[
        dcc.Interval(id="intervalo", interval=300000, n_intervals=0),
        html.Div(
            style={
                "maxWidth": "1380px",
                "margin": "0 auto",
                "display": "flex",
                "flexDirection": "column",
                "gap": "24px",
            },
            children=[
                html.Div(
                    style={
                        "background": "linear-gradient(135deg, #0c2340 0%, #0f4c81 60%, #2d78c4 100%)",
                        "borderRadius": "24px",
                        "padding": "24px 30px",
                        "boxShadow": "0 18px 40px rgba(12, 35, 64, 0.22)",
                        "color": "white",
                    },
                    children=[
                        html.Div(
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "center",
                                "gap": "20px",
                                "flexWrap": "wrap",
                            },
                            children=[
                                html.Div(
                                    style={"display": "flex", "alignItems": "center", "gap": "18px"},
                                    children=[
                                        html.Img(
                                            src=app.get_asset_url("logo.png"),
                                            style={
                                                "height": "82px",
                                                "width": "auto",
                                                "backgroundColor": "rgba(255, 255, 255, 0.96)",
                                                "padding": "10px 14px",
                                                "borderRadius": "18px",
                                                "boxShadow": "0 10px 24px rgba(0, 0, 0, 0.18)",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                html.H1(
                                                    "Safety Launch",
                                                    style={
                                                        "margin": "0",
                                                        "fontSize": "34px",
                                                        "fontWeight": "700",
                                                        "letterSpacing": "0.5px",
                                                    },
                                                ),
                                                html.P(
                                                    "Painel de inspeção, contenção e acompanhamento de refugo por produto.",
                                                    style={
                                                        "margin": "8px 0 0 0",
                                                        "fontSize": "15px",
                                                        "color": "rgba(255, 255, 255, 0.85)",
                                                    },
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="txt-update",
                                    style={
                                        "textAlign": "right",
                                        "fontSize": "13px",
                                        "padding": "10px 14px",
                                        "borderRadius": "14px",
                                        "backgroundColor": "rgba(255, 255, 255, 0.12)",
                                        "border": "1px solid rgba(255, 255, 255, 0.18)",
                                    },
                                ),
                            ],
                        )
                    ],
                ),
                html.Div(id="kpis-content"),
                html.Div(
                    style=ESTILO_CARD,
                    children=[
                        html.H3(
                            "Análise de Defeitos por Produto",
                            style={"margin": "0", "color": CORES["azul_escuro"], "fontSize": "24px"},
                        ),
                        html.P(
                            "Selecione um produto para visualizar o total de refugo e o detalhamento dos principais defeitos.",
                            style={"margin": "8px 0 18px 0", "color": CORES["texto_suave"]},
                        ),
                        dcc.Dropdown(
                            id="dropdown-prod",
                            clearable=False,
                            style={"maxWidth": "420px", "marginBottom": "18px"},
                        ),
                        dcc.Graph(id="grafico-detalhe", config={"displayModeBar": False}),
                    ],
                ),
                html.Div(
                    style=ESTILO_CARD,
                    children=[
                        html.H3(
                            "Visão Geral de Inspeção vs Refugo",
                            style={"margin": "0", "color": CORES["azul_escuro"], "fontSize": "24px"},
                        ),
                        html.P(
                            "Comparativo consolidado por produto com escalas independentes para inspeção e refugo.",
                            style={"margin": "8px 0 18px 0", "color": CORES["texto_suave"]},
                        ),
                        dcc.Graph(id="grafico-geral", config={"displayModeBar": False}),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    [
        Output("kpis-content", "children"),
        Output("dropdown-prod", "options"),
        Output("dropdown-prod", "value"),
        Output("grafico-geral", "figure"),
        Output("txt-update", "children"),
    ],
    [Input("intervalo", "n_intervals")],
    [Input("dropdown-prod", "value")],
)
def atualizar_pagina(n, prod_sel):
    df, df_def = carregar_dados_reais()
    if df is None:
        return html.Div("Erro"), [], None, go.Figure(), "Erro"

    prods = sorted(df["Produto"].unique())
    opcoes = [{"label": p, "value": p} for p in prods]
    val = prod_sel if prod_sel in prods else (prods[0] if prods else None)

    hoje = pd.Timestamp.now().normalize()
    df_p = df[df["Produto"] == val].sort_values("Data", ascending=False)
    falhas = df_p[df_p["Qtd Ruim"] > 0]
    ultima_f = falhas["Data"].max() if not falhas.empty else df_p["Data"].min()
    dias = (hoje - ultima_f).days if pd.notnull(ultima_f) else 0
    cor = CORES["verde"] if dias >= 90 else CORES["laranja"]
    txt_status = f"LIBERADO ({dias} Dias OK)" if dias >= 90 else f"EM CONTENÇÃO ({dias}/90 Dias)"

    kpis = html.Div(
        style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(240px, 1fr))",
            "gap": "20px",
        },
        children=[
            html.Div(
                style=ESTILO_CARD,
                children=[
                    html.Div(
                        "INSPECIONADO TOTAL",
                        style={"color": CORES["texto_suave"], "fontWeight": "600", "letterSpacing": "0.6px"},
                    ),
                    html.H2(
                        f"{df['Qtd Inspecionada'].sum():,.0f}",
                        style={"margin": "10px 0 0 0", "color": CORES["azul_escuro"], "fontSize": "34px"},
                    ),
                ],
            ),
            html.Div(
                style={
                    **ESTILO_CARD,
                    "border": f"2px solid {cor}",
                    "background": f"linear-gradient(135deg, {cor}10 0%, #ffffff 80%)",
                },
                children=[
                    html.Div(
                        f"STATUS: {val}",
                        style={"color": CORES["texto_suave"], "fontWeight": "600", "letterSpacing": "0.6px"},
                    ),
                    html.H2(txt_status, style={"margin": "10px 0 0 0", "color": cor, "fontSize": "28px"}),
                ],
            ),
            html.Div(
                style=ESTILO_CARD,
                children=[
                    html.Div(
                        "REFUGO TOTAL",
                        style={"color": CORES["texto_suave"], "fontWeight": "600", "letterSpacing": "0.6px"},
                    ),
                    html.H2(
                        f"{df['Qtd Ruim'].sum():,.0f}",
                        style={"margin": "10px 0 0 0", "color": CORES["vermelho"], "fontSize": "34px"},
                    ),
                ],
            ),
        ],
    )

    df_g = df.groupby("Produto")[["Qtd Inspecionada", "Qtd Ruim"]].sum().reset_index()
    fig_g = make_subplots(specs=[[{"secondary_y": True}]])

    fig_g.add_trace(
        go.Bar(
            x=df_g["Produto"],
            y=df_g["Qtd Inspecionada"],
            name="Inspecionado",
            marker_color=CORES["azul"],
            text=df_g["Qtd Inspecionada"],
            textposition="auto",
            offsetgroup=1,
        ),
        secondary_y=False,
    )

    fig_g.add_trace(
        go.Bar(
            x=df_g["Produto"],
            y=df_g["Qtd Ruim"],
            name="Refugo",
            marker_color=CORES["vermelho"],
            text=df_g["Qtd Ruim"],
            textposition="outside",
            offsetgroup=2,
        ),
        secondary_y=True,
    )

    fig_g.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=20, b=30),
        font=dict(color=CORES["texto"]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis={"title": "Produtos"},
        yaxis={"title": "Qtd Inspecionada", "rangemode": "tozero"},
        yaxis2={"title": "Qtd Ruim", "rangemode": "tozero", "overlaying": "y", "side": "right"},
    )
    fig_g.update_xaxes(showgrid=False)
    fig_g.update_yaxes(gridcolor="rgba(12, 35, 64, 0.08)")

    return kpis, opcoes, val, fig_g, f"Sincronizado: {pd.Timestamp.now().strftime('%H:%M:%S')}"


@app.callback(
    Output("grafico-detalhe", "figure"),
    [Input("dropdown-prod", "value"), Input("intervalo", "n_intervals")],
)
def atualizar_defeitos(prod, n):
    df, df_def = carregar_dados_reais()
    if df_def is None or df_def.empty or not prod:
        return px.bar()

    total_refugo = df[df["Produto"] == prod]["Qtd Ruim"].sum()
    df_f = df_def[df_def["Produto"] == prod].groupby("Descricao", as_index=False)["Quantidade"].sum()

    df_plot = pd.concat(
        [
            pd.DataFrame([{"Descricao": "TOTAL GERAL", "Quantidade": total_refugo}]),
            df_f.sort_values("Quantidade", ascending=True),
        ],
        ignore_index=True,
    )

    fig = px.bar(
        df_plot,
        x="Quantidade",
        y="Descricao",
        orientation="h",
        text="Quantidade",
        color="Descricao",
        color_discrete_map={"TOTAL GERAL": CORES["azul_escuro"]},
        color_discrete_sequence=[CORES["vermelho"]],
    )
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=20, b=30),
        font=dict(color=CORES["texto"]),
        yaxis={"type": "category", "autorange": "reversed", "title": ""},
    )
    fig.update_xaxes(gridcolor="rgba(12, 35, 64, 0.08)", title="")
    fig.update_traces(textposition="outside")
    return fig


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5004)
