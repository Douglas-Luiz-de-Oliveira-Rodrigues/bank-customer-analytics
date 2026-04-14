# ============================================================
# Projeto: Análise de Clientes Bancários
# Arquivo: analise_clientes.py
# Descrição: Análise exploratória + Machine Learning
# Autor: Douglas Rodrigues - Portfólio de Dados - Estágio Bancário
# ============================================================

# -------------------------------------------------------
# 0. IMPORTAÇÕES
# -------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.preprocessing import StandardScaler

print("=" * 60)
print("  ANÁLISE DE CLIENTES BANCÁRIOS — PORTFÓLIO DE DADOS")
print("=" * 60)


# -------------------------------------------------------
# 1. CARREGAMENTO DOS DADOS
# -------------------------------------------------------

print("\n[1] Carregando dados...")
df = pd.read_csv("../data/clientes.csv")

print(f"    ✔ {len(df)} registros carregados com sucesso.")
print(f"    Colunas: {list(df.columns)}")


# -------------------------------------------------------
# 2. ANÁLISE EXPLORATÓRIA (EDA)
# -------------------------------------------------------

print("\n[2] Análise Exploratória dos Dados\n")

# Descrição estatística
print("── Estatísticas Descritivas ──")
print(df.describe().round(2).to_string())

# Verificar valores nulos
print("\n── Valores Nulos por Coluna ──")
print(df.isnull().sum())

# Distribuição de clientes ativos vs inativos
total = len(df)
ativos = df['ativo'].sum()
inativos = total - ativos
print(f"\n── Distribuição de Status ──")
print(f"   Ativos  : {ativos:>4}  ({100*ativos/total:.1f}%)")
print(f"   Inativos: {inativos:>4}  ({100*inativos/total:.1f}%)")


# -------------------------------------------------------
# 3. ENGENHARIA DE VARIÁVEIS (FEATURE ENGINEERING)
# -------------------------------------------------------

print("\n[3] Criando novas variáveis...")

# Faixa etária
bins   = [0, 25, 35, 45, 55, 100]
labels = ['18-25', '26-35', '36-45', '46-55', '56+']
df['faixa_etaria'] = pd.cut(df['idade'], bins=bins, labels=labels, right=True)

# Faixa de score de crédito
def classifica_score(score):
    if score < 400:
        return 'Muito Baixo'
    elif score < 550:
        return 'Baixo'
    elif score < 700:
        return 'Médio'
    elif score < 800:
        return 'Bom'
    else:
        return 'Excelente'

df['faixa_score'] = df['score_credito'].apply(classifica_score)

# Faixa salarial
df['faixa_salario'] = pd.qcut(
    df['salario'],
    q=4,
    labels=['Baixo', 'Médio-Baixo', 'Médio-Alto', 'Alto']
)

print("    ✔ Variáveis criadas: faixa_etaria, faixa_score, faixa_salario")

# Estatísticas por faixa etária
print("\n── Métricas por Faixa Etária ──")
resumo_faixa = (
    df.groupby('faixa_etaria', observed=True)
      .agg(
          total=('id', 'count'),
          ativos=('ativo', 'sum'),
          media_salario=('salario', 'mean'),
          media_score=('score_credito', 'mean'),
      )
      .assign(pct_ativos=lambda x: (100 * x['ativos'] / x['total']).round(1))
)
resumo_faixa['media_salario'] = resumo_faixa['media_salario'].round(2)
resumo_faixa['media_score']   = resumo_faixa['media_score'].round(0)
print(resumo_faixa.to_string())


# -------------------------------------------------------
# 4. VISUALIZAÇÕES
# -------------------------------------------------------

