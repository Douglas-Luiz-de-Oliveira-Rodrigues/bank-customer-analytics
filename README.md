# 🏦 Análise de Clientes Bancários — Portfólio de Dados

> Projeto de portfólio simulando atividades reais da área de dados em um contexto bancário.
> Desenvolvi para demonstrar habilidades em **análise de dados**, **SQL**, **Python** e **Machine Learning**.

---

## 📌 Objetivo

Simular o ciclo completo de trabalho de um analista de dados júnior em uma instituição financeira, incluindo:

- Exploração e limpeza de dados de clientes
- Criação de variáveis analíticas (feature engineering)
- Consultas SQL para relatórios gerenciais
- Modelo preditivo de classificação de clientes
- Construção de dashboard executivo

---

## 🚀 Tecnologias Utilizadas

| Ferramenta       | Uso                                      |
|------------------|------------------------------------------|
| **Python 3.x**   | Análise de dados e Machine Learning      |
| **pandas**       | Manipulação e transformação de dados     |
| **scikit-learn** | Modelagem preditiva (Regressão Logística)|
| **matplotlib**   | Visualizações e gráficos                 |
| **SQL**          | Consultas analíticas                     |
| **Power BI**     | Dashboard executivo (instruções incluídas)|

---

## 📁 Estrutura do Projeto

```
banco-dados-portfolio/
│
├── data/
│   └── clientes.csv             # Base de dados fictícia (500 clientes)
│
├── sql/
│   └── consultas.sql            # Consultas SQL para análise gerencial
│
├── notebook/
│   └── analise_clientes.py      # Script completo de análise e ML
│
├── dashboard/
│   ├── DASHBOARD_GUIDE.md       # Guia passo a passo para Power BI
│   ├── graficos_analise.png     # Gráficos gerados pelo Python
│   └── matriz_confusao.png      # Resultado do modelo de ML
│
└── README.md                    # Este arquivo
```

---

## 📊 Base de Dados

O arquivo `data/clientes.csv` contém **500 registros fictícios** de clientes com as seguintes colunas:

| Coluna          | Tipo    | Descrição                                     |
|-----------------|---------|-----------------------------------------------|
| `id`            | inteiro | Identificador único do cliente                |
| `idade`         | inteiro | Idade do cliente (18–69 anos)                 |
| `salario`       | decimal | Salário mensal em reais                       |
| `score_credito` | inteiro | Score de crédito (300–900)                    |
| `ativo`         | binário | Status do cliente: 1 = Ativo, 0 = Inativo     |

---

## ⚙️ Como Executar

### Pré-requisitos

```bash
pip install pandas numpy matplotlib scikit-learn
```

### Executar a análise

```bash
cd notebook/
python analise_clientes.py
```

Os gráficos serão salvos automaticamente na pasta `dashboard/`.

---

## 🔍 Etapas do Projeto

### 1. Análise Exploratória (EDA)
- Estatísticas descritivas da base
- Verificação de valores nulos
- Distribuição de clientes ativos vs inativos

### 2. Engenharia de Variáveis
- **faixa_etaria**: categoriza clientes em grupos (18-25, 26-35, 36-45, 46-55, 56+)
- **faixa_score**: classifica o risco de crédito (Muito Baixo → Excelente)
- **faixa_salario**: quartis de renda (Baixo, Médio-Baixo, Médio-Alto, Alto)

### 3. Consultas SQL
- Média e distribuição de salários
- Filtros de clientes ativos com score acima da média
- Agrupamento por faixa etária com KPIs
- Análise de risco por faixa de score
- Resumo executivo consolidado

### 4. Machine Learning
- **Algoritmo**: Regressão Logística
- **Target**: Prever se o cliente é ativo (1) ou inativo (0)
- **Features**: idade, salário, score de crédito
- **Divisão**: 80% treino / 20% teste
- **Métricas**: acurácia, precision, recall, F1-score

### 5. Dashboard (Power BI)
- Cartões KPI: total de clientes, % ativos, salário médio, score médio
- Gráfico de pizza: ativos vs inativos
- Barras: salário por faixa etária e score por status
- Histograma: distribuição do score de crédito
- Dispersão: score vs salário por status
- Filtros interativos por status, faixa etária e score

---

## 📈 Resultados

| Métrica               | Valor                      |
|-----------------------|----------------------------|
| Total de clientes     | 500                        |
| Taxa de clientes ativos | ~75%                    |
| Salário médio         | R$ 5.770,47                |
| Score médio           | 598 pontos                 |
| Acurácia do modelo    | ~76%                       |

---

## 💡 Principais Insights

- Clientes com **score acima de 700** têm taxa de atividade significativamente maior
- A faixa etária **36-45 anos** concentra os maiores salários médios
- **Score de crédito** é a variável mais determinante para o status do cliente
- Clientes inativos apresentam score médio ~15% menor que os ativos

---

## 🎯 Contexto Bancário

Este projeto simula análises típicas realizadas em:

- **Inteligência de Clientes**: segmentação e perfil de base
- **Risco de Crédito**: predição de inadimplência e churn
- **Business Intelligence**: relatórios gerenciais e KPIs
- **CRM Bancário**: identificação de clientes de maior valor

---

## 👤 Autor

Desenvolvido como projeto de portfólio para área bancária/financeira.

- Habilidades demonstradas: Python, SQL, Machine Learning, Power BI, análise exploratória
- Área de interesse: Data Analytics, Credit Risk, Business Intelligence

---

*Dados totalmente fictícios, gerados para fins educacionais e de portfólio.*
