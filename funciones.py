import math
import numpy as np 
from scipy.optimize import curve_fit
import json  
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, Paragraph
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from nltk.tokenize import word_tokenize
from clases import *
from datetime import date
import shutil

def aLitros(volumen,volumen_unidad):
    unidades = {'gal':3.785411784,'cm3':0.001,'m3':1000,'ft3':28.316846592,'ml':0.001,'m³':1000}
    if type(volumen) is list: 
        if type(volumen[0]) is not list:
            for e in unidades:
                if volumen_unidad == e:
                    for i,v in enumerate(volumen):
                        volumen[i] = volumen[i]*unidades[e]
                    volumen_unidad = 'L'       
            return volumen, volumen_unidad
        elif type(volumen[0]) is list:
            resultado = []
            for l in volumen: 
                if type(l) is list:
                    for e in unidades:
                        if volumen_unidad == e: 
                            for i,v in enumerate(l):
                                l[i] = l[i]*unidades[e] 
                    resultado.append(l)         
            volumen_unidad = 'L'
            return resultado, volumen_unidad
    elif type(volumen) is not list:
        for e in unidades:
            if volumen_unidad == e:
                volumen = float(volumen)*unidades[e]
                volumen_unidad = 'L'
                break
        return float(volumen), volumen_unidad

def aMiliLitros(volumen,volumen_unidad):
    unidades = {'gal':3785.411784, 'cm3':1, 'm3':1000000, 'ft3':28316.846592, 'L':1000, 'm³':1000000}
    if type(volumen) is list: 
        if type(volumen[0]) is not list:
            for e in unidades:
                if volumen_unidad == e:
                    for i,v in enumerate(volumen):
                        volumen[i] = volumen[i]*unidades[e]
                    volumen_unidad = 'ml'       
            return volumen, volumen_unidad
        elif type(volumen[0]) is list:
            resultado = []
            for l in volumen: 
                if type(l) is list:
                    for e in unidades:
                        if volumen_unidad == e:  
                            for i,v in enumerate(l):
                                l[i] = l[i]*unidades[e] 
                    resultado.append(l)         
            volumen_unidad = 'ml'
            return resultado, volumen_unidad
    elif type(volumen) is not list:
        for e in unidades:
            if volumen_unidad == e:
                volumen = float(volumen)*unidades[e]
                volumen_unidad = 'ml'
                break
        return float(volumen), volumen_unidad

def aGalones(volumen,volumen_unidad):
    unidades = {'L':0.264172052,'cm3':0.000264172052,'m3':264.172052,'ft3':7.48052,'ml':0.000264172052,'m³':264.172052}
    if type(volumen) is list: 
        if type(volumen[0]) is not list:
            for e in unidades:
                if volumen_unidad == e:
                    for i,v in enumerate(volumen):
                        volumen[i] = volumen[i]*unidades[e]
                    volumen_unidad = 'gal'       
            return volumen, volumen_unidad
        elif type(volumen[0]) is list:
            resultado = []
            for l in volumen: 
                if type(l) is list:
                    for e in unidades:
                        if volumen_unidad == e: 
                            for i,v in enumerate(l):
                                l[i] = l[i]*unidades[e] 
                    resultado.append(l)         
            volumen_unidad = 'gal'
            return resultado, volumen_unidad
    elif type(volumen) is not list:
        for e in unidades:
            if volumen_unidad == e:
                volumen = float(volumen)*unidades[e]
                volumen_unidad = 'gal'
                break
        return float(volumen), volumen_unidad



def aUnidad(valor,valor_unidad, unidad):
    if unidad == "L": return aLitros(valor,valor_unidad)
    elif unidad == "ml": return aMiliLitros(valor, valor_unidad)
    elif unidad == "gal": return aGalones(valor, valor_unidad)

