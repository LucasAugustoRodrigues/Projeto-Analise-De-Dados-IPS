# Dashboard IPS Brasil 2024 - Versão Didática
# Projeto de Estatística e Probabilidade
# Aluno: Lucas

# =============================================================================
# IMPORTAÇÕES DAS BIBLIOTECAS
# =============================================================================

import streamlit as st      # Para criar a interface web
import pandas as pd         # Para manipular dados (tabelas)
import plotly.express as px # Para criar gráficos interativos
import numpy as np          # Para cálculos matemáticos

# =============================================================================
# CONFIGURAÇÃO INICIAL DA PÁGINA
# =============================================================================

# Configura como a página vai aparecer no navegador
st.set_page_config(
    page_title="Dashboard IPS Brasil 2024",  # Título da aba do navegador
    page_icon="🇧🇷",                        # Ícone da aba
    layout="wide"                            # Layout largo (usa toda a tela)
)

# =============================================================================
# FUNÇÃO PARA CARREGAR OS DADOS
# =============================================================================

@st.cache_data  # Decorator que faz o Streamlit "lembrar" dos dados carregados
def carregar_dados():
    """
    Esta função carrega os dados do arquivo Excel e faz algumas limpezas básicas.
    
    Returns:
        DataFrame: Tabela com os dados do IPS Brasil 2024
    """
    try:
        # Lê o arquivo Excel
        dados = pd.read_excel('Cpy_IPS_Brasil_2024.xlsx')
        
        # Renomeia algumas colunas para nomes mais simples
        dados = dados.rename(columns={
            'IPS Brasil 2024': 'IPS',
            'Necessidades Humanas Básicas': 'Necessidades_Basicas',
            'Fundamentos do Bem-estar': 'Bem_Estar',
            'Capital?': 'E_Capital'
        })
        
        # Padroniza a coluna Capital (alguns valores estavam diferentes)
        dados['E_Capital'] = dados['E_Capital'].replace({'Capital': 'Sim'})
        
        # Remove linhas que não têm valor de IPS
        dados = dados.dropna(subset=['IPS'])
        
        return dados
    
    except Exception as erro:
        st.error(f"Erro ao carregar o arquivo: {erro}")
        return None

# =============================================================================
# FUNÇÃO PRINCIPAL DO DASHBOARD
# =============================================================================

def main():
    """
    Função principal que controla todo o dashboard
    """
    
    # Título principal da página
    st.title("🇧🇷 Dashboard IPS Brasil 2024")
    st.subheader("Análise do Índice de Progresso Social dos Municípios Brasileiros")
    
    # Carrega os dados
    df = carregar_dados()
    
    # Se não conseguiu carregar os dados, para o programa
    if df is None:
        st.stop()
    
    # Barra lateral para navegação entre páginas
    st.sidebar.title("📊 Navegação")
    st.sidebar.write("Escolha uma análise:")
    
    # Menu de seleção na barra lateral
    pagina = st.sidebar.selectbox(
        "Selecione uma página:",
        [
            "📈 Visão Geral",
            "🗺️ Análise por Região", 
            "🏛️ Capitais vs Interior",
            "📊 Gráficos Detalhados"
        ]
    )
    
    # Mostra informações básicas na barra lateral
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Informações dos Dados")
    st.sidebar.info(f"""
    **Total de municípios:** {len(df):,}
    **Regiões analisadas:** {df['Região'].nunique()}
    **Estados:** {df['Estado'].nunique()}
    **IPS médio nacional:** {df['IPS'].mean():.2f}
    """)
    
    # Chama a função correspondente à página selecionada
    if pagina == "📈 Visão Geral":
        pagina_visao_geral(df)
    elif pagina == "🗺️ Análise por Região":
        pagina_analise_regional(df)
    elif pagina == "🏛️ Capitais vs Interior":
        pagina_capitais_vs_interior(df)
    elif pagina == "📊 Gráficos Detalhados":
        pagina_graficos_detalhados(df)

# =============================================================================
# PÁGINA 1: VISÃO GERAL
# =============================================================================

