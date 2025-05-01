import random
import json
import os
import time
import matplotlib.pyplot as plt
from collections import deque, defaultdict

# Папка для графов
DATA_DIR = "levit_graphs"

# Генерация случайных графов
def generate_sparse_graph(n):
    edges = set()
    for _ in range(n * 2):  # разреженный граф
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            edges.add((u, v, random.randint(1, 100)))
    return list(edges)

def generate_graphs():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for i in range(50):
        n = random.randint(100, 10000)
        graph = {
            "nodes": n,
            "edges": generate_sparse_graph(n)
        }
        with open(os.path.join(DATA_DIR, f"graph_{i}.json"), "w") as f:
            json.dump(graph, f)

# Алгоритм Левита
def levit(graph, start):
    n = graph["nodes"]
    edges = defaultdict(list)
    for u, v, w in graph["edges"]:
        edges[u].append((v, w))
        edges[v].append((u, w))  # неориентированный граф

    INF = float('inf')
    dist = [INF] * n
    dist[start] = 0

    m0, m1, m2 = set(range(n)), deque(), set()
    m0.remove(start)
    m1.append(start)

    iterations = 0

    while m1:
        u = m1.popleft()
        for v, weight in edges[u]:
            iterations += 1
            if v in m0:
                dist[v] = dist[u] + weight
                m1.append(v)
                m0.remove(v)
            elif v in m1 and dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
            elif v in m2 and dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
                m1.append(v)
                m2.remove(v)
        m2.add(u)
    return dist, iterations

# Проведение экспериментов
def run_experiments():
    results = []
    for filename in sorted(os.listdir(DATA_DIR)):
        with open(os.path.join(DATA_DIR, filename)) as f:
            graph = json.load(f)

        start_time = time.perf_counter()
        _, iterations = levit(graph, 0)
        elapsed_time = time.perf_counter() - start_time

        print(f"{filename}: {graph['nodes']} узлов, {len(graph['edges'])} рёбер, "
              f"{iterations} итераций, {elapsed_time:.6f} сек.")

        results.append({
            "nodes": graph["nodes"],
            "edges": len(graph["edges"]),
            "iterations": iterations,
            "time": elapsed_time
        })
    return results

# Построение графиков
def plot_results(results):
    nodes = [r["nodes"] for r in results]
    times = [r["time"] for r in results]
    iters = [r["iterations"] for r in results]

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(nodes, times, marker='o')
    plt.title("Время выполнения алгоритма Левита")
    plt.xlabel("Количество вершин")
    plt.ylabel("Время (сек)")

    plt.subplot(1, 2, 2)
    plt.plot(nodes, iters, marker='x', color='orange')
    plt.title("Количество итераций алгоритма Левита")
    plt.xlabel("Количество вершин")
    plt.ylabel("Итерации")

    plt.tight_layout()
    plt.savefig("levit_analysis_results.png")
    plt.show()

if __name__ == "__main__":
    generate_graphs()
    results = run_experiments()
    plot_results(results)
