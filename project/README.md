# Ride-Sharing Optimization Problem

Solver para o problema de otimização de deslocações com múltiplos veículos, baseado no desafio Google Hash Code.

## Estrutura do Projeto

```
project/
├── data/                 # Ficheiros de input (instâncias do problema)
│   ├── input_1.txt      # Instância pequena (3x4 grid, 2 veículos, 3 rides)
│   ├── input_2.txt      # Instância média (6x6 grid, 3 veículos, 8 rides)
│   └── input_3.txt      # Instância grande (10x10 grid, 4 veículos, 14 rides)
├── results/             # Outputs (ficheiros de solução)
├── src/
│   ├── main.py          # Entrypoint - executa algoritmo selecionado
│   ├── models.py        # Classes: Ride, Problem, Vehicle
│   ├── parser.py        # Parse de ficheiros input
│   ├── greedy.py        # Algoritmo greedy (implementado)
│   ├── hill_climbing.py # Algoritmo hill climbing (TODO)
│   ├── simulation.py    # Simulação de tempo e pontuação
│   ├── output.py        # Escrita de ficheiros output
│   └── evaluator.py     # Avaliação de soluções (TODO)
└── README.md            # Este ficheiro
```

## Como Executar

```bash
cd project
python src/main.py
```

### Benchmark e Comparação de Algoritmos

Para comparar algoritmos e parameterizações (com médias de score e tempo):

```bash
cd project
python src/benchmark.py --runs 10 --seed 42
```

Resultados gerados:
- `results/benchmark_detailed.csv` (resultados por execução)
- `results/benchmark_summary.csv` (médias/desvios por configuração)
- `results/benchmark_summary.txt` (resumo legível em texto)

O programa vai pedir para escolher uma instância (1, 2 ou 3) e executar o greedy solver.

### Exemplo

```
Escolhe o numero da instancia (1-3): 1
Input: data/input_1.txt
Score: 10
Output: results/greedy_output_1.txt
Greedy solution (ride ids per vehicle):
Vehicle 0: [0, 1]
Vehicle 1: [2]
```

## Formato do Input

Cada ficheiro `input_N.txt` contém:
- **Linha 1**: `R C F N B T` onde:
  - `R` = linhas da grelha
  - `C` = colunas da grelha
  - `F` = nº de veículos
  - `N` = nº de rides
  - `B` = bonus por ride (se apanhada no tempo certo)
  - `T` = passos totais da simulação
- **Linhas 2 a N+1**: `a b x y s f` onde:
  - `(a, b)` = posição inicial da ride
  - `(x, y)` = posição final da ride
  - `s` = earliest_start (tempo mínimo para começar)
  - `f` = latest_finish (tempo máximo para terminar)

### Exemplo (input_1.txt)
```
3 4 2 3 2 10
0 0 1 3 2 9    # Ride 0: (0,0) -> (1,3), começa em t=2, termina em t=9
1 2 1 0 0 9    # Ride 1: (1,2) -> (1,0), começa em t=0, termina em t=9
2 0 2 2 0 9    # Ride 2: (2,0) -> (2,2), começa em t=0, termina em t=9
```

## Formato do Output

Cada ficheiro `greedy_output_N.txt`:
- Uma linha por veículo
- Formato: `k id1 id2 ... idk` onde:
  - `k` = número de rides atribuídas
  - `id1, id2, ...` = IDs das rides (em ordem)

### Exemplo (output_1.txt)
```
2 0 1    # Vehicle 0 faz rides 0, 1
1 2      # Vehicle 1 faz ride 2
```

## Algoritmos

### Greedy (Implementado ✅)
- Seleciona iterativamente o melhor par (vehicle, ride)
- Critério: `ratio = pontos / custo`
- Pára quando não há mais rides rentáveis

**Scores nas instâncias:**
- input_1: 10
- input_2: 37
- input_3: 58

### Hill Climbing (Próximo)
- Começa com uma solução inicial (ex: greedy)
- Aplica pequenas mudanças (swaps, relocations)
- Aceita se melhora o score
- Pára quando fica estável

## Ferramentas Úteis

### Avaliador
```python
from evaluator import evaluate_solution

problem = parse_input('data/input_1.txt')
solution = greedy_solution(problem)
score = evaluate_solution(problem, solution)
print(f"Score: {score}")
```

## Notas

- Distância = Manhattan distance (`|x1-x2| + |y1-y2|`)
- Todas as coordenadas começam de (0, 0)
- Custo = tempo total consumido pela ride (pickup + distância)
- Bonus só é contado se a ride começar exatamente no `earliest_start`
