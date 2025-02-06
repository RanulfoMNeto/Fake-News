# Modelagem do Problema de Minimização da Propagação de Fake News

A disseminação de notícias falsas, ou popularmente conhecidas como *fake news*, é um problema gravíssimo que está literalmente ao alcance dos nossos dedos. De acordo com uma matéria publicada no *Journal da USP*¹, entre 21 países pesquisados, o Brasil possui a população com maior dificuldade em identificar *fake news*. 
Uma forma de coibir que tais notícias sejam propagadas é criar mecanismos de atraso na difusão de pacotes de dados pouco confiáveis nas redes de computadores. Para tanto, suponha que uma mensagem classificada como suspeita por meio de uma rede neural seja enviada através de um vértice $s \in V$ de uma rede modelada por um grafo direcionado $G(V, E)$. O conjunto de vértices $V$ corresponde aos servidores que processam as informações, enquanto os arcos $(u,v) \in E$ são os enlaces de comunicação entre os servidores $u,v$. Deseja-se reduzir o número de servidores em que a notícia falsa pode se encontrar após um período de tempo igual a $T$.

A propagação de uma informação no enlace $(u, v) \in E$ possui tempo estimado igual a $t_{uv}$. O Setor de Tecnologia da Informação (STI) do governo federal possui recursos (*softwares* auxiliares, por exemplo) tecnológicos que podem ser aplicados aos servidores para retardar o tempo de *broadcast* da *fake news*. Assim, caso o servidor $u$ possua algum dos $\alpha$ recursos instalados, o tempo de transmissão da *fake news* no enlace $(u, v)$ seria $t_{uv} + \delta$, em que $\delta > 0$ representa um atraso de propagação. Cada um dos $i = 1, \dots, \alpha$ recursos fica disponível no instante $\beta_i$.

A solução do problema consiste em determinar a designação dos recursos aos servidores. Cada servidor receberá, no máximo, um recurso. Considera-se que um recurso $i$ é alocado no menor tempo $\beta_i$. O objetivo definido é a minimização da quantidade de servidores em que a *fake news* poderia chegar em um tempo menor ou igual a $T$.

