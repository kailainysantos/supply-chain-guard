import pandas as pd
from sqlalchemy import create_engine
import datetime

engine = create_engine('postgresql://admin:admin_password@localhost:5432/postgres')

def finalize_pipeline():
    print("✨ Iniciando refino para a Camada Gold...")
    
    # 1. Carregar dados da Bronze
    df = pd.read_sql('SELECT * FROM stg_logistica', engine)
    total = len(df)
    
    # 2. Filtrar apenas os registros que passam nas regras (Preço > 0 e Peso > 0)
    # E remover duplicatas de IDs
    df_clean = df[(df['weight'] > 0) & (df['shipping_cost'] > 0)].drop_duplicates(subset=['order_id'])
    valid_count = len(df_clean)
    score = (valid_count / total) * 100

    # 3. Salvar os dados LIMPOS na Camada Gold
    # Usamos 'replace' para ter sempre a versão mais atualizada e limpa
    df_clean.to_sql('gold_logistica_limpa', engine, if_exists='replace', index=False)
    
    # 4. Salvar o HISTÓRICO da auditoria (Metadados)
    historico = pd.DataFrame([{
        'total_processado': total,
        'registros_validos': valid_count,
        'score_qualidade': round(score, 2)
    }])
    historico.to_sql('tb_historico_qualidade', engine, if_exists='append', index=False)

    print("-" * 30)
    print(f"🏆 CAMADA GOLD ATUALIZADA")
    print(f"📊 {valid_count} registros de alta confiança persistidos.")
    print(f"📜 Histórico de auditoria registrado no banco.")
    print("-" * 30)

if __name__ == "__main__":
    finalize_pipeline()