import sys
import random
import math
import time
import argparse
from collections import deque

def parse_instancia():
    linhas = sys.stdin.readlines()
    _, delta, T_max = map(int, linhas[0].split())
    m = int(linhas[1])
    
    recursos = []
    for i in range(2, 2 + m):
        t, k = map(int, linhas[i].split())
        recursos.extend([t] * k)
    
    grafo = {}
    for linha in linhas[2 + m:]:
        if linha.strip():
            x1_y1, x2_y2, t = linha.strip().split()
            x1, y1 = map(int, x1_y1.split('-'))
            x2, y2 = map(int, x2_y2.split('-'))
            t = int(t)
            u = (x1, y1)
            v = (x2, y2)
            if u not in grafo:
                grafo[u] = []
            if v not in grafo:
                grafo[v] = []
            grafo[u].append((v, t))
    
    return delta, T_max, recursos, grafo

def calcular_custo(grafo, alocacao_recursos, T, delta):
    pior_caso = 0
    
    for s in grafo:
        fila = deque([(s, 0)])
        visitados = set()
        temp_infectados = set()
        
        while fila:
            v, tempo = fila.popleft()
            if v in visitados or tempo > T:
                continue
            visitados.add(v)
            temp_infectados.add(v)
            
            for vizinho, t in grafo[v]:
                atraso = delta if v in alocacao_recursos else 0
                if tempo + t + atraso <= T:
                    fila.append((vizinho, tempo + t + atraso))
        
        pior_caso = max(pior_caso, len(temp_infectados))
    
    return pior_caso

def gerar_vizinhos(alocacao_recursos, servidores):
    novo_estado = alocacao_recursos[:]
    if novo_estado:
        idx = random.randint(0, len(novo_estado) - 1)
        novo_servidor = random.choice(servidores)
        novo_estado[idx] = novo_servidor
    return novo_estado

def inicializar_alocacao(servidores, recursos, grafo):
    servidores_ordenados = sorted(servidores, key=lambda v: -len(grafo.get(v, [])))
    return servidores_ordenados[:min(len(servidores), len(recursos))]

def simulated_annealing(grafo, servidores, T_max, delta, recursos, iteracoes, T_ini, T_min, alpha):
    alocacao_recursos = inicializar_alocacao(servidores, recursos, grafo)
    custo_inicial = calcular_custo(grafo, alocacao_recursos, T_max, delta)
    melhor_alocacao = alocacao_recursos[:]
    melhor_custo = custo_inicial
    
    T = T_ini
    for _ in range(iteracoes):
        novo_estado = gerar_vizinhos(alocacao_recursos, servidores)
        custo_novo = calcular_custo(grafo, novo_estado, T_max, delta)
        
        if custo_novo < melhor_custo or random.random() < math.exp((melhor_custo - custo_novo) / T):
            alocacao_recursos = novo_estado
            melhor_custo = custo_novo
            melhor_alocacao = novo_estado[:]
        
        T = max(T_min, T * alpha)
    
    return melhor_alocacao, custo_inicial, melhor_custo

def main():
    parser = argparse.ArgumentParser(description="Simulated Annealing para o Problema de Alocação de Recursos.")
    parser.add_argument("output_file", type=str, help="Arquivo para salvar a melhor solução encontrada.")
    parser.add_argument("--iteracoes", type=int, default=10, help="Número de iterações do algoritmo.")
    parser.add_argument("--T_ini", type=float, default=2000, help="Temperatura inicial do Simulated Annealing.")
    parser.add_argument("--T_min", type=float, default=0.1, help="Temperatura mínima do Simulated Annealing.")
    parser.add_argument("--alpha", type=float, default=0.98, help="Taxa de resfriamento da temperatura.")
    args = parser.parse_args()
    
    delta, T_max, recursos, grafo = parse_instancia()
    servidores = list(grafo.keys())
    
    inicio_tempo = time.time()
    melhor_alocacao, custo_inicial, melhor_custo = simulated_annealing(
        grafo, servidores, T_max, delta, recursos, args.iteracoes, args.T_ini, args.T_min, args.alpha
    )
    tempo_execucao = time.time() - inicio_tempo
    
    with open(args.output_file, "w") as f:
        f.write(f"Valor da solucao inicial (SI): {custo_inicial}\n")
        f.write(f"Valor da melhor solução final (SF): {melhor_custo}\n")
        f.write(f"Tempo computacional: {tempo_execucao:.4f} segundos\n")
        f.write(f"Melhor solucao encontrada: {melhor_alocacao}\n")

if __name__ == "__main__":
    main()
