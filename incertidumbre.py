import statistics
import numpy as np
import json
from funciones import *
from datos import * 


# determinacion del volumen
def V_t(N,V0,gammaRS,t0RS,tRS,beta,tSCM,gammaSCM,t,deltaV):
    #print("A: ",N*V0*(1-gammaRS*(t0RS-tRS)+beta*(tSCM-tRS)+gammaSCM*(t-tSCM)))
    #print("B: ",deltaV)
    return N*V0*(1-gammaRS*(t0RS-tRS)+beta*(tSCM-tRS)+gammaSCM*(t-tSCM)) + deltaV


# Incertidumbres
# u(V0)
def u_cal_V0(clave):
    U_cal = datos[clave]["U"]  
    U_cal_unidad = datos[clave]["U_unidad"]
    U_cal, U_cal_unidad = aLitros(U_cal, U_cal_unidad)
    k = datos[clave]["k"]
    return U_cal/k  # en L


def u_drift_V0(clave):
    delta_drift_V0 = datos[clave]["drift"]  # diferencia de valores de referencia entre calibraciones en L
    delta_drift_V0_unidad = datos[clave]["drift_unidad"]
    delta_drift_V0, delta_drift_V0_unidad = aLitros(delta_drift_V0, delta_drift_V0_unidad)
    return delta_drift_V0/raiz(3)  # en L

# si se usa metodo de llenado
def u_V0(clave, N=1):
    return N*raiz(u_cal_V0(clave)**2 + u_drift_V0(clave)**2), "L" # en litros porque se convieron en litros


# u(tRS)
def u_cal_tRS(clave,tRS=0):
    U_cal = datos[clave]["U"]
    if isinstance(U_cal,list):
        valor = datos[clave]["valor"]
        longitud = len(U_cal)
        if longitud <= 3: 
            U_cal = ajustePolinomial(valor,U_cal,tRS,1)
        elif longitud > 3 and longitud < 5: 
            U_cal = ajustePolinomial(valor,U_cal,tRS,2)
        elif longitud >= 5: 
            U_cal = ajustePolinomial(valor,U_cal,tRS,3)
    U_cal_unidad = datos[clave]["U_unidad"]
    k = datos[clave]["k"]
    return U_cal/k  # en L


def u_res_tRS(clave):
    res = datos[clave]['res']
    res_unidad = datos[clave]['res_unidad']
    return res/(2*raiz(3))  # en °C

def u_drift_tRS(clave):
    drift = datos[clave]["drift"]
    drift_unidad = datos[clave]["drift_unidad"]
    return drift/(2*raiz(3)) # en °C

def u_deltat_tRS(tmin,tmax):
    return (tmax-tmin)/raiz(12)

def u_deltats_RS(ta,tRS):
    return abs(tRS-ta)/(8*raiz(3))

def u_tRS(clave, tmin, tmax, ta, tRS):
    return raiz(u_cal_tRS(clave, tRS)**2 + u_res_tRS(clave)**2 + u_drift_tRS(clave)**2 + 
                u_deltat_tRS(tmin, tmax)**2 + u_deltats_RS(ta, tRS)**2), "°C"

# u(tSCM)
def u_cal_tSCM(clave, tSCM=0):
    U_cal = datos[clave]["U"]  
    if isinstance(U_cal,list):
        valor = datos[clave]["valor"]
        longitud = len(U_cal)
        if longitud <= 3: 
            U_cal = ajustePolinomial(valor,U_cal,tSCM,1)
        elif longitud > 3 and longitud < 5: 
            U_cal = ajustePolinomial(valor,U_cal,tSCM,2)
        elif longitud >= 5: 
            U_cal = ajustePolinomial(valor,U_cal,tSCM,3)

    U_cal_unidad = datos[clave]["U_unidad"]
    k = datos[clave]["k"]
    return U_cal/k  # en L


def u_res_tSCM(clave):
    res = datos[clave]['res']
    res_unidad = datos[clave]['res_unidad']
    return res/(2*raiz(3))  # en °C

def u_drift_tSCM(clave):
    drift = datos[clave]["drift"]
    drift_unidad = datos[clave]["drift_unidad"]
    return drift/(2*raiz(3)) # en °C

def u_deltat_tSCM(tmin,tmax):
    return (tmax-tmin)/raiz(12)

def u_deltats_SCM(ta,tSCM):
    return abs(tSCM-ta)/(8*raiz(3))