def aMetros(longitud,longitud_unidad):
    unidades = {'km':1000,'cm':0.01,'mm':0.001,'μm':0.000001,'pie':0.3048,'in': 0.0254,'yd':0.9144,'mi':1609.34}
    if type(longitud) is list: 
        if type(longitud[0]) is not list:
            for e in unidades:
                if longitud_unidad == e:
                    for i,v in enumerate(longitud):
                        longitud[i] = float(longitud[i])*unidades[e]
                    longitud_unidad = 'm'       
            return longitud, longitud_unidad
        elif type(longitud[0]) is list:
            resultado = []
            for l in longitud:
                if type(l) is list:
                    for e in unidades:
                        if longitud_unidad == e:
                            for i,v in enumerate(l):
                                l[i] = float(l[i])*unidades[e] 
                    resultado.append(l)         
            longitud_unidad = 'm'
            return resultado, longitud_unidad
    elif type(longitud) is not list:
        for e in unidades:
            if longitud_unidad == e:
                longitud = float(longitud)*unidades[e]
                longitud_unidad = 'm'
                break
        return longitud, longitud_unidad


def raiz(n):
    return math.sqrt(n)

def promediar(lista):
    if isinstance(lista, list):
        if isinstance(lista[0],list):
            for i,e in enumerate(lista):
                lista[i] = promediar(e)
            return lista
        else:
            return sum(lista)/len(lista)
    else:
        return lista
def func_exponencial(x, a, b, c):
    return a * np.exp(-b * x) + c




def ajuste_v_eff(x):
    v_eff_values = np.array([1, 2, 3, 4, 5, 6, 7, 8, 10, 20, 50, 200])
    k_values = np.array([13.97, 4.53, 3.31, 2.87, 2.65, 2.52, 2.43, 2.37, 2.28, 2.13, 2.05, 2.00])
    params, covariance = curve_fit(func_exponencial, v_eff_values, k_values, p0=(2, 0.01, 2))
    a, b, c = params
    x_valor = x
    y_valor = func_exponencial(x_valor, a, b, c)

    return y_valor


def aplicar_condicion(valor, nombre):
    if isinstance(valor, str):
        if valor.strip() == "":
            print("Debe ingresar un valor :[")
            return aplicar_condicion(input(f"{nombre}"),nombre)
        else:
            return valor
    else:
        return valor



class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()  # Convierte el objeto date a una cadena ISO 8601
        return super().default(obj)
    
def guardar_datos(nombre_archivo, diccionario):
    with open(f'{nombre_archivo}.json', 'w', encoding='utf-8') as json_file:
        json.dump(diccionario, json_file, ensure_ascii=False, indent=4, cls=DateEncoder)
    

