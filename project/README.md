# Ride-Sharing Optimization Problem

Solver para o problema de otimização de deslocações com múltiplos veículos (estilo Google Hash Code).

## Estado Atual

O projeto implementa:
- Greedy
- Hill Climbing
- Simulated Annealing
- Genetic Algorithm

Inclui ainda:
- execução individual (CLI e GUI)
- comparação de algoritmos na GUI
- warm start / cold start para HC e SA

## Estrutura do Projeto

```
project/
├── data/                     # Instâncias input_1.txt ... input_7.txt
├── results/                  # Outputs gerados
├── src/
│   ├── main.py               # Execução em terminal
│   ├── gui.py                # Interface Streamlit
│   ├── solvers.py            # Dispatcher de algoritmos
│   ├── greedy.py
│   ├── hill_climbing.py
│   ├── simulated_annealing.py
│   ├── genetic_algorithm.py
│   ├── neighborhood.py
│   ├── benchmark.py          # Benchmark por script (opcional)
│   ├── evaluator.py
│   ├── simulation.py
│   ├── parser.py
│   ├── output.py
│   └── models.py
└── README.md
```

## Como Executar

### 1) Terminal (execução simples)

```bash
cd project
python src/main.py
```

### 2) GUI (recomendado)

```bash
cd project/src
python -m streamlit run gui.py
```

Na GUI tens dois modos:
- **Single Execution**: corre 1 algoritmo numa instância
- **Algorithms Comparison**: compara vários algoritmos com médias de score/tempo

### 3) Benchmark por script (opcional)

O fluxo principal de comparação é a GUI. O `benchmark.py` pode ser usado para corridas batch via terminal.

```bash
cd project
python src/benchmark.py --runs 10 --seed 42
```

## Warm Start / Cold Start

Para Hill Climbing e Simulated Annealing existe `start_strategy`:
- `warm_start`: começa da solução greedy
- `cold_start`: começa de solução aleatória

Na GUI isto aparece como:
- **Warm Start**
- **Cold Start**

## Formato do Input

Cada `input_N.txt`:
- Linha 1: `R C F N B T`
- Linhas seguintes: `a b x y s f`

Onde:
- `R, C`: dimensões da grelha
- `F`: número de veículos
- `N`: número de rides
- `B`: bónus por começar exatamente no `earliest_start`
- `T`: total de passos

Para cada ride:
- `(a, b)` origem
- `(x, y)` destino
- `s` earliest_start
- `f` latest_finish

## Formato do Output

Uma linha por veículo:
- `k id1 id2 ... idk`

Onde:
- `k` = nº de rides atribuídas ao veículo
- `id1..idk` = IDs das rides na ordem de execução

## Notas

- Distância usada: Manhattan (`|x1-x2| + |y1-y2|`)
- Coordenadas começam em `(0,0)`
- O bónus só conta se a ride começar exatamente em `earliest_start`
