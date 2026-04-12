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
    
    instancia_escolhida = st.selectbox("Escolhe a instância:", ["1", "2", "3", "4", "5", "6", "7"])
    algoritmo_escolhido = st.selectbox("Escolhe o algoritmo:", ["greedy", "hill_climbing", "simulated_annealing", "genetic_algorithm"])

    algorithm_params = {} # Dicionário para guardar os parâmetros
    if algoritmo_escolhido == "simulated_annealing":
        st.subheader("⚙️ Parâmetros do SA")
        algorithm_params['T0'] = st.slider("Temperatura Inicial (T0)", min_value=100, max_value=5000, value=1000, step=100)
        algorithm_params['alpha'] = st.slider("Taxa de Arrefecimento (alpha)", min_value=0.80, max_value=0.99, value=0.95, step=0.01)
        algorithm_params['max_iterations'] = st.number_input("Máximo de Iterações", min_value=100, max_value=5000, value=1000, step=100)
        algorithm_params['max_no_improvement'] = st.number_input("Parar após X iterações sem melhoria", min_value=10, max_value=500, value=100, step=10)
    elif algoritmo_escolhido == "genetic_algorithm":
        st.subheader("⚙️ Parâmetros do GA")
        is_large_instance = instancia_escolhida in ("5", "6", "7")
        default_population = 12 if is_large_instance else 30
        default_generations = 20 if is_large_instance else 80

        algorithm_params['population_size'] = st.number_input("Tamanho da População", min_value=5, max_value=200, value=default_population, step=5)
        algorithm_params['generations'] = st.number_input("Número de Gerações", min_value=5, max_value=1000, value=default_generations, step=5)
        algorithm_params['tournament_size'] = st.number_input("Tamanho do Torneio", min_value=2, max_value=20, value=3, step=1)
        algorithm_params['elite_count'] = st.number_input("Número de Elites", min_value=0, max_value=50, value=4, step=1)
        algorithm_params['mutation_rate'] = st.slider("Taxa de Mutação", min_value=0.00, max_value=1.00, value=0.35, step=0.01)
        algorithm_params['order_crossover_prob'] = st.slider("Probabilidade de Ordered Crossover", min_value=0.00, max_value=1.00, value=0.50, step=0.01)
        algorithm_params['max_no_improvement_generations'] = st.number_input("Parar após X gerações sem melhoria", min_value=1, max_value=200, value=8 if is_large_instance else 20, step=1)
        algorithm_params['max_seconds'] = st.number_input("Limite de Tempo (segundos)", min_value=5, max_value=1800, value=60 if is_large_instance else 180, step=5)
    
    st.divider()
    run_button = st.button("Correr Algoritmo", type="primary", use_container_width=True)

# --- 3. Execução Principal ---
if run_button:
    with st.spinner('A processar o algoritmo...'):
        try:
            input_path = f"../data/input_{instancia_escolhida}.txt"
            problem = parse_input(input_path)
            
            st.success(f"Ficheiro carregado! Grelha: {problem.grid_rows}x{problem.grid_columns} | Veículos: {problem.vehicles} | Viagens: {len(problem.rides)}")

            if algoritmo_escolhido == "genetic_algorithm" and algorithm_params['elite_count'] > algorithm_params['population_size']:
                st.error("Parâmetros inválidos: o número de elites não pode ser maior que o tamanho da população.")
                st.stop()
            
            solution, score, history = solve_with_algorithm(problem, algoritmo_escolhido, **algorithm_params)
            
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
                    if isinstance(history[0], dict):
                        chart_data = pd.DataFrame(history)
                        if 'best_score' in chart_data.columns:
                            chart_data = chart_data.set_index('generation')[['best_score']].rename(columns={'best_score': 'Score'})
                        else:
                            chart_data = pd.DataFrame({'Score': []})
                    else:
                        chart_data = pd.DataFrame({'Score': history})
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