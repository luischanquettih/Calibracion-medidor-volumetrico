# Este codigo solo usará el metodo de llenado
from incertidumbre import * 
from datos import *
from calibracion_escala import *

# Seleccionando los patrones
codigo_RS = "MVP001"
codigo_tRS = "TP001"
codigo_tSCM = "TP002"
codigo_AUX = "MVAP001"
codigo_t = "Termometro001"
codigo_h = "Higrometro001"
codigo_p = "Barometro001"

VN_RS, VN_RS_unidad = datos[codigo_RS]["VN"], datos[codigo_RS]["VN_unidad"]
VN_RS, VN_RS_unidad = aLitros(VN_RS, VN_RS_unidad)
corrRS, corrRS_unidad = datos[codigo_RS]["correccion"], datos[codigo_RS]["correccion_unidad"]
corrRS, corrRS_unidad = aLitros(corrRS, corrRS_unidad)
V0 = VN_RS+corrRS
V0_unidad = "L"
t0RS = datos[codigo_RS]["t_ref"]

VN_SCM = datos["calibrando"]["VN"]
VN_SCM_unidad = datos["calibrando"]["VN_unidad"]
t = 20  # °C  , temperatura de referencia del SCM
VN_SCM, VN_SCM_unidad = aLitros(VN_SCM, VN_SCM_unidad)
print("--------------------------------------------------")
print("----------- SOFTWARE SERAPHIN v0.0 beta ----------")
#condiciones_previas()
print("------------------- Información ------------------")



if VN_SCM > 100: nro_repeticiones = 2
elif VN_SCM <= 100: nro_repeticiones = 3
print("N° de repeticiones: ", nro_repeticiones)

if VN_SCM >= 2000: nro_lugares = 3
elif VN_SCM >= 500: nro_lugares = 2
else: nro_lugares = 1
print("N° de lugares: ", nro_lugares)

# Determinación del número de llenados
N = round(VN_SCM/VN_RS) 
print("N° de llenados: ", N)


realizar_ajuste = aplicar_condicion(input("¿El cliente aceptó el ajuste de la escala? S/N: "),"¿El cliente aceptó el ajuste de la escala? S/N: ").replace("Si","S").replace("Sí","S").replace("si","S").replace("s","S")
if realizar_ajuste == "S": realizar_ajuste = True
else: realizar_ajuste = False
valvula_drenaje = aplicar_condicion(input("¿El calibrando posee válvula de drenaje? S/N: "),"¿El calibrando posee válvula de drenaje? S/N: ").replace("Si","S").replace("Sí","S").replace("si","S").replace("s","S")
if valvula_drenaje == "S": valvula_drenaje = True
else: valvula_drenaje = False

