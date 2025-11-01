# Calculadora de Teoria das Filas (M/M/1, M/M/c e M/M/1/K)

Aplicação interativa desenvolvida em **Python (Tkinter)** para o cálculo de métricas clássicas de **Teoria das Filas**, incluindo os modelos **M/M/1**, **M/M/c (ou M/M/s)** e **M/M/1/K**.

---

## Sumário

- [Visão Geral](#-visão-geral)
- [Modelos Suportados](#-modelos-suportados)
- [Métricas Calculadas](#-métricas-calculadas)

---

## Visão Geral

A **Calculadora de Teoria das Filas** fornece uma interface gráfica intuitiva que permite inserir parâmetros (taxas de chegada, atendimento, número de servidores, capacidade do sistema) e obter automaticamente:

- **Probabilidades do sistema (vazio, cheio, espera, etc.)**
- **Número médio de clientes no sistema e na fila**
- **Tempos médios de espera e de permanência**
- **Taxa de utilização dos servidores**

Tudo isso com explicações e formatação amigável.

---

## Modelos Suportados

| Modelo | Descrição | Parâmetros |
|:-------|:-----------|:------------|
| **M/M/1** | 1 servidor, fila infinita | λ (taxa de chegada), μ (taxa de atendimento) |
| **M/M/c** | c servidores, fila infinita | λ, μ, c (número de servidores) |
| **M/M/1/K** | 1 servidor, fila finita de capacidade K | λ, μ, K (capacidade total do sistema) |

---

## Métricas Calculadas

As seguintes grandezas são calculadas automaticamente conforme o modelo selecionado:

| Símbolo | Nome | Interpretação |
|:---------|:------|:---------------|
| ρ (rho) | Fator de utilização | Proporção de tempo em que o sistema está ocupado |
| P₀ | Probabilidade do sistema vazio | Nenhum cliente presente |
| Pk | Probabilidade do sistema cheio | (somente em M/M/1/K) |
| L | Número médio de clientes no sistema | Fila + atendimento |
| Lq | Número médio de clientes na fila | Apenas os que esperam |
| W | Tempo médio no sistema | Espera + atendimento |
| Wq | Tempo médio de espera na fila | Apenas tempo de espera |
| λ_eff | Taxa de chegada efetiva | (somente em M/M/1/K) — desconta perdas |

---