import gurobipy as gp
from gurobipy import GRB

modelo = gp.Model()

modelo = gp.read('modeloTeste.lp')

modelo.optimize()