nro_certificado = aplicar_condicion(input("Número de certificado: "),"Número de certificado: ")
cotizacion = aplicar_condicion(input("Cotización: "),"Cotización: ")
solicitante = aplicar_condicion(input("Solicitante: "),"Solicitante: ")
direccion = aplicar_condicion(input("Dirección: "),"Dirección: ")
marca = aplicar_condicion(input("Marca: "),"Marca: ")
modelo = aplicar_condicion(input("Modelo: "),"Modelo: ")
nro_serie = aplicar_condicion(input("N° serie: "),"N° serie:")
procedencia = aplicar_condicion(input("Procedencia: "), "Procedencia: ")
cod_id = aplicar_condicion(input("Código de identificación: "),"Código de identificación: ")
color = aplicar_condicion(input("Color: "),"Color: ")
valor_nominal = aplicar_condicion(input("Valor nominal (L/gal): "),"Valor nominal (L/gal): ")
interv_ind = aplicar_condicion(input("Intervalo de indicación (± L/gal/ml): "),"Intervalo de indicación (± L/gal/ml): ")
clase = aplicar_condicion(input("Clase: "),"Clase: ")
res = aplicar_condicion(input("Resolución (L/gal/ml/líneas): "),"Resolución (L/gal/ml/líneas): ")
tipo_SCM = aplicar_condicion(input("El calibrando se calibrará como tipo (Ex/In): "), "El calibrando se calibrará como tipo (Ex/In): ").capitalize()
fecha_cal = aplicar_condicion(input("Fecha de calibración: "), "Fecha de calibración: ")
fecha_emi = aplicar_condicion(input("Fecha de emisión: "), "Fecha de emisión: ")
print("""
--------------- Lista de materiales --------------
1) Fibra de carbon
2) Vidrio de borosilicato 3,3
3) Vidrio de borosilicato 5,0
4) Vidrio de cal sodada
5) Acero
6) Carbono suave
7) Acero inoxidable grado 304
8) Acero inoxidable grado 316
9) Acero inoxidable 17-4PH
10) Cobre - aleación de zinc (latón)
11) Aluminio
12) PVC
""")
material_RS = nro_material[aplicar_condicion(input("Material del recipiente volumétrico patrón: "),"Material del recipiente volumétrico patrón: ")]
material_SCM = nro_material[aplicar_condicion(input("Material del calibrando: "),"Material del calibrando: ")]
ancho=aplicar_condicion(input("Ancho de la escala(cm): "),"Ancho de la escala(cm): ").replace(",",".")
ancho_unidad = "cm"
diametro=aplicar_condicion(input("Diametro del cuello de la escala(cm): "),"Diametro del cuello de la escala(cm): ").replace(",",".")
diametro_unidad = "cm"
sensibilidad=aplicar_condicion(input("Espaciamiento entre marcas(mm): "),"Espaciamiento entre marcas(mm): ").replace(",",".")
sensibilidad_unidad = "mm"


