import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from parser import parse_input
from solvers import solve_with_algorithm
from matplotlib.lines import Line2D

def draw_map(problem, solution):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Define os limites do mapa com base no tamanho da cidade
    ax.set_xlim(-1, problem.grid_columns)
    ax.set_ylim(-1, problem.grid_rows)
    
    # Escalonamento Dinâmico: Só desenha todas as grelhas se a cidade for pequena
    if problem.grid_columns <= 100 and problem.grid_rows <= 100:
        ax.set_xticks(range(problem.grid_columns))
        ax.set_yticks(range(problem.grid_rows))
        ax.grid(color='lightgrey', linestyle='--', linewidth=1, alpha=0.5)
    else:
        # Para cidades gigantes, deixa o Matplotlib decidir o espaçamento da grelha sozinho
        ax.grid(color='lightgrey', linestyle='--', linewidth=0.5, alpha=0.5)
    
    cmap = plt.get_cmap('tab10')
    
    # Contar quantas viagens existem no total para decidir o nível de detalhe
    total_rides = sum(len(rides) for rides in solution)
    is_small_input = total_rides <= 200
    
    # Ajustar tamanho das linhas e pontos dependendo do tamanho do problema
    marker_size = 60 if is_small_input else 15
    line_width = 2.5 if is_small_input else 1.0
    
    for vehicle_id, rides in enumerate(solution):
        color = cmap(vehicle_id % 10)
        
        for ride in rides:
            start_x, start_y = ride.start_column, ride.start_row
            end_x, end_y = ride.end_column, ride.end_row
            
            # Desenha o caminho em "L"
            ax.plot([start_x, end_x, end_x], [start_y, start_y, end_y], color=color, linewidth=line_width, alpha=0.7)
            
            # Desenha Início e Fim
            ax.scatter(start_x, start_y, color=color, marker='o', s=marker_size, zorder=5)
            ax.scatter(end_x, end_y, color=color, marker='x', s=marker_size, zorder=5)
            
            # Só desenha os nomes das viagens ("R1", "R2") se houver poucas, para não poluir
            if is_small_input:
                ax.text(end_x, start_y, f"R{ride.id}", color=color, fontsize=9, fontweight='bold', ha='center', va='center')

    ax.set_title("Routing Simulation Map")
    ax.set_xlabel("Columns (X)")
    ax.set_ylabel("Rows (Y)")
    
    # Legenda Base
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', markersize=8, label='Departure'),
        Line2D([0], [0], marker='x', color='w', markeredgecolor='grey', markersize=8, label='Destination')
    ]
    
    ax.legend(handles=legend_elements, title="Nodes", bbox_to_anchor=(1.05, 1), loc='upper left')
        
    return fig

# --- 1. Page Config & CSS ---
st.set_page_config(page_title="Routing Optimizer", layout="wide")

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            .block-container { padding-top: 2rem; padding-bottom: 2rem; }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Autonomous Vehicle Routing Optimizer")
st.markdown("Optimization Dashboard | Hash Code Simulation")

# --- 2. TABS ---
tab_single, tab_benchmark = st.tabs(["🚀 Single Execution", "📊 Algorithms Comparison"])

