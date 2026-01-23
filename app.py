import streamlit as st
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Calculadora de Precificação", layout="wide")

# CSS para cards brancos individuais e estilização
st.markdown("""
    <style>
    .stApp { background-color: #F94F2F; }
    [data-testid="stVerticalBlock"] > div > [data-testid="stVerticalBlock"] {
        background-color: white !important;
        padding: 25px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        margin-bottom: 20px !important;
    }
    .header-box {
        background-color: white; padding: 20px; border-radius: 15px; border: 2px solid #333;
        text-align: center; margin-bottom: 30px; max-width: 500px; margin-left: auto; margin-right: auto;
    }
    .section-title { color: #5D5FEF !important; font-weight: bold !important; text-transform: uppercase; margin-bottom: 15px !important; font-size: 1.1rem !important; }
    .stNumberInput label p { color: #333 !important; font-weight: bold !important; }
    .res-card { padding: 12px; border-radius: 10px; color: white; margin-bottom: 8px; }
    .res-card small { font-weight: bold; text-transform: uppercase; font-size: 0.7rem; display: block; }
    .res-card b { font-size: 1.4rem; display: block; margin: 2px 0; }
    .res-card .subtitle { font-size: 0.65rem; opacity: 0.9; font-weight: normal; }
    .stButton > button { width: 100%; background-color: #6C63FF; color: white; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0; color: #111; font-size: 1.8rem;'>CALCULADORA DE PRECIFICAÇÃO</h1>
        <p style='color: #666; margin:0;'>Jefferson & Nayla</p>
    </div>
""", unsafe_allow_html=True)

col_dados, col_res = st.columns([1.8, 1.2], gap="large")

with col_dados:
    with st.container():
        st.markdown('<p class="section-title">📋 DADOS PRINCIPAIS</p>', unsafe_allow_html=True)
        custo_prod = st.number_input("Preço de Custo (R$)", value=25.00, step=0.01)
        custo_emb = st.number_input("Preço de Embalagem (R$)", value=0.50, step=0.01)
        imposto_perc = st.number_input("Impostos (%)", value=3.99, step=0.01) / 100

    with st.container():
        st.markdown('<p class="section-title">⚖️ PRECIFICAÇÃO E TAXAS</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        comissao_shopee = st.number_input("Comissão Shopee (%)", value=20.00, step=0.1) / 100
        taxa_fixa = st.number_input("Taxa Fixa (R$)", value=4.00, step=0.01)
        
        with c1:
            lucro_desejado_perc = st.number_input("Lucro Desejado (%)", value=0.0, step=0.1) / 100
        with c2:
            if lucro_desejado_perc > 0:
                divisor = (1 - comissao_shopee - imposto_perc - lucro_desejado_perc)
                pv_calculado = (custo_prod + custo_emb + taxa_fixa) / divisor if divisor > 0 else 0.0
            else:
                pv_calculado = 70.00
            preco_venda = st.number_input("Preço de Venda Desejado (R$)", value=float(pv_calculado), step=0.01)

    with st.container():
        st.markdown('<p class="section-title">📊 SIMULADOR DE VENDAS</p>', unsafe_allow_html=True)
        vendas = st.number_input("Número de Vendas", value=1, min_value=1)

    st.button("Calcular Preços")

# --- LÓGICA DE CÁLCULO ---
v_imposto = preco_venda * imposto_perc
v_comissao = preco_venda * comissao_shopee
liquido = preco_venda - v_imposto - v_comissao - taxa_fixa
lucro_real = liquido - (custo_prod + custo_emb)
margem_real = (lucro_real / preco_venda) * 100 if preco_venda > 0 else 0
roas_min = preco_venda / lucro_real if lucro_real > 0 else 0

# --- DADOS DO GRÁFICO ---
val_custos = custo_prod + custo_emb
val_taxas = v_imposto + v_comissao + taxa_fixa
val_ads = lucro_real if lucro_real > 0 else 0

with col_res:
    with st.container():
        st.markdown('<p class="section-title">📈 RESULTADOS</p>', unsafe_allow_html=True)
        
        res_list = [
            {"label": "Preço de Venda", "val": f"R$ {preco_venda:.2f}", "sub": "", "color": "#0FA6A6"},
            {"label": "Líquido a Receber", "val": f"R$ {liquido:.2f}", "sub": "", "color": "#14A653"},
            {"label": "Lucro Real", "val": f"R$ {lucro_real:.2f}", "sub": "", "color": "#914BF2"},
            {"label": "% de Lucro", "val": f"{margem_real:.2f}%", "sub": "", "color": "#F2790F"},
            {"label": "Simulação de Vendas", "val": f"R$ {lucro_real * vendas:.2f}", "sub": f"{vendas} vendas", "color": "#0FA6A6"},
            {"label": "Máximo para ADS", "val": f"R$ {lucro_real:.2f}", "sub": "Valor total do lucro real", "color": "#F2387C"},
            {"label": "ROAS Mínimo", "val": f"{roas_min:.2f}x", "sub": "Retorno sobre investimento em ADS", "color": "#0FA6A6"}
        ]

        for r in res_list:
            st.markdown(f'<div class="res-card" style="background-color:{r["color"]};"><small>{r["label"]}</small><b>{r["val"]}</b><div class="subtitle">{r["sub"]}</div></div>', unsafe_allow_html=True)

    # --- CARD DO GRÁFICO (ANÁLISE VISUAL) ---
    with st.container():
        st.markdown('<p class="section-title">📊 ANÁLISE VISUAL</p>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Pie(
            labels=['Custos', 'Impostos & Taxas', 'Orçamento ADS'],
            values=[val_custos, val_taxas, val_ads],
            hole=.3,
            marker_colors=['#FF4B4B', '#FFAA00', '#7D3CFF'],
            # Configuração do Popup (Hover) com R$ e 2 casas decimais
            hovertemplate="<b>%{label}</b><br>Valor: R$ %{value:.2f}<br>Percentual: %{percent}<extra></extra>"
        )])
        
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            height=250,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<p style='color: white; font-size: 0.7rem; margin-top: 20px;'>Condições e Suporte | Política de Privacidade</p>", unsafe_allow_html=True)