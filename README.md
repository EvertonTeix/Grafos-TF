# Algoritmo de Christofides em Python

Este repositório contém uma implementação completa do algoritmo de **Christofides** para resolver o problema do **Caixeiro Viajante (TSP)** de forma aproximada, com garantia de erro de no máximo 1.5 vezes o ótimo em grafos métricos.

---

## Descrição

O algoritmo segue os seguintes passos:

1. **Leitura do grafo** a partir de um arquivo `.txt` com matriz de adjacência.
2. Construção da **Árvore Geradora Mínima (AGM)** via algoritmo de Prim.
3. Identificação de **vértices de grau ímpar** na AGM.
4. Cálculo do **emparelhamento de custo mínimo** entre os vértices ímpares.
5. Combinação da AGM com o emparelhamento para gerar um **multigrafo euleriano**.
6. Geração de um **circuito euleriano**.
7. Aplicação de **atalhos** (shortcutting) para gerar um **ciclo hamiltoniano**.
8. Cálculo do **custo da solução** e do **erro percentual** em relação ao ótimo conhecido.

---

## Estrutura do Arquivo de Entrada

O arquivo `.txt` deve conter:
- Primeira linha: número de vértices.
- Linhas seguintes: matriz de adjacência (uma linha por linha da matriz), usando listas Python (ex: `[0, 2, 3]`).

**Exemplo (`exemplo_entrada.txt`):**
```
4
[0, 2, 9, 10]
[2, 0, 6, 4]
[9, 6, 0, 8]
[10, 4, 8, 0]
```

---

## Execução

Para executar o algoritmo:

```bash
python christofides.py
```

Edite o final do script (`if __name__ == "__main__"`) para escolher o arquivo e o valor ótimo:

```python
christofides("exemplo_entrada.txt", valor_otimo=14)
```

---

## Dependências

- Python 3.7+
- [NetworkX](https://networkx.org/)

Instalação:

```bash
pip install networkx
```

---

## Saída Esperada

Exemplo de saída no terminal:

```
Árvore Geradora Mínima:
[(0, 1, {'weight': 2}), (1, 3, {'weight': 4}), (1, 2, {'weight': 6})]
Peso da árvore geradora mínima: 12.0

Solução Aproximada Encontrada por Christofides:
[0, 1, 2, 3, 0]
Peso da Solução: 14.0

Valor da Solução Ótima: 14
Erro percentual: 0.0 %
```

---

## Licença

MIT