# ==========================================
# ABA 1: EXECUÇÃO ÚNICA (Agora com os menus aqui dentro!)
# ==========================================
with tab_single:
    st.subheader("⚙️ Experiment Setup")
    
    # Colocar as caixas de seleção lado a lado
    col_inst, col_algo = st.columns(2)
    with col_inst:
        selected_instance = st.selectbox("Dataset Instance:", ["1", "2", "3", "4", "5", "6", "7"], key="inst_single")
    with col_algo:
        selected_algorithm = st.selectbox("Search Algorithm:", ["greedy", "hill_climbing", "simulated_annealing", "genetic_algorithm"], key="algo_single")

    algorithm_params = {}
    
    # Colocar os sliders em 4 colunas horizontais para poupar espaço
    if selected_algorithm == "simulated_annealing":
        st.markdown("**Hyperparameters (SA)**")
        c1, c2, c3, c4 = st.columns(4)
        with c1: algorithm_params['T0'] = st.slider("Initial Temperature", 100, 5000, 1000, 100)
        with c2: algorithm_params['alpha'] = st.slider("Cooling Rate", 0.80, 0.99, 0.95, 0.01)
        with c3: algorithm_params['max_iterations'] = st.number_input("Max Iterations", 100, 5000, 1000, 100)
        with c4: algorithm_params['max_no_improvement'] = st.number_input("Patience", 10, 500, 100, 10)
        
    elif selected_algorithm == "genetic_algorithm":
        st.markdown("**Hyperparameters (GA)**")
        is_large = selected_instance in ("5", "6", "7")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            algorithm_params['population_size'] = st.number_input("Population Size", 5, 200, 12 if is_large else 30, 5)
            algorithm_params['mutation_rate'] = st.slider("Mutation Rate", 0.00, 1.00, 0.35, 0.01)
        with c2:
            algorithm_params['generations'] = st.number_input("Generations", 5, 1000, 20 if is_large else 80, 5)
            algorithm_params['order_crossover_prob'] = st.slider("Crossover Prob", 0.00, 1.00, 0.50, 0.01)
        with c3:
            algorithm_params['tournament_size'] = st.number_input("Tournament Size", 2, 20, 3, 1)
            algorithm_params['max_no_improvement_generations'] = st.number_input("Patience (Gen)", 1, 200, 8 if is_large else 20, 1)
        with c4:
            algorithm_params['elite_count'] = st.number_input("Elitism Count", 0, 50, 4, 1)
            algorithm_params['max_seconds'] = st.number_input("Time Limit (s)", 5, 1800, 60 if is_large else 180, 5)
    
    st.markdown("<br>", unsafe_allow_html=True)
    run_single = st.button("Execute Optimizer 🚀", type="primary", use_container_width=True)

    st.divider()

    # O Bloco da Execução
    if run_single:
        with st.spinner('Computing optimal routes...'):
            try:
                problem = parse_input(f"../data/input_{selected_instance}.txt")
                st.success(f"Instance loaded. Grid: {problem.grid_rows}x{problem.grid_columns} | Fleet: {problem.vehicles} | Requests: {len(problem.rides)}")
                
                if selected_algorithm == "genetic_algorithm" and algorithm_params.get('elite_count', 0) > algorithm_params.get('population_size', 1):
                    st.error("Constraint Violation: Elite count cannot exceed population size.")
                    st.stop()
                
                start_time = time.perf_counter()
                solution, score, history = solve_with_algorithm(problem, selected_algorithm, **algorithm_params)
                exec_time = time.perf_counter() - start_time
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Objective Score", f"{score:,}")
                col2.metric("Total Iterations", len(history))
                col3.metric("Computation Time", f"{exec_time:.3f} s")
                
                st.divider()
                map_col, chart_col = st.columns(2)
                
                with map_col:
                    st.markdown("#### Spatial Distribution")
                    with st.spinner("Rendering map..."):
                        map_figure = draw_map(problem, solution)
                        st.pyplot(map_figure)
                
                with chart_col:
                    st.markdown("#### Convergence Plot")
                    if len(history) > 1:
                        df_hist = pd.DataFrame(history)
                        if 'best_score' in df_hist.columns:
                            df_hist = df_hist.set_index('generation')[['best_score']].rename(columns={'best_score': 'Score'})
                        else:
                            df_hist = pd.DataFrame({'Score': history})
                        st.line_chart(df_hist)
                    else:
                        st.info("No iterative evolution to display for this algorithm.")
                        
                st.markdown("#### Schedule Output")
                with st.expander("View raw assignments per vehicle"):
                    for vehicle_id, rides in enumerate(solution):
                        ride_ids = [ride.id for ride in rides]
                        st.write(f"**Vehicle {vehicle_id}:** {ride_ids if ride_ids else 'Idle'}")
            except Exception as e:
                st.error(f"Runtime Exception: {e}")

# ==========================================
# ABA 2: COMPARAÇÃO (BENCHMARK)
# ==========================================
with tab_benchmark:
    st.header("Algorithmic Arena (Benchmark)")
    st.write("Compare the performance and speed of multiple algorithms on the same instance.")
    
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        comp_instance = st.selectbox("Select Target Instance:", ["1", "2", "3", "4", "5", "6", "7"], key="inst_bench")
    with comp_col2:
        comp_algos = st.multiselect("Select Algorithms to Compare:", 
                                    ["greedy", "hill_climbing", "simulated_annealing", "genetic_algorithm"], 
                                    default=["greedy", "simulated_annealing"])
    
    run_bench = st.button("Start Benchmark Battle ⚔️", type="primary")
    
    if run_bench:
        if not comp_algos:
            st.warning("Please select at least one algorithm.")
        else:
            problem_bench = parse_input(f"../data/input_{comp_instance}.txt")
            results = []
            
            progress_bar = st.progress(0)
            st.write("Running algorithms...")
            
            for idx, algo in enumerate(comp_algos):
                with st.spinner(f"Running {algo}..."):
                    start = time.perf_counter()
                    out = solve_with_algorithm(problem_bench, algo)
                    score_bench = out[1] if isinstance(out, tuple) else out
                    end = time.perf_counter()
                    
                    results.append({
                        "Algorithm": algo.replace("_", " ").title(),
                        "Score": score_bench,
                        "Time (s)": round(end - start, 3)
                    })
                progress_bar.progress((idx + 1) / len(comp_algos))
                
            st.success("Benchmark Complete!")
            
            # Usar a tabela sem o .style para garantir que funciona em qualquer PC sem instalar nada extra
            df_results = pd.DataFrame(results).set_index("Algorithm")
            
            st.divider()
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.markdown("#### Final Scores Comparison")
                st.bar_chart(df_results["Score"])
                
            with col_res2:
                st.markdown("#### Execution Time Comparison (Seconds)")
                st.bar_chart(df_results["Time (s)"], color="#FF4B4B")
                
            st.markdown("#### Detailed Results Table")
            st.dataframe(df_results, use_container_width=True)