"""
Script para Processar Dados Reais dos PDFs
Use este script após baixar os Anuários de Segurança Pública

IMPORTANTE: Antes de executar este script:
1. Baixe os PDFs dos Anuários (2015-2025)
2. Coloque-os na pasta 'dados/' com os nomes indicados abaixo
3. Ajuste as configurações conforme necessário
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from extracao_dados import ExtratorDadosPDF
from gerar_graficos import GeradorGraficos
from gerar_relatorio import GeradorRelatorioCompleto


def processar_dados_reais():
    """Processa dados reais dos PDFs baixados"""
    
    print("\n" + "="*70)
    print("📊 PROCESSAMENTO DE DADOS REAIS - VIOLÊNCIA CONTRA MULHERES")
    print("="*70 + "\n")
    
    # ============================================
    # CONFIGURAÇÃO: CAMINHOS DOS PDFs
    # ============================================
    # Ajuste os nomes dos arquivos conforme necessário
    base_path = os.path.join(os.path.dirname(__file__), '..', 'dados')
    
    caminhos_pdfs = {
        2025: os.path.join(base_path, 'anuario_2025.pdf'),
        2024: os.path.join(base_path, 'anuario_2024.pdf'),
        2023: os.path.join(base_path, 'anuario_2023.pdf'),
        2022: os.path.join(base_path, 'anuario_2022.pdf'),
        2021: os.path.join(base_path, 'anuario_2021.pdf'),
        2020: os.path.join(base_path, 'anuario_2020.pdf'),
        2019: os.path.join(base_path, 'anuario_2019.pdf'),
        2018: os.path.join(base_path, 'anuario_2018.pdf'),
        2017: os.path.join(base_path, 'anuario_2017.pdf'),
        2016: os.path.join(base_path, 'anuario_2016.pdf'),
        2015: os.path.join(base_path, 'anuario_2015.pdf'),
    }
    
    # ============================================
    # CONFIGURAÇÃO: ESTADOS E ÍNDICES
    # ============================================
    estados_alvo = ['Amazonas', 'Roraima', 'Acre']
    
    # Verifica quais PDFs existem
    pdfs_existentes = {ano: path for ano, path in caminhos_pdfs.items() 
                       if os.path.exists(path)}
    
    pdfs_faltantes = {ano: path for ano, path in caminhos_pdfs.items() 
                      if not os.path.exists(path)}
    
    print(f"✅ PDFs encontrados: {len(pdfs_existentes)}")
    for ano in sorted(pdfs_existentes.keys()):
        print(f"   - {ano}: {os.path.basename(pdfs_existentes[ano])}")
    
    if pdfs_faltantes:
        print(f"\n⚠️  PDFs faltantes: {len(pdfs_faltantes)}")
        for ano in sorted(pdfs_faltantes.keys()):
            print(f"   - {ano}: {os.path.basename(pdfs_faltantes[ano])}")
        print("\n💡 Baixe os anuários em:")
        print("   - https://forumseguranca.org.br/anuario-brasileiro-de-seguranca-publica/")
        print("   - https://www.ipea.gov.br/atlasviolencia/")
    
    if not pdfs_existentes:
        print("\n❌ Nenhum PDF encontrado! Baixe os anuários primeiro.")
        print("\n📝 Instruções:")
        print("   1. Baixe os PDFs dos anuários")
        print("   2. Renomeie-os para 'anuario_XXXX.pdf' (ex: anuario_2025.pdf)")
        print("   3. Coloque na pasta 'dados/'")
        print("   4. Execute este script novamente")
        return
    
    continuar = input("\n▶️  Continuar com a extração? (s/n): ")
    if continuar.lower() != 's':
        print("❌ Processo cancelado pelo usuário.")
        return
    
    # ============================================
    # EXTRAÇÃO DE DADOS
    # ============================================
    extrator = ExtratorDadosPDF(estados_alvo=estados_alvo)
    df_dados = extrator.processar_multiplos_pdfs(pdfs_existentes)
    
    if df_dados.empty:
        print("\n❌ Nenhum dado foi extraído!")
        print("\n💡 Possíveis problemas:")
        print("   - As tabelas nos PDFs podem estar em formato não suportado")
        print("   - Os nomes dos estados podem estar escritos diferente")
        print("   - Pode ser necessário especificar páginas específicas")
        print("\n📖 Consulte a documentação para ajustar a extração.")
        return
    
    # Salva dados extraídos
    arquivo_dados = os.path.join(base_path, 'dados_consolidados.csv')
    df_dados.to_csv(arquivo_dados, index=False, encoding='utf-8-sig')
    print(f"\n💾 Dados consolidados salvos em: {arquivo_dados}")
    
    # Mostra amostra dos dados
    print("\n📊 Amostra dos Dados Extraídos:")
    print("-" * 70)
    print(df_dados.head(10).to_string())
    print(f"\n... Total: {len(df_dados)} registros")
    
    # ============================================
    # GERAÇÃO DE GRÁFICOS
    # ============================================
    gerar_graficos = input("\n▶️  Gerar gráficos? (s/n): ")
    
    if gerar_graficos.lower() == 's':
        pasta_graficos = os.path.join(os.path.dirname(__file__), '..', 'graficos')
        gerador_graficos = GeradorGraficos(df_dados, pasta_saida=pasta_graficos)
        caminhos_graficos = gerador_graficos.gerar_todos_graficos()
        
        # ============================================
        # GERAÇÃO DE RELATÓRIO PDF
        # ============================================
        if caminhos_graficos:
            gerar_pdf = input("\n▶️  Gerar relatório PDF? (s/n): ")
            
            if gerar_pdf.lower() == 's':
                # Solicita informações do relatório
                print("\n📝 Informações do Relatório:")
                autor = input("   Nome do autor (Enter para pular): ").strip()
                instituicao = input("   Instituição (Enter para pular): ").strip()
                
                gerador_relatorio = GeradorRelatorioCompleto()
                
                arquivo_saida = os.path.join(
                    os.path.dirname(__file__), '..',
                    'Relatorio_Violencia_Mulher_Regiao_Norte.pdf'
                )
                
                sucesso = gerador_relatorio.gerar_relatorio(
                    caminhos_graficos=caminhos_graficos,
                    arquivo_saida=arquivo_saida,
                    autor=autor or None,
                    instituicao=instituicao or None
                )
                
                if sucesso:
                    print("\n" + "="*70)
                    print("🎉 PROCESSO CONCLUÍDO COM SUCESSO!")
                    print("="*70)
                    print(f"\n📁 Arquivos gerados:")
                    print(f"   - Dados: {arquivo_dados}")
                    print(f"   - Gráficos: {len(caminhos_graficos)} arquivos")
                    print(f"   - Relatório: {arquivo_saida}")
    
    print("\n✅ Processo finalizado!")


if __name__ == "__main__":
    # Verifica se Java está instalado (necessário para tabula-py)
    try:
        import subprocess
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode != 0:
            print("⚠️  Java não encontrado!")
            print("   O tabula-py requer Java para funcionar.")
            print("   Baixe em: https://www.java.com/download/")
            sys.exit(1)
    except FileNotFoundError:
        print("⚠️  Java não está instalado!")
        print("   O tabula-py requer Java para funcionar.")
        print("   Baixe em: https://www.java.com/download/")
        sys.exit(1)
    
    processar_dados_reais()
