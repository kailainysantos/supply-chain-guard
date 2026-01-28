import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configuração visual da página
st.set_page_config(page_title="SupplyChainGuard Dashboard", layout="wide")

# Conexão com o banco (Docker)
engine = create_engine('postgresql://admin:admin_password@localhost:5432/postgres')

def load_data():
    # Busca o histórico de auditoria
    df_hist = pd.read_sql('SELECT * FROM tb_historico_qualidade ORDER BY data_execucao DESC', engine)
    # Busca os dados limpos (Gold)
    df_gold = pd.read_sql('SELECT * FROM gold_logistica_limpa', engine)
    return df_hist, df_gold

st.title("🛡️ SupplyChainGuard: Data Quality Dashboard")
st.markdown("Monitoramento de Integridade e SLA da Cadeia de Suprimentos")

try:
    df_hist, df_gold = load_data()
    latest = df_hist.iloc[0] # Pega a última auditoria realizada

    # --- LINHA 1: Métricas de Alto Nível ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Mostra o Score de Confiança
        st.metric("Data Quality Score", f"{latest['score_qualidade']}%", delta="SLA Target: 90%")
    with col2:
        st.metric("Total de Pedidos Processados", int(latest['total_processado']))
    with col3:
        st.metric("Registros Aprovados (Gold)", int(latest['registros_validos']))

    st.divider()

    # --- LINHA 2: Visualização de Dados e Auditoria ---
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📈 Evolução da Qualidade")
        # Gráfico de linha mostrando o histórico de scores
        st.line_chart(df_hist.set_index('data_execucao')['score_qualidade'])

    with col_right:
        st.subheader("🏆 Amostra de Dados Certificados (Gold)")
        st.write("Dados 100% auditados e prontos para o negócio.")
        st.dataframe(df_gold.head(10), use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar o dashboard: {e}")
    st.info("Dica: Certifique-se de que o Docker está ligado e você já rodou os scripts das fases anteriores.")