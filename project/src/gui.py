import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from parser import parse_input
from solvers import solve_with_algorithm
from matplotlib.lines import Line2D

def draw_map(problem, solution):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.set_xticks(range(problem.grid_columns))
    ax.set_yticks(range(problem.grid_rows))
    ax.grid(color='lightgrey', linestyle='--', linewidth=1, alpha=0.5)
    
    cmap = plt.get_cmap('tab10')
    
    for vehicle_id, rides in enumerate(solution):
        color = cmap(vehicle_id % 10)
        
        for ride in rides:
            start_x, start_y = ride.start_column, ride.start_row
            end_x, end_y = ride.end_column, ride.end_row
            
            ax.plot([start_x, end_x, end_x], [start_y, start_y, end_y], color=color, linewidth=2.5, alpha=0.7, label=f"V{vehicle_id}" if ride == rides[0] else "")
            
            ax.scatter(start_x, start_y, color=color, marker='o', s=60, zorder=5)
            ax.scatter(end_x, end_y, color=color, marker='x', s=60, zorder=5)
            
            ax.text(end_x, start_y, f"R{ride.id}", color=color, fontsize=9, fontweight='bold', ha='center', va='center')

    ax.set_title("Routing Simulation Map")
    ax.set_xlabel("X Coordinates")
    ax.set_ylabel("Y Coordinates")
    
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', markersize=8, label='Departure'),
        Line2D([0], [0], marker='x', color='w', markeredgecolor='grey', markersize=8, label='Destination')
    ]
    
    if problem.vehicles <= 10:
        handles, labels = ax.get_legend_handles_labels()
        handles.extend(legend_elements)
        ax.legend(handles=handles, title="Vehicles", bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        ax.legend(handles=legend_elements, title="Nodes", bbox_to_anchor=(1.05, 1), loc='upper left')
        
    return fig

# --- 1. Page Config ---
st.set_page_config(page_title="Routing Optimizer", layout="wide")

# --- 3. Header Customizado ---
st.title("Autonomous Vehicle Routing Optimizer")
st.markdown("Optimization Dashboard | Hash Code Simulation")
st.divider()

# --- 4. Sidebar ---
with st.sidebar:
    st.header("Experiment Setup")
    
    selected_instance = st.selectbox("Dataset Instance:", ["1", "2", "3", "4", "5", "6", "7"])
    selected_algorithm = st.selectbox("Search Algorithm:", ["greedy", "hill_climbing", "simulated_annealing", "genetic_algorithm"])

    algorithm_params = {}
    if selected_algorithm == "simulated_annealing":
        st.subheader("Hyperparameters (SA)")
        algorithm_params['T0'] = st.slider("Initial Temperature", min_value=100, max_value=5000, value=1000, step=100)
        algorithm_params['alpha'] = st.slider("Cooling Rate", min_value=0.80, max_value=0.99, value=0.95, step=0.01)
        algorithm_params['max_iterations'] = st.number_input("Max Iterations", min_value=100, max_value=5000, value=1000, step=100)
        algorithm_params['max_no_improvement'] = st.number_input("Patience (Iter. w/o improvement)", min_value=10, max_value=500, value=100, step=10)
        
    elif selected_algorithm == "genetic_algorithm":
        st.subheader("Hyperparameters (GA)")
        is_large_instance = selected_instance in ("5", "6", "7")
        default_population = 12 if is_large_instance else 30
        default_generations = 20 if is_large_instance else 80

        algorithm_params['population_size'] = st.number_input("Population Size", min_value=5, max_value=200, value=default_population, step=5)
        algorithm_params['generations'] = st.number_input("Generations", min_value=5, max_value=1000, value=default_generations, step=5)
        algorithm_params['tournament_size'] = st.number_input("Tournament Size", min_value=2, max_value=20, value=3, step=1)
        algorithm_params['elite_count'] = st.number_input("Elitism Count", min_value=0, max_value=50, value=4, step=1)
        algorithm_params['mutation_rate'] = st.slider("Mutation Rate", min_value=0.00, max_value=1.00, value=0.35, step=0.01)
        algorithm_params['order_crossover_prob'] = st.slider("Crossover Probability", min_value=0.00, max_value=1.00, value=0.50, step=0.01)
        algorithm_params['max_no_improvement_generations'] = st.number_input("Patience (Gen. w/o improvement)", min_value=1, max_value=200, value=8 if is_large_instance else 20, step=1)
        algorithm_params['max_seconds'] = st.number_input("Time Limit (s)", min_value=5, max_value=1800, value=60 if is_large_instance else 180, step=5)
    
    st.markdown("<br>", unsafe_allow_html=True)
    run_button = st.button("Execute Optimizer", type="primary", use_container_width=True)

# --- 5. Main Execution ---
if run_button:
    with st.spinner('Computing optimal routes...'):
        try:
            input_path = f"../data/input_{selected_instance}.txt"
            problem = parse_input(input_path)
            
            st.success(f"Instance loaded successfully. Grid Dimensions: {problem.grid_rows}x{problem.grid_columns} | Fleet Size: {problem.vehicles} | Total Requests: {len(problem.rides)}")

            if selected_algorithm == "genetic_algorithm" and algorithm_params.get('elite_count', 0) > algorithm_params.get('population_size', 1):
                st.error("Constraint Violation: Elite count cannot exceed population size.")
                st.stop()
            
            start_time = time.perf_counter()
            solution, score, history = solve_with_algorithm(problem, selected_algorithm, params=algorithm_params)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            
            st.markdown("### Performance Metrics")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Objective Score", f"{score:,}")
            col2.metric("Total Iterations", len(history))
            col3.metric("Computation Time", f"{execution_time:.3f} s")
            
            st.divider()
            
            map_col, chart_col = st.columns(2)
            
            with map_col:
                st.markdown("#### Spatial Distribution")
                if problem.grid_rows <= 100:
                    map_figure = draw_map(problem, solution)
                    st.pyplot(map_figure)
                else:
                    st.info("Map visualization disabled for instances exceeding 100 grid rows to prevent memory overflow.")
            
            with chart_col:
                st.markdown("#### Convergence Plot")
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
                    st.info(f"Convergence plot unavailable. The {selected_algorithm} algorithm did not perform iterative improvements beyond the initial state.")
                
            st.divider()
            st.markdown("#### Schedule Output")
            with st.expander("View raw assignments per vehicle"):
                for vehicle_id, rides in enumerate(solution):
                    ride_ids = [ride.id for ride in rides]
                    st.write(f"**Vehicle {vehicle_id}:** {ride_ids if ride_ids else 'Idle'}")
                        
        except Exception as e:
            st.error(f"Runtime Exception: {e}")