def u_tSCM(clave, tmin, tmax, ta, tSCM):
    return raiz(u_cal_tSCM(clave)**2 + u_res_tSCM(clave)**2 + u_drift_tSCM(clave)**2 + 
                u_deltat_tSCM(tmin, tmax)**2 + u_deltats_SCM(ta, tSCM)**2), "°C"

# u(gammaRS) y u(gammaSCM)
def u_gammaRS(material_RS):
    return 0.05*coef_material[material_RS], "1/°C"

def u_gammaSCM(material_SCM):
    return 0.05*coef_material[material_SCM], "1/°C"

# beta
def beta(tRS,tSCM):
    t = (tRS+tSCM)/2
    return (-0.1176*t**2 + 15.846*t - 62.677)*1e-6    # en 1/°C


# u(beta)
def u_beta():
    return 2*1e-6, "1/°C" 

# u(deltaV)
def u_cal_deltaV(clave):
    U_cal = datos[clave]["U"]  
    U_cal_unidad = datos[clave]["U_unidad"]
    U_cal, U_cal_unidad = aLitros(U_cal, U_cal_unidad)
    k = datos[clave]["k"]
    return U_cal/k  # en L


def u_drift_deltaV(clave):
    delta_drift_deltaV = datos[clave]["drift"]  # diferencia de valores de referencia entre calibraciones en L
    delta_drift_deltaV_unidad = datos[clave]["drift_unidad"]
    delta_drift_deltaV, delta_drift_deltaV_unidad = aLitros(delta_drift_deltaV, delta_drift_deltaV_unidad)
    return delta_drift_deltaV/raiz(3)  # en L


def u_deltaV(clave):
    return raiz(u_cal_deltaV(clave)**2 + u_drift_deltaV(clave)**2), "L" # en litros porque se convieron en litros


# u(deltaVmen), porque se considera que se elimina o agrega vol para llegar al vSCM
def u_deltaVmen(ancho,ancho_unidad,diametro,diametro_unidad):
    ancho, ancho_unidad = aMetros(ancho, ancho_unidad)
    diametro, diametro_unidad = aMetros(diametro, diametro_unidad)
    E = (math.pi)*(diametro/2)**2
    u_p = ancho/2
    resultado, resultado_unidad = aLitros(u_p*E, "m³")
    return resultado, "L" # en L  

# u(deltaVrep)
def desv_estandar(lista):
    return statistics.stdev(lista)

def u_deltaVrep(lista,unidad):
    return desv_estandar(lista)/raiz(len(lista)), unidad


# u(deltaVadd)
def u_deltaVadd(VN_SCM,VN_SCM_unidad):
    VN_SCM, VN_SCM_unidad = aLitros(VN_SCM, VN_SCM_unidad)
    if VN_SCM == 2: return 0.00029, "L"    # en L
    elif VN_SCM == 5: return 0.000514, "L"   # en L
    elif VN_SCM == 10: return 0.0009, "L"    # en L
    elif VN_SCM == 20: return 0.00139, "L"   # en L
    elif VN_SCM == 50: return 0.0035, "L"    # en L
    elif VN_SCM == 100: return 0.007 , "L"   # en L
    elif VN_SCM == 200: return 0.014 , "L"   # en L
    elif VN_SCM == 400: return 0.028 , "L"   # en L
    elif VN_SCM == 500: return 0.035 , "L"   # en L
    elif VN_SCM == 1000: return 0.070 , "L"  # en L
    elif VN_SCM == 2000: return 0.140, "L"   # en L
    else:
        x = np.array([2, 5, 10, 20, 50, 100, 200, 400, 500, 1000, 2000])
        y = np.array([0.00029, 0.000514, 0.0009, 0.00139, 0.0035, 0.007, 0.014, 0.028, 0.035, 0.070, 0.140])
        m, b = np.polyfit(x, y, 1)
        return m*VN_SCM+b, "L"   # en L

# Coeficientes de sensibilidad 

# estándar de referencia
def δVt_δNV0(gammaRS,t0RS,tRS,beta,tSCM,gammaSCM,t):
    return 1-gammaRS*(t0RS-tRS)+beta*(tSCM-tRS)+gammaSCM*(t-tSCM)
    
# tRS
def δVt_δtRS(N,V0,gammaRS,beta):
    return N*V0*(gammaRS-beta)

