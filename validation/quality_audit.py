import pandas as pd
from sqlalchemy import create_engine

# Conexão com o seu banco no Docker
engine = create_engine('postgresql://admin:admin_password@localhost:5432/postgres')

def run_audit():
    print("🔍 Iniciando Auditoria de Qualidade (Camada Silver)...")
    
    # 1. Extração: Lendo os dados brutos da Bronze
    df = pd.read_sql('SELECT * FROM stg_logistica', engine)
    total_records = len(df)
    
    # 2. Identificação de Erros
    # Regra 1: Pesos ou custos menores ou iguais a zero
    invalid_values = df[(df['weight'] <= 0) | (df['shipping_cost'] <= 0)]
    
    # Regra 2: IDs duplicados
    duplicates = df[df.duplicated(subset=['order_id'], keep=False)]
    
    # 3. Cálculo da Métrica de Engenharia
    # Registros com erro são a união de todos os problemas encontrados
    records_with_errors = pd.concat([invalid_values, duplicates]).drop_duplicates()
    valid_records_count = total_records - len(records_with_errors)
    
    quality_score = (valid_records_count / total_records) * 100
    
    # 4. Relatório Final
    print("-" * 30)
    print(f"📊 RELATÓRIO DE QUALIDADE LOGÍSTICA")
    print(f"✅ Registros Válidos: {valid_records_count}")
    print(f"❌ Registros com Falha: {len(records_with_errors)}")
    print(f"📌 Score de Confiança: {quality_score:.2f}%")
    print("-" * 30)
    
    if quality_score < 90:
        print("⚠️ ALERTA: Qualidade abaixo do SLA de 90%! Revisar processos de origem.")
    else:
        print("🟢 DADOS CONFIÁVEIS: Score dentro da meta.")

if __name__ == "__main__":
    run_audit()