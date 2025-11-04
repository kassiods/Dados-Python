# 📥 Como Obter os PDFs dos Anuários

Este documento contém links e instruções para baixar os **Anuários Brasileiros de Segurança Pública** e o **Atlas da Violência** necessários para o projeto.

---

## 🔗 Links Diretos para Download

### Fórum Brasileiro de Segurança Pública (FBSP)

**Anuário Brasileiro de Segurança Pública:**

| Ano | Link de Download |
|-----|------------------|
| 2024 | [Anuário 2024](https://forumseguranca.org.br/wp-content/uploads/2024/07/anuario-2024.pdf) |
| 2023 | [Anuário 2023](https://forumseguranca.org.br/wp-content/uploads/2023/07/anuario-2023.pdf) |
| 2022 | [Anuário 2022](https://forumseguranca.org.br/wp-content/uploads/2022/06/anuario-2022.pdf) |
| 2021 | [Anuário 2021](https://forumseguranca.org.br/wp-content/uploads/2021/07/anuario-2021.pdf) |
| 2020 | [Anuário 2020](https://forumseguranca.org.br/wp-content/uploads/2020/10/anuario-14-2020-v1-interativo.pdf) |
| 2019 | [Anuário 2019](https://forumseguranca.org.br/wp-content/uploads/2019/09/Anuario-2019-FINAL-v3.pdf) |
| 2018 | [Anuário 2018](https://forumseguranca.org.br/wp-content/uploads/2018/09/FBSP_Anuario_Brasileiro_Seguranca_Publica_2018.pdf) |
| 2017 | [Anuário 2017](https://forumseguranca.org.br/wp-content/uploads/2017/12/ANUARIO_11_2017.pdf) |
| 2016 | [Anuário 2016](https://forumseguranca.org.br/wp-content/uploads/2016/07/Anuario-10.pdf) |
| 2015 | [Anuário 2015](https://forumseguranca.org.br/wp-content/uploads/2015/10/Anuario-2015.pdf) |

**⚠️ Nota:** Os links podem mudar ao longo do tempo. Se algum link não funcionar:
- Acesse: https://forumseguranca.org.br/anuario-brasileiro-de-seguranca-publica/
- Navegue até o ano desejado e faça o download

### Atlas da Violência (IPEA)

**Publicações Anuais:**

| Ano | Link de Download |
|-----|------------------|
| 2023 | [Atlas 2023](https://www.ipea.gov.br/atlasviolencia/arquivos/artigos/1375-atlasdaviolencia2023.pdf) |
| 2022 | [Atlas 2022](https://www.ipea.gov.br/atlasviolencia/arquivos/artigos/5141-atlasdaviolencia2022.pdf) |
| 2021 | [Atlas 2021](https://www.ipea.gov.br/atlasviolencia/arquivos/artigos/5111-atlasdaviolencia2021completo.pdf) |
| 2020 | [Atlas 2020](https://www.ipea.gov.br/atlasviolencia/arquivos/downloads/6537-atlas-da-violencia-2020.pdf) |
| 2019 | [Atlas 2019](https://www.ipea.gov.br/atlasviolencia/arquivos/downloads/5162-atlas-2019.pdf) |

**Acesso geral:** https://www.ipea.gov.br/atlasviolencia/

---

## 📋 Instruções Detalhadas de Download

### Método 1: Download Manual (Recomendado)

1. **Abra cada link** na tabela acima
2. **Salve o PDF** com o nome correto:
   - Formato: `anuario_XXXX.pdf` (ex: `anuario_2024.pdf`)
3. **Coloque os arquivos** na pasta `dados/` do projeto

### Método 2: Download via Script (Avançado)

Você pode usar este script PowerShell para baixar automaticamente:

```powershell
# Cria a pasta dados se não existir
New-Item -ItemType Directory -Force -Path "dados"

# Array de URLs (adicione os URLs completos)
$urls = @(
    @{ano="2024"; url="URL_DO_ANUARIO_2024"},
    @{ano="2023"; url="URL_DO_ANUARIO_2023"}
    # Adicione mais conforme necessário
)

# Baixa cada arquivo
foreach ($item in $urls) {
    $destino = "dados/anuario_$($item.ano).pdf"
    Write-Host "Baixando Anuário $($item.ano)..."
    Invoke-WebRequest -Uri $item.url -OutFile $destino
    Write-Host "✓ Salvo em: $destino"
}

Write-Host "`n✅ Download concluído!"
```

---

## 📊 Seções Importantes nos PDFs

Ao abrir os PDFs, procure por estas seções:

### 1. Violência Contra a Mulher
- Geralmente no Capítulo 5 ou 6
- Busque por: "Violência contra a Mulher", "Feminicídio", "LGBTQIA+"

### 2. Tabelas por UF (Unidade Federativa)
- Procure tabelas com dados estaduais
- Colunas: Estado, Ocorrências, Taxa por 100 mil habitantes

### 3. Dados Históricos
- Séries temporais de anos anteriores
- Comparações anuais

### Exemplo de Tabela Útil:

```
Tabela X: Feminicídios por UF - 2015-2025

UF         | 2015 | 2016 | 2017 | ... | 2025
-----------|------|------|------|-----|------
Amazonas   |  45  |  52  |  48  | ... |  65
Roraima    |  12  |  15  |  18  | ... |  22
Acre       |   8  |  10  |  12  | ... |  14
```

---

## 🔍 Páginas Específicas para Extração

Após baixar os PDFs, identifique as páginas com dados relevantes:

### Dica: Como Encontrar as Páginas

1. **Abra o PDF** no Adobe Reader ou similar
2. **Use Ctrl+F** para buscar:
   - "Amazonas"
   - "Feminicídio"
   - "Violência doméstica"
   - "Estupro"
3. **Anote o número das páginas** com tabelas

### Configurar no Script

Edite `processar_dados_reais.py` para usar páginas específicas:

```python
# Exemplo: dados estão nas páginas 45 a 52
df_ano = extrator.processar_pdf(
    caminho_pdf, 
    ano,
    paginas_especificas='45-52'
)
```

---

## 🗂️ Estrutura Final Esperada

Após baixar todos os PDFs, sua pasta `dados/` deve ficar assim:

```
dados/
├── anuario_2015.pdf  ✓
├── anuario_2016.pdf  ✓
├── anuario_2017.pdf  ✓
├── anuario_2018.pdf  ✓
├── anuario_2019.pdf  ✓
├── anuario_2020.pdf  ✓
├── anuario_2021.pdf  ✓
├── anuario_2022.pdf  ✓
├── anuario_2023.pdf  ✓
└── anuario_2024.pdf  ✓
```

---

## 💡 Dicas Importantes

### ✅ Faça:
- Verifique se os PDFs não estão corrompidos
- Confirme que são PDFs com texto (não imagens escaneadas)
- Mantenha os nomes de arquivo padronizados

### ❌ Evite:
- Renomear os arquivos depois de configurar
- Misturar diferentes fontes de dados
- Usar PDFs de baixa qualidade

---

## 🆘 Problemas Comuns

### Problema: Link não funciona

**Solução:**
- Acesse o site principal e navegue até a seção de publicações
- Use o buscador do site para encontrar o anuário
- Entre em contato com o FBSP se necessário

### Problema: PDF está protegido

**Solução:**
- Alguns PDFs podem ter proteção contra cópia
- Tente usar ferramentas online para remover proteção
- Ou transcreva manualmente as tabelas relevantes

### Problema: Tabelas são imagens

**Solução:**
- Use OCR (Reconhecimento Óptico de Caracteres)
- Ferramentas: Adobe Acrobat Pro, ABBYY FineReader
- Ou digite manualmente em uma planilha Excel

---

## 📞 Contatos Úteis

**Fórum Brasileiro de Segurança Pública:**
- Site: https://forumseguranca.org.br
- E-mail: contato@forumseguranca.org.br

**IPEA - Instituto de Pesquisa Econômica Aplicada:**
- Site: https://www.ipea.gov.br
- Atlas da Violência: atlasviolencia@ipea.gov.br

---

## ✅ Checklist Final

Antes de executar o script de processamento:

- [ ] Todos os PDFs foram baixados
- [ ] PDFs estão na pasta `dados/`
- [ ] Nomes dos arquivos estão no formato `anuario_XXXX.pdf`
- [ ] PDFs abrem corretamente e não estão corrompidos
- [ ] Identifiquei as páginas com dados relevantes
- [ ] Java está instalado (necessário para tabula-py)
- [ ] Dependências Python foram instaladas

---

**🎯 Próximo Passo:** Execute `python scripts\processar_dados_reais.py`
