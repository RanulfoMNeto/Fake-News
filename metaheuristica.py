import random
import math
import time
from collections import deque

def parse_instancia(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()
    
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

def simulated_annealing(grafo, servidores, T_max, delta, recursos, iteracoes=100, T_ini=2000, T_min=0.1, alpha=0.98):
    alocacao_recursos = inicializar_alocacao(servidores, recursos, grafo)
    custo_inicial = calcular_custo(grafo, alocacao_recursos, T_max, delta)
    melhor_alocacao = alocacao_recursos[:]
    melhor_custo = custo_inicial
    
    T = T_ini
    for _ in range(iteracoes):
        print(_)
        novo_estado = gerar_vizinhos(alocacao_recursos, servidores)
        custo_novo = calcular_custo(grafo, novo_estado, T_max, delta)
        
        if custo_novo < melhor_custo or random.random() < math.exp((melhor_custo - custo_novo) / T):
            alocacao_recursos = novo_estado
            melhor_custo = custo_novo
            melhor_alocacao = novo_estado[:]
        
        T = max(T_min, T * alpha)
    
    return melhor_alocacao, custo_inicial, melhor_custo

def executar_instancias(arquivos, referencia_solucoes, replicacoes=5):
    resultados = []
    with open("resultados.txt", "w") as f:
        for arquivo in arquivos:
            f.write(f"Executando {arquivo}...\n")
            delta, T_max, recursos, grafo = parse_instancia(arquivo)
            servidores = list(grafo.keys())
            
            custos_iniciais = []
            custos_finais = []
            tempos = []
            melhores_solucoes = []
            
            for _ in range(replicacoes):
                print(f"{arquivo} [{_}]")
                inicio_tempo = time.time()
                melhor_alocacao, custo_inicial, melhor_custo = simulated_annealing(grafo, servidores, T_max, delta, recursos)
                tempo_execucao = time.time() - inicio_tempo
                
                custos_iniciais.append(custo_inicial)
                custos_finais.append(melhor_custo)
                tempos.append(tempo_execucao)
                melhores_solucoes.append(melhor_alocacao)
            print()
            media_si = sum(custos_iniciais) / replicacoes
            media_sf = sum(custos_finais) / replicacoes
            media_tempo = sum(tempos) / replicacoes
            melhor_solucao = min(zip(custos_finais, melhores_solucoes))[1]
            desvio_percentual = 100 * (media_si - media_sf) / media_si
            referencia = referencia_solucoes.get(arquivo, None)
            desvio_sf_otima = 100 * (media_sf - referencia) / referencia if referencia else "N/A"
            
            f.write(f"Instância: {arquivo}\n")
            f.write(f"Valor da solucao inicial (SI): {media_si:.2f}\n")
            f.write(f"Valor da melhor solução final (SF): {media_sf:.2f}\n")
            f.write(f"Desvio percentual entre SI e SF: {desvio_percentual:.2f}%\n")
            f.write(f"Desvio percentual da SF em relacao a solucao otima: {desvio_sf_otima:.2f}%\n")
            f.write(f"Tempo computacional méedio: {media_tempo:.4f} segundos\n")
            f.write(f"Melhor solucao encontrada: {melhor_solucao}\n\n")

def main():
    arquivos = ['./instances/fn2.dat', './instances/fn3.dat']
    referencia_solucoes = {
        './instances/fn2.dat': 190,
        './instances/fn3.dat': 207,
    }
    executar_instancias(arquivos, referencia_solucoes)

if __name__ == "__main__":
    main()
