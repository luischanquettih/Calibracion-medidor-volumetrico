from funciones import *
from datos import *
from incertidumbre import *


def actualizar(nro_certificado):
    lista = ['calibracion_antes_ajuste','calibracion']
    for e in lista:
        try:
            nombre_calibracion = e
            if nombre_calibracion == "calibracion_antes_ajuste":
                nombre_presupuesto = "presupuesto_antes_ajuste"
                nombre_resultados = "resultados_antes_ajuste"
            else:
                nombre_presupuesto = "presupuesto"
                nombre_resultados = "resultados"

            data = extraer_datos(f"data/{nro_certificado}",nombre_calibracion)

            t_inicial = data['t_inicial_']
            t_final = data['t_final_']
            h_inicial = data['h_inicial_']
            h_final = data['h_final_']
            p_inicial = data['p_inicial_']
            p_final = data['p_final_']
            t_unidad = data['t_unidad_']
            h_unidad = data['h_unidad_']
            p_unidad = data['p_unidad_']
            t1_unidad = data['t1_unidad_']
            t2_unidad = data['t2_unidad_']
            deltaV_unidad = data['deltaV_unidad_']

            tRS = toFloat(eval(data['tRS_']))

            tSCM = toFloat(eval(data['tSCM_']))
            deltaV = toFloat(eval(data['deltaV_']))
            deltaV, deltaV_unidad = aLitros(deltaV, deltaV_unidad)



            # codigos
            codigo_RS = extraer_datos(f"data/{nro_certificado}","informacion")['codigo_RS']
            codigo_AUX = extraer_datos(f"data/{nro_certificado}","informacion")['codigo_AUX']
            codigo_tRS = extraer_datos(f"data/{nro_certificado}","informacion")['codigo_tRS']
            codigo_tSCM = extraer_datos(f"data/{nro_certificado}","informacion")['codigo_tSCM']
            codigo_t = extraer_datos(f"data/{nro_certificado}","informacion")['codigo_t']
            codigo_h = extraer_datos(f"data/{nro_certificado}","informacion")['codigo_h']
            codigo_p = extraer_datos(f"data/{nro_certificado}","informacion")['codigo_p']

            # corregir las condiciones ambientales
            t_inicial = corregir(codigo_t,data['t_inicial_'])
            t_final = corregir(codigo_t,data['t_final_'])
            h_inicial = corregir(codigo_h,data['h_inicial_'])
            h_final = corregir(codigo_h, data['h_final_'])
            p_inicial = corregir(codigo_p,data['p_inicial_'])
            p_final = corregir(codigo_p,data['p_final_'])

            ta = (t_inicial+t_final)/2

            if extraer_datos(f"data/{nro_certificado}","informacion")['valvula_drenaje'] == "SI":
                # tomo las unidades de tg y te
                tg_unidad = extraer_datos(f"data/{nro_certificado}",nombre_calibracion)['tg_unidad']
                te_unidad = extraer_datos(f"data/{nro_certificado}",nombre_calibracion)['te_unidad']
                tg = promediar(toFloat(eval(extraer_datos(f"data/{nro_certificado}",nombre_calibracion)['tiempo_goteo'])))
                te = promediar(toFloat(eval(extraer_datos(f"data/{nro_certificado}",nombre_calibracion)['tiempo_entrega'])))
                nombre="_antes_ajuste"
            else:
                nombre=""

            # corrigiendo tRS
            tRS_ = []
            tmin_RS = []
            tmax_RS = []
            for i,l in enumerate(tRS):
                for j,e in enumerate(l):
                    #tRS[i][j] = corregir(extraer_datos(f"data/{nro_certificado}","informacion")["codigo_tRS"],e.replace(",","."))
                    tRS_.append(corregir(codigo_tRS,e))
                tmin_RS.append(min(tRS_))
                tmax_RS.append(min(tRS_))



            """Determinación de Vt
            """
            material_RS = extraer_datos(f"data/{nro_certificado}","informacion")["material_RS"]
            material_SCM = extraer_datos(f"data/{nro_certificado}","informacion")["material_SCM"]
            t0RS = datos[codigo_RS]["t_ref"]
            t = 20  # °C  , temperatura de referencia del SCM

            VN_RS, VN_RS_unidad = datos[codigo_RS]["VN"], datos[codigo_RS]["VN_unidad"]
            VN_RS, VN_RS_unidad = aLitros(VN_RS, VN_RS_unidad)
            corrRS, corrRS_unidad = datos[codigo_RS]["correccion"], datos[codigo_RS]["correccion_unidad"]
            corrRS, corrRS_unidad = aLitros(corrRS, corrRS_unidad)
            V0 = VN_RS+corrRS
            V0_unidad = "L"

            VN_SCM = float(extraer_datos(f"data/{nro_certificado}","informacion")['valor_nominal'])
            VN_SCM_unidad = extraer_datos(f"data/{nro_certificado}","informacion")['valor_nominal_unidad']
            VN_SCM, VN_SCM_unidad = aLitros(VN_SCM, VN_SCM_unidad)
            

            if VN_SCM > 100: nro_repeticiones = 2
            elif VN_SCM <= 100: nro_repeticiones = 3

            if VN_SCM >= 2000: nro_lugares = 3
            elif VN_SCM >= 500: nro_lugares = 2
            else: nro_lugares = 1
            
            N = round(VN_SCM/VN_RS) 

            # tSCM
            tSCM_L = []
            tmin_SCM = []
            tmax_SCM = []
            tSCM_ = []
            for i in range(nro_repeticiones):
                for j in range(nro_lugares):
                    tSCM_L.append(corregir(codigo_tSCM,tSCM[i][j]))
                tmin_SCM.append(min(tSCM_L))
                tmax_SCM.append(max(tSCM_L))
                tSCM_.append(promediar(tSCM_L)) # tSCM tendra elementos correspondiante al numero de repeticiones
                tSCM_L = []


            listaVt = []
            for i in range(nro_repeticiones):
                listaVt.append(V_t(N,V0,coef_material[material_RS],t0RS,tRS_[i],beta(tRS_[i],tSCM_[i]),tSCM_[i],coef_material[material_SCM],t,deltaV[i]))
            listaVt_unidad = "L"

            Vt = promediar(listaVt)
            print("Volumen obtenido Vt: ", Vt)

            ancho_escala = extraer_datos(f"data/{nro_certificado}","informacion")['ancho']
            ancho_escala_unidad = extraer_datos(f"data/{nro_certificado}","informacion")['ancho_unidad']
            diametro_cuello = extraer_datos(f"data/{nro_certificado}","informacion")['diametro']
            diametro_cuello_unidad = extraer_datos(f"data/{nro_certificado}","informacion")['diametro_unidad']


            U_Vt_valor,k,veff,u_deltaVmen_valor,desv_estandar,nro_repeticiones = \
                    iniciar_calculos(N=N, 
                                    codigo_RS=codigo_RS, 
                                    codigo_tRS=codigo_tRS, tmin_RS=min(tmin_RS), tmax_RS=max(tmax_RS), ta=ta, tRS=promediar(tRS_),
                                    codigo_tSCM=codigo_tSCM, tmin_SCM=min(tmin_SCM), tmax_SCM=max(tmax_SCM), tSCM=promediar(tSCM_),
                                    material_RS=material_RS, material_SCM=material_SCM,
                                    codigo_AUX=codigo_AUX,
                                    ancho=ancho_escala,ancho_unidad=ancho_escala_unidad, diametro=diametro_cuello, diametro_unidad=diametro_cuello_unidad,
                                    listaVt=listaVt,listaVt_unidad=listaVt_unidad, # debido a 3 repeticiones
                                    VN_SCM=VN_SCM,VN_SCM_unidad=VN_SCM_unidad,
                                    t0RS=t0RS,t=t,
                                    V0=V0,
                                    nombre_presupuesto=nro_certificado+"/"+nombre_presupuesto,
                                    nro_repeticiones=nro_repeticiones,nro_certificado=nro_certificado, modificacion=True)


            if nombre_resultados == "resultados":
                correccion = datos[codigo_AUX]['correccion']
                correccion_unidad = datos[codigo_AUX]['correccion_unidad']
                vol_sup_unidad = data['vol_sup_unidad']
                vol_inf_unidad = data['vol_inf_unidad']  

                correccion, correccion_unidad = aUnidad(correccion, correccion_unidad, vol_sup_unidad)
                vol_sup_acumulado = 0
                lista_Vt_sup = []
                vol_sup = 0
                for e in toFloat(eval(data['vol_sup_'])):
                    vol_sup, vol_sup_unidad = aLitros(e+correccion,correccion_unidad)
                    vol_sup_acumulado += vol_sup
                    lista_Vt_sup.append(Vt+vol_sup_acumulado)

                correccion, correccion_unidad = aUnidad(correccion, correccion_unidad, vol_inf_unidad)
                vol_inf_acumulado = 0
                lista_Vt_inf = []
                vol_inf = 0
                for e in toFloat(eval(data['vol_inf_'])):
                    vol_inf, vol_inf_unidad = aLitros(e+correccion,correccion_unidad)
                    vol_inf_acumulado += vol_inf
                    lista_Vt_inf.append(Vt-vol_inf_acumulado)

                
                x = [i+1 for i in range(int(len(lista_Vt_inf)) + 1 + int(len(lista_Vt_sup)))]
                y = lista_Vt_inf + [Vt] + lista_Vt_sup

                print("Vt de las marcas: ", y, "L")

                x = np.array(x)
                y = np.array(y)
                m, b = np.polyfit(x, y, 1)

                resolucion = m
                resolucion_unidad = "L"

                resolucion_unidad_informacion = extraer_datos(f"data/{nro_certificado}","informacion")['res_unidad']
                if resolucion_unidad_informacion == "lineas": resolucion_unidad_informacion = "ml"
                resolucion, resolucion_unidad = aUnidad(resolucion,resolucion_unidad, resolucion_unidad_informacion)
                
                Vt_valor, Vt_unidad = Vt, "L"
                Vt_valor, Vt_unidad = aUnidad(Vt_valor, Vt_unidad, resolucion_unidad_informacion)
                resolucion_porcentaje = (resolucion/Vt_valor)*100
                resolucion_porcentaje_unidad = "%"
                
                nuevas_claves_valores = {
                    "VN_SCM": VN_SCM,
                    "VN_SCM_unidad": VN_SCM_unidad,
                    "Vt": promediar(listaVt),
                    "Vt_unidad": "L",
                    "U_Vt": U_Vt_valor[0],
                    "U_Vt_unidad": U_Vt_valor[1],
                    "k": k,
                    "veff": veff,
                    "u_deltaVmen": u_deltaVmen_valor[0],
                    "u_deltaVmen_unidad": u_deltaVmen_valor[1],
                    "desv_estandar": desv_estandar[0],
                    "desv_estandar_unidad": desv_estandar[1],
                    "nro_repeticiones": nro_repeticiones,
                    "resolucion": str(resolucion),
                    "resolucion_unidad": resolucion_unidad,
                    "resolucion_porcentaje": str(resolucion_porcentaje),
                    "resolucion_porcentaje_unidad": resolucion_porcentaje_unidad
                }
                modificar_data(nro_certificado,nombre_resultados, nuevas_claves_valores)
            else:
                nuevas_claves_valores = {
                        "VN_SCM": VN_SCM,
                        "VN_SCM_unidad": VN_SCM_unidad,
                        "Vt": promediar(listaVt),
                        "Vt_unidad": "L",
                        "U_Vt": U_Vt_valor[0],
                        "U_Vt_unidad": U_Vt_valor[1],
                        "k": k,
                        "veff": veff,
                        "u_deltaVmen": u_deltaVmen_valor[0],
                        "u_deltaVmen_unidad": u_deltaVmen_valor[1],
                        "desv_estandar": desv_estandar[0],
                        "desv_estandar_unidad": desv_estandar[1],
                        "nro_repeticiones": nro_repeticiones,
                }
                modificar_data(nro_certificado,nombre_resultados, nuevas_claves_valores)
        except:
            pass

