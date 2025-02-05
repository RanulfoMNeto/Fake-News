# Modelagem do Problema de Minimização da Propagação de Fake News

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

<!-- ### 3. Tempo de propagação considerando os recursos $x_v$
Se o servidor $u$ está infectado, o tempo mínimo de infecção do servidor $v$ depende do tempo de propagação $t_{uv}$ e do possível atraso $\delta$ se $x_u = 1$:

$$
t_{v,s} \geq t_{u,s} + t_{uv} + x_u \cdot \delta, \quad \forall (u,v) \in E, \forall s \in V
$$

Se um servidor recebe a fake news depois do tempo limite $T$, então ele não é infectado:

$$
y_{v,s} = 0, \quad \forall v \in V, \forall s \in V \text{ se } t_{v,s} > T
$$ 

[Restrição Não Linearizada] -->

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