import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard IPS Brasil 2024",
    page_icon="🇧🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e88e5;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1e88e5;
        margin: 1rem 0;
    }
    .sidebar-info {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #1e88e5;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Cache para carregar dados
@st.cache_data
def load_data():
    """Carrega e processa os dados do IPS Brasil 2024"""
    try:
        df = pd.read_excel('Cpy_IPS_Brasil_2024.xlsx')
        
        # Renomeando colunas principais para facilitar o uso
        df = df.rename(columns={
            'IPS Brasil 2024': 'IPS',
            'Necessidades Humanas Básicas': 'NH_Basica',
            'Fundamentos do Bem-estar': 'Fund_Bem_Estar',
            'Oportunidades': 'Oportunidades',
            'Capital?': 'Capital',
            'Amazônia Legal?': 'Amazonia_Legal',
            'Expectativa de Vida ': 'Expectativa_Vida'
        })
        
        # Padronizar valores das colunas categóricas
        df['Capital'] = df['Capital'].replace({'Capital': 'Sim'})
        
        # Limpeza básica
        df = df.dropna(subset=['IPS'])
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

def main():
    # Título principal
    st.markdown('<h1 class="main-header">🇧🇷 Dashboard IPS Brasil 2024</h1>', unsafe_allow_html=True)
    st.markdown("### *Análise Interativa do Índice de Progresso Social nos Municípios Brasileiros*")
    
    # Carregando dados
    df = load_data()
    if df is None:
        st.stop()
    
    # Sidebar para navegação
    st.sidebar.markdown("""
    <div class="sidebar-info">
        <h3>🎯 Navegação</h3>
        <p>Selecione uma análise para explorar os dados do IPS Brasil 2024</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.selectbox(
        "Escolha a análise:",
        ["🏠 Visão Geral", "🗺️ Análise Regional", "⚖️ Comparações", "📊 Correlações", "🔍 Análise Detalhada"]
    )
    
    # Informações sobre o dataset na sidebar
    st.sidebar.markdown("### 📈 Sobre os Dados")
    st.sidebar.info(f"""
    **Total de municípios:** {len(df):,}
    
    **Regiões:** {df['Região'].nunique()}
    
    **Estados:** {df['Estado'].nunique()}
    
    **Capitais:** {len(df[df['Capital'] == 'Sim'])}
    
    **IPS Médio Nacional:** {df['IPS'].mean():.2f}
    """)
    
    # Roteamento de páginas
    if page == "🏠 Visão Geral":
        visao_geral(df)
    elif page == "🗺️ Análise Regional":
        analise_regional(df)
    elif page == "⚖️ Comparações":
        comparacoes(df)
    elif page == "📊 Correlações":
        correlacoes(df)
    elif page == "🔍 Análise Detalhada":
        analise_detalhada(df)

def visao_geral(df):
    """Página de visão geral com métricas principais"""
    st.header("🏠 Visão Geral do IPS Brasil 2024")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🇧🇷 IPS Médio Nacional",
            value=f"{df['IPS'].mean():.2f}",
            delta=f"Desvio: ±{df['IPS'].std():.2f}"
        )
    
    with col2:
        melhor_municipio = df.loc[df['IPS'].idxmax(), 'Município']
        st.metric(
            label="🥇 Melhor IPS",
            value=f"{df['IPS'].max():.2f}",
            delta=f"{melhor_municipio}"
        )
    
    with col3:
        pior_municipio = df.loc[df['IPS'].idxmin(), 'Município']
        st.metric(
            label="⚠️ Menor IPS",
            value=f"{df['IPS'].min():.2f}",
            delta=f"{pior_municipio}"
        )
    
    with col4:
        amplitude = df['IPS'].max() - df['IPS'].min()
        st.metric(
            label="📏 Amplitude",
            value=f"{amplitude:.2f}",
            delta="Diferença Max-Min"
        )
    
    st.markdown("---")
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Distribuição do IPS no Brasil")
        fig_hist = px.histogram(
            df, x='IPS', nbins=50,
            title="Distribuição do Índice de Progresso Social",
            color_discrete_sequence=['#1e88e5']
        )
        fig_hist.add_vline(x=df['IPS'].mean(), line_dash="dash", line_color="red", 
                          annotation_text=f"Média: {df['IPS'].mean():.2f}")
        fig_hist.update_layout(showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        st.subheader("🏆 Top 10 Melhores Municípios")
        top10 = df.nlargest(10, 'IPS')[['Município', 'Estado', 'IPS']]
        fig_top10 = px.bar(
            top10, x='IPS', y='Município',
            title="Municípios com Maior IPS",
            color='IPS',
            color_continuous_scale='Viridis',
            orientation='h'
        )
        fig_top10.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top10, use_container_width=True)
    
    # Análise por componentes
    st.subheader("🔍 Decomposição do IPS por Componentes")
    
    componentes = ['NH_Basica', 'Fund_Bem_Estar', 'Oportunidades']
    medias_componentes = df[componentes].mean()
    
    fig_componentes = go.Figure()
    fig_componentes.add_trace(go.Bar(
        x=componentes,
        y=medias_componentes.values,
        text=[f'{val:.2f}' for val in medias_componentes.values],
        textposition='auto',
        marker_color=['#ff7f0e', '#2ca02c', '#d62728']
    ))
    fig_componentes.update_layout(
        title="Média Nacional dos Componentes do IPS",
        xaxis_title="Componentes",
        yaxis_title="Valor Médio",
        showlegend=False
    )
    st.plotly_chart(fig_componentes, use_container_width=True)
    
    # Insights principais
    st.subheader("💡 Principais Insights")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Concentração Regional**
        - Sul e Sudeste lideram o ranking
        - Norte e Nordeste precisam de maior atenção
        - Diferenças significativas entre regiões
        """)
    
    with col2:
        st.markdown("""
        **🏙️ Efeito Capital**
        - Capitais geralmente têm IPS superior
        - Interior apresenta maior variabilidade
        - Oportunidades de desenvolvimento regional
        """)
    
    with col3:
        st.markdown("""
        **⚖️ Desigualdades**
        - Grande amplitude entre municípios
        - Necessidade de políticas focalizadas
        - Potencial de crescimento significativo
        """)

def analise_regional(df):
    """Análise detalhada por região com filtros interativos"""
    st.header("🗺️ Análise Regional do IPS")
    
    # Filtros interativos
    col1, col2 = st.columns(2)
    
    with col1:
        regioes_selecionadas = st.multiselect(
            "Selecione as regiões:",
            options=df['Região'].unique(),
            default=df['Região'].unique()
        )
    
    with col2:
        tipo_analise = st.selectbox(
            "Tipo de análise:",
            ["Média por Região", "Distribuição Completa", "Comparação de Estados"]
        )
    
    # Filtrando dados
    df_filtrado = df[df['Região'].isin(regioes_selecionadas)]
    
    if tipo_analise == "Média por Região":
        st.subheader("📊 Comparação das Médias Regionais")
        
        # Gráfico de médias por região
        medias_regiao = df_filtrado.groupby('Região')['IPS'].mean().sort_values(ascending=False)
        
        fig_regiao = px.bar(
            x=medias_regiao.index,
            y=medias_regiao.values,
            title="IPS Médio por Região",
            color=medias_regiao.values,
            color_continuous_scale='RdYlGn'
        )
        fig_regiao.update_layout(xaxis_title="Região", yaxis_title="IPS Médio")
        st.plotly_chart(fig_regiao, use_container_width=True)
        
        # Tabela com estatísticas
        stats_regiao = df_filtrado.groupby('Região')['IPS'].agg(['mean', 'median', 'std', 'min', 'max']).round(2)
        st.subheader("📋 Estatísticas Detalhadas por Região")
        st.dataframe(stats_regiao, use_container_width=True)
    
    elif tipo_analise == "Distribuição Completa":
        st.subheader("📈 Distribuição do IPS por Região")
        
        fig_violin = px.violin(
            df_filtrado, x='Região', y='IPS',
            box=True,
            title="Distribuição do IPS por Região (com quartis)",
            color='Região'
        )
        st.plotly_chart(fig_violin, use_container_width=True)
        
        # Análise dos extremos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Melhores por Região")
            for regiao in regioes_selecionadas:
                melhor = df_filtrado[df_filtrado['Região'] == regiao].nlargest(1, 'IPS')
                if not melhor.empty:
                    st.write(f"**{regiao}**: {melhor.iloc[0]['Município']} ({melhor.iloc[0]['IPS']:.2f})")
        
        with col2:
            st.subheader("⚠️ Menores por Região")
            for regiao in regioes_selecionadas:
                pior = df_filtrado[df_filtrado['Região'] == regiao].nsmallest(1, 'IPS')
                if not pior.empty:
                    st.write(f"**{regiao}**: {pior.iloc[0]['Município']} ({pior.iloc[0]['IPS']:.2f})")
    
    else:  # Comparação de Estados
        st.subheader("🏛️ Análise por Estados")
        
        # Top estados por IPS médio
        medias_estado = df_filtrado.groupby(['Região', 'Estado'])['IPS'].mean().sort_values(ascending=False)
        
        fig_estados = px.bar(
            x=medias_estado.values,
            y=[f"{estado} ({regiao})" for regiao, estado in medias_estado.index],
            orientation='h',
            title="IPS Médio por Estado",
            color=medias_estado.values,
            color_continuous_scale='Viridis'
        )
        fig_estados.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_estados, use_container_width=True)

