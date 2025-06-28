import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import streamlit as st
import random

def calcular_metricas(G):
    densidade = nx.density(G)
    clustering = nx.average_clustering(G.to_undirected())
    assort = nx.degree_assortativity_coefficient(G)
    try:
        scc = nx.number_strongly_connected_components(G) if G.is_directed() else "N/A"
    except:
        scc = "Erro"
    try:
        wcc = nx.number_weakly_connected_components(G) if G.is_directed() else nx.number_connected_components(G)
    except:
        wcc = "Erro"

    explicacoes = {
        "Densidade": (
            densidade,
            "Indica quão conectada é a rede. Valores próximos de 1 indicam que a maioria dos nós está interligada."
        ),
        "Assortatividade": (
            assort,
            "Mede se nós com graus similares tendem a se conectar. Valores positivos indicam conexão entre nós semelhantes."
        ),
        "Clustering Global": (
            clustering,
            "Avalia a tendência da rede em formar triângulos (grupos fechados de três nós). Valores altos indicam maior agrupamento."
        ),
        "Componentes Fortemente Conectados": (
            scc,
            "Número de subgrafos onde cada nó é alcançável a partir de qualquer outro seguindo as direções (só para grafos dirigidos)."
        ),
        "Componentes Fracamente Conectados": (
            wcc,
            "Número de subgrafos que seriam conexos se ignorarmos a direção das arestas."
        ),
    }
    return explicacoes

def exibir_metricas(metricas):
    for nome, (valor, explicacao) in metricas.items():
        st.markdown(f"**{nome}:** `{valor}`  \n*{explicacao}*")
def mostrar_distribuicao_grau(G):
    graus = [d for n, d in G.degree()]
    fig, ax = plt.subplots()
    ax.hist(graus, bins=10, color='skyblue', edgecolor='black')
    ax.set_title("Distribuição de Grau dos Nós")
    ax.set_xlabel("Grau")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

def mostrar_centralidades(G):
    top_k = st.slider("Top-k nós por centralidade", min_value=3, max_value=20, value=5)

    try:
        eigen = nx.eigenvector_centrality(G, max_iter=500)
    except:
        eigen = {n: 0 for n in G.nodes()}
    
    centrais = {
        "Degree Centrality": nx.degree_centrality(G),
        "Eigenvector Centrality": eigen,
        "Closeness Centrality": nx.closeness_centrality(G),
        "Betweenness Centrality": nx.betweenness_centrality(G)
    }

    for nome, valores in centrais.items():
        st.subheader(f"**{nome}**")
        top = sorted(valores.items(), key=lambda x: -x[1])[:top_k]
        for n, score in top:
            st.write(f"Nó {n}: {score:.4f}")

def subrede_conectada_por_grau(G, max_nodes=300):
    # Ordena os nós por grau (decrescente)
    graus = sorted(G.degree(), key=lambda x: x[1], reverse=True)

    for n, _ in graus:
        # Começa do nó de maior grau e faz BFS para expandir uma subrede conectada
        nodes_subrede = list(nx.bfs_tree(G, source=n, depth_limit=2).nodes())

        if len(nodes_subrede) >= max_nodes:
            # Trunca caso passe do limite
            nodes_subrede = nodes_subrede[:max_nodes]
            break

    # Extrai subgrafo e retorna
    return G.subgraph(nodes_subrede).copy()

def desenhar_grafo_colorido(G):
    nt = Network(height='600px', width='100%', notebook=False, cdn_resources='in_line')

    # Detectar comunidades com algoritmo de modularidade
    from networkx.algorithms.community import greedy_modularity_communities
    comunidades = list(greedy_modularity_communities(G))

    # Atribuir uma cor única por comunidade
    cores = {}
    for i, comunidade in enumerate(comunidades):
        cor = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        for node in comunidade:
            cores[node] = cor

    # Adicionar nós com cor
    for node in G.nodes():
        nt.add_node(
            node,
            label=str(node),
            color=cores.get(node, "#999999"),  # fallback
            title=f"Grau: {G.degree[node]}"
        )

    # Adicionar arestas
    for source, target in G.edges():
        nt.add_edge(source, target)

    return nt
