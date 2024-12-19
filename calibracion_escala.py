from funciones import *
from certificado import * 

def calibracion_escala(nombre, Vt, Vt_unidad, codigo_RS, codigo_tRS, codigo_tSCM, codigo_AUX):
    print("\n------------- Calibración de la escala ----------------")
    print("Se considerará marcas superiores a las marcas por encima del zero.")
    print("Se considerará marcas inferiores a las marcas por debajo del zero.")
    # Se sabe Vt, también se sabe el volumen agregado
    print("-Llene el calibrando hasta el zero")

    nro_marcas_sup = aplicar_condicion(int(input("Número de marcas superiores: ")),"superiores")

    lista_Vt_sup = []
    lista_Vt_inf = []
   
    vol_sup_acumulado = 0
    vol_inf_acumulado = 0
    Vt, Vt_unidad = aLitros(Vt, Vt_unidad)

    for i in range(nro_marcas_sup):
        vol_sup = input(F"Volumen agregado para llegar a la marca superior N°{i+1} (L/ml/gal): ").replace(",",".")
        if "gal" in vol_sup: vol_sup, vol_sup_unidad = aLitros(vol_sup.replace("gal",""),"gal") # a litros
        elif "ml" in vol_sup: vol_sup, vol_sup_unidad = aLitros(vol_sup.replace("ml",""),"ml") # a litros
        else: 
            vol_sup = float(vol_sup.replace("l","L").replace("L",""))

        vol_sup_acumulado += vol_sup
        lista_Vt_sup.append(Vt+vol_sup_acumulado)

    print("-Retire el volumen necesario para llegar a la posición zero.")

    nro_marcas_inf = aplicar_condicion(int(input("Número de marcas inferiores: ")),"inferiores")

    for i in range(nro_marcas_inf):
        vol_inf = input(F"Volumen retirado para llegar a la marca inferior N°{i+1} (L/ml/gal): ").replace(",",".")
        if "gal" in vol_inf: vol_inf, vol_inf_unidad = aLitros(vol_inf.replace("gal",""),"gal") # a litros
        elif "ml" in vol_inf: vol_inf, vol_inf_unidad = aLitros(vol_inf.replace("ml",""),"ml") # a litros
        else: 
            vol_inf = float(vol_inf.replace("l","L").replace("L",""))
    
        vol_inf_acumulado += vol_inf
        lista_Vt_inf.append(Vt-vol_inf_acumulado)
    
    lista_Vt_inf.reverse()
    x = [i+1 for i in range(nro_marcas_inf + 1 + nro_marcas_sup)]
    y = lista_Vt_inf + [Vt] + lista_Vt_sup

    x = np.array(x)
    y = np.array(y)
    m, b = np.polyfit(x, y, 1)
    resolucion = m
    resolucion_unidad = "L"

    resolucion_porcentaje = (resolucion/Vt)*100
    resolucion_porcentaje_unidad = "%"

    agregar_datos(nombre, "resolucion", str(resolucion))
    agregar_datos(nombre, "resolucion_unidad", resolucion_unidad)
    agregar_datos(nombre, "resolucion_porcentaje", str(resolucion_porcentaje))
    agregar_datos(nombre, "resolucion_porcentaje_unidad", resolucion_porcentaje_unidad)

    print("\n>>> Fin de la calibración de la escala.\n")

    # generar el certificado
    #ejecutar([codigo_RS, codigo_tRS, codigo_tSCM, codigo_AUX])