def comparacoes(df):
    """Análise comparativa entre diferentes grupos"""
    st.header("⚖️ Análises Comparativas")
    
    tipo_comparacao = st.selectbox(
        "Escolha o tipo de comparação:",
        ["Capitais vs Interior", "Amazônia Legal vs Demais", "Componentes do IPS", "Análise Socioeconômica"]
    )
    
    if tipo_comparacao == "Capitais vs Interior":
        st.subheader("🏛️ Capitais vs Interior")
        
        # Comparação básica
        col1, col2 = st.columns(2)
        
        capitais = df[df['Capital'] == 'Sim']
        interior = df[df['Capital'] == 'Não']
        
        with col1:
            st.metric(
                "🏛️ IPS Médio - Capitais",
                f"{capitais['IPS'].mean():.2f}",
                delta=f"vs Nacional: +{(capitais['IPS'].mean() - df['IPS'].mean()):.2f}"
            )
        
        with col2:
            st.metric(
                "🏘️ IPS Médio - Interior",
                f"{interior['IPS'].mean():.2f}",
                delta=f"vs Nacional: {(interior['IPS'].mean() - df['IPS'].mean()):.2f}"
            )
        
        # Gráfico comparativo por região
        df_comp = df.copy()
        df_comp['Tipo'] = df_comp['Capital'].map({'Sim': 'Capital', 'Não': 'Interior'})
        
        fig_comp = px.box(
            df_comp, x='Região', y='IPS', color='Tipo',
            title="Distribuição IPS: Capitais vs Interior por Região"
        )
        st.plotly_chart(fig_comp, use_container_width=True)
        
    elif tipo_comparacao == "Amazônia Legal vs Demais":
        st.subheader("🌳 Amazônia Legal vs Demais Regiões")
        
        amazonia = df[df['Amazonia_Legal'] == 'Sim']
        demais = df[df['Amazonia_Legal'] == 'Não']
        
        # Métricas comparativas
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "🌳 IPS Médio - Amazônia Legal",
                f"{amazonia['IPS'].mean():.2f}",
                delta=f"vs Nacional: {(amazonia['IPS'].mean() - df['IPS'].mean()):.2f}"
            )
        
        with col2:
            st.metric(
                "🏙️ IPS Médio - Demais",
                f"{demais['IPS'].mean():.2f}",
                delta=f"vs Nacional: +{(demais['IPS'].mean() - df['IPS'].mean()):.2f}"
            )
        
        # Análise por componentes
        componentes = ['NH_Basica', 'Fund_Bem_Estar', 'Oportunidades']
        
        comp_amazonia = amazonia[componentes].mean()
        comp_demais = demais[componentes].mean()
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            name='Amazônia Legal',
            x=componentes,
            y=comp_amazonia.values,
            marker_color='green'
        ))
        fig_comp.add_trace(go.Bar(
            name='Demais Regiões',
            x=componentes,
            y=comp_demais.values,
            marker_color='blue'
        ))
        
        fig_comp.update_layout(
            title="Comparação dos Componentes: Amazônia Legal vs Demais",
            barmode='group',
            xaxis_title="Componentes do IPS",
            yaxis_title="Valor Médio"
        )
        st.plotly_chart(fig_comp, use_container_width=True)
    
    elif tipo_comparacao == "Componentes do IPS":
        st.subheader("📊 Análise Detalhada dos Componentes")
        
        regiao_selecionada = st.selectbox(
            "Selecione uma região para análise detalhada:",
            ['Todas'] + list(df['Região'].unique())
        )
        
        if regiao_selecionada != 'Todas':
            df_comp = df[df['Região'] == regiao_selecionada]
        else:
            df_comp = df
        
        # Correlação entre componentes
        componentes = ['NH_Basica', 'Fund_Bem_Estar', 'Oportunidades']
        corr_matrix = df_comp[componentes].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title=f"Correlação entre Componentes - {regiao_selecionada}"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Scatter matrix dos componentes
        fig_scatter = px.scatter_matrix(
            df_comp,
            dimensions=componentes,
            title="Relação entre todos os Componentes do IPS"
        )
        fig_scatter.update_layout(height=600)
        st.plotly_chart(fig_scatter, use_container_width=True)

