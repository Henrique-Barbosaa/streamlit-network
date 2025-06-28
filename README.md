# 📊 Visualizador de Redes Complexas com Streamlit + Pyvis

Esta é uma aplicação interativa desenvolvida em **Python com Streamlit** para **visualização e análise de redes complexas**, utilizando um grafo a partir da Wikipedia com a seed "Eulerian path". A visualização interativa é feita com a biblioteca **Pyvis**, e diversas métricas estruturais são exibidas para auxiliar na análise do grafo.

## 🚀 Funcionalidades

- Carregamento de grafos a partir de arquivos `.graphml`
- Visualização interativa com Pyvis (suporte a destaque por comunidades)
- Filtros para visualizar subconjuntos do grafo:
  - Maior componente conectado
  - Cluster mais denso (modularidade)
  - Nós com grau acima da média
- Cálculo de métricas estruturais:
  - Densidade
  - Assortatividade
  - Clustering global
  - Componentes fortemente e fracamente conectados
- Visualização da distribuição de grau
- Destaque dos top-k nós por centralidade

---

## 🧰 Requisitos

Antes de rodar a aplicação, certifique-se de ter os pacotes abaixo instalados:

```bash
pip install streamlit networkx pyvis matplotlib wikipedia