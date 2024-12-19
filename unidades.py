from funciones import *

temperatura = [('0','°C')]
volumen = [('0','L'),('1','gal')]
volumen_aux = [('0','L'),('1','ml')]
longitud = [('mm','mm'),('cm','cm'),('in','in')]
tiempo = [('0','s')]
humedad = [('0','%')]
presion = [('0','hPa')]
ajuste_opciones = [('No seleccionado','-- Seleccionar --'),('SI','SI'),('NO','NO')]
valvula_drenaje_opciones = [('No seleccionado','-- Seleccionar --'),('SI','SI'),('NO','NO')]

clases = [('NO INDICA','NO INDICA'),('0.1','0,1 %'),('0.2','0,2 %'),('0.5','0,5 %')]

marcas = [('-1',"NO INDICA"),('0','Otra marca'),('1','Full Tanque'),('2','Amazing Combustible & Gas')]
marcas = convert_to_tuple_list(marcas)

metodos = [('0',"Guía de calibración EURAMET No.21 v2.1")]
metodos = convert_to_tuple_list(metodos)

lugares_calibraciones = [('0', 'Laboratorio de Volumen de Metrindust S.A.C. - SEDE LOS JAZMINES')]
lugares_calibraciones = convert_to_tuple_list(lugares_calibraciones)

procedencias = [('0','Perú'),('1','Estados Unidos'),('2','NO INDICA')]
procedencias = convert_to_tuple_list(procedencias)

colores = [('-1',"NO INDICA"),('0','Otro color'),('1','Azul'),('2','Morado'),('3','Verde'),('4','Plateado'),('5','Amarillo'),('6','Rojo'),('7','Celeste')]
colores = convert_to_tuple_list(colores)

realizados_por = [('0','Metrologo')]
realizados_por = convert_to_tuple_list(realizados_por)

supervisados_por = [('0','Dennis Gamarra Rodríguez')]
supervisados_por = convert_to_tuple_list(supervisados_por)

metodos_volumetricos = [('llenado','Llenado')]
metodos_volumetricos = convert_to_tuple_list(metodos_volumetricos)

def numeroALetraTemperatura(num):
    return dict(temperatura)[num]
def numeroALetraVolumen(num):
    return dict(volumen)[num]
def numeroALetraVolumenAux(num):
    return dict(volumen_aux)[num]
def numeroALetraLongitud(num):
    return dict(longitud)[num]
def numeroALetraTiempo(num):
    return dict(tiempo)[num]
def numeroALetraHumedad(num):
    return dict(humedad)[num]

def numeroALetraPresion(num):
    return dict(presion)[num]
def numeroALetraMarca(num):
    return dict(marcas)[num]
def numeroALetraMetodo(num):
    return dict(metodos)[num]
def numeroALetraLugares_Calibracion(num):
    return dict(lugares_calibraciones)[num]
def numeroALetraProcedencia(num):
    return dict(procedencias)[num]
def numeroALetraColor(num):
    return dict(colores)[num]
def numeroALetraRealizado_por(num):
    return dict(realizados_por)[num]
def numeroALetraSupervisado_por(num):
    return dict(supervisados_por)[num]
def numeroALetraMetodo_volumetrico(num):
    return dict(metodos_volumetricos)[num]

intervalos_indicaciones_unidades = [('lineas','líneas'),('L','L'),('ml','ml'),('gal','gal')]
res_unidades = [('lineas','líneas'),('L','L'),('ml','ml'),('gal','gal')]
materiales = [
                ('acero inoxidable grado 304','Acero inoxidable grado 304'),
                ('fibra de carbon','Fibra de carbon'),
                ('vidrio de borosilicato 3,3','Vidrio de borosilicato 3,3'),
                ('vidrio de borosilicato 5,0','Vidrio de borosilicato 5,0'),
                ('vidrio de cal sodada','Vidrio de cal sodada'),
                ('acero','Acero'),
                ('carbono suave','Carbono suave'),
                ('acero inoxidable grado 316','Acero inoxidable grado 316'),
                ('acero inoxidable 17-4 PH','Acero inoxidable 17-4 PH'),
                ('cobre - aleacion de zinc (latón)','Cobre - Aleacion de zinc (latón)'),
                ('aluminio','Aluminio')
            ]
from datos import * 


lista_claves_patrones = list(datos.keys())
recipientes_patrones = []
recipientes_auxiliares = []
for e in lista_claves_patrones:
    if "MVA" in e:
        recipientes_auxiliares.append((e,datos[e]['descripcion']))
    elif "MVP" in e:
        recipientes_patrones.append((e,datos[e]['descripcion']))
    else:
        pass
        
liquidos_calibraciones = [('agua','agua')]
termometrosRS = [('TP001',datos['TP001']['descripcion'])]
termometrosSCM = [('TP002',datos['TP002']['descripcion'])]
barotermohigrometros = [('BTHP001',datos['Termometro001']['descripcion']+" "+\
                         datos['Higrometro001']['descripcion']+" "+datos['Barometro001']['descripcion'])]