def pagina_visao_geral(df):
    """
    Página com estatísticas gerais e resumo dos dados
    """
    
    st.header("📈 Visão Geral do IPS Brasil")
    
    # ========== FILTROS INTERATIVOS ==========
    st.subheader("🎛️ Filtros Interativos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filtro por faixa de IPS
        ips_min, ips_max = st.slider(
            "📊 Faixa de IPS:",
            min_value=float(df['IPS'].min()),
            max_value=float(df['IPS'].max()),
            value=(float(df['IPS'].min()), float(df['IPS'].max())),
            step=0.1,
            help="Arraste para filtrar municípios por faixa de IPS"
        )
    
    with col2:
        # Filtro por número de municípios no Top
        num_top = st.selectbox(
            "🏆 Quantos no ranking?",
            options=[5, 10, 15, 20, 25],
            index=1,  # Padrão: 10
            help="Escolha quantos municípios mostrar no ranking"
        )
    
    with col3:
        # Checkbox para mostrar apenas capitais
        apenas_capitais = st.checkbox(
            "🏛️ Apenas Capitais",
            help="Marque para ver apenas as capitais brasileiras"
        )
    
    # Aplicar filtros
    df_filtrado = df[(df['IPS'] >= ips_min) & (df['IPS'] <= ips_max)]
    
    if apenas_capitais:
        df_filtrado = df_filtrado[df_filtrado['E_Capital'] == 'Sim']
        st.info(f"🏛️ Mostrando apenas capitais: {len(df_filtrado)} municípios")
    else:
        st.info(f"📊 Mostrando: {len(df_filtrado)} municípios (de {len(df)} total)")
    
    st.markdown("---")
    
    # Cria 4 colunas para mostrar métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    # Calcula estatísticas dos dados filtrados
    if len(df_filtrado) > 0:
        ips_medio = df_filtrado['IPS'].mean()
        ips_maximo = df_filtrado['IPS'].max()
        ips_minimo = df_filtrado['IPS'].min()
        desvio_padrao = df_filtrado['IPS'].std()
        
        # Encontra o melhor e pior município nos dados filtrados
        melhor_municipio = df_filtrado.loc[df_filtrado['IPS'].idxmax(), 'Município']
        pior_municipio = df_filtrado.loc[df_filtrado['IPS'].idxmin(), 'Município']
    else:
        st.warning("⚠️ Nenhum município atende aos filtros selecionados!")
        return
    
    # Mostra as métricas em caixas
    with col1:
        st.metric("🇧🇷 IPS Médio Nacional", f"{ips_medio:.2f}")
    
    with col2:
        st.metric("🏆 Maior IPS", f"{ips_maximo:.2f}", delta=melhor_municipio)
    
    with col3:
        st.metric("⚠️ Menor IPS", f"{ips_minimo:.2f}", delta=pior_municipio)
    
    with col4:
        st.metric("📊 Desvio Padrão", f"{desvio_padrao:.2f}")
    
    # Linha separadora
    st.markdown("---")
    
    # Cria duas colunas para os gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribuição do IPS")
        
        # Cria histograma (gráfico de barras da distribuição)
        fig_histograma = px.histogram(
            df_filtrado, 
            x='IPS', 
            nbins=30,  # Número de barras
            title="Como o IPS está distribuído entre os municípios filtrados",
            hover_data=['Município', 'Estado'],  # Mostra info ao passar o mouse
        )
        
        # Adiciona linha vertical na média
        fig_histograma.add_vline(
            x=ips_medio, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Média: {ips_medio:.2f}"
        )
        
        st.plotly_chart(fig_histograma, use_container_width=True)
    
    with col2:
        st.subheader(f"🏆 Top {num_top} Melhores Municípios")
        
        # Pega os N maiores valores de IPS (baseado na seleção do usuário)
        top_n = df_filtrado.nlargest(num_top, 'IPS')[['Município', 'Estado', 'Região', 'IPS']]
        
        # Cria gráfico de barras horizontal com degradê Turbo
        fig_top10 = px.bar(
            top_n,
            x='IPS',
            y='Município',
            orientation='h',
            title=f"Top {num_top} municípios com melhores índices",
            color='IPS',
            color_continuous_scale='Turbo',  # Degradê vibrante e bem distinto
            hover_data=['Estado', 'Região']
        )
        
        # Ajusta altura dinamicamente: máximo 500px, mínimo 300px
        altura_grafico = min(max(num_top * 25, 300), 500)
        
        fig_top10.update_layout(
            coloraxis_showscale=False,  # Remove barra de escala para visual limpo
            height=altura_grafico,  # Altura ajustável com rolagem
            yaxis={'categoryorder':'total ascending'}  # Ordena do menor para maior IPS
        )
        
        st.plotly_chart(fig_top10, use_container_width=True)
    
    # Seção de insights
    st.subheader("💡 Principais Descobertas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🎯 Variação do IPS**
        - IPS varia de {:.2f} a {:.2f}
        - Grande diferença entre municípios
        - Oportunidade de melhoria
        """.format(ips_minimo, ips_maximo))
    
    with col2:
        # Calcula quantos municípios estão acima da média
        acima_media = len(df[df['IPS'] > ips_medio])
        percentual = (acima_media / len(df)) * 100
        
        st.info(f"""
        **📊 Distribuição**
        - {acima_media} municípios acima da média
        - Isso representa {percentual:.1f}% do total
        - Distribuição relativamente equilibrada
        """)
    
    with col3:
        # Encontra a região com melhor IPS médio
        media_por_regiao = df.groupby('Região')['IPS'].mean()
        melhor_regiao = media_por_regiao.idxmax()
        
        st.info(f"""
        **🗺️ Destaque Regional**
        - Região **{melhor_regiao}** tem a melhor média
        - IPS médio: {media_por_regiao[melhor_regiao]:.2f}
        - Referência para as demais regiões
        """)
    
    # ========== SEÇÃO INTERATIVA DE COMPARAÇÃO ==========
    st.markdown("---")
    st.subheader("🔍 Explore os Dados Interativamente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🎯 Buscar Município Específico:**")
        municipio_busca = st.selectbox(
            "Digite ou selecione um município:",
            options=[''] + sorted(df['Município'].unique().tolist()),
            help="Busque informações de um município específico"
        )
        
        if municipio_busca:
            dados_municipio = df[df['Município'] == municipio_busca].iloc[0]
            
            st.success(f"""
            **📍 {municipio_busca} - {dados_municipio['Estado']}**
            
            - **IPS:** {dados_municipio['IPS']:.2f}
            - **Região:** {dados_municipio['Região']}
            - **Tipo:** {'Capital' if dados_municipio['E_Capital'] == 'Sim' else 'Interior'}
            - **Ranking Nacional:** {len(df[df['IPS'] > dados_municipio['IPS']]) + 1}º lugar
            """)
    
    with col2:
        st.write("**📊 Comparar com a Média Nacional:**")
        
        # Input para valor personalizado
        ips_comparacao = st.number_input(
            "Digite um valor de IPS para comparar:",
            min_value=0.0,
            max_value=100.0,
            value=df['IPS'].mean(),
            step=0.1,
            help="Compare qualquer valor com a distribuição nacional"
        )
        
        # Calcula posição percentual
        posicao_percentual = (len(df[df['IPS'] < ips_comparacao]) / len(df)) * 100
        
        if ips_comparacao > df['IPS'].mean():
            st.success(f"""
            **📈 IPS {ips_comparacao:.2f} está ACIMA da média nacional**
            
            - **{posicao_percentual:.1f}%** dos municípios têm IPS menor
            - **{100-posicao_percentual:.1f}%** dos municípios têm IPS maior
            - Diferença da média: **+{ips_comparacao - df['IPS'].mean():.2f}**
            """)
        else:
            st.warning(f"""
            **📉 IPS {ips_comparacao:.2f} está ABAIXO da média nacional**
            
            - **{posicao_percentual:.1f}%** dos municípios têm IPS menor
            - **{100-posicao_percentual:.1f}%** dos municípios têm IPS maior
            - Diferença da média: **{ips_comparacao - df['IPS'].mean():.2f}**
            """)

# =============================================================================
# PÁGINA 2: ANÁLISE POR REGIÃO
# =============================================================================

def pagina_analise_regional(df):
    """
    Página com análise detalhada por região do Brasil
    """
    
    st.header("🗺️ Análise por Região do Brasil")
    
    # ========== FILTROS AVANÇADOS ==========
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filtro por regiões
        regioes_disponiveis = df['Região'].unique()
        regioes_selecionadas = st.multiselect(
            "🗺️ Selecione as regiões:",
            regioes_disponiveis,
            default=regioes_disponiveis,  # Por padrão, seleciona todas
            help="Escolha quais regiões comparar"
        )
    
    with col2:
        # Filtro por tipo de análise
        tipo_visualizacao = st.selectbox(
            "📊 Tipo de visualização:",
            ["Médias por Região", "Box Plot (Distribuições)", "Todos os Municípios"],
            help="Escolha como visualizar os dados regionais"
        )
    
    with col3:
        # Filtro para incluir/excluir capitais
        incluir_capitais = st.radio(
            "🏛️ Incluir capitais?",
            ["Todos", "Apenas Capitais", "Apenas Interior"],
            help="Filtre por tipo de município"
        )
    
    # Aplica todos os filtros
    df_filtrado = df[df['Região'].isin(regioes_selecionadas)]
    
    # Filtro por tipo de município
    if incluir_capitais == "Apenas Capitais":
        df_filtrado = df_filtrado[df_filtrado['E_Capital'] == 'Sim']
    elif incluir_capitais == "Apenas Interior":
        df_filtrado = df_filtrado[df_filtrado['E_Capital'] == 'Não']
    
    if len(regioes_selecionadas) == 0:
        st.warning("⚠️ Selecione pelo menos uma região para ver a análise!")
        return
    
    if len(df_filtrado) == 0:
        st.warning("⚠️ Nenhum município atende aos filtros selecionados!")
        return
    
    st.success(f"📊 Analisando {len(df_filtrado)} municípios nas regiões selecionadas")
    
    # Calcula estatísticas por região
    stats_regiao = df_filtrado.groupby('Região')['IPS'].agg([
        ('Média', 'mean'),
        ('Mediana', 'median'),
        ('Máximo', 'max'),
        ('Mínimo', 'min'),
        ('Desvio Padrão', 'std')
    ]).round(2)
    
    # Mostra tabela com estatísticas
    st.subheader("📊 Estatísticas por Região")
    st.dataframe(stats_regiao, use_container_width=True)
    
    # Gráficos baseados no tipo de visualização selecionado
    if tipo_visualizacao == "Médias por Região":
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 IPS Médio por Região")
            
            # Calcula médias das regiões FILTRADAS
            media_regiao = df_filtrado.groupby('Região')['IPS'].mean().sort_values(ascending=False)
            
            # Cria gráfico de barras
            fig_media = px.bar(
                x=media_regiao.index,
                y=media_regiao.values,
                title=f"IPS Médio por Região ({incluir_capitais})",
                labels={'x': 'Região', 'y': 'IPS Médio'},
                color=media_regiao.values,
                color_continuous_scale='RdYlGn'
            )
            
            # Adiciona valores nas barras
            fig_media.update_traces(texttemplate='%{y:.2f}', textposition='outside')
            
            st.plotly_chart(fig_media, use_container_width=True)
        
        with col2:
            st.subheader("� Comparação com Nacional")
            
            # Calcula média nacional para comparação
            media_nacional = df['IPS'].mean()
            
            # Cria dados para comparação
            comparacao_data = []
            for regiao in media_regiao.index:
                comparacao_data.append({
                    'Região': regiao,
                    'IPS_Regiao': media_regiao[regiao],
                    'IPS_Nacional': media_nacional,
                    'Diferenca': media_regiao[regiao] - media_nacional
                })
            
            df_comparacao = pd.DataFrame(comparacao_data)
            
            fig_comp = px.bar(
                df_comparacao,
                x='Região',
                y=['IPS_Regiao', 'IPS_Nacional'],
                title="Região vs Média Nacional",
                barmode='group'
            )
            
            fig_comp.update_xaxes(tickangle=45)
            st.plotly_chart(fig_comp, use_container_width=True)
    
    elif tipo_visualizacao == "Box Plot (Distribuições)":
        
        st.subheader("📦 Distribuição do IPS por Região")
        
        # Cria box plot com dados filtrados
        fig_box = px.box(
            df_filtrado,
            x='Região',
            y='IPS',
            title=f"Distribuição do IPS ({incluir_capitais})",
            hover_data=['Município', 'Estado']
        )
        
        fig_box.update_xaxes(tickangle=45)
        st.plotly_chart(fig_box, use_container_width=True)
    
    else:  # "Todos os Municípios"
        
        st.subheader("🏆 Todos os Municípios por Região")
        
        # Gráfico de dispersão com todos os municípios
        fig_scatter = px.scatter(
            df_filtrado,
            x='Região',
            y='IPS',
            color='E_Capital',
            hover_data=['Município', 'Estado'],
            title=f"Todos os Municípios ({len(df_filtrado)} total)",
            color_discrete_map={'Sim': 'red', 'Não': 'blue'}
        )
        
        fig_scatter.update_xaxes(tickangle=45)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Ranking dos melhores municípios por região
    st.subheader("🏆 Melhor Município de Cada Região")
    
    # Para cada região, encontra o município com maior IPS
    melhores_por_regiao = df_filtrado.loc[df_filtrado.groupby('Região')['IPS'].idxmax()]
    melhores_por_regiao = melhores_por_regiao[['Região', 'Município', 'Estado', 'IPS']].sort_values('IPS', ascending=False)
    
    # Mostra em formato de tabela bonita
    st.dataframe(
        melhores_por_regiao,
        column_config={
            "IPS": st.column_config.ProgressColumn(
                "IPS",
                help="Índice de Progresso Social",
                min_value=0,
                max_value=df['IPS'].max(),
            ),
        },
        hide_index=True,
        use_container_width=True
    )

# =============================================================================
# PÁGINA 3: CAPITAIS VS INTERIOR
# =============================================================================

def pagina_capitais_vs_interior(df):
    """
    Página que compara capitais com cidades do interior
    """
    
    st.header("🏛️ Capitais vs Interior")
    
    # ========== OPÇÕES INTERATIVAS ==========
    st.subheader("🎛️ Personalize sua Análise")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Seletor de regiões para análise
        regioes_analise = st.multiselect(
            "🗺️ Analisar regiões específicas:",
            df['Região'].unique(),
            default=df['Região'].unique(),
            help="Escolha quais regiões incluir na comparação"
        )
    
    with col2:
        # Tipo de estatística a comparar
        estatistica_comparar = st.selectbox(
            "📊 Estatística para comparar:",
            ["Média", "Mediana", "Máximo", "Mínimo"],
            help="Escolha qual medida estatística focar"
        )
    
    with col3:
        # Mostrar teste estatístico
        mostrar_teste = st.checkbox(
            "📈 Mostrar análise estatística",
            value=True,
            help="Inclui interpretação estatística da diferença"
        )
    
    # Filtra dados pelas regiões selecionadas
    df_analise = df[df['Região'].isin(regioes_analise)]
    
    if len(df_analise) == 0:
        st.warning("⚠️ Selecione pelo menos uma região!")
        return
    
    # Separa os dados entre capitais e interior (dados filtrados)
    capitais = df_analise[df_analise['E_Capital'] == 'Sim']
    interior = df_analise[df_analise['E_Capital'] == 'Não']
    
    # Verifica se há dados suficientes
    if len(capitais) == 0:
        st.warning("⚠️ Não há capitais nas regiões selecionadas!")
        return
    if len(interior) == 0:
        st.warning("⚠️ Não há cidades do interior nas regiões selecionadas!")
        return
    
    # Mostra informações sobre os dados filtrados
    st.info(f"📊 Analisando {len(capitais)} capitais e {len(interior)} cidades do interior nas regiões selecionadas")
    
    # Calcula estatísticas baseadas na seleção do usuário
    if estatistica_comparar == "Média":
        ips_capitais = capitais['IPS'].mean()
        ips_interior = interior['IPS'].mean()
    elif estatistica_comparar == "Mediana":
        ips_capitais = capitais['IPS'].median()
        ips_interior = interior['IPS'].median()
    elif estatistica_comparar == "Máximo":
        ips_capitais = capitais['IPS'].max()
        ips_interior = interior['IPS'].max()
    else:  # Mínimo
        ips_capitais = capitais['IPS'].min()
        ips_interior = interior['IPS'].min()
    
    diferenca = ips_capitais - ips_interior
    
    # Mostra métricas comparativas
    st.subheader("📊 Comparação Geral")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            f"🏛️ {estatistica_comparar} - Capitais",
            f"{ips_capitais:.2f}",
            delta=f"{len(capitais)} municípios"
        )
    
    with col2:
        st.metric(
            f"🏘️ {estatistica_comparar} - Interior", 
            f"{ips_interior:.2f}",
            delta=f"{len(interior)} municípios"
        )
    
    with col3:
        st.metric(
            "⚖️ Diferença",
            f"{diferenca:.2f}",
            delta="Capital - Interior"
        )
    
    # Análise da diferença
    if diferenca > 0:
        st.success(f"✅ As capitais têm IPS {diferenca:.2f} pontos maior que o interior, em média.")
    else:
        st.info(f"ℹ️ O interior tem IPS {abs(diferenca):.2f} pontos maior que as capitais, em média.")
    
    st.markdown("---")
    
    # Gráficos comparativos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Distribuição Comparativa")
        
        # Cria dados para o histograma comparativo usando dados filtrados
        dados_comparacao = []
        
        # Adiciona dados das capitais filtradas
        for ips in capitais['IPS']:
            dados_comparacao.append({'IPS': ips, 'Tipo': 'Capital'})
        
        # Adiciona dados do interior filtrado
        for ips in interior['IPS']:
            dados_comparacao.append({'IPS': ips, 'Tipo': 'Interior'})
        
        # Converte para DataFrame
        df_comparacao = pd.DataFrame(dados_comparacao)
        
        # Cria histograma sobreposto
        fig_hist = px.histogram(
            df_comparacao,
            x='IPS',
            color='Tipo',
            title=f"Distribuição do IPS: Capitais vs Interior ({estatistica_comparar})",
            opacity=0.7,  # Transparência para ver sobreposição
            nbins=15,
            hover_data={'Tipo': True}
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        st.subheader("📊 Comparação por Região Filtrada")
        
        # Calcula estatística escolhida de capitais e interior por região (dados filtrados)
        if estatistica_comparar == "Média":
            comparacao_regional = df_analise.groupby(['Região', 'E_Capital'])['IPS'].mean().reset_index()
        elif estatistica_comparar == "Mediana":
            comparacao_regional = df_analise.groupby(['Região', 'E_Capital'])['IPS'].median().reset_index()
        elif estatistica_comparar == "Máximo":
            comparacao_regional = df_analise.groupby(['Região', 'E_Capital'])['IPS'].max().reset_index()
        else:  # Mínimo
            comparacao_regional = df_analise.groupby(['Região', 'E_Capital'])['IPS'].min().reset_index()
        
        # Cria gráfico de barras agrupadas
        fig_regiao = px.bar(
            comparacao_regional,
            x='Região',
            y='IPS',
            color='E_Capital',
            title=f"{estatistica_comparar} do IPS por região: Capital vs Interior",
            barmode='group',  # Barras lado a lado
            color_discrete_map={'Sim': 'red', 'Não': 'blue'}
        )
        
        fig_regiao.update_xaxes(tickangle=45)
        
        st.plotly_chart(fig_regiao, use_container_width=True)
    
    # Ranking das capitais filtradas
    st.subheader("🏆 Ranking das Capitais (Regiões Selecionadas)")
    
    # Ordena capitais filtradas por IPS
    ranking_capitais = capitais[['Município', 'Estado', 'Região', 'IPS']].sort_values('IPS', ascending=False)
    
    st.dataframe(
        ranking_capitais,
        column_config={
            "IPS": st.column_config.ProgressColumn(
                "IPS",
                min_value=0,
                max_value=df['IPS'].max(),
            ),
        },
        hide_index=True,
        use_container_width=True
    )

# =============================================================================
# PÁGINA 4: GRÁFICOS DETALHADOS
# =============================================================================

def pagina_graficos_detalhados(df):
    """
    Página com gráficos mais avançados e análises específicas
    """
    
    st.header("📊 Gráficos Detalhados")
    

    
    # Seletor de tipo de análise
    tipo_analise = st.selectbox(
        "Escolha o tipo de análise:",
        [
            "🔍 Correlação entre Variáveis",
            "📈 Análise de Componentes do IPS", 
            "🗺️ Mapa de Calor por Estado",
            "📊 Estatísticas Descritivas"
        ]
    )
    
    if tipo_analise == "🔍 Correlação entre Variáveis":
        analise_correlacao(df)
    elif tipo_analise == "📈 Análise de Componentes do IPS":
        analise_componentes(df)
    elif tipo_analise == "🗺️ Mapa de Calor por Estado":
        mapa_calor_estados(df)
    elif tipo_analise == "📊 Estatísticas Descritivas":
        estatisticas_descritivas(df)

def analise_correlacao(df):
    """
    Análise de correlação entre diferentes variáveis
    """
    
    st.subheader("🔍 Correlação entre Variáveis")
    
    # Lista de variáveis numéricas disponíveis para análise
    colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove colunas que não fazem sentido para correlação
    colunas_interesse = [col for col in colunas_numericas if col not in ['Código IBGE']]
    
    # Seletores para escolher variáveis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        variavel_x = st.selectbox("Variável X (horizontal):", colunas_interesse, index=0)
    
    with col2:
        variavel_y = st.selectbox("Variável Y (vertical):", colunas_interesse, index=1 if len(colunas_interesse) > 1 else 0)
    
    with col3:
        # Opção de colorir por região
        colorir_por = st.selectbox(
            "🎨 Colorir pontos por:",
            ["Região", "Capital/Interior", "Estado"],
            help="Escolha como colorir os pontos no gráfico"
        )
    
    if variavel_x != variavel_y:
        # Define coluna para colorir baseado na seleção
        if colorir_por == "Capital/Interior":
            cor_coluna = 'E_Capital'
        elif colorir_por == "Estado":
            cor_coluna = 'Estado'
        else:
            cor_coluna = 'Região'
        
        # Cria gráfico de dispersão (scatter plot)
        fig_scatter = px.scatter(
            df,
            x=variavel_x,
            y=variavel_y,
            color=cor_coluna,
            hover_data=['Município', 'Estado', 'Região', 'IPS'],
            title=f"Relação entre {variavel_x} e {variavel_y} (colorido por {colorir_por})",
            opacity=0.7  # Transparência para melhor visualização
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Calcula e mostra correlação
        correlacao = df[variavel_x].corr(df[variavel_y])
        
        if abs(correlacao) > 0.7:
            st.success(f"🔥 Correlação forte: {correlacao:.3f}")
        elif abs(correlacao) > 0.3:
            st.warning(f"⚡ Correlação moderada: {correlacao:.3f}")
        else:
            st.info(f"📊 Correlação fraca: {correlacao:.3f}")
    else:
        st.warning("⚠️ Selecione variáveis diferentes para ver a correlação!")

def analise_componentes(df):
    """
    Análise dos componentes do IPS
    """
    
    st.subheader("📈 Análise dos Componentes do IPS")
    
    # Componentes do IPS (se existirem no dataset)
    componentes = ['Necessidades_Basicas', 'Bem_Estar', 'Oportunidades']
    componentes_disponiveis = [comp for comp in componentes if comp in df.columns]
    
    if len(componentes_disponiveis) > 0:
        # Calcula médias dos componentes
        medias_componentes = df[componentes_disponiveis].mean()
        
        # Cria gráfico de barras dos componentes
        fig_componentes = px.bar(
            x=componentes_disponiveis,
            y=medias_componentes.values,
            title="Média Nacional dos Componentes do IPS",
            color=medias_componentes.values,
            color_continuous_scale='Viridis'
        )
        
        # Adiciona valores nas barras
        fig_componentes.update_traces(texttemplate='%{y:.2f}', textposition='outside')
        
        st.plotly_chart(fig_componentes, use_container_width=True)
        
        # Análise por região
        st.subheader("📊 Componentes por Região")
        
        # Calcula médias por região
        componentes_por_regiao = df.groupby('Região')[componentes_disponiveis].mean()
        
        # Cria gráfico de barras agrupadas
        fig_regiao_comp = px.bar(
            componentes_por_regiao.reset_index(),
            x='Região',
            y=componentes_disponiveis,
            title="Componentes do IPS por Região",
            barmode='group'
        )
        
        st.plotly_chart(fig_regiao_comp, use_container_width=True)
    else:
        st.warning("⚠️ Componentes do IPS não encontrados nos dados disponíveis.")

def mapa_calor_estados(df):
    """
    Cria mapa de calor com IPS médio por estado
    """
    
    st.subheader("🗺️ Mapa de Calor por Estado")
    
    # Calcula IPS médio por estado
    ips_por_estado = df.groupby('Estado')['IPS'].mean().sort_values(ascending=False)
    
    # Cria gráfico de barras horizontal
    fig_estados = px.bar(
        x=ips_por_estado.values,
        y=ips_por_estado.index,
        orientation='h',
        title="IPS Médio por Estado (do maior para o menor)",
        color=ips_por_estado.values,
        color_continuous_scale='RdYlGn',
        height=800  # Altura maior para acomodar todos os estados
    )
    
    fig_estados.update_layout(yaxis={'categoryorder':'total ascending'})
    
    st.plotly_chart(fig_estados, use_container_width=True)
    
    # Tabela com dados detalhados
    st.subheader("📊 Dados Detalhados por Estado")
    
    stats_estado = df.groupby('Estado')['IPS'].agg([
        ('Média', 'mean'),
        ('Municípios', 'count'),
        ('Máximo', 'max'),
        ('Mínimo', 'min')
    ]).round(2).sort_values('Média', ascending=False)
    
    st.dataframe(stats_estado, use_container_width=True)

def estatisticas_descritivas(df):
    """
    Mostra estatísticas descritivas detalhadas
    """
    
    st.subheader("📊 Estatísticas Descritivas Completas")
    
    # Estatísticas do IPS
    st.write("### 📈 Estatísticas do IPS")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Média", f"{df['IPS'].mean():.2f}")
    
    with col2:
        st.metric("📊 Mediana", f"{df['IPS'].median():.2f}")
    
    with col3:
        st.metric("📊 Desvio Padrão", f"{df['IPS'].std():.2f}")
    
    with col4:
        st.metric("📊 Coef. Variação", f"{(df['IPS'].std()/df['IPS'].mean()*100):.1f}%")
    
    # Quartis
    st.write("### 📦 Quartis e Percentis")
    
    quartis = df['IPS'].quantile([0.25, 0.5, 0.75])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Q1 (25%)", f"{quartis[0.25]:.2f}")
    
    with col2:
        st.metric("Q2 (50% - Mediana)", f"{quartis[0.5]:.2f}")
    
    with col3:
        st.metric("Q3 (75%)", f"{quartis[0.75]:.2f}")
    
    # Tabela descritiva completa
    st.write("### 📋 Tabela Completa de Estatísticas")
    
    # Seleciona apenas colunas numéricas
    colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove colunas que não fazem sentido
    colunas_para_analise = [col for col in colunas_numericas if col not in ['Código IBGE']]
    
    if len(colunas_para_analise) > 0:
        estatisticas = df[colunas_para_analise].describe().round(2)
        st.dataframe(estatisticas, use_container_width=True)
    
    # Interpretação dos resultados
    st.write("### 💡 Interpretação dos Resultados")
    
    ips_medio = df['IPS'].mean()
    ips_std = df['IPS'].std()
    
    st.info(f"""
    **📊 Resumo da Análise:**
    
    - O IPS médio nacional é {ips_medio:.2f}, com desvio padrão de {ips_std:.2f}
    - Isso significa que a maioria dos municípios tem IPS entre {(ips_medio-ips_std):.2f} e {(ips_medio+ips_std):.2f}
    - O coeficiente de variação mostra {'alta' if (ips_std/ips_medio) > 0.3 else 'baixa' if (ips_std/ips_medio) < 0.15 else 'moderada'} dispersão dos dados
    - Há {'grande' if (df['IPS'].max() - df['IPS'].min()) > 30 else 'pequena'} diferença entre o melhor e pior município
    """)

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    main()