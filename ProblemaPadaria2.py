import gurobipy as gp
from gurobipy import GRB

# Cria um modelo vazio
m = gp.Model()

# Indices
I = range(0, 3) # Tipo de pão
J = range(0, 6) # Dia da semana - produção
T = range(0, 4) # Janela de produção
K = range(0, 6) # Dia da semana - estoque

X = m.addVars(I, J, lb = 0, vtype=GRB.CONTINUOUS, name="X")         # quantida de paes produzidos
E = m.addVars(I, J, lb = 0,  vtype=GRB.CONTINUOUS, name="E")         # excedente de paes
#P = m.addVars(I, J, K, lb = 0, vtype=GRB.CONTINUOUS, name="P")      # estoque de paes

# Dados

# Custos  
R = [0.8, 1, 0.9]                                  # custo de produção dos 3 tipos de pães
S = [0.05, 0.07, 0.1]                              # custo de armazenamento dos 3 tipos de pães
C = 300                                            # Capacidade de armazenamento 
D = [68, 264, 462, 540, 768, 750]                  # demanda total de cada dia

# Demanda total por pão

Q = [[48,20,0], [120,78,66], [330,114,18], [210,240,90], [480,108,180], [420,210,120]]          # Q [ dia da semana ] [ tipo de pão ]

# Capacidade de produção diaria
    
A = [[540,180,180], [360,360,540], [360,180,540], [540,360,180], [180,360,360], [540,360,180]]    # cada grupo é um dia da semana e cada item e o tipo de pão

# Restrições

for j in J:                                                         # para cada dia da semana
    for i in I:                                                     # para cada tipo de pao                     
            #m.addConstr(X[i,j] <= A[j][i])                         # restrição de capacidade maxima de produção                        
            m.addConstr(X[i,j] >= Q[j][i])                          # restrição de demanda  ( O PROBLEMA É, TEM Q SER FEITO PARA CADA TIPO DE PÃO)    
    m.addConstr(gp.quicksum(X[i,j] for i in I)  >= D[j]) 
    
for j in J:                                                         # para cada dia da semana
    for i in I:     
        m.addConstr(E[i,j] == X[i,j] - Q[j][i])
        m.addConstr(E[i,j] <= C)                                # restrição de capacidade de armazenamento
   
# Define a função objetivo
m.setObjective(gp.quicksum(R[i]*X[i,j] + S[i]*E[i,j] for i in I for j in J), GRB.MINIMIZE)  


m.write('modeloTeste.lp')
            
            

            