¹ Matéria: [Relatório da OCDE mostra que brasileiros são os piores em identificar notícias falsas](https://jornal.usp.br/radio-usp/relatorio-da-ocde-mostra-que-brasileiros-sao-os-piores-em-identificar-noticias-falsas/).

## 1. Definição do Problema
Dado um grafo direcionado $G(V, E)$, onde:
- Cada vértice $v \in V$ representa um servidor.
- Cada arco $(u, v) \in E$ representa um canal de comunicação entre dois servidores, com um tempo de propagação $t_{uv}$.
- A *fake news* pode começar em qualquer servidor $s \in V$.
- Queremos minimizar o número total de servidores infectados considerando **todos os possíveis pontos iniciais da fake news**.
- Podemos distribuir **recursos** que aumentam o tempo de propagação em $\delta$.

O objetivo é encontrar **a melhor configuração de distribuição de recursos** que minimiza a infecção total.

---

## 2. Parâmetros
- $G = (V,E)$ → Grafo representando a rede de servidores.
- $t_{uv}$ → Tempo normal de propagação da fake news pelo arco $(u,v)$.
- $\delta$ → Atraso na propagação causado por um recurso alocado.
- $\beta_i$ → Tempo mínimo em que o recurso $i$ pode ser alocado.
- $T$ → Tempo limite para considerar a propagação.
- $\alpha$ → Número máximo de recursos disponíveis.

---

## 3. Variáveis de Decisão
1. **Estados de infecção para cada cenário**:
   - $y_{v,s} \in \{0,1\}$ → 1 se o servidor $v$ é infectado quando a fake news começa em $s$, 0 caso contrário.

2. **Propagação da fake news**:
   - $z_{uv,s} \in \{0,1\}$ → 1 se a fake news propaga do servidor $u$ para $v$ quando começa em $s$, 0 caso contrário.

3. **Tempo de infecção dos servidores**:
   - $t_{v,s} \geq 0$ → Tempo em que o servidor $v$ é infectado quando a fake news começa em $s$.

4. **Alocação de recursos**:
   - $x_v \in \{0,1\}$ → 1 se um recurso é alocado no servidor $v$, 0 caso contrário.

5. **Uso de um recurso específico**:
   - $w_{vi} \in \{0,1\}$ → 1 se o recurso $i$ é alocado ao servidor $v$, 0 caso contrário.

---

## 4. Função Objetivo
Queremos minimizar o número total de infecções, considerando **todos os possíveis pontos iniciais da fake news**:

$$
\min \sum_{s \in V} \sum_{v \in V} y_{v,s}
$$

---

## 5. Restrições

### 1. Cada $s$ pode ser um ponto inicial
Se a fake news começa em $s$, então $s$ está infectado no instante 0:

$$
y_{s,s} = 1, \quad \forall s \in V
$$

E seu tempo de infecção é zero:

$$
t_{s,s} = 0, \quad \forall s \in V
$$

---

### 2. Propagação da fake news para cada ponto inicial $s$
A fake news pode se propagar de $u$ para $v$ **somente se $u$ já estiver infectado**:

$$
z_{uv,s} \leq y_{u,s}, \quad \forall (u,v) \in E, \forall s \in V
$$

Se a fake news se propaga de $u$ para $v$, então $v$ também deve estar infectado:

$$
y_{v,s} \geq z_{uv,s}, \quad \forall (u,v) \in E, \forall s \in V
$$

---

### 3. Tempo de propagação considerando os recursos $x_v$
Se o servidor $u$ está infectado, o tempo mínimo de infecção do servidor $v$ depende do tempo de propagação $t_{uv}$ e do possível atraso $\delta$ se $x_u = 1$:

$$
t_{v,s} \geq t_{u,s} + t_{uv} + x_u \cdot \delta, \quad \forall (u,v) \in E, \forall s \in V
$$

Para garantir que um servidor $v$ não seja infectado se seu tempo de infecção ultrapassar o limite $T$, introduzimos uma variável auxiliar binária $\gamma_{v,s}$ e um grande $M$, resultando nas seguintes restrições:

$$
y_{v,s} \leq M \cdot (1 - \gamma_{v,s}), \quad \forall v \in V, \forall s \in V
$$

$$
t_{v,s} \leq T + M \cdot \gamma_{v,s}, \quad \forall v \in V, \forall s \in V
$$

Onde:
- $M$ é um valor suficientemente grande para garantir a ativação correta da restrição.
- $\gamma_{v,s}$ é uma variável binária que indica se $t_{v,s}$ ultrapassou $T$:
  - Se $t_{v,s} > T$, então $\gamma_{v,s} = 1$ e $y_{v,s} = 0$, garantindo que o servidor não seja infectado.
  - Se $t_{v,s} \leq T$, então $\gamma_{v,s}$ pode ser 0 e $y_{v,s}$ pode ser ativado conforme necessário.

---

### 4. Número máximo de recursos alocados
Cada servidor pode receber no máximo um recurso, e o total de recursos distribuídos não pode ultrapassar $\alpha$:

$$
\sum_{v \in V} x_v \leq \alpha
$$

---

### 5. Disponibilidade dos recursos
Um servidor $v$ só pode receber um recurso **se houver pelo menos um disponível no tempo certo $\beta_i$**:

$$
t_{v,s} \geq \sum_{i \in I} \beta_i \cdot w_{vi}, \quad \forall v \in V, \forall s \in V
$$

---

### 6. Se um servidor recebe um recurso, ele deve estar alocado corretamente
$$
x_v = \sum_{i \in I} w_{vi}, \quad \forall v \in V
$$

---