print("\n[4] Gerando visualizações...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Análise de Clientes Bancários', fontsize=16, fontweight='bold', y=1.01)

cores_status = ['#e74c3c', '#2ecc71']

# --- Gráfico 1: Ativos vs Inativos ---
ax1 = axes[0, 0]
contagem = df['ativo'].value_counts()
ax1.bar(
    ['Inativos', 'Ativos'],
    [contagem.get(0, 0), contagem.get(1, 0)],
    color=cores_status,
    edgecolor='white',
    width=0.5,
)
ax1.set_title('Clientes Ativos vs Inativos', fontweight='bold')
ax1.set_ylabel('Quantidade')
for i, v in enumerate([contagem.get(0, 0), contagem.get(1, 0)]):
    ax1.text(i, v + 3, str(v), ha='center', fontweight='bold')
ax1.set_ylim(0, max(contagem.values) * 1.15)

# --- Gráfico 2: Distribuição de Score ---
ax2 = axes[0, 1]
ax2.hist(df['score_credito'], bins=20, color='#3498db', edgecolor='white', alpha=0.85)
ax2.axvline(df['score_credito'].mean(), color='#e74c3c', linestyle='--', linewidth=2,
            label=f"Média: {df['score_credito'].mean():.0f}")
ax2.set_title('Distribuição do Score de Crédito', fontweight='bold')
ax2.set_xlabel('Score de Crédito')
ax2.set_ylabel('Frequência')
ax2.legend()

# --- Gráfico 3: Salário médio por faixa etária ---
ax3 = axes[1, 0]
media_sal = df.groupby('faixa_etaria', observed=True)['salario'].mean().reset_index()
ax3.bar(
    media_sal['faixa_etaria'].astype(str),
    media_sal['salario'],
    color='#9b59b6',
    edgecolor='white',
)
ax3.set_title('Salário Médio por Faixa Etária', fontweight='bold')
ax3.set_xlabel('Faixa Etária')
ax3.set_ylabel('Salário Médio (R$)')
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R${x:,.0f}'))

# --- Gráfico 4: Score médio por status ---
ax4 = axes[1, 1]
score_status = df.groupby('ativo')['score_credito'].mean()
ax4.bar(
    ['Inativos', 'Ativos'],
    [score_status.get(0, 0), score_status.get(1, 0)],
    color=cores_status,
    edgecolor='white',
    width=0.5,
)
ax4.set_title('Score Médio por Status do Cliente', fontweight='bold')
ax4.set_ylabel('Score Médio')
for i, v in enumerate([score_status.get(0, 0), score_status.get(1, 0)]):
    ax4.text(i, v + 5, f'{v:.0f}', ha='center', fontweight='bold')
ax4.set_ylim(0, max(score_status.values) * 1.15)

plt.tight_layout()
plt.savefig('../dashboard/graficos_analise.png', dpi=150, bbox_inches='tight')
plt.close()
print("    ✔ Gráfico salvo em: dashboard/graficos_analise.png")


# -------------------------------------------------------
# 5. MODELO DE MACHINE LEARNING
# -------------------------------------------------------

print("\n[5] Treinando Modelo de Machine Learning...\n")

# Seleção de features e target
features = ['idade', 'salario', 'score_credito']
target   = 'ativo'

X = df[features]
y = df[target]

# Divisão treino/teste (80% / 20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"    Treino : {len(X_train)} amostras")
print(f"    Teste  : {len(X_test)} amostras")

# Normalização das features
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# Regressão Logística
modelo = LogisticRegression(random_state=42, max_iter=1000)
modelo.fit(X_train, y_train)

# Avaliação
y_pred   = modelo.predict(X_test)
acuracia = accuracy_score(y_test, y_pred)

print(f"\n── Resultados do Modelo ──")
print(f"   Algoritmo : Regressão Logística")
print(f"   Acurácia  : {acuracia * 100:.2f}%")
print(f"\n── Relatório de Classificação ──")
print(classification_report(y_test, y_pred, target_names=['Inativo', 'Ativo']))

# Importância das features (coeficientes)
print("── Importância das Variáveis (coeficientes) ──")
coefs = pd.Series(modelo.coef_[0], index=features).sort_values(ascending=False)
for feat, val in coefs.items():
    print(f"   {feat:<20}: {val:+.4f}")

# Matriz de Confusão
fig, ax = plt.subplots(figsize=(5, 4))
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Inativo', 'Ativo'])
disp.plot(ax=ax, colorbar=False, cmap='Blues')
ax.set_title(f'Matriz de Confusão — Acurácia: {acuracia*100:.1f}%', fontweight='bold')
plt.tight_layout()
plt.savefig('../dashboard/matriz_confusao.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n    ✔ Matriz de confusão salva em: dashboard/matriz_confusao.png")


# -------------------------------------------------------
# 6. RESUMO FINAL
# -------------------------------------------------------

print("\n" + "=" * 60)
print("  RESUMO EXECUTIVO")
print("=" * 60)
print(f"  Total de clientes   : {total}")
print(f"  Clientes ativos     : {ativos} ({100*ativos/total:.1f}%)")
print(f"  Clientes inativos   : {inativos} ({100*inativos/total:.1f}%)")
print(f"  Salário médio       : R$ {df['salario'].mean():,.2f}")
print(f"  Score médio         : {df['score_credito'].mean():.0f}")
print(f"  Idade média         : {df['idade'].mean():.1f} anos")
print(f"  Acurácia do modelo  : {acuracia*100:.2f}%")
print("=" * 60)
print("\n✅ Análise concluída com sucesso!")