def agregar_datos(nombre, clave, valor):
    data = {}
    if os.path.exists(f"{nombre}.json"):
        with open(f'{nombre}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    data[clave] = valor
    with open(f'{nombre}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4, cls=DateEncoder)



def agregar_datos2(nombre, clave, valor):
    data = {}
    if os.path.exists(f"{nombre}.json"):
        with open(f'{nombre}.json', 'r') as file:
            data = json.load(file)
    data[clave] = valor
    with open(f'{nombre}.json', 'w') as file:
        json.dump(data, file, indent=4)  # Utilizamos indent para mantener la estructura del JSON legible

def aGal(litros):
    return litros*0.2641720523581484

def condiciones_previas():
    print("\n-------------- Condiciones previas ---------------")
    print("-La variación máxima de la temperatura del agua este dentro de 20 ± 1°C (laboratorio).")
    print("-La variación máxima de la temperatura del agua este dentro de 20 ± 2°C (campo).")
    print("-La variación máxima de la temperatura del aire este dentro de 20 ± 3°C.")
    print("-Los recipientes deben almacenarse en el área de calibración durante al menos\n6 horas antes de la calibración.")
    print("-Se debe evitar la exposición a la radiación solar directa, viento y lluvia.")
    print("-Los equipos para medir condiciones ambientales, deberán estar en el área\nde calibración y encenderse al menos 1 hora antes.")
    print("-El calibrando debe ser limpiado por el cliente o por el laboratorio.")
    print("-La inspección y limpieza del calibrando debe realizarse antes de la calibración.")
    print("-Se debe comprobar la legibilidad y seguridad de la escala, el mecanismo de \nnivelación y los sellos pertinentes.")
    print("-Se debe anotar la existencia de golpes, fugas en los tubos o daños.")
    print("-Se recomienda realizar una verificación de fugas.")
    print("-Se debe garantizar que los líquidos se entreguen fácilmente hacia y desde el \nestándar y que no haya bolsas, abolladuras o grietas capaces de atrapar el líquido, aire o vapor.")
    print("-El calibrando se nivelará antes de que comience su calibración.")
    print("-El recipiente patrón debe calibrarse con una incertidumbre al menos 3 veces menor\nque la incertidumbre del calibrando.")

def aParrafo(texto,alineacion,text_color=colors.black):
    if alineacion == "justificado": alignment = 4
    elif alineacion == "izquierda": alignment = 0
    elif alineacion == "derecha": alignment = 2
    elif alineacion == "centrado": alignment = 1 
    # Crear un estilo de párrafo para la celda
    paragraph_style = ParagraphStyle(
        name='CellParagraphStyle',
        fontSize=8,
        leading=10,  # Espaciado entre líneas
        alignment=alignment,  # 0 para alineación izquierda, 1 para centrado, 2 para justificado, 3 para alineación derecha
        textColor=text_color
    )
    return Paragraph(texto, paragraph_style)
def aTexto(lista_palabras):
    return " ".join(lista_palabras).replace(" . ", ". ")

def separar_parrafo(nro_letras, parrafo):
    lista_palabras = word_tokenize(parrafo)
    filas = [[]]
    c = 0
    fila_actual = 0

    for palabra in lista_palabras:
        longitud_palabra = len(palabra)
        if c + longitud_palabra <= nro_letras:
            filas[fila_actual].append(palabra)
            c += longitud_palabra + 1  # Añadimos 1 para contar el espacio entre palabras
        else:
            fila_actual += 1
            filas.append([palabra])
            c = longitud_palabra + 1

    return [aTexto(fila) for fila in filas]



def extraer_datos(nombre, clave):
    if os.path.exists(f"{nombre}.json"):
        with open(f'{nombre}.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get(clave, None)    
    else:
        return False
    
print(extraer_datos("informacion", "t_unidad"))    

def puntoAComa(num):
    return str(num).replace(".",",")


def dicc_to_list(info):
    lista = []
    for i,e in enumerate(info):
        lista.append([list(info.keys())[i], ': '+list(info.values())[i]])
    return lista



def generar_certificado(ruta_certificado, nro_certificado, parrafos, ruta_fondo,titulo_firmaysello,ruta_firma,ruta_sello,nombre, cargo,
                        nro_paginas,nro_revision,titulo, nombre_laboratorio, cotizacion, solicitante, direccion, 
                        nombre_instrumento,informacion_instrumento, nombre_fecha_lugar,fecha_emi, fecha_cal, lugar_cal,nombre_metodo_cal,
                        t_inicial, t_final, h_inicial, h_final, p_inicial, p_final, trazabilidad, lista_resultados,
                        ajuste, vn, vn_unidad, vo_aa, vo_aa_unidad, U_aa, U_aa_unidad,
                        vo_da, vo_da_unidad, U_da, U_da_unidad, lista_obs, k, nro_decimales):

    
    c = Certificado(f"{ruta_certificado}.pdf", f"{ruta_fondo}", f"{ruta_firma}", f"{ruta_sello}", int(nro_paginas), f"{nro_revision}")

    #####################################   1er hoja   #####################################
    # titulo
    y_fijado = 720
    c.agregarTexto(f"{titulo}",186,y_fijado,font_size=14)

    # laboratorio
    y_fijado = y_fijado - 70
    c.agregarTexto(nombre_laboratorio,51,y_fijado,font_size=10)

    # nro de certificado
    datos = [['N° DE CERTIFICADO'],
             [f"{nro_certificado}"],
             ['']]
    c.crearTablaPersonalizada(False,datos,ancho_celda=[156],x=390,y=y_fijado,alto_celda=10, con_grilla=True,
                                        span=[((0,1),(0,2))],
                                        font_size=[{'12':((0,1),(0,2))}],
                                        font_name=[{'Helvetica-Bold':((0,1),(0,2))}],
                                        valign=[{'MIDDLE':((0,0),(-1,-1))}],
                                        align=[{'CENTER':((0,0),(-1,-1))}],
                                        background_color=[{'#1A50B2':((0,0),(0,0))}],
                                        text_color=[{'#ffffff':((0,0),(0,0))}])

    # linea
    y_fijado = y_fijado - 224
    c.agregarLineaHorizontal(51,640,496,1,colors.black)

    # informacion
    datos = [
             ]
    # ingresando la informacion
    tamano_alto = []
    x = np.array([150, 200, 241, 266])   # 60, 60, 56, 64, 90  alto de celda 
    y = np.array([56,60,64,90])  #164, 200, 150, 241, 266 tamaños de parrafos
    m, b = np.polyfit(x,y,1)
    for e in parrafos:
        tamano_alto.append(len(e)*m+  b)
        datos.append([aParrafo(e,'justificado')])
    c.crearTablaPersonalizada(False,datos,ancho_celda=[170],x=383,y=sum(tamano_alto)*-0.92+600.405,alto_celda=tamano_alto,con_grilla=False)
    
    # Cotizacion , solicitante y direccion
    datos2 = []
    cotizacion =[f"{cotizacion}"," "]
    comienzo = ['Cotización',':']
    for e in cotizacion:
        datos2.append([comienzo[0],f'{comienzo[1]} {e.upper()}'])
        comienzo = ['',' ']

    solicitante = f"{solicitante}"
    solicitante = separar_parrafo(45,solicitante)
    if len(solicitante) == 1: solicitante.append(" ")
    comienzo = ['Solicitante',':']
    for e in solicitante:
        datos2.append([comienzo[0],f'{comienzo[1]} {e.upper()}'])
        comienzo = ['',' ']

    direccion = f"{direccion}"
    direccion = separar_parrafo(45, direccion)
    if len(direccion) == 1: direccion.append(" ")
    comienzo = ['Dirección',':']
    for e in direccion:
        datos2.append([comienzo[0],f'{comienzo[1]} {e.upper()}'])
        comienzo = ['',' ']

    if len(datos2) == 6: y_fijado =  564
    elif len(datos2) == 7: y_fijado = 554
    elif len(datos2) == 8: y_fijado = 544


    c.crearTablaPersonalizada(False,datos2,ancho_celda=[55,230],x=45,y=y_fijado,alto_celda=10,con_grilla=False,
                                        font_name=[{'Helvetica-Bold':((0,2),(1,len(solicitante)+1))}],
                                        font_size=[{'8':((0,2),(1,2))}])


    datos = [
             ['INSTRUMENTO DE MEDICIÓN',f': {nombre_instrumento}']  
             ]
   
    for e in informacion_instrumento:
        datos.append(e)

    y_fijado = y_fijado - 10-len(datos)*11
    c.crearTablaPersonalizada(False,datos,ancho_celda=[120,185],x=45,y=y_fijado,alto_celda=11,con_grilla=False,
                                        font_name=[{'Helvetica-Bold':((0,0),(1,0))}])
    


    # Cotizacion , solicitante y direccion
    datos3 = []

    datos3.append([nombre_fecha_lugar,''])
    datos3.append(['Fecha de emisión',f': {fecha_emi}'])
    datos3.append(['Fecha de calibración',f': {fecha_cal}'])
    lugar_cal = lugar_cal
    lugar_cal = separar_parrafo(45, lugar_cal)
    comienzo = ['Lugar de calibración',':']
    for e in lugar_cal:
        datos3.append([comienzo[0],f'{comienzo[1]} {e}'])
        comienzo = ['',' ']

    y_fijado = y_fijado - 70
    c.crearTablaPersonalizada(False,datos3,ancho_celda=[120,120],x=45,y=y_fijado,alto_celda=10,con_grilla=False,
                                        span=[((0,0),(1,0))],
                                        font_name=[{'Helvetica-Bold':((0,0),(1,0))},{'Helvetica-Bold':((1,3),(1,5))}])


    # método de calibración
    datos = [
        ['MÉTODO DE CALIBRACIÓN'],
        [aParrafo(nombre_metodo_cal,'justificado')],
    ]
    y_fijado = y_fijado - 60
    c.crearTablaPersonalizada(False,datos,ancho_celda=[300],x=45,y=y_fijado,alto_celda=[13,37],
                                            align=[{'LEFT':((0,0),(-1,1))}],
                                            valign=[{'MIDDLE':((0,0),(-1,1))}],
                                            font_name=[{'Helvetica-Bold':((0,0),(0,0))},{'Helvetica-Bold':((0,-3),(0,-3))}])

    if y_fijado < 270: 
        y_fijado = y_fijado - 20
    else: y_fijado = 250
    
    # linea
    c.agregarLineaHorizontal(50,y_fijado,496,1,colors.black)

    # autorizado por
    y_fijado = y_fijado - 20
    c.agregarTexto(f"{titulo_firmaysello}",50,y_fijado,font_size=8)

    # firma
    c.agregarImagen(f'{ruta_firma}', 405-10, 150, width=90, height=48.6)
    # sello
    c.agregarImagen(f'{ruta_sello}', 340-10, 150, width=50, height=50)

    # linea
    c.agregarLineaHorizontal(250+150-10,151,120,1,colors.black)
    # nombre del revisor
    c.agregarTexto(f"{nombre}",261+150-10,142,font_size=6)
    # cargo
    c.agregarTexto(f"{cargo}",276+150-10,135,font_size=6)


    #####################################   2da hoja   #####################################
    c.agregarHoja()
    y_fijado = 735
    c.agregarPaginacionCertificado(f"{nro_certificado}", 470, y_fijado)

    # Condiciones ambientales
    y_fijado = y_fijado - 10
    c.agregarTexto("CONDICIONES AMBIENTALES",50,y_fijado,font_size=8)

    datos = [
        ['MAGNITUD','INICIAL','FINAL'],
        ['Temperatura',f'{t_inicial}' , f'{t_final}'],
        ['Humedad Relativa',f'{h_inicial}',f'{h_final}'],
        ['Presión Atmosférica',f'{p_inicial}',f'{p_final}'],
    ]
    y_fijado = y_fijado - 60
    c.crearTablaPersonalizada(False,datos, ancho_celda=[120,60,60], alto_celda=13,x="CENTER", y= y_fijado, con_grilla=True,
                            align=[{'CENTER':((0,0),(-1,-1))}],
                            valign=[{'MIDDLE':((0,0),(-1,-1))}],
                            background_color=[{'#1A50B2':((0,0),(-1,0))}],
                            text_color=[{'#ffffff':((0,0),(-1,0))}])

    # Trazabilidad
    y_fijado = y_fijado - 17
    c.agregarTexto("TRAZABILIDAD",50,y_fijado,font_size=8)

    datos = trazabilidad
    
    tamano_texto_trazabilidad = []
    lista_fila = []
    lista_total = []
    # determinar la cantidad de elementos de la primera fila de trazabilidad
    nro_columnas = len(trazabilidad[0])
    nro_filas = len(trazabilidad)-1
    lista = []
    lista_total = []
    for i in range(nro_filas):
        for j in range(nro_columnas):
            lista.append(len(trazabilidad[i+1][j].text))
        lista_total.append(max(lista))
        lista = []
    alto_celda = altoCelda(lista_total)

    y_fijado = y_fijado-sum(alto_celda)-25

    c.crearTablaPersonalizada(False,datos, ancho_celda=[120,150,140], 
                            alto_celda=[13]+alto_celda,
                            x="CENTER", y= y_fijado, con_grilla=True,
                            align=[{'CENTER':((0,0),(-1,-1))}],
                            valign=[{'MIDDLE':((0,0),(-1,-1))}],
                            background_color=[{'#1A50B2':((0,0),(-1,0))}],
                            text_color=[{'#ffffff':((0,0),(-1,0))}])
    
    # resultados
    y_fijado = y_fijado-26
    c.agregarTexto("RESULTADOS DE MEDICIÓN",50,y_fijado,font_size=8)

    datos = []
    # agregando los resultados
    for e in lista_resultados:
        datos.append([f'{e}'])
    
    if ajuste == "SI":
        datos.pop()

    y_fijado = y_fijado-len(datos)*13-13

    c.crearTablaPersonalizada(False,datos,[100],x=50,y=y_fijado,alto_celda=13,
                                            align=[{'LEFT':((0,0),(-1,1))}],
                                            valign=[{'MIDDLE':((0,0),(-1,1))}])

    datos = [
        [f'VOLUMEN NOMINAL ({vn_unidad})',f'VOLUMEN OBTENIDO ({vo_aa_unidad})',f'CORRECCIÓN ({vn_unidad})',f'INCERTIDUMBRE ({U_aa_unidad})'],
        [f'{strRoundFloatPC(vn,nro_decimales)}',f'{strRoundFloatPC(vo_aa,nro_decimales)}',f'{strRoundFloatPC(float(vn)-float(vo_aa),nro_decimales)}',f'{strRoundFloatPC(U_aa,nro_decimales)}']
    ]
    y_fijado = y_fijado-len(datos)*13-13

    c.crearTablaPersonalizada(False,datos,[120,120,100,100],x="CENTER",y=y_fijado,alto_celda=13,
                                            align=[{'CENTER':((0,0),(-1,1))}],
                                            valign=[{'MIDDLE':((0,0),(-1,1))}],
                                            background_color=[{'#1A50B2':((0,0),(-1,0))}],
                                            text_color=[{'#ffffff':((0,0),(-1,0))}],
                                            con_grilla=[(0,0),(-1,1)])
    
    if ajuste == "NO":
        if extraer_datos("informacion","valor_nominal_unidad") == "gal":
            datos = [
                    [f'VOLUMEN NOMINAL (gal)',f'VOLUMEN OBTENIDO (gal)',f'CORRECCIÓN (gal)',f'INCERTIDUMBRE (gal)'],
                    [f'{strRoundFloatPC(aGal(vn),nro_decimales)}',f'{strRoundFloatPC(aGal(vo_aa),nro_decimales)}',f'{strRoundFloatPC(aGal(vn-vo_aa),nro_decimales)}',f'{strRoundFloatPC(aGal(U_aa),nro_decimales)}']
                ]
            y_fijado = y_fijado-len(datos)*13-13

            c.crearTablaPersonalizada(False,datos,[120,120,100,100],x="CENTER",y=y_fijado,alto_celda=13,
                                                    align=[{'CENTER':((0,0),(-1,1))}],
                                                    valign=[{'MIDDLE':((0,0),(-1,1))}],
                                                    background_color=[{'#1A50B2':((0,0),(-1,0))}],
                                                    text_color=[{'#ffffff':((0,0),(-1,0))}],
                                                    con_grilla=[(0,0),(-1,1)])
    

    if ajuste == "SI":
        datos = [
        ]
        datos.append([lista_resultados[-1]])
        y_fijado = y_fijado-len(datos)*13-13

        c.crearTablaPersonalizada(False,datos,[100],x=50,y=y_fijado,alto_celda=13,
                                                align=[{'LEFT':((0,0),(-1,1))}],
                                                valign=[{'MIDDLE':((0,0),(-1,1))}])

        datos = [
            [f'VOLUMEN NOMINAL ({vn_unidad})',f'VOLUMEN OBTENIDO ({vo_da_unidad})',f'CORRECCIÓN ({vn_unidad})',f'INCERTIDUMBRE ({U_da_unidad})'],
            [f'{strRoundFloatPC(vn,nro_decimales)}',f'{strRoundFloatPC(vo_da,nro_decimales)}',f'{strRoundFloatPC(float(vn)-float(vo_da),nro_decimales)}',f'{strRoundFloatPC(U_da,nro_decimales)}']
        ]
        y_fijado = y_fijado-len(datos)*13-13

        c.crearTablaPersonalizada(False,datos,[120,120,100,100],x="CENTER",y=y_fijado,alto_celda=13,
                                                align=[{'CENTER':((0,0),(-1,1))}],
                                                valign=[{'MIDDLE':((0,0),(-1,1))}],
                                                background_color=[{'#1A50B2':((0,0),(-1,0))}],
                                                text_color=[{'#ffffff':((0,0),(-1,0))}],
                                                con_grilla=[(0,0),(-1,1)])

        if extraer_datos("informacion","valor_nominal_unidad") == "gal":
            datos = [
                [f'VOLUMEN NOMINAL (gal)',f'VOLUMEN OBTENIDO (gal)',f'CORRECCIÓN (gal)',f'INCERTIDUMBRE (gal)'],
                [f'{strRoundFloatPC(aGal(vn),nro_decimales)}',f'{strRoundFloatPC(aGal(vo_da),nro_decimales)}',f'{strRoundFloatPC(aGal(vn-vo_da),nro_decimales)}',f'{strRoundFloatPC(aGal(U_da),nro_decimales)}']
            ]
            y_fijado = y_fijado-len(datos)*13-13

            c.crearTablaPersonalizada(False,datos,[120,120,100,100],x="CENTER",y=y_fijado,alto_celda=13,
                                                align=[{'CENTER':((0,0),(-1,1))}],
                                                valign=[{'MIDDLE':((0,0),(-1,1))}],
                                                background_color=[{'#1A50B2':((0,0),(-1,0))}],
                                                text_color=[{'#ffffff':((0,0),(-1,0))}],
                                                con_grilla=[(0,0),(-1,1)])

    if extraer_datos("informacion","valor_nominal_unidad") == "gal":
        y_fijado = y_fijado - 15
        c.agregarTexto("1 galón = 3,785412 L",56,y_fijado,font_size=8, bold=False)
    
    datos = [
        ['OBSERVACIONES'],
        [''],
        ['INCERTIDUMBRE'],
        [f'La incertidumbre expandida reportada es la incertidumbre combinada multiplicada por el factor de cobertura (k = {k}) de modo que la'],
        ['probabilidad de cobertura corresponde aproximadamente a un nivel de confianza del 95 %.'],
    ]
    # agregando las observaciones
    for e in lista_obs:
        datos.insert(1,[aParrafo(e,'izquierda')])


    y_fijado = y_fijado-len(datos)*13-13

    c.crearTablaPersonalizada(False,datos,[500],x=45,y=y_fijado,alto_celda=13,
                                            align=[{'LEFT':((0,0),(-1,1))}],
                                            valign=[{'MIDDLE':((0,0),(-1,1))}],
                                            font_name=[{'Helvetica-Bold':((0,0),(0,0))},{'Helvetica-Bold':((0,-3),(0,-3))}])
    
    y_fijado = y_fijado-13
    c.agregarLineaHorizontal(50,y_fijado,496,1,colors.black)
    y_fijado = y_fijado-13
    c.agregarTexto("** FIN DEL DOCUMENTO **",250,y_fijado,font_size=9, bold=True)

    c.guardar()


def strRoundFloatPC(text,nro_decimales):
    if float(str(text).replace(",",".")) == -0.0: 
        result = "{:.{}f}".format(0.0, nro_decimales).replace(".",",")
    else:
        result = "{:.{}f}".format(float(text), nro_decimales).replace(".",",")
    return result





def convert_to_tuple_list(marcas):
    # Verificar si marcas es una lista de tuplas
    if isinstance(marcas, list) and all(isinstance(item, tuple) and len(item) == 2 for item in marcas):
        # Convertir la lista de tuplas a una tupla de tuplas
        marcas = tuple(marcas)
        return marcas
    else:
        raise ValueError("Input 'marcas' should be a list of tuples with length 2.")
    
def TrueFalse_To_10(var):
    if type(var) is list:
        for i,e in enumerate(var):
            if e == True: var[i]=1
            elif e== False: var[i]=0
        return var 
    if type(var) is not list:
        if var == True: var = 1
        elif var == False or var == None: var = 0
        return var
    

def altoCelda(lista):
    # Datos proporcionados para el ajuste, incluyendo el punto (35, 26)
    x = np.array([59, 43, 35, 43, 25])
    y = np.array([32, 20, 20, 20, 20])
    
    # Ajuste de la regresión lineal
    m, b = np.polyfit(x, y, 1)
    
    # Umbral para valores grandes
    limite = 100  # Puedes ajustar este valor según sea necesario
    
    # Calcular y devolver los valores ajustados
    result = []
    for e in lista:
        if e > limite:
            result.append(int(round((e * m + b)-25)))  # Ajuste para valores grandes
        else:
            result.append(int(round(e * m + b)))
    return result


def limpiarJsons():
    directorio_actual = os.getcwd()
    archivos_a_eliminar = ["informacion.json", "pre.json", 
                           "presupuesto_antes_ajuste.json", "presupuesto.json",
                            "resultados_antes_ajuste.json", "resultados.json",
                            "calibracion_antes_ajuste.json","calibracion.json",
                            "todo.json"
                           ]

    for archivo in archivos_a_eliminar:
        try:
            if archivo in os.listdir(directorio_actual):
                ruta_completa = os.path.join(directorio_actual, archivo)
                os.remove(ruta_completa)
            else:
                pass
        except:
            pass


def combinar_archivos(origenes, destino):
    data_combined = {}
    for origen in origenes:
        try:
            with open(f'{origen}.json', 'r') as file:
                data = json.load(file)
            data_combined.update(data)
        except FileNotFoundError:
            print(f"Archivo {origen}.json no encontrado, omitiendo...")
        except json.JSONDecodeError:
            print(f"Error al decodificar {origen}.json, omitiendo...")
        except Exception as e:
            print(f"Error inesperado con {origen}.json: {e}, omitiendo...")

    with open(f'data/{destino}.json', 'w') as file:
        json.dump(data_combined, file, indent=4)

def printLista(lista):
    for e in lista:
        print(e)

def toFloat(element):
    if isinstance(element, list):
        for i, e in enumerate(element):
            if isinstance(e, list):
                element[i] = toFloat(e)
            else:
                element[i] = float(e.replace(',', '.'))
        return element
    else:
        return float(element.replace(',', '.'))

def modificar_data(nro_certificado, clave_titular, nuevas_claves_valores):
    def actualizar_informacion(clave_titular, json_data, nuevas_claves_valores):
        # Verificamos si la clave "informacion" existe en el JSON
        if clave_titular in json_data:
            # Actualizamos las claves y valores en "informacion"
            for clave, valor in nuevas_claves_valores.items():
                if clave in json_data[clave_titular]:
                    json_data[clave_titular][clave] = valor
                else:
                    print(f"La clave '{clave}' no existe en '{clave_titular}' y no se ha añadido.")
        else:
            print(f"La clave '{clave_titular}' no existe en el JSON proporcionado.")
        return json_data

    def leer_json(nombre_archivo):
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)

    def escribir_json(nombre_archivo, datos):
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)


    nombre_archivo = f'data/{nro_certificado}.json' 
    json_data = leer_json(nombre_archivo)
    json_actualizado = actualizar_informacion(clave_titular, json_data, nuevas_claves_valores)
    escribir_json(nombre_archivo, json_actualizado)

def colocamosLetra(nro_certificado,letra):
    c = 0
    for i in range(len(nro_certificado)):
        if nro_certificado[i] == "-":
            c += 1
            if c == 2:
                return nro_certificado[:i]+letra+nro_certificado[i:]




def copiar_json(archivo_origen, archivo_destino):
    try:
        shutil.copyfile(archivo_origen, archivo_destino)
        print(f"Copia de {archivo_origen} creada exitosamente como {archivo_destino}")
    except IOError as e:
        print(f"No se pudo copiar el archivo: {e}")


def obtenerPosicion(texto,caracter):
    caracter = caracter
    c = 0
    lista = []
    for i in range(len(texto)):
        if texto[i] == caracter:
            c += 1
            lista.append(i)

    return lista

def ajustePolinomial(x,y,valor,grado):
    coef = np.polyfit(x,y,grado)
    y_fit = 0
    for i in range(grado+1):
        y_fit += coef[i]*valor**(grado-i)
    return y_fit