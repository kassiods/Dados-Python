# 📊 Análise de Violência contra Mulheres - Região Norte

Projeto Python para análise quantitativa de dados de violência contra mulheres nos estados do **Amazonas**, **Roraima** e **Acre**, no período de **2015 a 2025**.

## 🎯 Objetivo

Extrair, processar e visualizar dados de violência contra mulheres a partir dos Anuários Brasileiros de Segurança Pública e do Atlas da Violência, gerando relatórios acadêmicos completos em PDF.

## 📋 Funcionalidades

- ✅ **Extração automática** de dados de PDFs usando `tabula-py`
- ✅ **Processamento e limpeza** de dados com `pandas`
- ✅ **Visualizações profissionais** com `matplotlib` e `seaborn`
- ✅ **Geração de relatórios PDF** acadêmicos com `fpdf2`
- ✅ **Dados simulados** para teste sem necessidade de PDFs reais
- ✅ **Análise temporal** (séries históricas 2015-2025)
- ✅ **Análise comparativa** entre estados
- ✅ **Mapas de calor** (heatmaps) de intensidade

## 🏗️ Estrutura do Projeto

```
Dados-python/
│
├── dados/                          # Pasta para PDFs e dados extraídos
│   ├── anuario_2015.pdf           # (Você deve baixar)
│   ├── anuario_2016.pdf
│   ├── ...
│   └── dados_consolidados.csv     # Dados extraídos
│
├── graficos/                       # Gráficos gerados
│   ├── serie_temporal_amazonas.png
│   ├── comparativo_feminicidio.png
│   └── ...
│
├── src/                            # Código-fonte (módulos)
│   ├── extracao_dados.py          # Extração de PDFs
│   ├── gerar_graficos.py          # Geração de gráficos
│   └── gerar_relatorio.py         # Geração de PDF
│
├── scripts/                        # Scripts executáveis
│   └── processar_dados_reais.py   # Processa PDFs reais
│
├── exemplo_completo.py             # Demo com dados simulados
├── requirements.txt                # Dependências
└── README.md                       # Este arquivo
```

## 🚀 Instalação

### Pré-requisitos

1. **Python 3.8+**
   - Baixe em: https://www.python.org/downloads/

2. **Java (para tabula-py)**
   - Baixe em: https://www.java.com/download/
   - Ou use: `winget install Oracle.JavaRuntimeEnvironment`

### Instalar Dependências

```powershell
# Navegue até a pasta do projeto
cd "C:\Users\lardo\OneDrive\Área de Trabalho\Dados-python"

# Instale as dependências
pip install -r requirements.txt
```

### Verificar Instalação

```powershell
# Verifique se Java está instalado
java -version

# Verifique se Python está instalado
python --version
```

## 📖 Uso

### Opção 1: Exemplo Rápido (Dados Simulados)

**Ideal para testar o projeto sem baixar PDFs:**

```powershell
python exemplo_completo.py
```

Este script irá:
1. ✅ Gerar dados simulados de violência
2. ✅ Criar todos os gráficos
3. ✅ Gerar relatório PDF completo

**Arquivos gerados:**
- `dados/dados_simulados.csv` - Dados simulados
- `graficos/*.png` - Vários gráficos
- `Relatorio_Violencia_Mulher_Regiao_Norte.pdf` - Relatório final

### Opção 2: Processar Dados Reais

**Para trabalhar com dados reais dos anuários:**

#### Passo 1: Baixar os PDFs

Baixe os **Anuários Brasileiros de Segurança Pública** (2015-2025):

