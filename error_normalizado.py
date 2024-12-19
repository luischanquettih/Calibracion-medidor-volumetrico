from funciones import *
V_lab = 18.91906
V_ref = 18.9199

U_lab = 0.00581
U_ref = 0.0044

E_n = (V_lab - V_ref) / raiz(U_lab**2 + U_ref**2)
print(abs(E_n))