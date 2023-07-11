import gurobipy as gp
from gurobipy import GRB
import pandas as pd

modelo = gp.Model()

modelo = gp.read('modeloTeste.lp')

modelo.optimize()



dados = []

dados.append(["Função objetivo", modelo.objVal])

for v in modelo.getVars():
    dados.append([v.varName, v.x])


df = pd.DataFrame(dados, columns=["Variável", "Valor"])

df.to_csv("dados.csv", index=False)

print("Valor da função objetivo:", modelo.objVal)
print(df)