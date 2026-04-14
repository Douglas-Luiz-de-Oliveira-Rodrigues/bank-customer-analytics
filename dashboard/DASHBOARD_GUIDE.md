# Dashboard — Guia de Implementação no Power BI

## Visão Geral

Este documento descreve como reproduzir o dashboard de análise de clientes bancários
no **Power BI Desktop** (gratuito) utilizando o arquivo `../data/clientes.csv`.

---

## Passo a Passo

### 1. Importar os Dados
1. Abra o **Power BI Desktop**
2. Clique em **Obter Dados → Texto/CSV**
3. Selecione o arquivo `data/clientes.csv`
4. Clique em **Carregar**

---

### 2. Criar Colunas Calculadas (DAX)

No painel **Dados**, clique com o botão direito na tabela e selecione
**Nova Coluna**. Adicione as seguintes fórmulas:

#### Faixa Etária
```dax
faixa_etaria =
SWITCH(
    TRUE(),
    clientes[idade] <= 25, "18-25",
    clientes[idade] <= 35, "26-35",
    clientes[idade] <= 45, "36-45",
    clientes[idade] <= 55, "46-55",
    "56+"
)
```

#### Status do Cliente
```dax
status_cliente =
IF(clientes[ativo] = 1, "Ativo", "Inativo")
```

#### Faixa de Score
```dax
faixa_score =
SWITCH(
    TRUE(),
    clientes[score_credito] < 400, "Muito Baixo",
    clientes[score_credito] < 550, "Baixo",
    clientes[score_credito] < 700, "Médio",
    clientes[score_credito] < 800, "Bom",
    "Excelente"
)
```

---

### 3. Criar Medidas DAX

Clique em **Nova Medida** e adicione:

```dax
Total Clientes = COUNTROWS(clientes)

Clientes Ativos = CALCULATE(COUNTROWS(clientes), clientes[ativo] = 1)

Clientes Inativos = CALCULATE(COUNTROWS(clientes), clientes[ativo] = 0)

% Ativos = DIVIDE([Clientes Ativos], [Total Clientes], 0)

Salário Médio = AVERAGE(clientes[salario])

Score Médio = AVERAGE(clientes[score_credito])
```

---

### 4. Montar os Visuais

#### Página 1 — Visão Geral

| Visual                  | Tipo              | Campos                                 |
|-------------------------|-------------------|----------------------------------------|
| Total de Clientes       | Cartão            | Medida: `Total Clientes`               |
| % Ativos                | Cartão            | Medida: `% Ativos` (formato: %)        |
| Salário Médio           | Cartão            | Medida: `Salário Médio` (formato: R$)  |
| Score Médio             | Cartão            | Medida: `Score Médio`                  |
| Ativos vs Inativos      | Gráfico de pizza  | Legenda: `status_cliente`, Valores: `Total Clientes` |
| Score por Status        | Gráfico de barras | Eixo: `status_cliente`, Valores: `Score Médio` |

#### Página 2 — Análise por Faixa

| Visual                     | Tipo              | Campos                                             |
|----------------------------|-------------------|----------------------------------------------------|
| Salário por Faixa Etária   | Gráfico de colunas | Eixo: `faixa_etaria`, Valores: `Salário Médio`   |
| Clientes por Faixa Etária  | Gráfico de barras  | Eixo: `faixa_etaria`, Valores: `Total Clientes`  |
| Distribuição de Score      | Histograma         | Campo: `score_credito`                            |
| Tabela Detalhada           | Tabela             | Colunas: todas                                    |

#### Página 3 — Análise de Risco

| Visual                     | Tipo              | Campos                                             |
|----------------------------|-------------------|----------------------------------------------------|
| Clientes por Faixa Score   | Gráfico de barras  | Eixo: `faixa_score`, Valores: `Total Clientes`   |
| Score vs Salário           | Gráfico de dispersão | Eixo X: `salario`, Eixo Y: `score_credito`, Legenda: `status_cliente` |
| Mapa de Calor (Tabela)     | Matriz             | Linhas: `faixa_etaria`, Colunas: `faixa_score`, Valores: `Total Clientes` |

---

### 5. Filtros e Segmentações

Adicione **Segmentações (Slicers)** para:
- `status_cliente` — filtrar por Ativo / Inativo
- `faixa_etaria` — filtrar por grupo de idade
- `faixa_score` — filtrar por risco de crédito

---

### 6. Tema e Cores Sugeridas

| Elemento        | Cor (Hex) |
|-----------------|-----------|
| Ativos          | `#2ecc71` |
| Inativos        | `#e74c3c` |
| Destaque azul   | `#3498db` |
| Cor primária    | `#2c3e50` |
| Fundo           | `#f4f6f9` |

---

### 7. Alternativas Gratuitas ao Power BI

Caso não tenha acesso ao Power BI, as visualizações podem ser criadas com:

- **Google Looker Studio** (gratuito, online) — importar via Google Sheets
- **Metabase** (open source, autohost)
- **Apache Superset** (open source)
- **Tableau Public** (gratuito para publicação online)

Os gráficos gerados pelo script Python estão disponíveis em:
- `graficos_analise.png` — visão geral (4 gráficos)
- `matriz_confusao.png` — resultado do modelo de ML

---

*Projeto: Análise de Clientes Bancários | Portfólio de Dados*
