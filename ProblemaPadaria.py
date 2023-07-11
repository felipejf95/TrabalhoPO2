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

# Define a função objetivo
m.setObjective(X.sum(), GRB.MINIMIZE)  # NAO ESTA PRONTA

# Dados

# Custos  
R = [0.8, 1, 0.9]                                  # custo de produção dos 3 tipos de pães
S = [0.05, 0.07, 0.1]                              # custo de armazenamento dos 3 tipos de pães

D = [68, 264, 462, 540, 768, 750]                  # demanda total de cada dia

# Capacidade de produção diaria
    
A = [[540,180,360], [360,360,540], [360,360,540], [720,360,180], [360,360,360], [540,360,360]]    # cada grupo é um dia da semana e cada item e o tipo de pão

# Restrição de demanda 

for j in J:                                              # para cada dia da semana
    for i in I:                                          # para cada tipo de pao
        if i <= 2:            
            m.addConstr(X[i,j] <= A[j][i])
    m.addConstr(gp.quicksum(X[i,j] for i in I)  >= D[j])
   


m.write('modeloTeste.lp')
            
            

            

