"""
Módulo de Extração de Dados de PDFs
Extrai dados de violência contra mulheres dos Anuários de Segurança Pública
"""

import pandas as pd
import tabula
import os
from typing import List, Dict, Optional
import warnings

warnings.filterwarnings('ignore')


class ExtratorDadosPDF:
    """Classe para extrair e processar dados de PDFs de anuários"""
    
    def __init__(self, estados_alvo: List[str] = None):
        """
        Inicializa o extrator
        
        Args:
            estados_alvo: Lista de estados para filtrar (padrão: Amazonas, Roraima, Acre)
        """
        self.estados_alvo = estados_alvo or ['Amazonas', 'Roraima', 'Acre']
        self.dados_consolidados = []
    
    def extrair_tabelas_do_pdf(self, caminho_pdf: str, 
                                paginas: str = 'all',
                                multiplas_tabelas: bool = True) -> List[pd.DataFrame]:
        """
        Extrai todas as tabelas de um PDF usando tabula-py
        
        Args:
            caminho_pdf: Caminho completo para o arquivo PDF
            paginas: Páginas para extrair ('all' ou '1,2,3' ou '1-5')
            multiplas_tabelas: Se True, tenta extrair múltiplas tabelas
            
        Returns:
            Lista de DataFrames extraídos
        """
        if not os.path.exists(caminho_pdf):
            print(f"⚠️  Arquivo não encontrado: {caminho_pdf}")
            return []
        
        print(f"📄 Extraindo dados de: {os.path.basename(caminho_pdf)}")
        
        try:
            # Método 1: Stream (para tabelas sem bordas definidas)
            dfs_stream = tabula.read_pdf(
                caminho_pdf,
                pages=paginas,
                multiple_tables=multiplas_tabelas,
                stream=True,
                guess=True,
                encoding='utf-8'
            )
            
            if dfs_stream and len(dfs_stream) > 0:
                print(f"   ✓ Extraídas {len(dfs_stream)} tabela(s) com método Stream")
                return dfs_stream
            
            # Método 2: Lattice (para tabelas com bordas)
            dfs_lattice = tabula.read_pdf(
                caminho_pdf,
                pages=paginas,
                multiple_tables=multiplas_tabelas,
                lattice=True,
                encoding='utf-8'
            )
            
            if dfs_lattice and len(dfs_lattice) > 0:
                print(f"   ✓ Extraídas {len(dfs_lattice)} tabela(s) com método Lattice")
                return dfs_lattice
                
            print("   ⚠️  Nenhuma tabela encontrada")
            return []
            
        except Exception as e:
            print(f"   ❌ Erro ao extrair: {str(e)}")
            return []
    
    def limpar_e_filtrar_dados(self, df: pd.DataFrame, 
                                 ano: int,
                                 colunas_interesse: List[str] = None) -> pd.DataFrame:
        """
        Limpa e filtra o DataFrame extraído
        
        Args:
            df: DataFrame extraído do PDF
            ano: Ano dos dados
            colunas_interesse: Lista de colunas a manter (opcional)
            
        Returns:
            DataFrame limpo e filtrado
        """
        if df.empty:
            return pd.DataFrame()
        
        # Cria uma cópia para não modificar o original
        df_limpo = df.copy()
        
        # Remove linhas totalmente vazias
        df_limpo = df_limpo.dropna(how='all')
        
        # Tenta identificar coluna de estados
        coluna_estado = None
        for col in df_limpo.columns:
            valores_str = df_limpo[col].astype(str).str.lower()
            if any(estado.lower() in ' '.join(valores_str.values) 
                   for estado in self.estados_alvo):
                coluna_estado = col
                break
        
        if coluna_estado:
            # Filtra apenas os estados de interesse
            mask = df_limpo[coluna_estado].astype(str).str.contains(
                '|'.join(self.estados_alvo), 
                case=False, 
                na=False
            )
            df_limpo = df_limpo[mask]
        
        # Adiciona coluna de ano
        df_limpo['Ano'] = ano
        
        return df_limpo
    
    def processar_pdf(self, caminho_pdf: str, 
                      ano: int,
                      paginas_especificas: str = 'all') -> pd.DataFrame:
        """
        Processa um PDF completo e retorna DataFrame consolidado
        
        Args:
            caminho_pdf: Caminho para o PDF
            ano: Ano dos dados
            paginas_especificas: Páginas específicas para extrair
            
        Returns:
            DataFrame consolidado do ano
        """
        tabelas = self.extrair_tabelas_do_pdf(caminho_pdf, paginas_especificas)
        
        if not tabelas:
            return pd.DataFrame()
        
        # Processa cada tabela extraída
        dfs_processados = []
        for i, df in enumerate(tabelas):
            df_limpo = self.limpar_e_filtrar_dados(df, ano)
            if not df_limpo.empty:
                dfs_processados.append(df_limpo)
                print(f"   ✓ Tabela {i+1}: {len(df_limpo)} registros dos estados-alvo")
        
        # Consolida todas as tabelas do PDF
        if dfs_processados:
            return pd.concat(dfs_processados, ignore_index=True)
        
        return pd.DataFrame()
    
    def processar_multiplos_pdfs(self, 
                                  configuracao_pdfs: Dict[int, str]) -> pd.DataFrame:
        """
        Processa múltiplos PDFs de diferentes anos
        
        Args:
            configuracao_pdfs: Dicionário {ano: caminho_pdf}
            
        Returns:
            DataFrame consolidado de todos os anos
        """
        print("\n" + "="*70)
        print("📊 INICIANDO EXTRAÇÃO DE DADOS DOS ANUÁRIOS")
        print("="*70 + "\n")
        
        self.dados_consolidados = []
        
        for ano in sorted(configuracao_pdfs.keys()):
            caminho = configuracao_pdfs[ano]
            print(f"\n🗓️  Processando ano: {ano}")
            print("-" * 70)
            
            df_ano = self.processar_pdf(caminho, ano)
            
            if not df_ano.empty:
                self.dados_consolidados.append(df_ano)
                print(f"✅ Ano {ano}: {len(df_ano)} registros extraídos")
            else:
                print(f"⚠️  Ano {ano}: Nenhum dado extraído")
        
        # Consolida todos os anos
        if self.dados_consolidados:
            df_final = pd.concat(self.dados_consolidados, ignore_index=True)
            print("\n" + "="*70)
            print(f"✅ EXTRAÇÃO CONCLUÍDA: {len(df_final)} registros totais")
            print("="*70 + "\n")
            return df_final
        else:
            print("\n" + "="*70)
            print("⚠️  NENHUM DADO FOI EXTRAÍDO")
            print("="*70 + "\n")
            return pd.DataFrame()
    
    def transformar_para_formato_longo(self, df: pd.DataFrame,
                                        colunas_valor: List[str]) -> pd.DataFrame:
        """
        Transforma DataFrame de formato largo para longo (tidy data)
        
        Args:
            df: DataFrame em formato largo
            colunas_valor: Lista de colunas que contêm valores de violência
            
        Returns:
            DataFrame em formato longo
        """
        if df.empty:
            return pd.DataFrame()
        
        # Identifica colunas de identificação (não são valores)
        id_vars = [col for col in df.columns if col not in colunas_valor]
        
        # Transforma para formato longo
        df_longo = df.melt(
            id_vars=id_vars,
            value_vars=colunas_valor,
            var_name='Índice de Violência',
            value_name='Valor'
        )
        
        # Limpa valores
        df_longo['Valor'] = pd.to_numeric(df_longo['Valor'], errors='coerce')
        df_longo = df_longo.dropna(subset=['Valor'])
        
        return df_longo
    
    def salvar_dados(self, df: pd.DataFrame, 
                     caminho_saida: str,
                     formato: str = 'csv') -> bool:
        """
        Salva o DataFrame em arquivo
        
        Args:
            df: DataFrame para salvar
            caminho_saida: Caminho do arquivo de saída
            formato: 'csv' ou 'excel'
            
        Returns:
            True se salvou com sucesso
        """
        try:
            if formato.lower() == 'csv':
                df.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
            elif formato.lower() == 'excel':
                df.to_excel(caminho_saida, index=False, engine='openpyxl')
            
            print(f"💾 Dados salvos em: {caminho_saida}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar dados: {str(e)}")
            return False


# Função de conveniência para uso rápido
def extrair_dados_violencia(caminhos_pdfs: Dict[int, str],
                             estados: List[str] = None,
                             salvar_csv: bool = True,
                             arquivo_saida: str = 'dados/dados_consolidados.csv') -> pd.DataFrame:
    """
    Função de conveniência para extração rápida de dados
    
    Args:
        caminhos_pdfs: Dicionário {ano: caminho_pdf}
        estados: Lista de estados (padrão: Amazonas, Roraima, Acre)
        salvar_csv: Se True, salva resultado em CSV
        arquivo_saida: Caminho do arquivo CSV de saída
        
    Returns:
        DataFrame consolidado
    """
    extrator = ExtratorDadosPDF(estados_alvo=estados)
    df_final = extrator.processar_multiplos_pdfs(caminhos_pdfs)
    
    if salvar_csv and not df_final.empty:
        extrator.salvar_dados(df_final, arquivo_saida, formato='csv')
    
    return df_final
