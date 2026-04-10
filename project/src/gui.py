import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from parser import parse_input
from solvers import solve_with_algorithm
from matplotlib.lines import Line2D

# --- FUNÇÃO PARA DESENHAR O MAPA ---
def desenhar_mapa(problem, solution):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Desenhar a grelha da cidade
    ax.set_xticks(range(problem.grid_columns))
    ax.set_yticks(range(problem.grid_rows))
    ax.grid(color='lightgrey', linestyle='--', linewidth=1)
    
    cmap = plt.get_cmap('tab10')
    
    for vehicle_id, rides in enumerate(solution):
        cor = cmap(vehicle_id % 10)
        
        for ride in rides:
            start_x, start_y = ride.start_column, ride.start_row
            end_x, end_y = ride.end_column, ride.end_row
            
            # --- CORREÇÃO DA DIAGONAL (Caminho em "L" / Distância de Manhattan) ---
            # O carro viaja primeiro na horizontal (X) e depois na vertical (Y)
            ax.plot([start_x, end_x, end_x], [start_y, start_y, end_y], color=cor, linewidth=3, alpha=0.6, label=f"V{vehicle_id}" if ride == rides[0] else "")
            
            # Ponto de partida (bola) e chegada (X)
            ax.scatter(start_x, start_y, color=cor, marker='o', s=80, zorder=5)
            ax.scatter(end_x, end_y, color=cor, marker='x', s=80, zorder=5)
            
            # Etiqueta com o ID da viagem colocada na "esquina" do percurso
            ax.text(end_x, start_y, f"R{ride.id}", color=cor, fontsize=10, fontweight='bold', ha='center', va='center')

    ax.set_title("Rotas Atribuídas na Cidade (Grelha)")
    ax.set_xlabel("Colunas (x)")
    ax.set_ylabel("Linhas (y)")
    
    # --- NOVA LEGENDA PERSONALIZADA ---
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', markersize=10, label='Início da Viagem'),
        Line2D([0], [0], marker='x', color='w', markeredgecolor='grey', markersize=10, label='Fim da Viagem')
    ]
    
    if problem.vehicles <= 10:
        # Junta a legenda dos veículos com a legenda dos símbolos
        handles, labels = ax.get_legend_handles_labels()
        handles.extend(legend_elements)
        ax.legend(handles=handles, title="Legenda", bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        # Mostra apenas a legenda dos símbolos para não poluir o ecrã
        ax.legend(handles=legend_elements, title="Símbolos", bbox_to_anchor=(1.05, 1), loc='upper left')
        
    return fig

# --- 1. Configuração base da página ---
st.set_page_config(page_title="Self-Driving Rides - IA", layout="wide")

st.title("🚗 Self-Driving Rides - Otimizador")
st.markdown("Interface Gráfica para o Projeto de Inteligência Artificial")

# --- 2. Barra Lateral ---
with st.sidebar:
    st.header("Configurações do Problema")
    
    instancia_escolhida = st.selectbox("Escolhe a instância:", ["1", "2", "3"])
    algoritmo_escolhido = st.selectbox("Escolhe o algoritmo:", ["greedy", "hill_climbing", "simulated_annealing"])

    params_sa = {} # Dicionário para guardar os parâmetros
    if algoritmo_escolhido == "simulated_annealing":
        st.subheader("⚙️ Parâmetros do SA")
        params_sa['T0'] = st.slider("Temperatura Inicial (T0)", min_value=100, max_value=5000, value=1000, step=100)
        params_sa['alpha'] = st.slider("Taxa de Arrefecimento (alpha)", min_value=0.80, max_value=0.99, value=0.95, step=0.01)
        params_sa['max_iterations'] = st.number_input("Máximo de Iterações", min_value=100, max_value=5000, value=1000, step=100)
        params_sa['max_no_improvement'] = st.number_input("Parar após X iterações sem melhoria", min_value=10, max_value=500, value=100, step=10)
    
    st.divider()
    run_button = st.button("Correr Algoritmo", type="primary", use_container_width=True)

# --- 3. Execução Principal ---
if run_button:
    with st.spinner('A processar o algoritmo...'):
        try:
            input_path = f"../data/input_{instancia_escolhida}.txt"
            problem = parse_input(input_path)
            
            st.success(f"Ficheiro carregado! Grelha: {problem.grid_rows}x{problem.grid_columns} | Veículos: {problem.vehicles} | Viagens: {problem.rides}")
            
            solution, score, history = solve_with_algorithm(problem, algoritmo_escolhido, **params_sa)
            
            st.divider()
            st.header("Resultados")
            
            col1, col2 = st.columns(2)
            col1.metric("Pontuação Final", score)
            col2.metric("Iterações Efetuadas", len(history))
            
            # Dividir o ecrã em duas colunas para o Mapa e para o Gráfico de Evolução
            col_mapa, col_grafico = st.columns(2)
            
            with col_mapa:
                st.subheader("🗺️ Mapa de Viagens")
                if problem.grid_rows <= 100: # Proteção para não "rebentar" com mapas gigantes
                    figura_mapa = desenhar_mapa(problem, solution)
                    st.pyplot(figura_mapa)
                else:
                    st.warning("O mapa é demasiado grande para ser visualizado (>100 linhas).")
            
            with col_grafico:
                st.subheader("📈 Evolução da Solução")
                if len(history) > 1:
                    chart_data = pd.DataFrame(history, columns=['Score'])
                    st.line_chart(chart_data)
                else:
                    if algoritmo_escolhido == "greedy":
                        st.info("O algoritmo Greedy é construtivo, logo não há evolução iterativa para desenhar.")
                    else:
                        st.warning(f"⚠️ O {algoritmo_escolhido} parou logo na 1ª iteração!")
                
            st.subheader("📋 Viagens Atribuídas")
            with st.expander("Ver lista detalhada de viagens por veículo"):
                for vehicle_id, rides in enumerate(solution):
                    ride_ids = [ride.id for ride in rides]
                    st.write(f"**Veículo {vehicle_id}:** {ride_ids if ride_ids else 'Nenhuma viagem'}")
                        
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")