- 🌐 [Fórum Brasileiro de Segurança Pública](https://forumseguranca.org.br/anuario-brasileiro-de-seguranca-publica/)
- 🌐 [Atlas da Violência - IPEA](https://www.ipea.gov.br/atlasviolencia/)

#### Passo 2: Organizar os PDFs

Coloque os PDFs na pasta `dados/` com os nomes:
- `anuario_2015.pdf`
- `anuario_2016.pdf`
- ...
- `anuario_2025.pdf`

#### Passo 3: Executar o Script

```powershell
python scripts\processar_dados_reais.py
```

O script irá:
1. 🔍 Verificar quais PDFs estão disponíveis
2. 📄 Extrair dados das tabelas
3. 💾 Salvar dados consolidados em CSV
4. 📊 Gerar gráficos (opcional)
5. 📑 Criar relatório PDF (opcional)

### Opção 3: Uso Programático (Avançado)

```python
import sys
sys.path.insert(0, 'src')

from extracao_dados import ExtratorDadosPDF
from gerar_graficos import GeradorGraficos
from gerar_relatorio import GeradorRelatorioCompleto

# 1. Extrair dados
extrator = ExtratorDadosPDF(estados_alvo=['Amazonas', 'Roraima', 'Acre'])
caminhos_pdfs = {
    2025: 'dados/anuario_2025.pdf',
    2024: 'dados/anuario_2024.pdf',
    # ... adicione mais anos
}
df_dados = extrator.processar_multiplos_pdfs(caminhos_pdfs)

# 2. Gerar gráficos
gerador = GeradorGraficos(df_dados, pasta_saida='graficos')
graficos = gerador.gerar_todos_graficos()

# 3. Gerar relatório
relatorio = GeradorRelatorioCompleto()
relatorio.gerar_relatorio(
    caminhos_graficos=graficos,
    arquivo_saida='meu_relatorio.pdf',
    autor='Seu Nome',
    instituicao='Sua Universidade'
)
```

## 📊 Tipos de Gráficos Gerados

### 1. Séries Temporais por Estado
Mostra a evolução de cada tipo de violência ao longo dos anos para cada estado.

### 2. Gráficos Comparativos
Compara os três estados para cada tipo de violência específica.

### 3. Mapas de Calor (Heatmaps)
Visualiza a intensidade da violência por estado e ano.

### 4. Tendência Geral
Mostra a tendência agregada de toda a região Norte.

## 🛠️ Personalização

### Adicionar Mais Estados

Edite o arquivo que você está usando:

```python
estados_alvo = ['Amazonas', 'Roraima', 'Acre', 'Pará', 'Rondônia']
```

### Ajustar Extração de Páginas Específicas

Se souber quais páginas contêm as tabelas:

```python
extrator.processar_pdf(
    caminho_pdf='dados/anuario_2025.pdf',
    ano=2025,
    paginas_especificas='15-20'  # Apenas páginas 15 a 20
)
```

### Customizar Gráficos

```python
gerador = GeradorGraficos(df_dados)

# Gerar apenas série temporal do Amazonas
gerador.grafico_serie_temporal_por_estado('Amazonas')

# Gerar apenas comparativo de Feminicídio
gerador.grafico_comparativo_estados('Feminicídio', tipo='barra')
```

## ⚠️ Solução de Problemas

### Erro: "Java not found"

**Solução:**
```powershell
# Instale o Java
winget install Oracle.JavaRuntimeEnvironment

# Ou baixe manualmente em:
# https://www.java.com/download/
```

### Erro: "Nenhuma tabela extraída"

**Possíveis causas:**
1. O PDF está protegido ou é uma imagem digitalizada
2. As tabelas estão em formato não suportado
3. Necessário ajustar parâmetros de extração

**Soluções:**
- Tente usar `Camelot` em vez de `tabula-py`
- Use `lattice=True` ou `stream=True`
- Especifique páginas e áreas específicas manualmente

### Erro de Import

**Solução:**
```python
# Adicione no início do seu script
import sys
sys.path.insert(0, 'src')
```

## 📚 Fontes de Dados Recomendadas

### Principais:
- 📊 [Fórum Brasileiro de Segurança Pública - Anuários](https://forumseguranca.org.br/anuario-brasileiro-de-seguranca-publica/)
- 📊 [Atlas da Violência - IPEA](https://www.ipea.gov.br/atlasviolencia/)

### Complementares:
- 📊 [Rede de Observatórios da Segurança - "Elas Vivem"](https://observatorioseguranca.com.br/)
- 📊 [DataSUS - Ministério da Saúde](https://datasus.saude.gov.br/)

## 🤝 Contribuindo

Este é um projeto acadêmico. Sugestões e melhorias são bem-vindas!

## 📄 Licença

Este projeto é de código aberto para fins educacionais e acadêmicos.

## 👤 Autor

Desenvolvido como ferramenta de apoio para trabalho acadêmico sobre violência contra mulheres na região Norte do Brasil.

## 📞 Suporte

Se encontrar problemas:
1. Verifique a seção "Solução de Problemas"
2. Revise se todas as dependências estão instaladas
3. Confira se os PDFs estão no formato correto

---

## 🎓 Para Trabalhos Acadêmicos

### Citação Sugerida dos Dados:

```
FÓRUM BRASILEIRO DE SEGURANÇA PÚBLICA. Anuário Brasileiro de Segurança Pública. 
São Paulo: FBSP, [ano]. Disponível em: https://forumseguranca.org.br/. 
Acesso em: [data].

IPEA; FBSP. Atlas da Violência [ano]. Rio de Janeiro: IPEA, [ano]. 
Disponível em: https://www.ipea.gov.br/atlasviolencia/. Acesso em: [data].
```

### Estrutura Sugerida para Dissertação:

1. **Introdução** - Contexto da violência contra mulheres na Amazônia
2. **Metodologia** - Como os dados foram coletados e analisados
3. **Resultados** - Apresentação dos gráficos e estatísticas
4. **Discussão** - Interpretação dos resultados
5. **Conclusão** - Síntese e recomendações

---

**💡 Dica:** Execute primeiro o `exemplo_completo.py` para familiarizar-se com a estrutura antes de trabalhar com dados reais!

**🌟 Importante:** Este projeto é uma ferramenta de análise. A interpretação contextualizada dos dados requer conhecimento da realidade social, econômica e cultural da região estudada.
#   D a d o s - P y t h o n  
 