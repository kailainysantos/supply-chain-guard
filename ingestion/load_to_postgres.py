import pandas as pd
from sqlalchemy import create_engine

# 1. Configurar a conexão com o banco que subimos no Docker
# Formato: postgresql://usuario:senha@localhost:porta/nome_do_banco
engine = create_engine('postgresql://admin:admin_password@localhost:5432/postgres')

def run_ingestion():
    print("🚚 Iniciando transporte dos dados para o banco...")
    
    try:
        # 2. Ler o CSV que o seu gerador criou
        df = pd.read_csv('data/raw_logistics.csv')
        
        # 3. Mandar para o PostgreSQL
        # Criamos a tabela 'stg_logistica' (stg significa Staging, que é a camada Bronze)
        df.to_sql('stg_logistica', engine, if_exists='replace', index=False)
        
        print(f"✅ Sucesso! {len(df)} registros carregados na tabela 'stg_logistica'.")
    
    except Exception as e:
        print(f"❌ Erro na carga: {e}")

if __name__ == "__main__":
    run_ingestion()