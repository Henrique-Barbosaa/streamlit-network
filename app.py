import streamlit as st
import networkx as nx
from pyvis.network import Network
import os
from IPython.display import IFrame
from networkx.algorithms.community import greedy_modularity_communities
from utils import (
    calcular_metricas,
    exibir_metricas,
    mostrar_distribuicao_grau,
    mostrar_centralidades,
    desenhar_grafo_colorido
)

st.title("🔍 Análise e Visualização de Redes Complexas")
graph_path = os.path.join("dataset", "network_analysis.graphml")
st.subheader("Grafo extraído da Wikipédia com a seed Eulerian path")

try:
    G = nx.read_graphml(graph_path)
    st.success(f"Grafo carregado com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas.")
except Exception as e:
    st.error(f"Erro ao carregar o grafo: {e}")
    st.stop()

filtro = st.selectbox("Selecionar subconjunto:", [
    "Grafo completo",
    "Cluster mais denso (modularidade)",
    "Nós com grau maior que a média"
])
st.write("No grafo completo, os nós estão sendo coloridos baseado nos seus clusters. Cada cluster tem uma cor.")

G_original = G.copy()

if filtro == "Cluster mais denso (modularidade)":
    comunidades = list(greedy_modularity_communities(G))
    cluster = comunidades[0]
    G = G_original.subgraph(cluster).copy()
elif filtro == "Nós com grau maior que a média":
    grau_medio = sum(dict(G.degree()).values()) / G.number_of_nodes()
    nos_filtrados = [n for n, d in G.degree() if d > grau_medio]
    G = G_original.subgraph(nos_filtrados).copy()
elif filtro == "Grafo completo":
    G = G_original.copy()

if filtro == "Grafo completo":
    net = desenhar_grafo_colorido(G)
else:
    net = Network(height='600px', width='100%', notebook=False, cdn_resources='in_line')
    net.from_nx(G)

net.show_buttons(filter_=['physics'])

html_str = net.generate_html()
with open("grafo.html", "w", encoding="utf-8") as f:
    f.write(html_str)

with open("grafo.html", "r", encoding="utf-8") as f:
    html_content = f.read()
st.components.v1.html(html_content, height=600, scrolling=True)

st.subheader("📈 Métricas Estruturais")
metricas = calcular_metricas(G)
exibir_metricas(metricas)

st.subheader("📊 Distribuição de Grau")
mostrar_distribuicao_grau(G)

st.subheader("🏅 Centralidades")
mostrar_centralidades(G)