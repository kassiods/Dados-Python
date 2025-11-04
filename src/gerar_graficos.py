"""
Módulo de Geração de Gráficos
Cria visualizações dos dados de violência contra mulheres
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional, Tuple
import os

# Configurações padrão do matplotlib
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Paleta de cores
PALETA_CORES = sns.color_palette("husl", 8)


class GeradorGraficos:
    """Classe para gerar gráficos de análise de violência"""
    
    def __init__(self, df_dados: pd.DataFrame, pasta_saida: str = 'graficos'):
        """
        Inicializa o gerador de gráficos
        
        Args:
            df_dados: DataFrame com os dados consolidados
            pasta_saida: Pasta onde os gráficos serão salvos
        """
        self.df = df_dados
        self.pasta_saida = pasta_saida
        self.arquivos_gerados = []
        
        # Cria pasta de saída se não existir
        os.makedirs(pasta_saida, exist_ok=True)
    
    def grafico_serie_temporal_por_estado(self, 
                                           estado: str,
                                           indices: Optional[List[str]] = None,
                                           salvar: bool = True) -> str:
        """
        Cria gráfico de série temporal para um estado específico
        
        Args:
            estado: Nome do estado
            indices: Lista de índices de violência a plotar (None = todos)
            salvar: Se True, salva o gráfico
            
        Returns:
            Caminho do arquivo salvo
        """
        # Filtra dados do estado
        df_estado = self.df[self.df['Estado'].str.contains(estado, case=False, na=False)]
        
        if df_estado.empty:
            print(f"⚠️  Nenhum dado encontrado para {estado}")
            return ""
        
        # Filtra índices se especificado
        if indices:
            df_estado = df_estado[df_estado['Índice de Violência'].isin(indices)]
        
        # Cria figura
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Plota linhas para cada índice
        for i, indice in enumerate(df_estado['Índice de Violência'].unique()):
            df_indice = df_estado[df_estado['Índice de Violência'] == indice]
            
            ax.plot(
                df_indice['Ano'], 
                df_indice['Valor'],
                marker='o',
                linewidth=2.5,
                markersize=8,
                label=indice,
                color=PALETA_CORES[i % len(PALETA_CORES)]
            )
        
        # Customização
        ax.set_title(
            f'Índices de Violência contra Mulheres - {estado} (2015-2025)',
            fontsize=16,
            fontweight='bold',
            pad=20
        )
        ax.set_xlabel('Ano', fontsize=13, fontweight='bold')
        ax.set_ylabel('Número de Ocorrências', fontsize=13, fontweight='bold')
        
        # Configurar eixo X com todos os anos
        anos_unicos = sorted(df_estado['Ano'].unique())
        ax.set_xticks(anos_unicos)
        ax.set_xticklabels(anos_unicos, rotation=45)
        
        # Grade e legenda
        ax.grid(True, linestyle='--', alpha=0.4, linewidth=0.8)
        ax.legend(title='Tipo de Violência', loc='best', framealpha=0.9)
        
        # Ajuste de layout
        plt.tight_layout()
        
        # Salvar
        if salvar:
            nome_arquivo = f'serie_temporal_{estado.lower().replace(" ", "_")}.png'
            caminho_completo = os.path.join(self.pasta_saida, nome_arquivo)
            plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
            self.arquivos_gerados.append(caminho_completo)
            print(f"✅ Gráfico salvo: {nome_arquivo}")
            plt.close()
            return caminho_completo
        else:
            plt.show()
            return ""
    
    def grafico_comparativo_estados(self,
                                     indice_violencia: str,
                                     tipo: str = 'linha',
                                     salvar: bool = True) -> str:
        """
        Cria gráfico comparando todos os estados para um índice específico
        
        Args:
            indice_violencia: Nome do índice de violência
            tipo: 'linha' ou 'barra'
            salvar: Se True, salva o gráfico
            
        Returns:
            Caminho do arquivo salvo
        """
        # Filtra dados do índice
        df_indice = self.df[self.df['Índice de Violência'].str.contains(
            indice_violencia, case=False, na=False
        )]
        
        if df_indice.empty:
            print(f"⚠️  Nenhum dado encontrado para {indice_violencia}")
            return ""
        
        # Cria figura
        fig, ax = plt.subplots(figsize=(12, 7))
        
        if tipo.lower() == 'linha':
            # Gráfico de linhas
            for i, estado in enumerate(df_indice['Estado'].unique()):
                df_estado = df_indice[df_indice['Estado'] == estado]
                
                ax.plot(
                    df_estado['Ano'],
                    df_estado['Valor'],
                    marker='o',
                    linewidth=2.5,
                    markersize=8,
                    label=estado,
                    color=PALETA_CORES[i % len(PALETA_CORES)]
                )
        
        elif tipo.lower() == 'barra':
            # Gráfico de barras agrupadas
            df_pivot = df_indice.pivot(index='Ano', columns='Estado', values='Valor')
            df_pivot.plot(kind='bar', ax=ax, color=PALETA_CORES[:len(df_pivot.columns)])
        
        # Customização
        ax.set_title(
            f'Comparativo entre Estados - {indice_violencia} (2015-2025)',
            fontsize=16,
            fontweight='bold',
            pad=20
        )
        ax.set_xlabel('Ano', fontsize=13, fontweight='bold')
        ax.set_ylabel('Número de Ocorrências', fontsize=13, fontweight='bold')
        
        if tipo.lower() == 'barra':
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        
        # Grade e legenda
        ax.grid(True, linestyle='--', alpha=0.4, axis='y')
        ax.legend(title='Estado', loc='best', framealpha=0.9)
        
        # Ajuste de layout
        plt.tight_layout()
        
        # Salvar
        if salvar:
            nome_arquivo = f'comparativo_{indice_violencia.lower().replace(" ", "_")}.png'
            caminho_completo = os.path.join(self.pasta_saida, nome_arquivo)
            plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
            self.arquivos_gerados.append(caminho_completo)
            print(f"✅ Gráfico salvo: {nome_arquivo}")
            plt.close()
            return caminho_completo
        else:
            plt.show()
            return ""
    
    def grafico_heatmap_estados_anos(self,
                                      indice_violencia: str,
                                      salvar: bool = True) -> str:
        """
        Cria heatmap mostrando a intensidade por estado e ano
        
        Args:
            indice_violencia: Nome do índice de violência
            salvar: Se True, salva o gráfico
            
        Returns:
            Caminho do arquivo salvo
        """
        # Filtra dados do índice
        df_indice = self.df[self.df['Índice de Violência'].str.contains(
            indice_violencia, case=False, na=False
        )]
        
        if df_indice.empty:
            print(f"⚠️  Nenhum dado encontrado para {indice_violencia}")
            return ""
        
        # Cria pivot table
        df_pivot = df_indice.pivot_table(
            index='Estado',
            columns='Ano',
            values='Valor',
            aggfunc='sum'
        )
        
        # Cria figura
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Heatmap
        sns.heatmap(
            df_pivot,
            annot=True,
            fmt='.0f',
            cmap='YlOrRd',
            linewidths=0.5,
            cbar_kws={'label': 'Ocorrências'},
            ax=ax
        )
        
        # Customização
        ax.set_title(
            f'Mapa de Calor - {indice_violencia} (2015-2025)',
            fontsize=16,
            fontweight='bold',
            pad=20
        )
        ax.set_xlabel('Ano', fontsize=13, fontweight='bold')
        ax.set_ylabel('Estado', fontsize=13, fontweight='bold')
        
        plt.tight_layout()
        
        # Salvar
        if salvar:
            nome_arquivo = f'heatmap_{indice_violencia.lower().replace(" ", "_")}.png'
            caminho_completo = os.path.join(self.pasta_saida, nome_arquivo)
            plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
            self.arquivos_gerados.append(caminho_completo)
            print(f"✅ Gráfico salvo: {nome_arquivo}")
            plt.close()
            return caminho_completo
        else:
            plt.show()
            return ""
    
    def grafico_tendencia_geral(self, salvar: bool = True) -> str:
        """
        Cria gráfico mostrando a tendência geral agregada de todos os estados
        
        Args:
            salvar: Se True, salva o gráfico
            
        Returns:
            Caminho do arquivo salvo
        """
        # Agrupa por ano e índice
        df_agregado = self.df.groupby(['Ano', 'Índice de Violência'])['Valor'].sum().reset_index()
        
        # Cria figura
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Plota cada índice
        for i, indice in enumerate(df_agregado['Índice de Violência'].unique()):
            df_indice = df_agregado[df_agregado['Índice de Violência'] == indice]
            
            ax.plot(
                df_indice['Ano'],
                df_indice['Valor'],
                marker='o',
                linewidth=2.5,
                markersize=8,
                label=indice,
                color=PALETA_CORES[i % len(PALETA_CORES)]
            )
        
        # Customização
        ax.set_title(
            'Tendência Geral de Violência - Região Norte (2015-2025)',
            fontsize=16,
            fontweight='bold',
            pad=20
        )
        ax.set_xlabel('Ano', fontsize=13, fontweight='bold')
        ax.set_ylabel('Total de Ocorrências', fontsize=13, fontweight='bold')
        
        # Grade e legenda
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.legend(title='Tipo de Violência', loc='best', framealpha=0.9)
        
        plt.tight_layout()
        
        # Salvar
        if salvar:
            nome_arquivo = 'tendencia_geral_regiao_norte.png'
            caminho_completo = os.path.join(self.pasta_saida, nome_arquivo)
            plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
            self.arquivos_gerados.append(caminho_completo)
            print(f"✅ Gráfico salvo: {nome_arquivo}")
            plt.close()
            return caminho_completo
        else:
            plt.show()
            return ""
    
    def gerar_todos_graficos(self) -> List[str]:
        """
        Gera todos os gráficos padrão do projeto
        
        Returns:
            Lista com caminhos dos arquivos gerados
        """
        print("\n" + "="*70)
        print("📊 GERANDO GRÁFICOS DE ANÁLISE")
        print("="*70 + "\n")
        
        self.arquivos_gerados = []
        
        # 1. Séries temporais por estado
        print("📈 Gerando séries temporais por estado...")
        for estado in self.df['Estado'].unique():
            self.grafico_serie_temporal_por_estado(estado)
        
        # 2. Comparativos entre estados
        print("\n📊 Gerando gráficos comparativos...")
        for indice in self.df['Índice de Violência'].unique():
            self.grafico_comparativo_estados(indice, tipo='linha')
        
        # 3. Heatmaps
        print("\n🔥 Gerando mapas de calor...")
        for indice in self.df['Índice de Violência'].unique():
            self.grafico_heatmap_estados_anos(indice)
        
        # 4. Tendência geral
        print("\n📈 Gerando gráfico de tendência geral...")
        self.grafico_tendencia_geral()
        
        print("\n" + "="*70)
        print(f"✅ GRÁFICOS GERADOS: {len(self.arquivos_gerados)} arquivos")
        print("="*70 + "\n")
        
        return self.arquivos_gerados


# Função de conveniência
def gerar_graficos_violencia(df_dados: pd.DataFrame,
                               pasta_saida: str = 'graficos') -> List[str]:
    """
    Função de conveniência para gerar todos os gráficos
    
    Args:
        df_dados: DataFrame com os dados
        pasta_saida: Pasta de saída dos gráficos
        
    Returns:
        Lista de caminhos dos arquivos gerados
    """
    gerador = GeradorGraficos(df_dados, pasta_saida)
    return gerador.gerar_todos_graficos()
