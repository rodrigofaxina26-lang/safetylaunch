# Relatorio de Projeto: Safety Launch

## 1. Visao geral

O **Safety Launch** e um painel de acompanhamento desenvolvido para apoiar o controle de produtos em fase de lancamento, com foco em inspecao, contencao, monitoramento de refugo e tomada de decisao baseada em dados.

O projeto transforma registros operacionais de uma planilha corporativa em um dashboard interativo, permitindo que a equipe visualize rapidamente indicadores de qualidade por produto, acompanhe o status de liberacao apos 90 dias sem falhas e identifique os principais defeitos encontrados durante o processo de inspecao.

## 2. Contexto do problema

Em processos de lancamento de produtos, e comum que as informacoes de inspecao fiquem concentradas em planilhas, dificultando a leitura rapida de indicadores importantes como:

- Quantidade total inspecionada.
- Quantidade de pecas refugadas.
- Horas consumidas em inspecao.
- Principais defeitos por produto.
- Status de contencao ou liberacao.
- Historico de falhas por data.

Antes de um painel estruturado, a analise dependia de consultas manuais, filtros em planilhas e interpretacao individual dos registros. Isso aumentava o tempo de resposta e dificultava a padronizacao do acompanhamento entre produtos.

## 3. Objetivo do programa

O objetivo principal do Safety Launch e **centralizar e automatizar o acompanhamento de produtos em lancamento**, oferecendo uma visao clara do desempenho de qualidade e do andamento da contencao.

Objetivos especificos:

- Automatizar a leitura da base de registros de lancamento seguro.
- Padronizar dados mesmo quando houver variacoes nos nomes das colunas.
- Consolidar indicadores de inspecao, refugo e horas.
- Exibir status automatico de cada produto com base na regra de 90 dias sem falha.
- Permitir filtro por produto e por mes.
- Detalhar os defeitos mais recorrentes por item.
- Facilitar a comunicacao dos resultados para qualidade, producao e gestao.

## 4. Solucao desenvolvida

Foi desenvolvido um dashboard web em Python utilizando **Dash**, **Pandas** e **Plotly**. A aplicacao le uma planilha de registros de inspecao, trata os dados, gera indicadores consolidados e apresenta as informacoes em uma interface visual.

A solucao conta com:

- Cabecalho institucional com identidade visual da empresa.
- Atualizacao automatica a cada 5 minutos.
- Indicadores de desempenho em cards.
- Grafico comparativo de quantidade inspecionada versus refugo.
- Analise detalhada de defeitos por produto.
- Filtros por produto e mes.
- Calculo automatico de status de contencao ou liberacao.
- Cache local para manter a ultima leitura valida caso a planilha ou rede esteja indisponivel.

## 5. Funcionamento do sistema

O fluxo do programa pode ser resumido em cinco etapas:

1. **Leitura da base**
   O sistema acessa a planilha oficial armazenada na rede corporativa.

2. **Tratamento e padronizacao**
   As colunas sao renomeadas e padronizadas internamente, reduzindo falhas causadas por variacoes de escrita como "Qtd Inspecionada", "Inspecionado", "Qtd Ruim" ou "Refugo".

3. **Conversao dos dados**
   Datas, quantidades, horas e defeitos sao convertidos para formatos adequados de analise.

4. **Geracao dos indicadores**
   O programa calcula totais de inspecao, refugo, horas acumuladas, horas por mes e status individual do produto.

5. **Exibicao no dashboard**
   Os dados sao apresentados em graficos e cards, permitindo leitura rapida e comparacao entre produtos.

## 6. Principais funcionalidades

### KPIs operacionais

O painel apresenta indicadores-chave para acompanhamento diario:

- Total de pecas inspecionadas.
- Total de refugo.
- Horas acumuladas de inspecao.
- Horas de inspecao no mes selecionado.
- Status atual do produto selecionado.

### Status de 90 dias

O programa calcula automaticamente se um produto esta:

- **Em contencao**, quando ainda nao atingiu 90 dias sem falha.
- **Liberado**, quando ja passou 90 dias sem registro de falha.

Esse recurso reduz a necessidade de calculos manuais e ajuda a manter o criterio de liberacao padronizado.

### Analise por produto

O usuario pode selecionar um produto especifico e visualizar:

- Total de refugo do item.
- Defeitos registrados.
- Quantidade por tipo de defeito.
- Comparacao com o total geral do produto.

### Filtro por mes

O painel permite filtrar os dados por mes, possibilitando analises periodicas e acompanhamento da evolucao recente dos lancamentos.

### Comparativo geral

O grafico de visao geral compara, por produto:

- Quantidade inspecionada.
- Quantidade refugado.

Como os volumes de inspecao e refugo possuem escalas diferentes, o grafico utiliza eixos independentes para melhorar a leitura.

### Cache de seguranca

Caso ocorra erro na leitura da planilha principal, o programa tenta carregar os dados salvos no cache local da ultima leitura valida. Isso aumenta a disponibilidade do painel e evita interrupcoes completas no acompanhamento.

## 7. Dados analisados

Com base no cache local disponivel no projeto, a aplicacao contempla:

