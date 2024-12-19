import numpy as np
from funciones import * 

def corregir(codigo, valor):
    valor = float(valor)
    if isinstance(datos[codigo]["correccion"], list):
        x = np.array(datos[codigo]["valor"])  # valor nominal
        y = np.array(datos[codigo]["correccion"])  # correccion
        m, b = np.polyfit(x, y, 1)
        return valor+ valor*m+b
    else:
        return valor+datos[codigo]["correccion"]

# M-144 de Masa para T1 en patron
# LA-27 de longitud para T2 en calibrando
# BTH-01 de masa

datos = {
    "MVP001":{
        "VN":500,
        "VN_unidad":"L",
        "valor":[500],
        "correccion":0.26,
        "correccion_unidad":"L",
        "U":0.19,
        "U_unidad":"L",
        "drift":0,
        "drift_unidad":"L",
        "k":2,
        "clase":0.02,
        "tipo":"Ex",
        "material":"Acero inoxidable grado 304",
        "coef":0.000052,
        "coef_unidad":"1/°C",
        "tiempo_entrega":30,
        "tiempo_entrega_unidad":"s",
        "t_ref":20,
        "t_ref_unidad":"1/°C",
        "trazabilidad":"Patrones de referencia de LO JUSTO",
        "descripcion":"Medidor volumétrico 500 L Clase 0,02",
        "certificado_calibracion":"loJusto001-2024"
    },   
    "MVP002":{
        "VN":18.9271,
        "VN_unidad":"L",
        "correccion":0.0001,
        "correccion_unidad":"L",
        "U":0.0029,
        "U_unidad":"L",
        "drift":0.0029,
        "drift_unidad":"L",
        "k":2,
        "clase":0.02,
        "tipo":"Ex",
        "material":"Acero inoxidable grado 304",
        "coef":0.000052,
        "coef_unidad":"1/°C",
        "t_ref":20,
        "t_ref_unidad":"1/°C",
        "trazabilidad":"Patrones de referencia de METRINDUST S.A.C.",
        "descripcion":"Medidor volumétrico 5 gal Clase 0,02",
        "certificado_calibracion":"E293-L-578A-2023-1"
    }, 
    "MVAP001":{
        "VN":50,
        "VN_unidad":"ml",
        "valor":50,
        "correccion":0.23,
        "correccion_unidad":"ml",
        "unidad":"L",
        "res": 1,
        "res_unidad":"ml",
        "U":0.022,
        "U_unidad":"ml",
        "drift": 0.022,
        "drift_unidad": "ml",
        "k":2,
        "clase":"0.1",
        "trazabilidad":"Patrones de referencia de METRINDUST S.A.C.",
        "descripcion":"Probeta 50 ml U=0,28e-3",
        "certificado_calibracion":"MV-002-2024"
    },
    "TP001":{
        "valor":[-50.05,-0.05,50.01,100.02],
        "correccion":[0.075,0.012,0.001,-0.005],
        "unidad":"°C",
        "res": 0.01,
        "res_unidad":"°C",
        "U":[0.032,0.027,0.027,0.029],
        "U_unidad":"°C",
        "drift":0.032,
        "drift_unidad":"°C",
        "k":2,
        "trazabilidad":"Patrones de referencia de METRINDUST S.A.C.",
        "descripcion":"T001 - Termómetro: U= 0,06 °C",
        "certificado_calibracion":"T-001-2024"
    },
    "TP002":{ 
        "valor":[-50.05,-0.05,50.01,100.02],
        "correccion":[0.075,0.012,0.001,-0.005],
        "unidad":"°C",
        "res": 0.01,
        "res_unidad": "°C",
        "U":[0.032,0.027,0.027,0.029],
        "U_unidad":"°C",
        "k":2,
        "drift":0.032,
        "drift_unidad":"°C",
        "trazabilidad":"Patrones de referencia de INACAL-DM",
        "descripcion":"T002 - Termómetro: U= 0,06 °C",
        "certificado_calibracion":"T-002-2024"
    },
    "Termometro001":{
        "valor":[15.4,25.4,30.4],
        "correccion":[-0.4, -0.4, -0.4],
        "res": 0.1,
        "U":0.3,
        "U_unidad":"°C",
        "drift":0.3,
        "drift_unidad":"°C",
        "k":2,
        "trazabilidad":"INACAL-DM",
        "descripcion":"Descripcion de termometro",
        "certificado_calibracion":"Termometro001-2024"
    },
    "Higrometro001":{
        "valor":[41.6,64.2,89.4],
        "correccion":[-6.6, -4.2, 0.6],
        "res": 0.1,
        "U":3.1,
        "U_unidad":"%",
        "drift":3.1,
        "drift_unidad":"%",
        "k":2,
        "trazabilidad":"INACAL-DM",
        "descripcion":"Descripcion de higrometro",
        "certificado_calibracion":"Higrometro001-2024"
    },
    "Barometro001":{
        "valor":[970,1000,1030],
        "correccion":[-1.0, -1.2, -1.1],
        "res": 0.1,
        "U":0.8,
        "U_unidad":"mbar",
        "drift":0.8,
        "drift_unidad":"mbar",
        "k":2,
        "trazabilidad":"INACAL-DM",
        "descripcion":"descripcion de barometro",
        "certificado_calibracion":"Barometro001-2024"
    }
}


coef_material = {
    "Fibra de carbon": 1e-6,
    "Vidrio de borosilicato 3,3": 9.9e-6,
    "Vidrio de borosilicato 5,0": 15e-6,
    "Vidrio de cal sodada": 27e-6,
    "Acero": 33e-6,
    "Carbono suave": 33.5e-6,
    "Acero inoxidable grado 304": 51.8e-6,
    "Acero inoxidable grado 316": 47.7e-6,
    "Acero inoxidable 17-4PH": 32.4e-6,
    "Cobre - aleación de zinc (latón)": 54e-6,
    "Aluminio": 69e-6,
    "PVC": 80e-6
}

nro_material = {}
for i,e in enumerate(list(coef_material.keys())):
    nro_material[f"{i+1}"]=e


def modificarDatos_valor(codigo,clave,valor):
    datos[codigo][clave] = valor

def modificarDatos_clave(codigo,clave,clave_new):
    datos[codigo][clave_new] = datos[codigo].pop(clave)

lista_codigo_RS = ["MVP001","MVP002"]
lista_codigo_tRS = ["TP001"]
lista_codigo_tSCM = ["TP002"]
lista_codigo_AUX = ["MVAP001"]
lista_codigo_t = ["Termometro001"]
lista_codigo_h = ["Higrometro001"]
lista_codigo_p = ["Barometro001"]

alternativas_materiales=[('','-- Seleccionar --')]
for e in list(nro_material.values()):
    alternativas_materiales.append((e,e))


