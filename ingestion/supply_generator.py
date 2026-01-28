import pandas as pd
import random
from datetime import datetime, timedelta

def generate_dirty_data(n=100):
    rows = []
    for i in range(1, n + 1):
        order_id = 2000 + i
        sku = f"PROD-{random.randint(10, 99)}"
        weight = round(random.uniform(2.0, 450.0), 2)
        cost = round(weight * 1.8, 2)
    
        # Inserindo Erros Críticos (O que o seu projeto vai detectar)
        if i % 12 == 0: weight = 0.0          # Peso inválido
        if i % 20 == 0: cost = -50.0          # Custo impossível
        if i == 50: order_id = 2049           # ID Duplicado

        rows.append([order_id, sku, weight, cost])
    
    df = pd.DataFrame(rows, columns=['order_id', 'sku', 'weight', 'shipping_cost'])
    df.to_csv('data/raw_logistics.csv', index=False)
    print("✅ Arquivo 'data/raw_logistics.csv' gerado com falhas para teste.")

if __name__ == "__main__":
    generate_dirty_data()