def correlacoes(df):
    """Análise de correlações e relações entre variáveis"""
    st.header("📊 Análise de Correlações")
    
    # Seleção de variáveis para análise
    variaveis_interesse = [
        'IPS', 'NH_Basica', 'Fund_Bem_Estar', 'Oportunidades',
        'Expectativa_Vida', 'Ideb Ensino Fundamental', 'Nota Média no Enem',
        'Mortalidade Infantil até 5 anos', 'Homicídios', 'Obesidade'
    ]
    
    # Filtrar apenas colunas que existem
    variaveis_disponiveis = [var for var in variaveis_interesse if var in df.columns]
    
    st.subheader("🎯 Selecione as variáveis para análise")
    variaveis_selecionadas = st.multiselect(
        "Variáveis:",
        options=variaveis_disponiveis,
        default=variaveis_disponiveis[:6]
    )
    
    if len(variaveis_selecionadas) >= 2:
        # Matriz de correlação
        df_numeric = df[variaveis_selecionadas].select_dtypes(include=[np.number])
        corr_matrix = df_numeric.corr()
        
        # Heatmap de correlações
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Matriz de Correlação",
            color_continuous_scale="RdBu"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Análise de scatter plots
        st.subheader("🔍 Análise de Relações Específicas")
        
        col1, col2 = st.columns(2)
        with col1:
            var_x = st.selectbox("Variável X:", variaveis_selecionadas)
        with col2:
            var_y = st.selectbox("Variável Y:", [v for v in variaveis_selecionadas if v != var_x])
        
        if var_x and var_y:
            fig_scatter = px.scatter(
                df, x=var_x, y=var_y,
                color='Região',
                size='IPS',
                hover_data=['Município', 'Estado'],
                title=f"Relação entre {var_x} e {var_y}"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Estatísticas da correlação
            corr_valor = df[var_x].corr(df[var_y])
            st.info(f"**Correlação entre {var_x} e {var_y}: {corr_valor:.3f}**")
            
            if abs(corr_valor) > 0.7:
                st.success("🔥 Correlação forte!")
            elif abs(corr_valor) > 0.3:
                st.warning("⚡ Correlação moderada")
            else:
                st.info("📊 Correlação fraca")

def analise_detalhada(df):
    """Análise detalhada e exploração livre dos dados"""
    st.header("🔍 Análise Detalhada")
    
    st.subheader("🎯 Exploração Personalizada")
    
    # Filtros múltiplos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        regiao_filtro = st.multiselect(
            "Região:",
            options=df['Região'].unique(),
            default=df['Região'].unique()
        )
    
    with col2:
        capital_filtro = st.multiselect(
            "Tipo de Município:",
            options=df['Capital'].unique(),
            default=df['Capital'].unique()
        )
    
    with col3:
        amazonia_filtro = st.multiselect(
            "Amazônia Legal:",
            options=df['Amazonia_Legal'].unique(),
            default=df['Amazonia_Legal'].unique()
        )
    
    # Aplicar filtros
    df_filtrado = df[
        (df['Região'].isin(regiao_filtro)) &
        (df['Capital'].isin(capital_filtro)) &
        (df['Amazonia_Legal'].isin(amazonia_filtro))
    ]
    
    # Filtro por IPS
    ips_range = st.slider(
        "Faixa de IPS:",
        float(df['IPS'].min()),
        float(df['IPS'].max()),
        (float(df['IPS'].min()), float(df['IPS'].max()))
    )
    
    df_filtrado = df_filtrado[
        (df_filtrado['IPS'] >= ips_range[0]) & 
        (df_filtrado['IPS'] <= ips_range[1])
    ]
    
    st.info(f"📊 **{len(df_filtrado):,} municípios** selecionados com os filtros aplicados")
    
    # Análise dos dados filtrados
    if len(df_filtrado) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Distribuição IPS (Filtrado)")
            fig_hist = px.histogram(
                df_filtrado, x='IPS',
                title="Distribuição do IPS nos Municípios Selecionados"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            st.subheader("🏆 Top 10 Selecionados")
            top_filtrado = df_filtrado.nlargest(10, 'IPS')[['Município', 'Estado', 'Região', 'IPS']]
            st.dataframe(top_filtrado, use_container_width=True)
        
        # Análise personalizada por indicador
        st.subheader("📊 Análise por Indicador Específico")
        
        # Lista de indicadores interessantes
        indicadores = [
            'Expectativa_Vida', 'Ideb Ensino Fundamental', 'Homicídios',
            'Mortalidade Infantil até 5 anos', 'Obesidade', 'Suicídios',
            'Empregados com Ensino Superior', 'Gravidez na Adolescência (<19)'
        ]
        
        indicadores_disponiveis = [ind for ind in indicadores if ind in df.columns]
        
        indicador_selecionado = st.selectbox(
            "Selecione um indicador para análise:",
            indicadores_disponiveis
        )
        
        if indicador_selecionado:
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico do indicador vs IPS
                fig_scatter = px.scatter(
                    df_filtrado, x=indicador_selecionado, y='IPS',
                    color='Região',
                    hover_data=['Município', 'Estado'],
                    title=f"{indicador_selecionado} vs IPS"
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            with col2:
                # Distribuição do indicador por região
                fig_box = px.box(
                    df_filtrado, x='Região', y=indicador_selecionado,
                    title=f"Distribuição de {indicador_selecionado} por Região"
                )
                fig_box.update_xaxes(tickangle=45)
                st.plotly_chart(fig_box, use_container_width=True)
        
        # Tabela interativa dos dados
        st.subheader("📋 Dados Detalhados")
        
        colunas_mostrar = st.multiselect(
            "Selecione as colunas para visualizar:",
            options=df.columns.tolist(),
            default=['Município', 'Estado', 'Região', 'IPS', 'NH_Basica', 'Fund_Bem_Estar', 'Oportunidades']
        )
        
        if colunas_mostrar:
            st.dataframe(
                df_filtrado[colunas_mostrar].sort_values('IPS', ascending=False),
                use_container_width=True
            )
    
    else:
        st.warning("⚠️ Nenhum município atende aos critérios selecionados. Ajuste os filtros.")

if __name__ == "__main__":
    main()
