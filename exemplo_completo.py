"""
Script de Exemplo Completo com Dados Simulados
Demonstra o fluxo completo do projeto sem necessidade de PDFs reais

Este script:
1. Gera dados simulados de violência contra mulheres
2. Cria visualizações gráficas
3. Gera relatório PDF completo
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import numpy as np
from gerar_graficos import GeradorGraficos
from gerar_relatorio import GeradorRelatorioCompleto


def gerar_dados_simulados() -> pd.DataFrame:
    """
    Gera dados simulados de violência para demonstração
    
    Returns:
        DataFrame com dados simulados
    """
    print("🔄 Gerando dados simulados...")
    
    np.random.seed(42)  # Para reprodutibilidade
    
    # Configurações
    estados = ['Amazonas', 'Roraima', 'Acre']
    anos = list(range(2015, 2026))  # 2015 a 2025
    indices_violencia = ['Feminicídio', 'Estupro', 'Lesão Corporal', 'Violência Doméstica']
    
    # Gera dados
    dados = []
    
    for estado in estados:
        # Fatores de multiplicação específicos por estado
        if estado == 'Amazonas':
            fator_base = 2.5
        elif estado == 'Roraima':
            fator_base = 1.2
        else:  # Acre
            fator_base = 1.0
        
        for indice in indices_violencia:
            # Base específica por tipo de violência
            if indice == 'Feminicídio':
                base = 15
                tendencia = 0.5  # Leve aumento ao longo dos anos
            elif indice == 'Estupro':
                base = 120
                tendencia = -1.5  # Tendência de redução (melhoria na denúncia)
            elif indice == 'Lesão Corporal':
                base = 350
                tendencia = 2.0  # Aumento (mais denúncias)
            else:  # Violência Doméstica
                base = 280
                tendencia = 1.0
            
            for i, ano in enumerate(anos):
                # Valor com tendência temporal e variação aleatória
                valor = (base * fator_base + 
                        tendencia * i +
                        np.random.normal(0, base * 0.15))
                
                valor = max(0, int(valor))  # Garante valores positivos
                
                dados.append({
                    'Ano': ano,
                    'Estado': estado,
                    'Índice de Violência': indice,
                    'Valor': valor
                })
    
    df = pd.DataFrame(dados)
    
    print(f"✅ Dados simulados gerados: {len(df)} registros")
    print(f"   - Estados: {', '.join(estados)}")
    print(f"   - Anos: {anos[0]} a {anos[-1]}")
    print(f"   - Tipos de violência: {len(indices_violencia)}")
    
    return df


def executar_exemplo_completo():
    """Executa o fluxo completo do projeto com dados simulados"""
    
    print("\n" + "="*70)
    print("🚀 EXEMPLO COMPLETO - ANÁLISE DE VIOLÊNCIA CONTRA MULHERES")
    print("="*70 + "\n")
    
    # 1. Gera dados simulados
    df_dados = gerar_dados_simulados()
    
    # Salva dados em CSV para referência
    arquivo_dados = 'dados/dados_simulados.csv'
    df_dados.to_csv(arquivo_dados, index=False, encoding='utf-8-sig')
    print(f"\n💾 Dados salvos em: {arquivo_dados}")
    
    # Mostra estatísticas básicas
    print("\n📊 Estatísticas dos Dados:")
    print("-" * 70)
    print(f"Total de registros: {len(df_dados)}")
    print(f"\nTotal por Estado:")
    print(df_dados.groupby('Estado')['Valor'].sum().to_string())
    print(f"\nTotal por Tipo de Violência:")
    print(df_dados.groupby('Índice de Violência')['Valor'].sum().to_string())
    
    # 2. Gera gráficos
    print("\n" + "="*70)
    gerador_graficos = GeradorGraficos(df_dados, pasta_saida='graficos')
    caminhos_graficos = gerador_graficos.gerar_todos_graficos()
    
    if not caminhos_graficos:
        print("❌ Nenhum gráfico foi gerado!")
        return
    
    # 3. Gera relatório PDF
    print("\n" + "="*70)
    
    # Textos do relatório
    introducao = (
        "Este relatório apresenta uma análise detalhada dos índices de violência contra mulheres "
        "nos estados do Amazonas, Roraima e Acre, abrangendo o período de 2015 a 2025. "
        "\n\n"
        "A violência contra a mulher é um grave problema de saúde pública e violação dos direitos "
        "humanos. Na região Norte do Brasil, devido às suas características geográficas, sociais "
        "e econômicas particulares, este fenômeno apresenta desafios específicos que requerem "
        "atenção especial das políticas públicas. "
        "\n\n"
        "O presente estudo busca contribuir para a compreensão da evolução temporal destes índices, "
        "identificando tendências e fornecendo subsídios para o desenvolvimento de estratégias "
        "mais efetivas de prevenção e combate à violência de gênero."
    )
    
    conclusao = (
        "A análise dos dados de violência contra mulheres na região Norte, especificamente "
        "nos estados do Amazonas, Roraima e Acre, durante o período de 2015 a 2025, revela "
        "aspectos importantes que merecem atenção. "
        "\n\n"
        "Os gráficos de série temporal demonstram variações significativas ao longo dos anos, "
        "indicando tanto avanços quanto desafios persistentes no combate à violência de gênero. "
        "A análise comparativa entre os estados evidencia a necessidade de abordagens "
        "contextualizadas, considerando as especificidades de cada região. "
        "\n\n"
        "É fundamental que as políticas públicas de enfrentamento à violência contra a mulher "
        "sejam baseadas em evidências e dados confiáveis. Este estudo contribui para essa "
        "base de conhecimento e aponta para a necessidade de continuidade no monitoramento "
        "destes indicadores, bem como na avaliação da efetividade das intervenções implementadas. "
        "\n\n"
        "Recomenda-se: (1) fortalecimento das redes de proteção à mulher; (2) ampliação dos "
        "canais de denúncia e acolhimento; (3) investimento em educação e conscientização; "
        "(4) integração entre os diferentes setores e esferas de governo no enfrentamento "
        "à violência de gênero."
    )
    
    gerador_relatorio = GeradorRelatorioCompleto(
        titulo="Análise de Violência contra Mulheres",
        subtitulo="Região Norte - Amazonas, Roraima e Acre",
        periodo="2015-2025"
    )
    
    sucesso = gerador_relatorio.gerar_relatorio(
        caminhos_graficos=caminhos_graficos,
        arquivo_saida='Relatorio_Violencia_Mulher_Regiao_Norte.pdf',
        autor="Pesquisa Acadêmica",
        instituicao="IFPI - Campus Picos",
        introducao=introducao,
        conclusao=conclusao
    )
    
    if sucesso:
        print("\n" + "="*70)
        print("🎉 EXEMPLO CONCLUÍDO COM SUCESSO!")
        print("="*70)
        print("\n📁 Arquivos gerados:")
        print(f"   - Dados: {arquivo_dados}")
        print(f"   - Gráficos: {len(caminhos_graficos)} arquivos na pasta 'graficos/'")
        print(f"   - Relatório: Relatorio_Violencia_Mulher_Regiao_Norte.pdf")
        print("\n💡 Próximos passos:")
        print("   1. Revise o relatório PDF gerado")
        print("   2. Confira os gráficos na pasta 'graficos/'")
        print("   3. Adapte o código para seus dados reais dos PDFs")
        print("   4. Execute: python scripts/processar_dados_reais.py")
    else:
        print("\n❌ Erro ao gerar relatório!")


if __name__ == "__main__":
    executar_exemplo_completo()
