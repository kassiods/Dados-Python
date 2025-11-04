"""
Módulo de Geração de Relatório PDF
Cria relatório acadêmico consolidando gráficos e análises
"""

from fpdf import FPDF
from typing import List, Optional, Dict
import os
from datetime import datetime


class RelatorioPDF(FPDF):
    """Classe customizada para gerar relatórios acadêmicos"""
    
    def __init__(self, titulo: str = "Análise de Violência contra Mulheres",
                 subtitulo: str = "Região Norte - Amazonas, Roraima e Acre",
                 periodo: str = "2015-2025"):
        """
        Inicializa o relatório
        
        Args:
            titulo: Título principal do relatório
            subtitulo: Subtítulo do relatório
            periodo: Período analisado
        """
        super().__init__()
        self.titulo_relatorio = titulo
        self.subtitulo_relatorio = subtitulo
        self.periodo = periodo
        self.margem_esquerda = 20
        self.margem_direita = 20
        self.largura_util = 210 - self.margem_esquerda - self.margem_direita
        
        # Configurações
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(self.margem_esquerda, 20, self.margem_direita)
    
    def header(self):
        """Cabeçalho das páginas"""
        if self.page_no() > 1:  # Não mostrar no título
            self.set_font('Arial', 'I', 9)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, self.titulo_relatorio, 0, 0, 'C')
            self.ln(5)
            self.set_draw_color(200, 200, 200)
            self.line(self.margem_esquerda, self.get_y(), 
                     210 - self.margem_direita, self.get_y())
            self.ln(10)
            self.set_text_color(0, 0, 0)
    
    def footer(self):
        """Rodapé das páginas"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        
        # Linha separadora
        self.set_draw_color(200, 200, 200)
        self.line(self.margem_esquerda, self.get_y() - 5,
                 210 - self.margem_direita, self.get_y() - 5)
        
        # Número da página e data
        pagina_texto = f'Página {self.page_no()}/{{nb}}'
        data_texto = datetime.now().strftime('%d/%m/%Y')
        
        self.cell(self.largura_util / 2, 10, data_texto, 0, 0, 'L')
        self.cell(self.largura_util / 2, 10, pagina_texto, 0, 0, 'R')
        self.set_text_color(0, 0, 0)
    
    def pagina_titulo(self, autor: str = "", instituicao: str = ""):
        """
        Cria página de título do relatório
        
        Args:
            autor: Nome do autor
            instituicao: Nome da instituição
        """
        self.add_page()
        
        # Espaço superior
        self.ln(40)
        
        # Título principal
        self.set_font('Arial', 'B', 24)
        self.set_text_color(30, 30, 80)
        self.multi_cell(0, 12, self.titulo_relatorio, 0, 'C')
        
        self.ln(5)
        
        # Subtítulo
        self.set_font('Arial', '', 16)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 10, self.subtitulo_relatorio, 0, 'C')
        
        self.ln(3)
        
        # Período
        self.set_font('Arial', 'I', 14)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Período: {self.periodo}', 0, 1, 'C')
        
        # Linha decorativa
        self.ln(10)
        self.set_draw_color(30, 30, 80)
        self.set_line_width(0.5)
        x_centro = 105
        self.line(x_centro - 30, self.get_y(), x_centro + 30, self.get_y())
        
        # Autor e instituição
        if autor or instituicao:
            self.ln(40)
            self.set_font('Arial', '', 12)
            self.set_text_color(0, 0, 0)
            
            if autor:
                self.cell(0, 10, f'Autor: {autor}', 0, 1, 'C')
            
            if instituicao:
                self.cell(0, 10, f'Instituição: {instituicao}', 0, 1, 'C')
        
        # Data e Local
        self.ln(20)
        self.set_font('Arial', 'I', 11)
        self.set_text_color(100, 100, 100)
        # Mês em português
        meses = {
            'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
            'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
            'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
            'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
        }
        data_en = datetime.now().strftime('%B de %Y')
        mes_en = datetime.now().strftime('%B')
        data_pt = data_en.replace(mes_en, meses.get(mes_en, mes_en))
        
        self.cell(0, 10, 'Picos - Piauí', 0, 1, 'C')
        self.cell(0, 10, data_pt, 0, 1, 'C')
        
        self.set_text_color(0, 0, 0)
        self.set_line_width(0.2)
    
    def capitulo_titulo(self, titulo: str):
        """
        Adiciona título de capítulo
        
        Args:
            titulo: Texto do título
        """
        self.ln(5)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(30, 30, 80)
        self.cell(0, 10, titulo, 0, 1, 'L')
        
        # Linha abaixo do título
        self.set_draw_color(30, 30, 80)
        self.set_line_width(0.5)
        self.line(self.margem_esquerda, self.get_y(),
                 self.margem_esquerda + 80, self.get_y())
        
        self.ln(8)
        self.set_text_color(0, 0, 0)
        self.set_line_width(0.2)
    
    def secao_titulo(self, titulo: str):
        """
        Adiciona título de seção
        
        Args:
            titulo: Texto do título
        """
        self.ln(3)
        self.set_font('Arial', 'B', 13)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, titulo, 0, 1, 'L')
        self.ln(2)
        self.set_text_color(0, 0, 0)
    
    def texto_paragrafo(self, texto: str):
        """
        Adiciona parágrafo de texto
        
        Args:
            texto: Conteúdo do parágrafo
        """
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, texto, 0, 'J')
        self.ln(3)
    
    def adicionar_imagem_centralizada(self, caminho_imagem: str, 
                                       largura: Optional[float] = None,
                                       legenda: str = ""):
        """
        Adiciona imagem centralizada com legenda
        
        Args:
            caminho_imagem: Caminho da imagem
            largura: Largura da imagem (None = largura máxima)
            legenda: Texto da legenda
        """
        if not os.path.exists(caminho_imagem):
            print(f"⚠️  Imagem não encontrada: {caminho_imagem}")
            return
        
        # Define largura
        if largura is None:
            largura = self.largura_util
        
        # Calcula posição X para centralizar
        x_pos = (210 - largura) / 2
        
        # Adiciona imagem
        try:
            self.image(caminho_imagem, x=x_pos, w=largura)
            
            # Adiciona legenda se fornecida
            if legenda:
                self.ln(3)
                self.set_font('Arial', 'I', 9)
                self.set_text_color(80, 80, 80)
                self.multi_cell(0, 5, legenda, 0, 'C')
                self.set_text_color(0, 0, 0)
            
            self.ln(5)
            
        except Exception as e:
            print(f"❌ Erro ao adicionar imagem {caminho_imagem}: {str(e)}")


class GeradorRelatorioCompleto:
    """Classe para gerar relatório completo com análises"""
    
    def __init__(self, titulo: str = "Análise de Violência contra Mulheres",
                 subtitulo: str = "Região Norte - Amazonas, Roraima e Acre",
                 periodo: str = "2015-2025"):
        """
        Inicializa o gerador de relatório
        
        Args:
            titulo: Título do relatório
            subtitulo: Subtítulo do relatório
            periodo: Período analisado
        """
        self.pdf = RelatorioPDF(titulo, subtitulo, periodo)
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.periodo = periodo
    
    def gerar_relatorio(self,
                        caminhos_graficos: List[str],
                        arquivo_saida: str = 'relatorio.pdf',
                        autor: str = "",
                        instituicao: str = "",
                        introducao: str = "",
                        conclusao: str = "",
                        metadados_graficos: Optional[Dict[str, str]] = None) -> bool:
        """
        Gera relatório completo
        
        Args:
            caminhos_graficos: Lista de caminhos das imagens dos gráficos
            arquivo_saida: Nome do arquivo PDF de saída
            autor: Nome do autor
            instituicao: Nome da instituição
            introducao: Texto de introdução
            conclusao: Texto de conclusão
            metadados_graficos: Dicionário com legendas personalizadas {caminho: legenda}
            
        Returns:
            True se gerou com sucesso
        """
        try:
            print("\n" + "="*70)
            print("📄 GERANDO RELATÓRIO PDF")
            print("="*70 + "\n")
            
            # Página de título
            print("📑 Criando página de título...")
            self.pdf.pagina_titulo(autor, instituicao)
            
            # Introdução
            if introducao:
                print("📝 Adicionando introdução...")
                self.pdf.add_page()
                self.pdf.capitulo_titulo("1. Introdução")
                self.pdf.texto_paragrafo(introducao)
            
            # Metodologia
            print("🔬 Adicionando metodologia...")
            self.pdf.add_page()
            self.pdf.capitulo_titulo("2. Metodologia")
            texto_metodologia = (
                "Este relatório apresenta uma análise quantitativa dos índices de violência "
                "contra mulheres nos estados do Amazonas, Roraima e Acre, no período de 2015 a 2025. "
                "Os dados foram extraídos dos Anuários Brasileiros de Segurança Pública publicados "
                "pelo Fórum Brasileiro de Segurança Pública (FBSP) e do Atlas da Violência do IPEA. "
                "\n\n"
                "A análise contempla diferentes tipos de violência, incluindo feminicídio, homicídio "
                "de mulheres, estupro e outras formas de agressão. Os dados foram consolidados em "
                "séries temporais para permitir a identificação de tendências e padrões ao longo do tempo."
            )
            self.pdf.texto_paragrafo(texto_metodologia)
            
            # Resultados e Análise
            print("📊 Adicionando gráficos...")
            self.pdf.add_page()
            self.pdf.capitulo_titulo("3. Resultados e Análise")
            
            metadados = metadados_graficos or {}
            
            for i, caminho in enumerate(caminhos_graficos, 1):
                if os.path.exists(caminho):
                    nome_arquivo = os.path.basename(caminho)
                    
                    # Determina tipo de gráfico
                    if 'serie_temporal' in nome_arquivo:
                        estado = nome_arquivo.split('_')[2].replace('.png', '').capitalize()
                        self.pdf.secao_titulo(f"3.{i}. Análise Temporal - {estado}")
                    elif 'comparativo' in nome_arquivo:
                        self.pdf.secao_titulo(f"3.{i}. Análise Comparativa entre Estados")
                    elif 'heatmap' in nome_arquivo:
                        self.pdf.secao_titulo(f"3.{i}. Mapa de Intensidade")
                    elif 'tendencia' in nome_arquivo:
                        self.pdf.secao_titulo(f"3.{i}. Tendência Geral da Região")
                    
                    # Legenda personalizada ou padrão
                    legenda = metadados.get(caminho, f"Figura {i}: {nome_arquivo}")
                    
                    self.pdf.adicionar_imagem_centralizada(
                        caminho,
                        largura=170,
                        legenda=legenda
                    )
                    
                    print(f"   ✓ Gráfico {i}/{len(caminhos_graficos)} adicionado")
                    
                    # Nova página a cada 2 gráficos
                    if i % 2 == 0 and i < len(caminhos_graficos):
                        self.pdf.add_page()
            
            # Conclusão
            if conclusao:
                print("📝 Adicionando conclusão...")
                self.pdf.add_page()
                self.pdf.capitulo_titulo("4. Conclusão")
                self.pdf.texto_paragrafo(conclusao)
            else:
                print("📝 Adicionando conclusão padrão...")
                self.pdf.add_page()
                self.pdf.capitulo_titulo("4. Conclusão")
                texto_conclusao = (
                    "A análise dos dados de violência contra mulheres na região Norte do Brasil, "
                    "especificamente nos estados do Amazonas, Roraima e Acre, revela a necessidade "
                    "urgente de políticas públicas efetivas de prevenção e combate à violência de gênero. "
                    "\n\n"
                    "Os gráficos apresentados evidenciam padrões e tendências que devem ser considerados "
                    "na formulação de estratégias de enfrentamento à violência contra a mulher, "
                    "levando em conta as particularidades regionais e os desafios específicos de cada estado."
                )
                self.pdf.texto_paragrafo(texto_conclusao)
            
            # Página de Fontes e Referências
            print("📚 Adicionando página de fontes...")
            self.pdf.add_page()
            self.pdf.capitulo_titulo("5. Fontes e Referências")
            
            # Subtítulo
            self.pdf.secao_titulo("5.1. Origem dos Dados")
            
            texto_fontes = (
                "Os dados analisados neste relatório são REAIS e foram extraídos diretamente dos "
                "Anuários Brasileiros de Segurança Pública oficiais, publicados pelo Fórum Brasileiro "
                "de Segurança Pública (FBSP) e pelo Instituto de Pesquisa Econômica Aplicada (IPEA). "
                "\n\n"
                "Todos os dados foram processados e analisados utilizando a linguagem de programação "
                "Python, com bibliotecas especializadas em ciência de dados (Pandas, NumPy) e "
                "visualização de informações (Matplotlib, Seaborn)."
            )
            self.pdf.texto_paragrafo(texto_fontes)
            
            # Referências Bibliográficas
            self.pdf.secao_titulo("5.2. Referências Bibliográficas")
            
            self.pdf.set_font('Arial', '', 10)
            self.pdf.ln(2)
            
            referencias = [
                "FÓRUM BRASILEIRO DE SEGURANÇA PÚBLICA. Anuário Brasileiro de Segurança Pública 2024. São Paulo: FBSP, 2024. Disponível em: https://forumseguranca.org.br/. Acesso em: 03 nov. 2025.",
                "",
                "FÓRUM BRASILEIRO DE SEGURANÇA PÚBLICA. Anuário Brasileiro de Segurança Pública 2023. São Paulo: FBSP, 2023. Disponível em: https://forumseguranca.org.br/. Acesso em: 03 nov. 2025.",
                "",
                "FÓRUM BRASILEIRO DE SEGURANÇA PÚBLICA. Anuário Brasileiro de Segurança Pública 2022. São Paulo: FBSP, 2022. Disponível em: https://forumseguranca.org.br/. Acesso em: 03 nov. 2025.",
                "",
                "FÓRUM BRASILEIRO DE SEGURANÇA PÚBLICA. Anuário Brasileiro de Segurança Pública 2020. São Paulo: FBSP, 2020. Disponível em: https://forumseguranca.org.br/. Acesso em: 03 nov. 2025.",
                "",
                "FÓRUM BRASILEIRO DE SEGURANÇA PÚBLICA. Anuário Brasileiro de Segurança Pública 2019. São Paulo: FBSP, 2019. Disponível em: https://forumseguranca.org.br/. Acesso em: 03 nov. 2025.",
                "",
                "FÓRUM BRASILEIRO DE SEGURANÇA PÚBLICA. Anuário Brasileiro de Segurança Pública 2017. São Paulo: FBSP, 2017. Disponível em: https://forumseguranca.org.br/. Acesso em: 03 nov. 2025.",
            ]
            
            for ref in referencias:
                if ref:
                    self.pdf.multi_cell(0, 5, ref, 0, 'J')
                else:
                    self.pdf.ln(2)
            
            # Ferramentas Utilizadas
            self.pdf.ln(5)
            self.pdf.secao_titulo("5.3. Ferramentas e Tecnologias")
            
            texto_ferramentas = (
                "Este relatório foi produzido utilizando as seguintes tecnologias:\n\n"
                "- Python 3.11: Linguagem de programação para análise de dados\n"
                "- Pandas: Manipulação e análise de dados estruturados\n"
                "- NumPy: Computação numérica e operações matemáticas\n"
                "- Matplotlib e Seaborn: Visualização de dados e criação de gráficos\n"
                "- Tabula-py: Extração de tabelas de documentos PDF\n"
                "- FPDF2: Geração de relatórios em formato PDF\n\n"
                "Todos os dados são provenientes de fontes oficiais do governo brasileiro "
                "e foram analisados de forma automatizada, garantindo precisão e reprodutibilidade."
            )
            self.pdf.texto_paragrafo(texto_ferramentas)
            
            # Salva o PDF
            self.pdf.alias_nb_pages()
            self.pdf.output(arquivo_saida)
            
            print("\n" + "="*70)
            print(f"✅ RELATÓRIO GERADO COM SUCESSO: {arquivo_saida}")
            print("="*70 + "\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Erro ao gerar relatório: {str(e)}")
            return False


# Função de conveniência
def gerar_relatorio_violencia(caminhos_graficos: List[str],
                                arquivo_saida: str = 'Relatorio_Violencia_Mulher.pdf',
                                **kwargs) -> bool:
    """
    Função de conveniência para gerar relatório
    
    Args:
        caminhos_graficos: Lista de caminhos dos gráficos
        arquivo_saida: Nome do arquivo de saída
        **kwargs: Argumentos adicionais (autor, instituicao, introducao, conclusao)
        
    Returns:
        True se gerou com sucesso
    """
    gerador = GeradorRelatorioCompleto()
    return gerador.gerar_relatorio(caminhos_graficos, arquivo_saida, **kwargs)
