import pandas as pd
import random
from datetime import datetime, timedelta

def generate_dirty_data(n=100):
    rows = []
    # Usamos o timestamp atual para simular diferentes momentos de auditoria
    now = datetime.now()
    
    for i in range(1, n + 1):
        order_id = random.randint(1000, 9999) + i
        sku = f"PROD-{random.randint(10, 99)}"
        weight = round(random.uniform(10.0, 500.0), 2)
        cost = round(weight * 2.1, 2)
        
        # --- MOTOR DE CAOS ALEATÓRIO ---
        # Isso garante que o seu gráfico de evolução suba e desça
        chance_de_erro = random.random()
        
        if chance_de_erro < 0.10:   # 10% de chance de peso zerado
            weight = 0.0
        elif chance_de_erro > 0.92: # 8% de chance de custo negativo
            cost = -25.0
        elif chance_de_erro > 0.45 and chance_de_erro < 0.48: # Pequena chance de ID duplicado
            order_id = 2001 

        rows.append([order_id, sku, weight, cost])
    
    df = pd.DataFrame(rows, columns=['order_id', 'sku', 'weight', 'shipping_cost'])
    df.to_csv('data/raw_logistics.csv', index=False)
    print(f"✅ [MENSAGEM]: Dados gerados com sucesso às {now.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    generate_dirty_data()