# tSCM
def δVt_δtSCM(N,V0,beta,gammaSCM):
    return N*V0*(beta-gammaSCM)

# gammaRS
def δVt_δgammaRS(N,V0,t0RS,tRS):
    return -N*V0*(t0RS-tRS)

# gammaSCM
def δVt_δgammaSCM(N,V0,t,tSCM):
    return N*V0*(t-tSCM)

# beta
def δVt_δbeta(N,V0,tSCM,tRS):
    return N*V0*(tSCM-tRS)

# deltaV
def δVt_δdeltaV():
    return 1

# deltaVmen
def δVt_δdeltaVmen():
    return 1

# deltaVrep
def δVt_δdeltaVrep():
    return 1

# deltaVadd
def δVt_δdeltaVadd():
    return 1


# iniciar calculos

def iniciar_calculos(N, 
                     codigo_RS, 
                     codigo_tRS, tmin_RS, tmax_RS, ta, tRS, 
                     codigo_tSCM, tmin_SCM, tmax_SCM, tSCM,
                     material_RS, material_SCM,
                     codigo_AUX,
                     ancho, ancho_unidad, diametro, diametro_unidad,
                     listaVt,listaVt_unidad,
                     VN_SCM,VN_SCM_unidad,
                     t0RS,t,
                     V0,
                     nombre_presupuesto,
                     nro_repeticiones,
                     nro_certificado,
                     modificacion=False):


    """calculos de incertidumbres
    """
    # patron de referencia
    u_NV0_valor = u_V0(codigo_RS,N)
    # tRS
    u_tRS_valor = u_tRS(codigo_tRS, tmin_RS, tmax_RS, ta, tRS)
    # tSCM
    u_tSCM_valor = u_tSCM(codigo_tSCM, tmin_SCM, tmax_SCM, ta, tSCM)
    # gammaRS y gammaSCM
    u_gammaRS_valor = u_gammaRS(material_RS)
    u_gammaSCM_valor = u_gammaSCM(material_SCM)
    # beta
    u_beta_valor = u_beta()
    # deltaV
    u_deltaV_valor = u_deltaV(codigo_AUX)
    # lectura del menisco del SCM
    u_deltaVmen_valor = u_deltaVmen(ancho,ancho_unidad,diametro,diametro_unidad)
    # repetibilidad
    u_deltaVrep_valor = u_deltaVrep(listaVt,listaVt_unidad)
    # factores adicionales
    u_deltaVadd_valor = u_deltaVadd(VN_SCM,VN_SCM_unidad)

    """calculos de coeficientes de sensibilidad
    """
    # V0
    δVt_δNV0_valor = δVt_δNV0(coef_material[material_RS],t0RS,tRS,beta(tRS,tSCM),tSCM,coef_material[material_SCM],t)
    # tRS
    
    δVt_δtRS_valor = δVt_δtRS(N,V0,coef_material[material_RS],beta(tRS,tSCM)), "L/°C"
    # tSCM
    δVt_δtSCM_valor = δVt_δtSCM(N,V0,beta(tRS,tSCM),coef_material[material_SCM]), "L/°C"
    # gammaRS
    δVt_δgammaRS_valor = δVt_δgammaRS(N,V0,t0RS,tRS), "L°C"
    # gammaSCM
    δVt_δgammaSCM_valor = δVt_δgammaSCM(N,V0,t,tSCM), "L°C"
    # beta
    δVt_δbeta_valor = δVt_δbeta(N,V0,tSCM,tRS), "L°C"
    # deltaV
    δVt_δdeltaV_valor = δVt_δdeltaV()
    # deltaVmen
    δVt_δdeltaVmen_valor = δVt_δdeltaVmen()
    # deltaVrep
    δVt_δdeltaVrep_valor = δVt_δdeltaVrep()
    # deltaVadd
    δVt_δdeltaVadd_valor = δVt_δdeltaVadd()

    """ Incertidumbre estándar combinada del mensurando
    """
    u1 = δVt_δNV0_valor*u_NV0_valor[0]
    u2 = δVt_δtRS_valor[0]*u_tRS_valor[0]
    u3 = δVt_δtSCM_valor[0]*u_tSCM_valor[0]
    u4 = δVt_δgammaRS_valor[0]*u_gammaRS_valor[0]
    u5 = δVt_δgammaSCM_valor[0]*u_gammaSCM_valor[0]
    u6 = δVt_δbeta_valor[0]*u_beta_valor[0]
    u7 = δVt_δdeltaV_valor*u_deltaV_valor[0]
    u8 = u_deltaVmen_valor[0]
    u9 = u_deltaVrep_valor[0]
    u10 = u_deltaVadd_valor[0]

    u_Vt_valor = raiz(
                        (u1)**2+
                        (u2)**2+
                        (u3)**2+
                        (u4)**2+
                        (u5)**2+
                        (u6)**2+
                        (u7)**2+
                        (u8)**2+
                        (u9)**2+
                        (u10)**2
                    ), "L"
 
    veff_u1 = 50
    veff_u2 = 200
    veff_u3 = 200
    veff_u4 = 200
    veff_u5 = 200
    veff_u6 = 200
    veff_u7 = 50
    veff_u8 = 200
    veff_u9 = nro_repeticiones-1
    veff_u10 = 200

    # elección de un factor de cobertura apropiado k 
    numerador = u_Vt_valor[0]**4
    denominador = (u1**4)/veff_u1 + (u2**4)/veff_u2 + (u3**4)/veff_u3 + (u4**4)/veff_u4 + \
                    (u5**4)/veff_u5 + (u6**4)/veff_u6 + (u7**4)/veff_u7 + (u8**4)/veff_u8 + \
                    (u9**4)/veff_u9 + (u10**4)/veff_u10
    
    veff = numerador/denominador
    k = round(ajuste_v_eff(veff))

    U_Vt_valor = k*u_Vt_valor[0], u_Vt_valor[1]

    presupuesto = u_NV0_valor, u_tRS_valor, u_tSCM_valor, \
            u_gammaRS_valor, u_gammaSCM_valor, u_beta_valor, u_deltaV_valor, \
            u_deltaVmen_valor, u_deltaVrep_valor, u_deltaVadd_valor, \
            δVt_δNV0_valor, δVt_δtRS_valor, δVt_δtSCM_valor, \
            δVt_δgammaRS_valor, δVt_δgammaSCM_valor, δVt_δbeta_valor, \
            δVt_δdeltaV_valor, δVt_δdeltaVmen_valor, δVt_δdeltaVrep_valor, δVt_δdeltaVadd_valor, \
            u_Vt_valor, k, U_Vt_valor


    presupuesto = {
        "nro_certificado":nro_certificado,
        "u_NV0":u_NV0_valor,
        "u_tRS":u_tRS_valor,
        "u_tSCM":u_tSCM_valor,
        "u_gammaRS":u_gammaRS_valor,
        "u_gammaSCM":u_gammaSCM_valor,
        "u_beta":u_beta_valor,
        "u_deltaV":u_deltaV_valor,
        "u_deltaVmen":u_deltaVmen_valor,
        "u_deltaVrep":u_deltaVrep_valor,
        "u_deltaVadd":u_deltaVadd_valor,
        "deltaVt_deltaNV0": δVt_δNV0_valor,
        "deltaVt_deltatRS":δVt_δtRS_valor,
        "deltaVt_deltatSCM":δVt_δtSCM_valor,
        "deltaVt_deltagammaRS":δVt_δgammaRS_valor,
        "deltaVt_deltagammaSCM":δVt_δgammaSCM_valor,
        "deltaVt_deltabeta":δVt_δbeta_valor,
        "deltaVt_deltadeltaV":δVt_δdeltaV_valor,
        "deltaVt_deltadeltaVmen":δVt_δdeltaVmen_valor,
        "deltaVt_deltadeltaVrep":δVt_δdeltaVrep_valor,
        "deltaVt_deltadeltaVadd":δVt_δdeltaVadd_valor,
        "u1":u1,
        "u2":u2,
        "u3":u3,
        "u4":u4,
        "u5":u5,
        "u6":u6,
        "u7":u7,
        "u8":u8,
        "u9":u9,
        "u10":u10,
        "u_unidad":"L",
        "uu_Vt":u_Vt_valor,
        "k":k,
        "U_Vt":U_Vt_valor
    }

    if modificacion == False:
        guardar_datos(nombre_presupuesto,presupuesto)
    else:
        var = nombre_presupuesto
        var = var.split("/")
        modificar_data(var[0],var[1],presupuesto)

    # Se mostrará en Litros
    print("u(NV0): ",u_NV0_valor)
    print("u(tRS): ",u_tRS_valor)
    print("u(tSCM): ",u_tSCM_valor)
    print("u(γRS): ",u_gammaRS_valor)
    print("u(γSCM): ",u_gammaSCM_valor,)
    print("u(β): ",u_beta_valor)
    print("u(ΔV): ",u_deltaV_valor)
    print("u(ΔVmen): ",u_deltaVmen_valor)
    print("u(ΔVrep): ",u_deltaVrep_valor)
    print("u(ΔVadd): ",u_deltaVadd_valor)
    print("δ(Vt)/δ(NV0): ",δVt_δNV0_valor)
    print("δ(Vt)/δ(tRS): ",δVt_δtRS_valor)
    print("δ(Vt)/δ(tSCM): ",δVt_δtSCM_valor)
    print("δ(Vt)/δ(γRS): ",δVt_δgammaRS_valor)
    print("δ(Vt)/δ(γSCM): ",δVt_δgammaSCM_valor)
    print("δ(Vt)/δ(β): ",δVt_δbeta_valor)
    print("δ(Vt)/δ(ΔV): ",δVt_δdeltaV_valor)
    print("δ(Vt)/δ(ΔVmen): ",δVt_δdeltaVmen_valor)
    print("δ(Vt)/δ(ΔVrep): ",δVt_δdeltaVrep_valor)
    print("δ(Vt)/δ(ΔVadd): ",δVt_δdeltaVadd_valor)
    print("u1: ",u1)
    print("u2: ",u2)
    print("u3: ",u3)
    print("u4: ",u4)
    print("u5: ",u5)
    print("u6: ",u6)
    print("u7: ",u7)
    print("u8: ",u8)
    print("u9: ",u9)
    print("u10: ",u10)
    print("u(Vt): ",u_Vt_valor)
    print("k: ",k)
    print("U(Vt): ",U_Vt_valor)

    return U_Vt_valor,k,veff,u_deltaVmen_valor,(desv_estandar(listaVt),listaVt_unidad),nro_repeticiones
