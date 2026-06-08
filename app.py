import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração Global da Página e Estilo Visual (Princípios de Gestalt)
st.set_page_config(
    page_title="Cinema Ratings Analytics",
    page_icon="🎬",
    layout="wide"
)

# Injeção de CSS para customização dos cartões de KPI focados em Notas e Votos
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #ffffff !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 11px !important;
        color: #9ca3af !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] {
        background-color: #0b1329;
        padding: 12px 15px;
        border-radius: 6px;
        border-left: 4px solid #e76f51;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Pipeline de ETL com Cache Centralizado
@st.cache_data
def carregar_dados_sistema():
    filme = pd.read_csv("tb_filme.csv", sep=";")
    genero = pd.read_csv("tb_genero.csv", sep=";")
    filme_genero = pd.read_csv("tb_filme_genero.csv", sep=";")
    diretor = pd.read_csv("tb_diretor.csv", sep=";")
    ator = pd.read_csv("tb_ator.csv", sep=";")
    filme_ator = pd.read_csv("tb_filme_ator.csv", sep=";")
    calendario = pd.read_csv("d_calendario.csv", sep=";")
    
    # Padronização de tipos temporais
    filme["data_lanc"] = pd.to_datetime(filme["data_lanc"], errors="coerce")
    calendario["data"] = pd.to_datetime(calendario["data"], errors="coerce")
    filme["ano_lanc"] = filme["data_lanc"].dt.year
    
    return filme, genero, filme_genero, diretor, ator, filme_ator, calendario

df_filme, df_genero, df_filme_genero, df_diretor, df_ator, df_filme_ator, df_calendario = carregar_dados_sistema()

# 3. Definição da Página Inicial Introdutória
def pagina_inicial():
    st.title("🎬 Projeto Analítico de Dados Abertos — Indústria Cinematográfica")
    st.markdown("### Entendimento do Negócio e Arquitetura do Projeto")
    st.markdown("---")
    
    col_texto, col_info = st.columns([1.8, 1.2])
    
    with col_texto:
        st.markdown("""
        #### Definição do Problema
        Como os fatores de produção (*gênero cinematográfico, época de lançamento e composição de equipe técnica*) 
        determinam diretamente a aceitação crítica (notas ponderadas) e o engajamento do público (volume de votos) de uma obra?
        
        #### Matriz de KPIs de Avaliações
        - **Amostragem:** Contagem de títulos únicos avaliados.
        - **Volume Total de Votos:** Mensuração da tração e engajamento do público.
        - **Nota Média Ponderada:** Avaliação real ponderada pelo volume de votos por título.
        - **Popularidade Média:** Índice de interesse contínuo medido pela plataforma.
        - **Taxa de Excelência (≥7):** Proporção de filmes com alta aceitação crítica.
        """)
        
    with col_info:
        st.markdown("### Escopo do DER Normalizado")
        st.info("""
        O modelo de dados original foi decomposto em Tabelas Fato e Dimensões (3ª Forma Normal):
        - **tb_filme:** Entidade centralizadora com granularidade única por título.
        - **d_calendario:** Dimensão temporal contínua para inteligência de tempo.
        - **tb_diretor & tb_ator:** Dimensões cadastrais de equipe técnica.
        - **tb_filme_genero & tb_filme_ator:** Entidades associativas para quebra de cardinalidades N:M.
        """)
    
    st.success("Use o menu de navegação na barra lateral esquerda para acessar o Painel Analítico Interativo.")

