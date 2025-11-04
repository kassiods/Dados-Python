
# 📊 Análise de Violência contra Mulheres - Região Norte (2015-2025)

## 🎯 Objetivo

Projeto Python para análise quantitativa da violência contra mulheres no **Amazonas, Roraima e Acre** (2015-2025). O objetivo é extrair dados de fontes oficiais (FBSP, IPEA), processá-los e gerar um **relatório acadêmico completo em PDF** com gráficos e séries históricas.

## 📋 Funcionalidades Chave

  * **Extração Robusta:** Captura dados de tabelas em PDFs (via `tabula-py`) e planilhas XLSX.
  * **Processamento de Dados:** Utiliza `pandas` para limpeza, consolidação e análise da série temporal.
  * **Visualização:** Gera gráficos de tendência e comparação com `matplotlib` e `seaborn`.
  * **Geração de Relatório:** Cria o documento final em PDF (`fpdf2`) com todos os achados.

## 🏗️ Estrutura Essencial do Projeto

```
Dados-python/
│
├── dados/                          # PDFs baixados (anuario_20xx.pdf) e CSV consolidado
├── graficos/                       # Imagens .png geradas
├── src/                            # Módulos Python (extracao, graficos, relatorio)
├── scripts/                        # Scripts de execução principal
├── exemplo_completo.py             # Demo com dados simulados
└── requirements.txt                # Dependências (pandas, tabula-py, etc.)
```

## 🚀 Instalação e Uso

### 1\. Pré-requisitos

Certifique-se de ter **Python 3.8+** e **Java** (necessário para o `tabula-py`) instalados.

### 2\. Instalar Dependências

```powershell
# Instale as dependências listadas no arquivo requirements.txt
pip install -r requirements.txt
```

### 3\. Execução

Você tem duas opções:

#### A. Exemplo Rápido (Recomendado para Teste)

Gera um relatório completo usando **dados simulados**, ideal para verificar a estrutura:

```powershell
python exemplo_completo.py
# Gera Relatorio_Violencia_Mulher_Regiao_Norte.pdf
```

#### B. Dados Reais

1.  Baixe os **Anuários do FBSP** e os **Atlas do IPEA** e coloque os arquivos na pasta `dados/`.
2.  Execute o script principal, que fará a extração e o processamento:

<!-- end list -->

```powershell
python scripts\processar_dados_reais.py
```

## 📚 Fontes de Dados

Os dados são provenientes de fontes oficiais de Segurança Pública, como:

  * [Fórum Brasileiro de Segurança Pública (FBSP)](https://forumseguranca.org.br/anuario-brasileiro-de-seguranca-publica/)
  * [Instituto de Pesquisa Econômica Aplicada (IPEA)](https://www.ipea.gov.br/atlasviolencia/)