"""
print(iniciar_calculos(N=4, 
                       codigo_RS="patron", 
                       codigo_tRS="TP001", tmin_RS=0, tmax_RS=0, ta=21, tRS=20.45,
                       codigo_tSCM="TP002", tmin_SCM=0, tmax_SCM=0.03, tSCM=20.50,
                       material_RS="Acero inoxidable grado 304", material_SCM="Acero inoxidable grado 304",
                       codigo_AUX="MVAP001",
                       ancho=0.1,ancho_unidad="cm", diametro=19.15, diametro_unidad="cm",
                       listaVt=[1999.95,2000,2000.05],listaVt_unidad="L", # debido a 3 repeticiones
                       VN_SCM=2000,VN_SCM_unidad="L",
                       t0RS=20,t=20,
                       V0=500.26
                       )       
        )
"""

def guardar_resultados(VN_SCM,VN_SCM_unidad,listaVt,listaVt_unidad,U_Vt_valor,k,veff,u_deltaVmen_valor,
                       desv_estandar,nro_repeticiones,nombre,nro_certificado):

    Vt, Vt_unidad = promediar(listaVt), listaVt_unidad
    U_Vt, U_Vt_unidad = U_Vt_valor[0], U_Vt_valor[1]

    # Se guardará en ml
    #VN_SCM, VN_SCM_unidad = aMiliLitros(VN_SCM, VN_SCM_unidad)
    #Vt, Vt_unidad = aMiliLitros(Vt, Vt_unidad)
    #U_Vt, U_Vt_unidad = aMiliLitros(U_Vt_valor[0], U_Vt_valor[1])
    resultados = {
                    "nro_certificado":nro_certificado,
                    "VN_SCM":VN_SCM,
                    "VN_SCM_unidad": VN_SCM_unidad,
                    "Vt":Vt,
                    "Vt_unidad":Vt_unidad,
                    "U_Vt":U_Vt,
                    "U_Vt_unidad":U_Vt_unidad,
                    "k":k,
                    "veff":veff,
                    "u_deltaVmen":str(u_deltaVmen_valor[0]),
                    "u_deltaVmen_unidad":u_deltaVmen_valor[1],
                    "desv_estandar":str(desv_estandar[0]),
                    "desv_estandar_unidad":desv_estandar[1],
                    "nro_repeticiones":nro_repeticiones
                }


    with open(f'{nombre}.json', 'w') as json_file:
        json.dump(resultados, json_file, indent=4)