# 4. Definição do Painel Analítico Interativo
def painel_analitico():
    st.title("📊 Painel Analítico de Avaliações")
    st.markdown("Explore o impacto cruzado das variáveis sobre os indicadores de classificação do público.")
    st.markdown("---")
    
    # Painel Lateral de Filtros (Fatores de Produção)
    st.sidebar.header("Filtros Segmentadores")
    
    # Filtro 1: Ano de Lançamento (d_calendario)
    anos = sorted(df_calendario["ano"].dropna().unique().astype(int))
    ano_ini, ano_fim = st.sidebar.select_slider("1. Período Histórico", options=anos, value=(min(anos), max(anos)))
    
    # Filtro 2: Gênero (tb_genero)
    lista_gen = ["Todos"] + sorted(df_genero["nome_genero"].dropna().tolist())
    gen_sel = st.sidebar.selectbox("2. Gênero", lista_gen)
    
    # Filtro 3: Direção (tb_diretor)
    lista_dir = ["Todos"] + sorted(df_diretor["nome_diretor"].dropna().tolist())
    dir_sel = st.sidebar.selectbox("3. Diretor", lista_dir)
    
    # Filtro 4: Elenco (tb_ator)
    lista_act = ["Todos"] + sorted(df_ator["nome_ator"].dropna().tolist())
    act_sel = st.sidebar.selectbox("4. Ator/Atriz Principal", lista_act)
    
    # Motor de Filtragem Cruzada Relacional
    datas_validas = df_calendario[(df_calendario["ano"] >= ano_ini) & (df_calendario["ano"] <= ano_fim)]["data"]
    df_f = df_filme[df_filme["data_lanc"].isin(datas_validas)]
    
    if gen_sel != "Todos":
        id_g = df_genero[df_genero["nome_genero"] == gen_sel]["id_genero"].values[0]
        ids_f_g = df_filme_genero[df_filme_genero["id_genero"] == id_g]["id_filme"]
        df_f = df_f[df_f["id_filme"].isin(ids_f_g)]
        
    if dir_sel != "Todos":
        id_d = df_diretor[df_diretor["nome_diretor"] == dir_sel]["id_diretor"].values[0]
        df_f = df_f[df_f["id_diretor"] == id_d]
        
    if act_sel != "Todos":
        id_a = df_ator[df_ator["nome_ator"] == act_sel]["id_ator"].values[0]
        ids_f_a = df_filme_ator[df_filme_ator["id_ator"] == id_a]["id_filme"]
        df_f = df_f[df_f["id_filme"].isin(ids_f_a)]
        
    # Processamento da Matriz de KPIs
    total_titulos = int(df_f["id_filme"].count())
    votos_totais = int(df_f["vote_count"].sum())
    
    nota_ponderada = (df_f["vote_average"] * df_f["vote_count"]).sum() / votos_totais if votos_totais > 0 else 0.0
    popularidade_media = float(df_f["popularity"].mean()) if total_titulos > 0 else 0.0
    
    filmes_bons = df_f[df_f["vote_average"] >= 7.0]["id_filme"].count()
    taxa_excelencia = (filmes_bons / total_titulos * 100) if total_titulos > 0 else 0.0
    
    # Renderização dos Cartões de Métricas
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric("Amostragem", f"{total_titulos:,} Filmes")
    with kpi2:
        st.metric("Volume Total de Votos", f"{votos_totais:,}")
    with kpi3:
        st.metric("Nota Média Ponderada", f"{nota_ponderada:.2f} / 10")
    with kpi4:
        st.metric("Popularidade Média", f"{popularidade_media:.1f}")
    with kpi5:
        st.metric("Taxa de Excelência (≥7)", f"{taxa_excelencia:.1f} %")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualização de Gráficos
    g_esq, g_dir = st.columns([1.2, 1.8])
    
    with g_esq:
        st.subheader("Distribuição de Notas por Gênero")
        df_g_c = df_filme_genero[df_filme_genero["id_filme"].isin(df_f["id_filme"])].merge(df_genero, on="id_genero")
        df_g_c = df_g_c.merge(df_f, on="id_filme")
        
        if not df_g_c.empty:
            f_box = px.box(df_g_c, x="nome_genero", y="vote_average", color="nome_genero", labels={"nome_genero": "Gênero", "vote_average": "Nota"}, color_discrete_sequence=px.colors.qualitative.Safe)
            f_box.update_layout(showlegend=False, height=350, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(f_box, use_container_width=True)
        else:
            st.warning("Dados insuficientes para renderização gráfica.")
        
    with g_dir:
        st.subheader("Correlação: Volume de Votos vs Nota Média")
        if not df_f.empty:
            f_scatter = px.scatter(df_f, x="vote_count", y="vote_average", size="popularity", hover_name="title", labels={"vote_count": "Contagem de Votos", "vote_average": "Nota do Filme"}, color_discrete_sequence=["#e76f51"], opacity=0.6)
            f_scatter.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(f_scatter, use_container_width=True)
        else:
            st.warning("Dados insuficientes para renderização gráfica.")
        
    # Tabela: Resumo Geral dos Filmes Filtrados
    st.markdown("---")
    st.subheader("📋 Resumo Geral e Detalhado das Obras Selecionadas")
    
    if not df_f.empty:
        # Cruzamento estruturado para enriquecer a tabela fato com a dimensão de diretores
        df_resumo_geral = df_f[["title", "id_diretor", "ano_lanc", "vote_average", "vote_count", "popularity", "budget", "revenue"]].merge(
            df_diretor, on="id_diretor", how="left"
        ).sort_values(by="vote_average", ascending=False)
        
        # Formatação de colunas numéricas e strings antes de exibir no componente
        df_resumo_geral["budget"] = df_resumo_geral["budget"].map(lambda x: f"$ {x:,.2f}" if x > 0 else "Não Declarado")
        df_resumo_geral["revenue"] = df_resumo_geral["revenue"].map(lambda x: f"$ {x:,.2f}" if x > 0 else "Não Declarado")
        df_resumo_geral["ano_lanc"] = df_resumo_geral["ano_lanc"].fillna("N/A").astype(str).str.replace(".0", "", regex=False)
        
        st.dataframe(
            df_resumo_geral[["title", "nome_diretor", "ano_lanc", "vote_average", "vote_count", "popularity", "budget", "revenue"]].rename(
                columns={
                    "title": "Título do Filme",
                    "nome_diretor": "Diretor Principal",
                    "ano_lanc": "Ano Lançamento",
                    "vote_average": "Nota Média",
                    "vote_count": "Total de Votos",
                    "popularity": "Índice Popularidade",
                    "budget": "Orçamento",
                    "revenue": "Faturamento"
                }
            ),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum filme corresponde aos critérios de filtragem selecionados para exibição do resumo.")

# 5. Roteamento Nativo do Sistema de Menu Multi-Páginas
navegacao = st.navigation([
    st.Page(pagina_inicial, title="Apresentação do Projeto", icon="🏠"),
    st.Page(painel_analitico, title="Painel Analítico Interativo", icon="📊")
])
navegacao.run()