def calibracion(nombre,nro_repeticiones=nro_repeticiones):
    tRS = []
    vRS = []
    tSCM = []
    vSCM = []
    lista_deltaV = []
    listaVt = []
    if N == 1:
        print("\n------------- Llenado No Múltiple  ---------------")
        print("-------- Condiciones ambientales iniciales -------")
        t_inicial = corregir(codigo_t,float(input("Temperatura inicial (°C): ").replace(",",".")))
        h_inicial = corregir(codigo_h,int(input("Humedad inicial (%): ").replace(",",".")))
        p_inicial = corregir(codigo_p,float(input("Presión inicial (mbar): ").replace(",",".")))

        for i in range(nro_repeticiones):
            print(f"\n--------------- Repetición N° {i+1}---------------")

            print("-Llenar el patrón RS")
            print("-Empezaremos midiendo la temperatura y volumen del patrón (RS)")
            tRS_value = corregir(codigo_tRS,float(input("Temperatura en el recipiente patrón (tRS) en °C: ").replace(",",".")))
            tRS.append(tRS_value)
            print("-Ajustar el menisco")
            vRS_value = input("Volumen del recipiente patrón (vRS) en (L/gal/ml): ").replace(",",".")
            
            if "gal" in vRS_value: vRS_value, vRS_value_unidad = aLitros(vRS_value.replace("gal",""),"gal") # a litros
            elif "ml" in vRS_value: vRS_value, vRS_value_unidad = aLitros(vRS_value.replace("ml",""),"ml") # a litros
            else: 
                vRS_value = vRS_value.replace("l","L").replace("L","")
            vRS.append(float(vRS_value))  # sera el mismo debido al patron que se tiene(1 raya)
            print("-Preparar el calibrando por si se va a calibrar como tipo 'Ex'(humedecer) o 'In'(secarlo)")
            print("-Vaciar el agua del recipiente patron al calibrando, manteniendo el tiempo de goteo")

            # puedo promediar tRS y vRS
            tmin_RS = min(tRS)
            tmax_RS = max(tRS)

            print("----------------------------------------------------")
            print("-Empezaremos midiendo la temperatura y volumen ΔV agregado/retirado al/del calibrando (SCM)")
            tSCM_value = 0
            for k in range(nro_lugares):
                tSCM_value += corregir(codigo_tSCM, float(input(f"Temperatura del calibrando (tSCM) en °C en la ubicación {k+1}: ").replace(",",".")))
            tSCM_value /= nro_lugares

            tSCM.append(tSCM_value)
            deltaV_value = input("Volumen agregado o retirado (ΔV) en (L/gal/ml): ").replace(",",".")
            if "gal" in deltaV_value: deltaV_value, deltaV_value_unidad = aLitros(deltaV_value.replace("gal",""),"gal") # a litros
            elif "ml" in deltaV_value: deltaV_value, deltaV_value_unidad = aLitros(deltaV_value.replace("ml",""),"ml") # a litros
            else: 
                deltaV_value = float(deltaV_value.replace("l","L").replace("L",""))
                deltaV_value_unidad = "L"

            """Determinación de Vt
            """
            Vt_valor = V_t(N,V0,coef_material[material_RS],t0RS,promediar(tRS),beta(promediar(tRS),promediar(tSCM)),promediar(tSCM),coef_material[material_SCM],t,deltaV_value)
            lista_deltaV.append(deltaV_value)
            listaVt.append(Vt_valor)
            listaVt_unidad = "L"
            print("Volumen obtenido Vt: ", listaVt, listaVt_unidad)

            if valvula_drenaje == True:
                tiempo_goteo = input("Tiempo de goteo (s): ")
                tiempo_entrega = input("Tiempo de entrega (s): ")
                

        tmin_SCM = min(tSCM)
        tmax_SCM = max(tSCM)
            
        print("\n-------- Condiciones ambientales finales -------")
        t_final = corregir(codigo_t,float(input("Temperatura final (°C): ").replace(",",".")))
        h_final = corregir(codigo_h,int(input("Humedad final (%): ").replace(",",".")))
        p_final = corregir(codigo_p,float(input("Presión final (mbar): ").replace(",",".")))

        ta = (t_inicial + t_final)/2

        print("\n---------- Presupuesto de incertidumbre ----------")
        U_Vt_valor,k,veff,u_deltaVmen_valor,desv_estandar,nro_repeticiones = \
        iniciar_calculos(N=N, 
                        codigo_RS=codigo_RS, 
                        codigo_tRS=codigo_tRS, tmin_RS=tmin_RS, tmax_RS=tmax_RS, ta=ta, tRS=promediar(tRS),
                        codigo_tSCM=codigo_tSCM, tmin_SCM=tmin_SCM, tmax_SCM=tmax_SCM, tSCM=promediar(tSCM),
                        material_RS=material_RS, material_SCM=material_SCM,
                        codigo_AUX=codigo_AUX,
                        ancho=ancho,ancho_unidad=ancho_unidad, diametro=diametro, diametro_unidad=diametro_unidad,
                        listaVt=listaVt,listaVt_unidad=listaVt_unidad, # debido a 3 repeticiones
                        VN_SCM=VN_SCM,VN_SCM_unidad=VN_SCM_unidad,
                        t0RS=t0RS,t=t,
                        V0=V0,
                        nombre_presupuesto="presupuesto"+nombre,
                        nro_repeticiones=nro_repeticiones)
  
        guardar_resultados(VN_SCM,VN_SCM_unidad,listaVt,listaVt_unidad,
                           U_Vt_valor,k,veff,u_deltaVmen_valor,desv_estandar,nro_repeticiones,nombre="resultados"+nombre)
        


        guardar_datos("informacion",
                      {
                        "realizar_ajuste":realizar_ajuste,
                        "valvula_drenaje":valvula_drenaje,
                        "nro_certificado":nro_certificado, 
                        "cotizacion":cotizacion, 
                        "solicitante":solicitante, 
                        "direccion":direccion,
                        "marca":marca,
                        "modelo":modelo,
                        "nro_serie":nro_serie,
                        "procedencia":procedencia,
                        "cod_id":cod_id,
                        "color":color,
                        "valor_nominal":valor_nominal, 
                        "interv_ind":interv_ind,
                        "clase":clase,
                        "res":res,
                        "tipo_SCM":tipo_SCM,
                        "fecha_cal":fecha_cal,
                        "fecha_emi":fecha_emi,
                        "material_RS":material_RS,
                        "material_SCM":material_SCM,
                        "coeff_material_RS":coef_material[material_RS],
                        "coeff_material_SCM":coef_material[material_SCM],
                        "ancho": ancho,
                        "ancho_unidad": ancho_unidad,
                        "diametro":diametro,
                        "diametro_unidad": diametro_unidad,
                        "sensibilidad":sensibilidad,
                        "sensibilidad_unidad":sensibilidad_unidad,
                        "t_inicial":str(round(t_inicial,1)),
                        "h_inicial":str(int(h_inicial)),
                        "p_inicial":str(p_inicial),
                        "t_final":str(round(t_final,1)),
                        "h_final":str(int(h_final)),
                        "p_final":str(p_final),
                        "t_unidad":"°C",
                        "h_unidad":"%",
                        "p_unidad":"mbar",
                        "realizar_ajuste":realizar_ajuste})
        
        if valvula_drenaje == True:
            agregar_datos("informacion", "tiempo_goteo", tiempo_goteo)
            agregar_datos("informacion", "tiempo_entrega", tiempo_entrega)

        return listaVt, listaVt_unidad, lista_deltaV, deltaV_value_unidad

    elif N > 1 and N <= 10:
        tRS_total = []
        vRS_total = []

        print("\n--------------- Llenado Múltiple  ----------------")
        print("-------- Condiciones ambientales iniciales -------")
        t_inicial = corregir(codigo_t,float(input("Temperatura inicial (°C): ").replace(",",".")))
        h_inicial = corregir(codigo_h,int(input("Humedad inicial (%): ").replace(",",".")))
        p_inicial = corregir(codigo_p,float(input("Presión inicial (mbar): ").replace(",",".")))

        for i in range(nro_repeticiones):
            tRS = []
            vRS = []
            print(f"\n----------------- Repetición N° {i+1} ----------------")
            for j in range(N):
                print(f"------------------ Llenado N° {j+1} ------------------")
                print("-Llenar el patrón RS")
                print("-Empezaremos midiendo la temperatura y volumen del patrón (RS)")
                tRS_value = corregir(codigo_tRS,float(input("Temperatura en el recipiente patrón (tRS) en °C: ").replace(",",".")))
                tRS.append(tRS_value)
                print("-Ajustar el menisco")
                vRS_value = input("Volumen del recipiente patrón (vRS) en (L/gal/ml): ").replace(",",".")

                if "gal" in vRS_value: vRS_value, vRS_value_unidad = aLitros(vRS_value.replace("gal",""),"gal") # a litros
                elif "ml" in vRS_value: vRS_value, vRS_value_unidad = aLitros(vRS_value.replace("ml",""),"ml") # a litros
                else:  
                    vRS_value = vRS_value.replace("l","L").replace("L","")
                vRS.append(float(vRS_value))  # sera el mismo debido al patron que se tiene(1 raya)
                print("-Preparar el calibrando por si se va a calibrar como tipo 'Ex'(humedecer) o 'In'(secarlo)")
                print("-Vaciar el agua del recipiente patron al calibrando, mantener el tiempo de goteo")

            tRS_total.append(promediar(tRS))
            tmin_RS = min(tRS_total)
            tmax_RS = max(tRS_total)

            vRS_total.append(promediar(vRS))

            print("--------------------------------------------------")
            print("-Empezaremos midiendo la temperatura y ΔV agregado/quitado al/del calibrando (SCM)")
            tSCM_value = 0
            for k in range(nro_lugares):
                tSCM_value += corregir(codigo_tSCM,float(input(f"Temperatura del calibrando (tSCM) en °C en la ubicación {k+1}: ").replace(",",".")))
            tSCM_value /= nro_lugares

            tSCM.append(tSCM_value)
            deltaV_value = input("Volumen agregado o retirado (ΔV) en (L/gal/ml): ").replace(",",".")
            if "gal" in deltaV_value: deltaV_value, deltaV_value_unidad = aLitros(deltaV_value.replace("gal",""),"gal") # a litros
            elif "ml" in deltaV_value: deltaV_value, deltaV_value_unidad = aLitros(deltaV_value.replace("ml",""),"ml") # a litros
            else: 
                deltaV_value = float(deltaV_value.replace("l","L").replace("L",""))
                deltaV_value_unidad = "L"

            """Determinación de Vt
            """
            Vt_valor = V_t(N,V0,coef_material[material_RS],t0RS,promediar(tRS),beta(promediar(tRS),promediar(tSCM)),promediar(tSCM),coef_material[material_SCM],t,deltaV_value)
            lista_deltaV.append(deltaV_value)
            listaVt.append(Vt_valor)
            listaVt_unidad = "L"
            print("Volumen obtenido Vt: ", listaVt, listaVt_unidad)

            if valvula_drenaje == True:
                tiempo_goteo = input("Tiempo de goteo (s): ")
                tiempo_entrega = input("Tiempo de entrega (s): ")

        tmin_SCM = min(tSCM)
        tmax_SCM = max(tSCM)
    
            
        print("\n-------- Condiciones ambientales finales -------")
        t_final = corregir(codigo_t,float(input("Temperatura final (°C): ").replace(",",".")))
        h_final = corregir(codigo_h,int(input("Humedad final (%): ").replace(",",".")))
        p_final = corregir(codigo_p,float(input("Presión final (mbar): ").replace(",",".")))

        ta = (t_inicial + t_final)/2

        print("\n---------- Presupuesto de incertidumbre ----------")
        # iniciando los calculos
        U_Vt_valor,k,veff,u_deltaVmen_valor,desv_estandar,nro_repeticiones = \
        iniciar_calculos(N=N, 
                        codigo_RS=codigo_RS, 
                        codigo_tRS=codigo_tRS, tmin_RS=tmin_RS, tmax_RS=tmax_RS, ta=ta, tRS=promediar(tRS_total),
                        codigo_tSCM=codigo_tSCM, tmin_SCM=tmin_SCM, tmax_SCM=tmax_SCM, tSCM=promediar(tSCM),
                        material_RS=material_RS, material_SCM=material_SCM,
                        codigo_AUX=codigo_AUX,
                        ancho=ancho,ancho_unidad=ancho_unidad, diametro=diametro, diametro_unidad=diametro_unidad,
                        listaVt=listaVt,listaVt_unidad=listaVt_unidad, # debido a 3 repeticiones
                        VN_SCM=VN_SCM,VN_SCM_unidad=VN_SCM_unidad,
                        t0RS=t0RS,t=t,
                        V0=V0,
                        nombre_presupuesto="presupuesto"+nombre,
                        nro_repeticiones=nro_repeticiones)

       
        guardar_resultados(VN_SCM,VN_SCM_unidad,listaVt,listaVt_unidad,
                           U_Vt_valor,k,veff,u_deltaVmen_valor,desv_estandar,nro_repeticiones,nombre="resultados"+nombre)
        


        guardar_datos("informacion",
                      {
                        "realizar_ajuste":realizar_ajuste,
                        "valvula_drenaje":valvula_drenaje,
                        "nro_certificado":nro_certificado, 
                        "cotizacion":cotizacion, 
                        "solicitante":solicitante, 
                        "direccion":direccion,
                        "marca":marca,
                        "modelo":modelo,
                        "nro_serie":nro_serie,
                        "procedencia":procedencia,
                        "cod_id":cod_id,
                        "color":color,
                        "valor_nominal":valor_nominal, 
                        "interv_ind":interv_ind,
                        "clase":clase,
                        "res":res,
                        "tipo_SCM":tipo_SCM,
                        "fecha_cal":fecha_cal,
                        "fecha_emi":fecha_emi,
                        "material_RS":material_RS,
                        "material_SCM":material_SCM,
                        "coeff_material_RS":coef_material[material_RS],
                        "coeff_material_SCM":coef_material[material_SCM],
                        "ancho": ancho,
                        "ancho_unidad": ancho_unidad,
                        "diametro":diametro,
                        "diametro_unidad": diametro_unidad,
                        "sensibilidad":sensibilidad,
                        "sensibilidad_unidad":sensibilidad_unidad,
                        "t_inicial":str(round(t_inicial,1)),
                        "h_inicial":str(int(h_inicial)),
                        "p_inicial":str(p_inicial),
                        "t_final":str(round(t_final,1)),
                        "h_final":str(int(h_final)),
                        "p_final":str(p_final),
                        "t_unidad":"°C",
                        "h_unidad":"%",
                        "p_unidad":"mbar",
                        "realizar_ajuste":realizar_ajuste})
        
        if valvula_drenaje == True:
            agregar_datos("informacion", "tiempo_goteo", tiempo_goteo)
            agregar_datos("informacion", "tiempo_entrega", tiempo_entrega)


        return listaVt, listaVt_unidad, lista_deltaV, deltaV_value_unidad
    
    else:
        print("--------------------------------------------------")
        print("No es posible realizar la calibración, como máximo se puede realizar 10 llenados")
        print("--------------------------------------------------")



