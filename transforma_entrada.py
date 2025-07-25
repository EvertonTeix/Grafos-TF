import os
import math

def tsp_to_adj_matrix(tsp_path):
    with open(tsp_path) as f:
        lines = f.readlines()

    coord_section = False
    coords = []
    for line in lines:
        if "NODE_COORD_SECTION" in line:
            coord_section = True
            continue
        if "EOF" in line or not coord_section:
            continue
        parts = line.strip().split()
        if len(parts) >= 3:
            coords.append((float(parts[1]), float(parts[2])))

    def euclidean(p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return round(math.hypot(dx, dy), 6)


    n = len(coords)
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = euclidean(coords[i], coords[j])
    return matrix

def salvar_matriz_em_txt(matrix, path_out):
    with open(path_out, 'w') as f:
        f.write(str(len(matrix)) + '\n')
        for row in matrix:
            linha = ', '.join(f"{x}" for x in row)
            f.write(f"[{linha}]\n")

def converter_todos_tsp_em_txt(pasta_tsp, pasta_saida):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    subpastas = [os.path.join(pasta_tsp, d) for d in os.listdir(pasta_tsp) if os.path.isdir(os.path.join(pasta_tsp, d))]
    for subpasta in subpastas:
        arquivos = [arq for arq in os.listdir(subpasta) if arq.endswith(".tsp")]
        for arq in arquivos:
            tsp_path = os.path.join(subpasta, arq)
            matriz = tsp_to_adj_matrix(tsp_path)
            nome_saida = arq.replace(".tsp", ".txt")
            path_out = os.path.join(pasta_saida, nome_saida)
            salvar_matriz_em_txt(matriz, path_out)
            print(f"Convertido: {tsp_path} -> {path_out}")

# Exemplo de uso
if __name__ == "__main__":
    pasta_tsp = "instancias_tsp"        # pasta onde estão as subpastas com arquivos .tsp
    pasta_saida = "entradas_txt"        # pasta de saída para os .txt convertidos
    converter_todos_tsp_em_txt(pasta_tsp, pasta_saida)
