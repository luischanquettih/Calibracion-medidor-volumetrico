from datos import * 
from clases import *
from funciones import * 


def generar_certificado_modificado(nro_certificado,comentario,nro_decimales):

    ajuste = extraer_datos(f'data/{nro_certificado}','informacion')['realizar_ajuste']
    t_ref_cal = "20 °C"
    valvula_drenaje = extraer_datos(f'data/{nro_certificado}','informacion')['valvula_drenaje']

    # 1era hoja
    titulo = "CERTIFICADO DE CALIBRACIÓN"
    nombre_laboratorio = "Laboratorio de Grandes Volúmenes y Flujo"

    cotizacion = extraer_datos(f'data/{nro_certificado}','informacion')['cotizacion']
    solicitante = extraer_datos(f'data/{nro_certificado}','informacion')['solicitante']
    direccion = extraer_datos(f'data/{nro_certificado}','informacion')['direccion']

    nombre_instrumento = "MEDIDOR VOLUMÉTRICO METÁLICO"

    marca = extraer_datos(f'data/{nro_certificado}','informacion')['marca']
    modelo = extraer_datos(f'data/{nro_certificado}','informacion')['modelo']
    nro_serie = extraer_datos(f'data/{nro_certificado}','informacion')['nro_serie']
    procedencia = extraer_datos(f'data/{nro_certificado}','informacion')['procedencia']
    cod_id = extraer_datos(f'data/{nro_certificado}','informacion')['cod_id']
    color = extraer_datos(f'data/{nro_certificado}','informacion')['color'].capitalize()
   
    valor_nominal = extraer_datos(f'data/{nro_certificado}','informacion')['valor_nominal']+" "+extraer_datos(f'data/{nro_certificado}','informacion')['valor_nominal_unidad']
    interv_ind = "± "+extraer_datos(f'data/{nro_certificado}','informacion')['interv_ind']
    clase = extraer_datos(f'data/{nro_certificado}','informacion')['clase']
    res = extraer_datos(f'data/{nro_certificado}','informacion')['res']+" "+extraer_datos(f'data/{nro_certificado}','informacion')['res_unidad']
    tipo = extraer_datos(f'data/{nro_certificado}','informacion')['tipo_SCM']

    material = extraer_datos(f'data/{nro_certificado}','informacion')['material_SCM']
    c_material = coef_material[material]

    nombre_fecha_lugar = "FECHA Y LUGAR DE CALIBRACIÓN"
    fecha_cal = extraer_datos(f'data/{nro_certificado}','informacion')['fecha_cal']
    fecha_emi = extraer_datos(f'data/{nro_certificado}','informacion')['fecha_emi']
    lugar_cal = "Laboratorio de Volumen de Metrindust S.A.C. - SEDE LOS JAZMINES"
    #nombre_metodo_cal = """La calibración se realizó por comparación directa, según la EURAMET Calibration Guide No. 21 'Guidelines on the 
    #Calibration of Standard Capacity Measures Using the Volumetric Method'. Tercera Edición - Febrero 2024. EURAMET. """
    nombre_metodo_cal = "La calibración se realizó por comparación directa, según la EURAMET Calibration Guide No. 21 'Guidelines on the Calibration of Standard Capacity Measures Using the Volumetric Method'. Tercera Edición - Febrero 2024. EURAMET."
   

    if ajuste == "SI":
        vn = extraer_datos(f'data/{nro_certificado}','resultados_antes_ajuste')['VN_SCM']
        vn_unidad = extraer_datos(f'data/{nro_certificado}','resultados_antes_ajuste')['VN_SCM_unidad']
        vo_aa = extraer_datos(f'data/{nro_certificado}','resultados_antes_ajuste')['Vt']
        vo_aa_unidad = extraer_datos(f'data/{nro_certificado}','resultados_antes_ajuste')['Vt_unidad']
        U_aa = extraer_datos(f'data/{nro_certificado}','resultados_antes_ajuste')['U_Vt']
        U_aa_unidad = extraer_datos(f'data/{nro_certificado}','resultados_antes_ajuste')['U_Vt_unidad']

        vo_da = extraer_datos(f'data/{nro_certificado}','resultados')['Vt']
        vo_da_unidad = extraer_datos(f'data/{nro_certificado}','resultados')['Vt_unidad']
        U_da = extraer_datos(f'data/{nro_certificado}','resultados')['U_Vt']
        U_da_unidad = extraer_datos(f'data/{nro_certificado}','resultados')['U_Vt_unidad']

    else:
        vn = extraer_datos(f'data/{nro_certificado}','resultados')['VN_SCM']
        vn_unidad = extraer_datos(f'data/{nro_certificado}','resultados')['VN_SCM_unidad']
        vo_aa = extraer_datos(f'data/{nro_certificado}','resultados')['Vt']
        vo_aa_unidad = extraer_datos(f'data/{nro_certificado}','resultados')['Vt_unidad']
        U_aa = extraer_datos(f'data/{nro_certificado}','resultados')['U_Vt']
        U_aa_unidad = extraer_datos(f'data/{nro_certificado}','resultados')['U_Vt_unidad']

        vo_da = 0
        vo_da_unidad = 0
        U_da = 0
        U_da_unidad = 0

        #U_porcentaje_aa = 0.12
        #U_porcentaje_aa_unidad = "L"

    k = extraer_datos(f'data/{nro_certificado}','resultados')['k']

    parrafos = [
    """
    METRINDUST S.A.C. Departamento de Metrología realiza calibraciones y certificaciones en metrología según procedimientos de calibración validados o normalizados.
    """,
    """
    Este certificado de calibración documenta la trazabilidad a los patrones nacionales o internacionales, que realizan las unidades de medida de acuerdo con el Sistema Internacional de Unidades (SI).
    """,
    """
    Con el fin de asegurar la calidad de sus mediciones se le recomienda al cliente recalibrar sus instrumentos y equipos a intervalos apropiados.
    """,
    """
    Los resultados son válidos solamente para el ítem sometido a calibración, no deben ser utilizados como una certificación de conformidad con normas de producto o como certificado del sistema de calidad de la entidad que lo produce.
    """,
    """
    METRINDUST S.A.C. no se responsabiliza de los perjuicios que pueda ocasionar el uso inadecuado de este equipo, ni de una incorrecta interpretación de los resultados de la calibración aquí declarados. El certificado de calibración sin firma carece de validez.
    """
    ]

    # 2da hoja

    trazabilidad = [['TRAZABILIDAD','PATRÓN DE TRABAJO','CERTIFICADO DE CALIBRACIÓN']]


    codigos = [extraer_datos(f'data/{nro_certificado}','informacion')['codigo_RS'],
               extraer_datos(f'data/{nro_certificado}','informacion')['codigo_AUX'],
               extraer_datos(f'data/{nro_certificado}','informacion')['codigo_tRS'],
               extraer_datos(f'data/{nro_certificado}','informacion')['codigo_tSCM'],
               ]

    for codigo in codigos:
        trazabilidad.append([aParrafo(datos[codigo]['trazabilidad'],'centrado'),aParrafo(datos[codigo]['descripcion'],'centrado'),aParrafo(datos[codigo]['certificado_calibracion'],'centrado')])

    t_inicial = extraer_datos(f'data/{nro_certificado}','informacion')['t_inicial'].replace(".",",")+" "+extraer_datos(f'data/{nro_certificado}','informacion')['t_unidad']
    t_final =extraer_datos(f'data/{nro_certificado}','informacion')['t_final'].replace(".",",")+" "+extraer_datos(f'data/{nro_certificado}','informacion')['t_unidad']
    h_inicial = extraer_datos(f'data/{nro_certificado}','informacion')['h_inicial'].replace(".",",")+" "+extraer_datos(f'data/{nro_certificado}','informacion')['h_unidad']
    h_final = extraer_datos(f'data/{nro_certificado}','informacion')['h_final'].replace(".",",")+" "+extraer_datos(f'data/{nro_certificado}','informacion')['h_unidad']
    p_inicial = extraer_datos(f'data/{nro_certificado}','informacion')['p_inicial'].replace(".",",")+" "+extraer_datos(f'data/{nro_certificado}','informacion')['p_unidad']
    p_final = extraer_datos(f'data/{nro_certificado}','informacion')['p_final'].replace(".",",")+" "+extraer_datos(f'data/{nro_certificado}','informacion')['h_unidad']


    
    dev_st = strRoundFloatPC(extraer_datos(f'data/{nro_certificado}','resultados')['desv_estandar'],nro_decimales)+" "+extraer_datos(f'data/{nro_certificado}','resultados')['desv_estandar_unidad']
    nro_repeticiones = extraer_datos(f'data/{nro_certificado}','resultados')['nro_repeticiones']
    
    u_deltaVmen = strRoundFloatPC(extraer_datos(f'data/{nro_certificado}','resultados')['u_deltaVmen'],nro_decimales)+" "+extraer_datos(f'data/{nro_certificado}','resultados')['u_deltaVmen_unidad']
    
    resolucion_calculada = strRoundFloatPC(extraer_datos(f'data/{nro_certificado}','resultados')['resolucion'],nro_decimales)+" "+extraer_datos(f'data/{nro_certificado}','resultados')['resolucion_unidad']+\
        " ("+strRoundFloatPC(extraer_datos(f'data/{nro_certificado}','resultados')['resolucion_porcentaje'],nro_decimales)+" "+extraer_datos(f'data/{nro_certificado}','resultados')['resolucion_porcentaje_unidad']+")"




    lista_resultados = [f"El valor de resolución de escala calculada corresponde a: {resolucion_calculada}",
                        f"Incertidumbre de la lectura del menisco: {u_deltaVmen}",
                        f"Se realizaron {nro_repeticiones} repeticiones del volumen",
                        f"Desviación estándar: {dev_st}"]
    if ajuste == "SI":
        lista_resultados.append(f"Antes del ajuste el cero correspondia a: {strRoundFloatPC(vo_aa,nro_decimales)} {vo_aa_unidad}")      
        lista_resultados.append(f"Después del ajuste el cero corresponde a: {strRoundFloatPC(vo_da,nro_decimales)} {vo_da_unidad}")               
    else:
        lista_resultados.append(f'El cero corresponde a:  {strRoundFloatPC(vo_aa,nro_decimales)} {vo_aa_unidad}')
                        


    lista_obs = ["Con fines de identificación se colocó una etiqueta autoadhesiva con la indicación (CALIBRADO).",
                f"Los resultados están dados a la temperatura de referencia de {t_ref_cal}.",
                f"En la determinación del volumen se ha considerado un coeficiente de expansión cúbica de {puntoAComa("{:.7f}".format(c_material))} 1/°C"
                ]

    

    if valvula_drenaje == "SI":
        tiempo_goteo = int(promediar(toFloat(eval(extraer_datos(f'data/{nro_certificado}','calibracion')['tiempo_goteo']))))
        tiempo_entrega = int(promediar(toFloat(eval(extraer_datos(f'data/{nro_certificado}','calibracion')['tiempo_entrega']))))
        lista_obs.append(f"Tiempo de goteo del instrumento: {tiempo_goteo} s.")
        lista_obs.append(f"Tiempo de entrega del instrumento: {tiempo_entrega} s.")
        

    if ajuste == "SI":
        lista_obs.append("Se realizó el ajuste de la escala.")
    else:
        lista_obs.append("No se realizó el ajuste de la escala.")

    if "(*)" in cod_id: lista_obs.insert(0,"(*) Código de identificación asignado Metrindust S.A.C.")


    for e in comentario:
        if isinstance(e,list):
            for i,element in enumerate(e):
                if i == 0:
                    var = element.capitalize()
                    if "mt" in var:
                        var = var.replace("mt","MT")
                        var = var[:obtenerPosicion(var,"-")[0]]+\
                        var[obtenerPosicion(var,"-")[0]:obtenerPosicion(var,"-")[1]].upper()+\
                        var[obtenerPosicion(var,"-")[1]:]
                        lista_obs.insert(0,var)
                    else:
                        lista_obs.insert(0,element.capitalize())
                else:
                    lista_obs.insert(0,element.lower())
        else:
            if e.strip() != "": 
                lista_obs.insert(0,e.replace("\n","").replace("\r",""))
    #informacion_instrumento = {"Marca":"mark","Modelo":"Model","N° de Serie":"351"}


    informacion_instrumento = {'Marca':marca,
                            'Modelo':modelo,
                            'N° de serie':nro_serie,
                            'Procedencia':procedencia,
                            'Código de identificación':cod_id,
                            'Color':color,
                            'Valor nominal':valor_nominal,
                            'Intervalo de indicación':interv_ind,
                            'Clase':clase,
                            'Resolución':res,
                            'Tipo':tipo,
                            'Material':material}

    informacion_instrumento = dicc_to_list(informacion_instrumento)

    ruta_certificado = f"certificados_modificados/{nro_certificado}"
    
    ruta_fondo = "static/fondo.png"
    titulo_firmaysello = "AUTORIZADO POR: "
    ruta_firma = "static/firma.jpg"
    ruta_sello = "static/sello.jpg"
    nombre = "Gamarra Rodríguez Dennis"
    cargo = "Gerente Técnico"
    nro_paginas = 2
    nro_revision = "Revisión Seraphin 00"

    # codigo de certificado

    generar_certificado(ruta_certificado,nro_certificado,parrafos,ruta_fondo,titulo_firmaysello,ruta_firma,ruta_sello,nombre, cargo,
                            nro_paginas,nro_revision,titulo, nombre_laboratorio, cotizacion, solicitante, direccion, 
                            nombre_instrumento,informacion_instrumento, nombre_fecha_lugar,fecha_emi, fecha_cal, lugar_cal,nombre_metodo_cal,
                            t_inicial, t_final, h_inicial, h_final, p_inicial, p_final, trazabilidad, lista_resultados,
                            ajuste, vn, vn_unidad, vo_aa, vo_aa_unidad, U_aa, U_aa_unidad,
                            vo_da, vo_da_unidad, U_da, U_da_unidad, lista_obs, k, nro_decimales)

    print("Certificado generado exitósamente.")