if realizar_ajuste == True:
    print("\n################ 1era CALIBRACIÓN ################")
    listaVt, listaVt_unidad, lista_deltaV, lista_deltaV_unidad  = calibracion(nombre="_antes_ajuste")
    Vt = promediar(listaVt)
    Vt_unidad = listaVt_unidad
    E = VN_SCM - Vt
    E_unidad = "L"
    Volumen = promediar(lista_deltaV) + E
    Volumen_unidad = "L"
    print("\n------------- Ajuste de la escala ----------------")
    print("-Llene el calibrando hasta la marca nominal o zero")
    if E < 0: print(f"-Retire un volumen equivalente a {Volumen} {Volumen_unidad}")
    else: print(f"-Agrega un volumen equivalente a {Volumen} {Volumen_unidad}")
    print("-Desplaze la marca hasta la base del menisco")
    print("-Es necesario realizar nuevamente la calibración")
    print("\n################ 2da CALIBRACIÓN ################")
    listaVt, listaVt_unidad, lista_deltaV, lista_deltaV_unidad  =  calibracion(nombre="_despues_ajuste")
    Vt = promediar(listaVt)
    Vt_unidad = listaVt_unidad
    print("\n>>> Fin de la calibración del zero.")
    calibracion_escala(nombre="resultados_despues_ajuste",Vt=Vt,Vt_unidad=Vt_unidad, codigo_RS=codigo_RS, codigo_tRS=codigo_tRS, codigo_tSCM=codigo_tSCM, codigo_AUX=codigo_AUX)
else:
    listaVt, listaVt_unidad, lista_deltaV, lista_deltaV_unidad  = calibracion(nombre="",nro_repeticiones=nro_repeticiones)
    Vt = promediar(listaVt)
    Vt_unidad = listaVt_unidad
    print("\n>>> Fin de la calibración del zero.")
    calibracion_escala(nombre="resultados", Vt=Vt, Vt_unidad=Vt_unidad, codigo_RS=codigo_RS, codigo_tRS=codigo_tRS, codigo_tSCM=codigo_tSCM, codigo_AUX=codigo_AUX)