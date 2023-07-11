import gurobipy as gp
from gurobipy import GRB

# Cria um modelo vazio
m = gp.Model()

# Indices
I = range(0, 3) # Tipo de pão
J = range(0, 6) # Dia da semana - produção
T = range(0, 4) # Janela de produção
K = range(0, 6) # Dia da semana - estoque

X = m.addVars(I, J, vtype=GRB.CONTINUOUS, name="X")         # quantida de paes produzidos
E = m.addVars(I, J, vtype=GRB.CONTINUOUS, name="E")         # excedente de paes
P = m.addVars(I, J, K, vtype=GRB.CONTINUOUS, name="P")      # estoque de paes


# Dados

# Custos  
R = [0.8, 1, 0.9]                                  # custo de produção dos 3 tipos de pães
S = [0.05, 0.07, 0.1]                              # custo de armazenamento dos 3 tipos de pães
C = 300                                            # Capacidade de armazenamento 
D = [68, 264, 462, 540, 768, 750]                  # demanda total de cada dia

# Demanda total por pão

Q = [[48,20,0], [120,78,66], [330,114,18], [210,240,90], [480,108,180], [420,210,120]]

# Capacidade de produção diaria
    
A = [[540,180,360], [360,360,540], [360,360,540], [720,360,180], [360,360,360], [540,360,360]]    # cada grupo é um dia da semana e cada item e o tipo de pão

# Restrições

for j in J:                                                         # para cada dia da semana
    for i in I:                                                     # para cada tipo de pao                     
            m.addConstr(X[i,j] <= A[j][i])                          # restrição de capacidade maxima de produção            
    m.addConstr(gp.quicksum(X[i,j] for i in I)  >= D[j])            # restrição de demanda
    
    for i in I:                                                     # para cada tipo de pao
        for k in K:                                                 # para cada dia da semana (estoque)
            if k >= j:                                              # se o dia do estoque for maior ou igual ao dia da produção
                if k == j:                                          # se for o mesmo dia da produção
                    m.addConstr(P[i,j,k] == E[i,j])                 # o estoque é igual ao excedente da produção
            else:
                if k > 0:
                    m.addConstr(P[i,j,k] == P[i,j,k-1] + E[i,j])    # o estoque é igual ao estoque do dia anterior mais o excedente da produção
            
            m.addConstr(P[i,j,k] <= C)                              # restrição do estoque máximo
            
            if k < j+3 and k >= j:                                  # se o dia do estoque estiver dentro da janela de produção (3 dias)
                    m.addConstr(X[i,j] - (D[j]-P[i,j,k]) <= 300)    # restrição do estoque máximo durante a janela de produção
                    
                    
# Define a função objetivo
m.setObjective(gp.quicksum(R[i]*X[i,j] + S[i]*E[i,j] for i in I for j in J), GRB.MINIMIZE)  


m.write('modeloTeste.lp')
            
            

            

