import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configuração da página e ícone
st.set_page_config(page_title="SupplyChainGuard | Auditoria", layout="wide", page_icon="🛡️")

# Estilo para as métricas e fundo
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetricValue"] { color: #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# Conexão com o Banco no Docker
engine = create_engine('postgresql://admin:admin_password@localhost:5432/postgres')

def load_data():
    # Histórico para o gráfico e dados limpos para a tabela
    df_hist = pd.read_sql('SELECT * FROM tb_historico_qualidade ORDER BY data_execucao ASC', engine)
    df_gold = pd.read_sql('SELECT * FROM gold_logistica_limpa ORDER BY order_id DESC LIMIT 15', engine)
    return df_hist, df_gold

st.title("🛡️ SupplyChainGuard: Data Observability")
st.markdown("---")

try:
    df_hist, df_gold = load_data()
    
    if not df_hist.empty:
        # Pega o último score registrado
        latest_audit = df_hist.iloc[-1]
        score = latest_audit['score_qualidade']
        
        # --- ALERTA DE STATUS (A "LUZ" DO SISTEMA) ---
        if score >= 90:
            st.success(f"✅ **SLA COMPLIANT:** A qualidade atual dos dados é de {score}%. O sistema está operando dentro da meta.")
        else:
            st.error(f"🚨 **DATA QUALITY ALERT:** O score caiu para {score}%. Inconsistências críticas detectadas na origem.")

        # --- LINHA 1: KPIs ---
        c1, c2, c3 = st.columns(3)
        c1.metric("Current DQ Score", f"{score}%", delta=f"{score - 90:.1f}% vs Target")
        c2.metric("Records Ingested", int(latest_audit['total_processado']))
        c3.metric("Verified Valid", int(latest_audit['registros_validos']))

        st.markdown("---")

        # --- LINHA 2: Gráfico e Tabela ---
        col_grafico, col_tabela = st.columns([1.3, 0.7])

        with col_grafico:
            st.markdown("### 📈 Evolução Histórica (Confiabilidade)")
            # Area chart para um visual preenchido e moderno
            st.area_chart(df_hist.set_index('data_execucao')['score_qualidade'], color="#00ffcc")

        with col_tabela:
            st.markdown("### 🏆 Camada Gold (Amostra)")
            st.write("Dados 100% auditados e prontos para o BI.")
            st.dataframe(df_gold, use_container_width=True, hide_index=True)
            
    else:
        st.info("Aguardando processamento do pipeline para exibir dados...")

except Exception as e:
    st.error(f"Erro de conexão: {e}")