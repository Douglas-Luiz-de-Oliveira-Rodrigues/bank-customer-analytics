-- ============================================================
-- Projeto: Análise de Clientes Bancários
-- Arquivo: consultas.sql
-- Descrição: Consultas SQL para análise exploratória dos dados
-- Autor: Douglas Rodrigues - Portfólio de Dados - Estágio Bancário
-- ============================================================


-- -------------------------------------------------------
-- 1. VISÃO GERAL DA BASE
-- -------------------------------------------------------

-- Total de clientes na base
SELECT COUNT(*) AS total_clientes
FROM clientes;


-- -------------------------------------------------------
-- 2. MÉDIA DE SALÁRIO
-- -------------------------------------------------------

-- Média geral de salário
SELECT
    ROUND(AVG(salario), 2) AS media_salario,
    ROUND(MIN(salario), 2) AS menor_salario,
    ROUND(MAX(salario), 2) AS maior_salario
FROM clientes;

-- Média de salário por status (ativo/inativo)
SELECT
    CASE WHEN ativo = 1 THEN 'Ativo' ELSE 'Inativo' END AS status_cliente,
    COUNT(*)                                             AS total,
    ROUND(AVG(salario), 2)                               AS media_salario,
    ROUND(AVG(score_credito), 0)                         AS media_score
FROM clientes
GROUP BY ativo
ORDER BY ativo DESC;


-- -------------------------------------------------------
-- 3. FILTRO DE CLIENTES ATIVOS
-- -------------------------------------------------------

-- Listar todos os clientes ativos
SELECT
    id,
    idade,
    salario,
    score_credito
FROM clientes
WHERE ativo = 1
ORDER BY score_credito DESC;

-- Clientes ativos com score acima da média
SELECT
    id,
    idade,
    salario,
    score_credito
FROM clientes
WHERE ativo = 1
  AND score_credito > (SELECT AVG(score_credito) FROM clientes)
ORDER BY score_credito DESC;


-- -------------------------------------------------------
-- 4. AGRUPAMENTO POR FAIXA ETÁRIA
-- -------------------------------------------------------

-- Classificação por faixa etária e métricas por grupo
SELECT
    CASE
        WHEN idade BETWEEN 18 AND 25 THEN '18-25'
        WHEN idade BETWEEN 26 AND 35 THEN '26-35'
        WHEN idade BETWEEN 36 AND 45 THEN '36-45'
        WHEN idade BETWEEN 46 AND 55 THEN '46-55'
        ELSE '56+'
    END                          AS faixa_etaria,
    COUNT(*)                     AS total_clientes,
    SUM(ativo)                   AS clientes_ativos,
    ROUND(AVG(salario), 2)       AS media_salario,
    ROUND(AVG(score_credito), 0) AS media_score
FROM clientes
GROUP BY faixa_etaria
ORDER BY faixa_etaria;


-- -------------------------------------------------------
-- 5. ANÁLISE DE RISCO DE CRÉDITO
-- -------------------------------------------------------

-- Distribuição por faixa de score de crédito
SELECT
    CASE
        WHEN score_credito < 400 THEN 'Muito Baixo (< 400)'
        WHEN score_credito < 550 THEN 'Baixo (400-549)'
        WHEN score_credito < 700 THEN 'Médio (550-699)'
        WHEN score_credito < 800 THEN 'Bom (700-799)'
        ELSE 'Excelente (800+)'
    END                    AS faixa_score,
    COUNT(*)               AS total,
    SUM(ativo)             AS ativos,
    ROUND(AVG(salario), 2) AS media_salario
FROM clientes
GROUP BY faixa_score
ORDER BY MIN(score_credito);


-- -------------------------------------------------------
-- 6. TOP CLIENTES
-- -------------------------------------------------------

-- Top 10 clientes por score de crédito
SELECT
    id,
    idade,
    ROUND(salario, 2) AS salario,
    score_credito,
    CASE WHEN ativo = 1 THEN 'Ativo' ELSE 'Inativo' END AS status
FROM clientes
ORDER BY score_credito DESC
LIMIT 10;


-- -------------------------------------------------------
-- 7. RESUMO EXECUTIVO
-- -------------------------------------------------------

-- Painel resumido para relatório gerencial
SELECT
    COUNT(*)                                             AS total_clientes,
    SUM(ativo)                                           AS total_ativos,
    COUNT(*) - SUM(ativo)                                AS total_inativos,
    ROUND(100.0 * SUM(ativo) / COUNT(*), 1)              AS pct_ativos,
    ROUND(AVG(salario), 2)                               AS media_salario,
    ROUND(AVG(score_credito), 0)                         AS media_score,
    ROUND(AVG(idade), 1)                                 AS media_idade
FROM clientes;
