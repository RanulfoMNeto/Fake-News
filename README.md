# Trabalho Prático Final

## GCC118 - Programação Matemática

**Universidade Federal de Lavras**

**Profa. Andreza C. Beezão Moreira**  
**Prof. Mayron César O. Moreira**  

---

## 1. Introdução

A disseminação de notícias falsas, ou popularmente conhecidas como *fake news*, é um problema gravíssimo que está literalmente ao alcance dos nossos dedos. De acordo com uma matéria publicada no *Journal da USP*¹, entre 21 países pesquisados, o Brasil possui a população com maior dificuldade em identificar *fake news*. 
Uma forma de coibir que tais notícias sejam propagadas é criar mecanismos de atraso na difusão de pacotes de dados pouco confiáveis nas redes de computadores. Para tanto, suponha que uma mensagem classificada como suspeita por meio de uma rede neural seja enviada através de um vértice $s \in V$ de uma rede modelada por um grafo direcionado $G(V, E)$. O conjunto de vértices $V$ corresponde aos servidores que processam as informações, enquanto os arcos $(u,v) \in E$ são os enlaces de comunicação entre os servidores $u,v$. Deseja-se reduzir o número de servidores em que a notícia falsa pode se encontrar após um período de tempo igual a $T$.

A propagação de uma informação no enlace $(u, v) \in E$ possui tempo estimado igual a $t_{uv}$. O Setor de Tecnologia da Informação (STI) do governo federal possui recursos (*softwares* auxiliares, por exemplo) tecnológicos que podem ser aplicados aos servidores para retardar o tempo de *broadcast* da *fake news*. Assim, caso o servidor $u$ possua algum dos $\alpha$ recursos instalados, o tempo de transmissão da *fake news* no enlace $(u, v)$ seria $t_{uv} + \delta$, em que $\delta > 0$ representa um atraso de propagação. Cada um dos $i = 1, \dots, \alpha$ recursos fica disponível no instante $\beta_i$.

A solução do problema consiste em determinar a designação dos recursos aos servidores. Cada servidor receberá, no máximo, um recurso. Considera-se que um recurso $i$ é alocado no menor tempo $\beta_i$. O objetivo definido é a minimização da quantidade de servidores em que a *fake news* poderia chegar em um tempo menor ou igual a $T$.

¹ Matéria: [Relatório da OCDE mostra que brasileiros são os piores em identificar notícias falsas](https://jornal.usp.br/radio-usp/relatorio-da-ocde-mostra-que-brasileiros-sao-os-piores-em-identificar-noticias-falsas/).

---

## 2. Objetivos

Essa atividade avaliativa visa verificar o aprendizado do discente em termos dos conteúdos de Programação Linear e Inteira vistos no curso de GCC118. Para tanto:

1. Formule o problema como programa linear ou inteiro.
2. Resolva as instâncias propostas com um solver genérico (CPLEX, Gurobi, Che, Coin-OR, GLPK, SCIP).
3. Defina e implemente a meta-heurística definida logo abaixo, no item 3.
4. Resolva as instâncias definidas com a meta-heurística.
5. Documente e analise os experimentos em um relatório.
6. Apresente os resultados em aula.

---

## 3. Regras

1. Metaheurística: **Simulated Annealing**.
2. O trabalho deve ser feito em duplas.
3. O objetivo do trabalho é conhecer uma meta-heurística profundamente e ganhar experiência prática para aplicá-la em novos problemas.
4. Todas as escolhas feitas para aplicar a meta-heurística devem ser claramente relatadas. Isso inclui:
   - Representação do problema
   - Função objetivo
   - Geração da solução inicial
   - Vizinhança e estratégia de escolha em buscas locais
   - Operadores (crossover, mutação) para algoritmos genéticos
   - Parâmetros do método (temperatura, lista tabu e tenure)
   - Critério de parada
5. Cuidado com a documentação das instâncias, tempo de execução, parâmetros, número de experimentos, semente do gerador randômico, dados experimentais, etc.
6. Para métodos estocásticos, os valores apresentados devem ser médias de pelo menos 5 replicações de cada experimento com sementes diferentes.
7. Todas as implementações devem aceitar uma instância no formato do problema na entrada padrão (*stdin*) e imprimir a melhor solução encontrada na saída padrão (*stdout*).
8. Os principais parâmetros do método devem ser definíveis pela linha de comando. O primeiro parâmetro da linha de comando é o nome de um arquivo para gravar a melhor solução encontrada.
9. Qualquer tentativa de plágio será punida com medidas administrativas cabíveis.

---

## 4. Entregáveis

A dupla deverá criar um repositório no GitHub contendo:

- **Código fonte** e README bem documentado.
- **Um relatório** com a documentação da solução, incluindo resultados e discussão. Elementos obrigatórios:
  - Introdução
  - Formulação
  - Descrição da solução
  - Resultados obtidos com análise
  - Conclusão e Bibliografia
- **Implementação do modelo matemático e da heurística**. Não é permitido o uso de bibliotecas proprietárias.
- **Resultados computacionais**, incluindo uma tabela com:
  - Valor da solução inicial (SI)
  - Valor da solução final (SF)
  - Desvio percentual entre SI e SF ($100 \times (SI-SF)/SI$)
  - Desvio percentual da SF em relação à solução ótima
  - Tempo computacional da metaheurística
  - Tempo computacional da resolução via solver
- **Protocolos das execuções** do solver e da meta-heurística e outros dados experimentais detalhados.
- **Uma apresentação em aula**.

---

## 5. Instâncias teste

As instâncias estão disponíveis em: [Link para as instâncias](https://drive.google.com/file/d/1mzyvWHxIkF--ZH-v1266RwYtRJzOUZI6/view?usp=sharing).

| Instância | Valor referência |
|-----------|-----------------|
| 01        | 189             |
| 02        | 190             |
| 03        | 207             |
| 04        | 216             |
| 05        | 226             |
| 06        | 196             |
| 07        | 196             |
| 08        | 213             |
| 09        | 226             |
| 10        | 235             |

---
