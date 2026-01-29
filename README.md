# 🛡️ SupplyChainGuard: Logistics Data Quality Framework

![SupplyChainGuard Dashboard](dashboard_preview1.png)

> *Dashboard de Observabilidade exibindo um Alerta de Qualidade (Score: 86%) e a evolução histórica da integridade dos dados.*

O **SupplyChainGuard** é um projeto de Engenharia de Dados focado em **DQaaP (Data Quality as a Product)**. Ele simula um ecossistema de governança para uma empresa de logística, garantindo que apenas dados confiáveis cheguem ao usuário final. 

Este projeto utiliza a **Arquitetura Medalhão** para processar e auditar registros de transporte, tratando inconsistências como pesos zerados e duplicidade de pedidos.

---

## 🏗️ Arquitetura do Pipeline

O projeto foi construído sobre uma infraestrutura dockerizada, seguindo o fluxo de camadas:

| Camada | Tabela SQL | Objetivo |
| :--- | :--- | :--- |
| **Bronze** | `stg_logistica` | Armazenamento de dados brutos (Staging) recém-ingeridos. |
| **Silver** | `Auditoria` | Camada de processamento onde as regras de qualidade são aplicadas. |
| **Gold** | `gold_logistica_limpa` | Dados certificados, higienizados e prontos para o BI/Dashboard. |

---

## ⚖️ Métrica de Data Quality (DQ Score)

A confiabilidade dos dados é medida através de um algoritmo de auditoria que calcula o índice de conformidade dos registros:

$$Score = \left( \frac{\text{Registros Válidos}}{\text{Total de Registros}} \right) \times 100$$

Se o Score de Confiança cair abaixo de **90%**, o sistema emite um alerta de integridade (como visto na imagem acima), garantindo a governança do produto de dados.

---

## 🛠️ Tecnologias e Ferramentas

* **Linguagem:** Python 3.x (Pandas, SQLAlchemy).
* **Banco de Dados:** PostgreSQL 13 (Docker).
* **Infraestrutura:** Docker & Docker Compose.
* **Frontend/Dashboard:** Streamlit.

---

## 📂 Estrutura do Repositório

* `ingestion/`: Scripts de geração de dados sintéticos e carga inicial (Bronze).
* `validation/`: O "coração" do projeto. Contém o motor de auditoria e persistência (Silver/Gold).
* `dashboard/`: Interface visual para monitoramento das métricas de qualidade.
* `data/`: Armazenamento local de arquivos temporários (ignorado pelo .gitignore).

---

## 🚀 Como Executar

1.  **Inicie o ambiente Docker:**
    ```bash
    docker-compose up -d
    ```

2.  **Gere e carregue os dados brutos:**
    ```bash
    python ingestion/supply_generator.py
    python ingestion/load_to_postgres.py
    ```

3.  **Execute a auditoria e gere a Camada Gold:**
    ```bash
    python validation/persistence_gold.py
    ```

4.  **Inicie o Dashboard:**
    ```bash
    streamlit run dashboard/app.py
    ```

---
Estudante de TI & Aspirante a Engenheira de Dados. Focada em transformar dados brutos em ativos de valor estratégico.

---