- **378 registros de inspecao**.
- **41 produtos acompanhados**.
- **436.040 pecas inspecionadas**.
- **5.412 pecas refugadas**.
- **2.272,6 horas de inspecao registradas**.
- Periodo de dados identificado: **23/03/2023 a 05/05/2026**.

Entre os produtos com maior volume inspecionado no cache analisado estao:

- MR10023A: 62.446 pecas inspecionadas.
- MR10020A: 39.924 pecas inspecionadas.
- MR10022A: 38.192 pecas inspecionadas.
- MR10017A: 36.166 pecas inspecionadas.
- MR10021A: 35.358 pecas inspecionadas.

Os principais defeitos consolidados no cache sao:

- Trinca: 4.478 ocorrencias.
- Marca de cavaco: 441 ocorrencias.
- Dimensional: 108 ocorrencias.
- Afinamento: 83 ocorrencias.
- Oxidacao: 79 ocorrencias.

## 8. Tecnologias utilizadas

- **Python**: linguagem principal do projeto.
- **Pandas**: leitura, tratamento e consolidacao dos dados.
- **Dash**: desenvolvimento da aplicacao web.
- **Plotly**: criacao dos graficos interativos.
- **Excel**: fonte de dados operacional.
- **Pickle/cache local**: armazenamento da ultima leitura valida.
- **HTML/CSS via Dash**: construcao da interface visual.

## 9. Ganhos do projeto

### Ganhos operacionais

- Reducao do tempo gasto em consultas manuais na planilha.
- Centralizacao das informacoes de qualidade em uma unica tela.
- Acompanhamento visual e rapido dos produtos em lancamento.
- Maior facilidade para identificar produtos com alto refugo.
- Melhor visibilidade dos defeitos mais recorrentes.

### Ganhos de qualidade

- Padronizacao do criterio de 90 dias para liberacao.
- Suporte a decisoes mais rapidas sobre contencao e acompanhamento.
- Maior rastreabilidade dos registros de inspecao.
- Identificacao de tendencias de falha por produto e por periodo.
- Apoio a priorizacao de acoes corretivas.

### Ganhos de gestao

- Indicadores consolidados para reunioes e apresentacoes.
- Visualizacao objetiva de desempenho por produto.
- Base mais clara para comunicacao entre qualidade, producao e lideranca.
- Menor dependencia de analises individuais em planilhas.
- Melhor acompanhamento da eficiencia das horas de inspecao.

### Ganhos tecnicos

- Aplicacao web acessivel pela rede local.
- Atualizacao automatica dos dados.
- Tratamento robusto de variacoes nas colunas da planilha.
- Uso de cache para reduzir impacto de indisponibilidade da fonte.
- Estrutura evolutiva para novas metricas e filtros.

## 10. Diferenciais do projeto

O projeto se destaca por unir conhecimento de processo industrial com automacao de dados. A solucao nao e apenas um grafico visual: ela incorpora uma regra operacional importante, a liberacao apos 90 dias sem falhas, e transforma esse criterio em um indicador automatico e padronizado.

Outro diferencial e a preocupacao com continuidade. A criacao de cache local permite que o painel continue exibindo a ultima base valida mesmo quando houver falha momentanea de leitura da planilha principal.

## 11. Aprendizados desenvolvidos

Durante o desenvolvimento do Safety Launch, foram aplicados e fortalecidos conhecimentos em:

- Automacao de leitura de planilhas.
- Tratamento e limpeza de dados com Python.
- Criacao de dashboards interativos.
- Desenvolvimento de indicadores de qualidade.
- Visualizacao de dados com Plotly.
- Estruturacao de aplicacoes web com Dash.
- Pensamento analitico aplicado a processos industriais.
- Traducao de regras operacionais em logica de sistema.

## 12. Resultado final

O Safety Launch entrega uma ferramenta pratica para acompanhamento de produtos em lancamento, conectando dados de inspecao a indicadores visuais e regras de qualidade. O painel melhora a leitura das informacoes, apoia decisoes de contencao/liberacao e fortalece a gestao dos indicadores de refugo.

Para portfolio profissional, este projeto demonstra capacidade de:

- Entender uma necessidade real do processo.
- Desenvolver uma solucao funcional com Python.
- Automatizar analises manuais.
- Criar visualizacoes objetivas para tomada de decisao.
- Trabalhar com dados reais de operacao industrial.
- Entregar uma ferramenta aplicavel ao dia a dia da empresa.

## 13. Resumo para portfolio

**Safety Launch** e um dashboard desenvolvido em Python para acompanhamento de produtos em lancamento. A ferramenta le registros de inspecao em Excel, trata os dados automaticamente e apresenta indicadores de quantidade inspecionada, refugo, horas de inspecao, principais defeitos e status de liberacao por produto. O sistema tambem calcula automaticamente a regra de 90 dias sem falhas, auxiliando o controle de contencao e a tomada de decisao da area de qualidade.

Com dados reais de operacao, o painel analisou 378 registros, 41 produtos, 436.040 pecas inspecionadas, 5.412 refugos e 2.272,6 horas de inspecao. O projeto gerou ganhos em agilidade, padronizacao, rastreabilidade e visibilidade dos indicadores de qualidade.
