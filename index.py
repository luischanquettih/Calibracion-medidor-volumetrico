from flask import Flask, render_template, redirect, url_for, flash, session, request
from forms import *
from datos import * 
from definir import *
from incertidumbre import * 
from certificado import * 
import datetime
from certificado_modificado import generar_certificado_modificado
import time 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'


@app.route('/', methods=['GET', 'POST'])
def registro():      
    limpiarJsons()              
    form = RegistrationForm()
    if form.validate_on_submit():
        # control 
        session['solicitante']=form.solicitante.data
        session['direccion']=form.direccion.data
        session['nro_certificado']="MT-"+form.nro_certificado.data+f"-{datetime.datetime.now().year}"
        session['cotizacion']=form.cotizacion.data
        session['fecha_cal']=form.fecha_cal.data
        session['fecha_emi']=form.fecha_emi.data

        # patrones
        session['codigo_RS'] = form.codigo_RS.data
        session['codigo_AUX'] = form.codigo_AUX.data
        session['codigo_tRS'] = form.codigo_tRS.data
        session['material_RS'] = datos[session.get('codigo_RS')]['material']
        session['codigo_tSCM'] = form.codigo_tSCM.data
        session['codigo_t'] = form.codigo_t.data
        session['codigo_h'] = form.codigo_h.data
        session['codigo_p'] = form.codigo_p.data


        # información del instrumento
        session['ajuste']=form.ajuste.data
        session['valvula_drenaje']=form.valvula_drenaje.data
        session['marca']=form.marca.data
        session['modelo']=form.modelo.data
        session['nro_serie']=form.nro_serie.data
        session['proced']=form.proced.data
        session['color']=form.color.data
        session['clase']=form.clase.data
        session['tipo']=form.tipo.data
        session['material']=form.material.data
        session['cod_id']=form.cod_id.data
        session['cod_id_unidad']=form.cod_id_unidad.data
        session['valor_nominal']=form.valor_nominal.data
        session['valor_nominal_unidad']=form.valor_nominal_unidad.data
        session['interval_ind']=form.interval_ind.data
        session['interval_ind_unidad']=form.interval_ind_unidad.data
        session['resolucion']=float(form.resolucion.data.replace(",","."))
        session['resolucion_unidad']=form.resolucion_unidad.data
        session['ancho_escala']=float(form.ancho_escala.data.replace(",","."))
        session['ancho_escala_unidad']=form.ancho_escala_unidad.data
        session['diametro_cuello']=float(form.diametro_cuello.data.replace(",","."))
        session['diametro_cuello_unidad']=form.diametro_cuello_unidad.data
        session['espaciamiento_marcas']=float(form.espaciamiento_marcas.data.replace(",","."))
        session['espaciamiento_marcas_unidad']=form.espaciamiento_marcas_unidad.data
    
        lista = ['solicitante','direccion','nro_certificado','cotizacion','fecha_cal','fecha_emi','codigo_RS','codigo_AUX','codigo_tRS','codigo_tSCM','codigo_t','codigo_h','codigo_p',
                 'ajuste','valvula_drenaje','marca','modelo','nro_serie','proced','color','clase','tipo','material','cod_id','cod_id_unidad','valor_nominal','valor_nominal_unidad','interval_ind',
                 'interval_ind_unidad','resolucion','resolucion_unidad','ancho_escala','ancho_escala_unidad','diametro_cuello','diametro_cuello_unidad','espaciamiento_marcas','espaciamiento_marcas_unidad']
        
        for e in lista:
            print(e+": ",session.get(e))


        guardar_datos("informacion",
                      {
                        "nro_certificado":session.get('nro_certificado'),
                        "solicitante":session.get('solicitante'), 
                        "direccion":session.get('direccion'),
                        "cotizacion":session.get('cotizacion'), 
                        "fecha_cal":session.get('fecha_cal'),
                        "fecha_emi":session.get('fecha_emi'),
                        "codigo_RS":session.get('codigo_RS'),
                        "codigo_AUX":session.get('codigo_AUX'),
                        "codigo_tRS":session.get('codigo_tRS'),
                        "codigo_tSCM":session.get('codigo_tSCM'),
                        "codigo_t":session.get('codigo_t'),
                        "codigo_h":session.get('codigo_h'),
                        "codigo_p":session.get('codigo_p'),
                        "realizar_ajuste":session.get('ajuste'),
                        "valvula_drenaje":session.get('valvula_drenaje'),
                        "marca":session.get('marca'),
                        "modelo":session.get('modelo'),
                        "nro_serie":session.get('nro_serie'),
                        "procedencia":session.get('proced'),
                        "color":session.get('color'),
                        "clase":session.get('clase'),
                        "tipo_SCM":session.get('tipo'),
                        "material_SCM":session.get('material'),
                        "cod_id":session.get('cod_id')+" "+session.get('cod_id_unidad'),
                        "valor_nominal":session.get('valor_nominal'), 
                        "valor_nominal_unidad":session.get('valor_nominal_unidad'),
                        "interv_ind":session.get('interval_ind')+" "+session.get('interval_ind_unidad'),
                        "res":str(int(session.get('resolucion'))),
                        "res_unidad":session.get('resolucion_unidad'),
                        "material_RS":session.get('material_RS'),
                        "coeff_material_RS":coef_material[session.get('material_RS')],
                        "coeff_material_SCM":coef_material[session.get('material')],
                        "ancho": session.get('ancho_escala'),
                        "ancho_unidad": session.get('ancho_escala_unidad'),
                        "diametro":session.get('diametro_cuello'),
                        "diametro_unidad": session.get('diametro_cuello_unidad'),
                        "sensibilidad":session.get('espaciamiento_marcas'),
                        "sensibilidad_unidad":session.get('espaciamiento_marcas_unidad'),
                        })
        
        # conversion
        flash(f'Registro almacenado correctamente!', 'success')
        return redirect(url_for('pre'))
    return render_template('registro.html', form=form)

@app.route('/pre', methods=['GET', 'POST'])
def pre():
    form = PreForm()
    if form.validate_on_submit():
        guardar_datos("pre",
                      {
                        "nro_certificado":session.get('nro_certificado'),
                        "p1": form.p1.data,
                        "p2": form.p2.data,
                        "p3": form.p3.data,
                        "p4": form.p4.data,
                        "p5": form.p5.data,
                        "p6": form.p6.data,
                        "p7": form.p7.data,
                        "p8": form.p8.data,
                        "p9": form.p9.data,
                        "p10": form.p10.data,
                        "p11": form.p11.data,
                        "p12": form.p12.data,
                        "p13": form.p13.data,
                        "p14": form.p14.data,
                        "c1": form.c1.data,
                        "c2": form.c2.data,
                        "c3": form.c3.data,
                        "c4": form.c4.data,
                        "c5": form.c5.data,
                        "c6": form.c6.data,
                        "c7": form.c7.data,
                        "c8": form.c8.data,
                        "c9": form.c9.data,
                        "c10": form.c10.data,
                        "c11": form.c11.data,
                        "c12": form.c12.data,
                        "c13": form.c13.data,
                        "c14": form.c14.data,
                        })


        flash(f'Datos previos almacenado correctamente!', 'success')
        return redirect(url_for('calibracion',titulo='Calibracion'))
    return render_template('pre.html', form=form)



@app.route('/calibracion/<titulo>', methods=['GET', 'POST'])
def calibracion(titulo):
    
    codigo_RS = session.get('codigo_RS')

    VN_RS, VN_RS_unidad = datos[codigo_RS]["VN"], datos[codigo_RS]["VN_unidad"]
    VN_RS, VN_RS_unidad = aLitros(VN_RS, VN_RS_unidad)
    corrRS, corrRS_unidad = datos[codigo_RS]["correccion"], datos[codigo_RS]["correccion_unidad"]
    corrRS, corrRS_unidad = aLitros(corrRS, corrRS_unidad)
    V0 = VN_RS+corrRS
    V0_unidad = "L"
    t0RS = datos[codigo_RS]["t_ref"]

    VN_SCM = float(session.get('valor_nominal').replace(",","."))
    VN_SCM_unidad = session.get('valor_nominal_unidad')

    t = 20  # °C  , temperatura de referencia del SCM
    VN_SCM, VN_SCM_unidad = aLitros(VN_SCM, VN_SCM_unidad)
  

    if VN_SCM > 100: nro_repeticiones = 2
    elif VN_SCM <= 100: nro_repeticiones = 3

    if VN_SCM >= 2000: nro_lugares = 3
    elif VN_SCM >= 500: nro_lugares = 2
    else: nro_lugares = 1
  
    N = round(VN_SCM/VN_RS) 

    if session.get('valvula_drenaje') == 'SI': encabezados = ["Temperatura patrón","Temperatura calibrando","Volumen agregado/retirado","tiempo goteo","tiempo entrega"]
    else: encabezados = ["tRS","tSCM","ΔV"]


    # Creando dinamicamente los inputs de la columna tRS
    lista = []
    lista_total = []
    for i in range(nro_repeticiones):
        for j in range(N):
            lista.append(f'tRS_{i+1}_{j+1}')
        lista_total.append(lista)
    for l in lista_total:
        for e in l:
            setattr(CalibracionForm, e, StringField('', validators=[DataRequired()]))

    # Creando dinamicamente los inputs de la columna tSCM
    lista = []
    lista_total = []
    for i in range(nro_repeticiones):
        for j in range(nro_lugares):
            lista.append(f'tSCM_{i+1}_{j+1}')
        lista_total.append(lista)
    for l in lista_total:
        for e in l:
            setattr(CalibracionForm, e, StringField('', validators=[DataRequired()]))

    # Creando dinamicamente los inputs de la columna deltaV
    lista = []
    for i in range(nro_repeticiones):
        lista.append(f'deltaV_{i+1}_1')
    for e in lista:
        setattr(CalibracionForm, e, StringField('', validators=[DataRequired()]))

    # Crenado dinamicamente los inputs de las unidades de tg y te
    if session.get('valvula_drenaje') == "SI":
        # Creando dinamicamente los inputs de la columna tg
        lista = []
        for i in range(nro_repeticiones):
            lista.append(f'tg_{i+1}_1')
        for e in lista:
            setattr(CalibracionForm, e, StringField('', validators=[DataRequired()]))

        # Creando dinamicamente los inputs de la columna te
        lista = []
        for i in range(nro_repeticiones):
            lista.append(f'te_{i+1}_1')
        for e in lista:
            setattr(CalibracionForm, e, StringField('', validators=[DataRequired()]))

        setattr(CalibracionForm, 'tg_unidad', SelectField('', choices=[('s','s'),('min','min'),('h','h')]))
        setattr(CalibracionForm, 'te_unidad', SelectField('', choices=[('s','s'),('min','min'),('h','h')]))
        
    # Que sea requerido cuando sea la ultima calibracion
    if session.get('ajuste') == "NO":
        # Creando dinamicamente los inputs 
       
        setattr(CalibracionForm, 'nro_marcas_sup', IntegerField('N° marcas superiores', validators=[DataRequired(), NumberRange(min=1, message='Debe ser mayor o igual a 1')]))
        setattr(CalibracionForm, 'nro_marcas_inf', IntegerField('N° marcas inferiores', validators=[DataRequired(), NumberRange(min=1, message='Debe ser mayor o igual a 1')]))
        session['nombre']=""
    else:
        # Creando dinamicamente los inputs 
        setattr(CalibracionForm, 'nro_marcas_sup', IntegerField('N° marcas superiores'))
        setattr(CalibracionForm, 'nro_marcas_inf', IntegerField('N° marcas inferiores'))
        session['nombre']="_antes_ajuste"

    form = CalibracionForm()
    
    if form.validate_on_submit():

        session['t_inicial']=corregir(session.get('codigo_t'),form.t_inicial.data.replace(",","."))
        session['t_final']=corregir(session.get('codigo_t'),form.t_final.data.replace(",","."))
        session['h_inicial']=corregir(session.get('codigo_h'),form.h_inicial.data.replace(",","."))
        session['h_final']=corregir(session.get('codigo_h'),form.h_final.data.replace(",","."))
        session['p_inicial']=corregir(session.get('codigo_p'),form.p_inicial.data.replace(",","."))
        session['p_final']=corregir(session.get('codigo_p'),form.p_final.data.replace(",","."))
        session['t_unidad']=form.t_unidad.data
        session['h_unidad']=form.h_unidad.data
        session['p_unidad']=form.p_unidad.data
        session['t1_unidad']=form.t1_unidad.data
        session['t2_unidad']=form.t2_unidad.data
        session['deltaV_unidad']=form.deltaV_unidad.data

        session['nombre_calibracion'] = "calibracion"+session.get('nombre')
  
        guardar_datos(session.get('nombre_calibracion'),{
            "nro_certificado":session.get('nro_certificado'),
            "t_inicial_":form.t_inicial.data,
            "t_final_":form.t_final.data,
            "h_inicial_":form.h_inicial.data,
            "h_final_":form.h_final.data,
            "p_inicial_":form.p_inicial.data,
            "p_final_":form.p_final.data,
            "t_unidad_":form.t_unidad.data,
            "h_unidad_":form.h_unidad.data,
            "p_unidad_":form.p_unidad.data,
            "t1_unidad_":form.t1_unidad.data,
            "t2_unidad_":form.t2_unidad.data,
            "deltaV_unidad_":form.deltaV_unidad.data
        })


        if session.get('valvula_drenaje') == "SI":
            session['tg_unidad']=form.tg_unidad.data
            session['te_unidad']=form.te_unidad.data
            agregar_datos(session.get('nombre_calibracion'),"tg_unidad",session.get('tg_unidad'))
            agregar_datos(session.get('nombre_calibracion'),"te_unidad",session.get('te_unidad'))


        agregar_datos("informacion","t_inicial",str(round(float(session.get('t_inicial')),1)))
        agregar_datos("informacion","h_inicial",str(round(float(session.get('h_inicial')))))
        agregar_datos("informacion","p_inicial",str(round(session.get('p_inicial'),1)))
        agregar_datos("informacion","t_final",str(round(float(session.get('t_final')),1)))
        agregar_datos("informacion","h_final",str(round(float(session.get('h_final')))))
        agregar_datos("informacion","p_final",str(round(session.get('p_final'),1)))
        agregar_datos("informacion","t_unidad",session.get('t_unidad'))
        agregar_datos("informacion","h_unidad",session.get('h_unidad'))
        agregar_datos("informacion","p_unidad",session.get('p_unidad'))
     
                        
        
        print("t_inicial: %s %s" % (session.get('t_inicial'),session.get('t_unidad')))
        print("t_final: %s %s" % (session.get('t_final'),session.get('t_unidad')))
        print("h_inicial: %s %s" % (session.get('h_inicial'),session.get('t_unidad')))
        print("h_final: %s %s" % (session.get('h_final'),session.get('h_unidad')))
        print("p_inicial: %s %s" % (session.get('p_inicial'),session.get('h_unidad')))
        print("p_final: %s %s" % (session.get('p_final'),session.get('p_unidad')))
        # aplicar conversion de ser necesario
        ta = (session.get('t_inicial')+session.get('t_final'))/2
        print("ta: %s %s" % (ta, session.get('t_unidad')))

        try:
            # tRS
            tRS_N = []
            tRS_N_ = [] # guardara cada celda
            tRS = []
            tRS_ = [] # guardara cada grupo de celdas
            tmin_RS = []
            tmax_RS = []
            for i in range(nro_repeticiones):
                for j in range(N):
                    session[f'tRS_{i+1}_{j+1}']=getattr(form, f'tRS_{i+1}_{j+1}').data
                    tRS_N.append(corregir(session.get('codigo_tRS'),float((session.get(f'tRS_{i+1}_{j+1}')).replace(",","."))))
                    tRS_N_.append(session.get(f'tRS_{i+1}_{j+1}'))
                tmin_RS.append(min(tRS_N))
                tmax_RS.append(max(tRS_N))
                tRS.append(promediar(tRS_N))  # tRS tendra elementos correspondiante al numero de repeticiones
                tRS_.append(tRS_N_) # para calibracion.json
                tRS_N = []
                tRS_N_ = []
            print("tRS: ",tRS)
            print("tmin_RS: ", min(tmin_RS))
            print("tmax_RS: ", max(tmax_RS))
            agregar_datos(session.get('nombre_calibracion'),"tRS_", str(tRS_))

            # tSCM
            tSCM_L = []
            tSCM_L_ = [] # guardara todas las celdas
            tSCM = []
            tSCM_ = []  # guardara el grupo de todas celdas
            tmin_SCM = []
            tmax_SCM = []
            for i in range(nro_repeticiones):
                for j in range(nro_lugares):
                    session[f'tSCM_{i+1}_{j+1}']=getattr(form, f'tSCM_{i+1}_{j+1}').data
                    tSCM_L.append(corregir(session.get('codigo_tSCM'),float((session.get(f'tSCM_{i+1}_{j+1}')).replace(",","."))))
                    tSCM_L_.append(session.get(f'tSCM_{i+1}_{j+1}'))
                tmin_SCM.append(min(tSCM_L))
                tmax_SCM.append(max(tSCM_L))
                tSCM.append(promediar(tSCM_L)) # tSCM tendra elementos correspondiante al numero de repeticiones
                tSCM_.append(tSCM_L_)# para calibracion.json
                tSCM_L = []
                tSCM_L_ = []
            print("tSCM: ", tSCM)
            print("tmin_SCM: ", min(tmin_SCM))
            print("tmax_SCM: ", min(tmax_SCM))
            agregar_datos(session.get('nombre_calibracion'),"tSCM_", str(tSCM_))


            # deltaV
            deltaV = []
            deltaV_ = []
            for i in range(nro_repeticiones):
                session[f'deltaV_{i+1}_1']=getattr(form, f'deltaV_{i+1}_1').data
                deltaV.append(float(session.get(f'deltaV_{i+1}_1').replace(",",".")))
                deltaV_.append(session.get(f'deltaV_{i+1}_1'))
            # convirtiendo a Litros
            deltaV, deltaV_unidad = aLitros(deltaV, session.get('deltaV_unidad'))
            print("deltaV: %s %s " % (deltaV, deltaV_unidad))
            agregar_datos(session.get('nombre_calibracion'),"deltaV_", str(deltaV_))

        except:
            print("Hubo un error al recepcionar los datos de tRS, tSCM o deltaV.")
            pass
        if session.get('valvula_drenaje') == "SI":
            try:
                # tg
                tg = []
                tg_ = []
                for i in range(nro_repeticiones):
                    session[f'tg_{i+1}_1']=getattr(form, f'tg_{i+1}_1').data
                    tg.append(float(session.get(f'tg_{i+1}_1').replace(",",".")))
                    tg_.append(session.get(f'tg_{i+1}_1'))
                print("tg: ",promediar(tg))
                agregar_datos("informacion","tiempo_goteo",str(round(promediar(tg))))
                agregar_datos(session.get('nombre_calibracion'),"tiempo_goteo",str(tg_))
                # te
                te = []
                te_ = []
                for i in range(nro_repeticiones):
                    session[f'te_{i+1}_1']=getattr(form, f'te_{i+1}_1').data
                    te.append(float(session.get(f'te_{i+1}_1').replace(",",".")))
                    te_.append(session.get(f'te_{i+1}_1'))
                print("te: ",promediar(te))
                agregar_datos("informacion","tiempo_entrega",str(round(promediar(te))))
                agregar_datos(session.get('nombre_calibracion'),"tiempo_entrega",str(te_))
            except:
                pass

        try:
            session['nro_marcas_sup']=form.nro_marcas_sup.data
            session['nro_marcas_inf']=form.nro_marcas_inf.data
            print("N° marcas sup: ",session.get('nro_marcas_sup'))
            print("N° marcas inf: ",session.get('nro_marcas_inf'))
        except:
            pass

        """Determinación de Vt
        """
        listaVt = []
        for i in range(nro_repeticiones):
            #print("Este es el deltaV: ", deltaV[i])
            listaVt.append(V_t(N,V0,coef_material[session.get('material_RS')],t0RS,tRS[i],beta(tRS[i],tSCM[i]),tSCM[i],coef_material[session.get('material')],t,deltaV[i]))
        listaVt_unidad = "L"

        print("Volumen obtenido Vt: ", listaVt)
        session['Vt']=promediar(listaVt)

        print("\n---------- Presupuesto de incertidumbre ----------")
        # iniciando los calculos
        #print("--------------------------- Lo que entra ---------------------------")
        #printLista([N,codigo_RS,session.get('codigo_tRS'),min(tmin_RS),max(tmax_RS),ta,promediar(tRS),session.get('codigo_tSCM'),min(tmin_SCM), max(tmax_SCM), promediar(tSCM),
        #           session.get('material_RS'), session.get('material'), session.get('codigo_AUX'), session.get('ancho_escala'), session.get('ancho_escala_unidad'),session.get('diametro_cuello'),session.get('diametro_cuello_unidad'),
        #           listaVt, listaVt_unidad, VN_SCM, VN_SCM_unidad, t0RS, t, V0])
        
        U_Vt_valor,k,veff,u_deltaVmen_valor,desv_estandar,nro_repeticiones = \
        iniciar_calculos(N=N, 
                        codigo_RS=codigo_RS, 
                        codigo_tRS=session.get('codigo_tRS'), tmin_RS=min(tmin_RS), tmax_RS=max(tmax_RS), ta=ta, tRS=promediar(tRS),
                        codigo_tSCM=session.get('codigo_tSCM'), tmin_SCM=min(tmin_SCM), tmax_SCM=max(tmax_SCM), tSCM=promediar(tSCM),
                        material_RS=session.get('material_RS'), material_SCM=session.get('material'),
                        codigo_AUX=session.get('codigo_AUX'),
                        ancho=session.get('ancho_escala'),ancho_unidad=session.get('ancho_escala_unidad'), diametro=session.get('diametro_cuello'), diametro_unidad=session.get('diametro_cuello_unidad'),
                        listaVt=listaVt,listaVt_unidad=listaVt_unidad, # debido a 3 repeticiones
                        VN_SCM=VN_SCM,VN_SCM_unidad=VN_SCM_unidad,
                        t0RS=t0RS,t=t,
                        V0=V0,
                        nombre_presupuesto="presupuesto"+session.get('nombre'),
                        nro_repeticiones=nro_repeticiones,nro_certificado=session.get('nro_certificado'),modificacion=False)

        guardar_resultados(VN_SCM,VN_SCM_unidad,listaVt,listaVt_unidad,
                           U_Vt_valor,k,veff,u_deltaVmen_valor,desv_estandar,nro_repeticiones,nombre="resultados"+session.get('nombre'),
                           nro_certificado=session.get('nro_certificado'))
        print("----------------------------------------------------")

        if session.get('ajuste') == "SI":
            Vt = promediar(listaVt)
            Vt_unidad = listaVt_unidad
            E, E_unidad = VN_SCM - Vt, "L"
            Volumen = promediar(deltaV) + E
            Volumen_unidad = "L"

            flash('¡Empecemos con el ajuste de la escala!', 'warning')
            flash('Llene el calibrando hasta la marca nominal o cero', 'info')
            flash(f'Retire un volumen equivalente a: {str(round(Volumen,5)).replace(".",",")} {Volumen_unidad} ', 'info')
            flash('Desplaze la marca cero hasta la base del menisco', 'info')
            flash('¡Es necesario realizar nuevamente la calibración!', 'warning')
            session['ajuste']  = "NO"
            session['nombre'] = "_despues_ajuste"


            return redirect(url_for('calibracion',titulo='2da Calibración'))
        else:
            flash('Llene el calibrando hasta el cero.','warning')
            session['nro_marcas_sup'] = form.nro_marcas_sup.data
            session['nro_marcas_inf'] = form.nro_marcas_inf.data

            

            return redirect(url_for('calibracion_escala'))


    return render_template('calibracion.html', form=form, N=N, 
                            nro_repeticiones=nro_repeticiones,
                            nro_lugares=nro_lugares,
                            encabezados=encabezados, valvula_drenaje=session.get('valvula_drenaje'),
                            ajuste=session.get('ajuste'),
                            titulo=titulo,
                           )

@app.route('/calibracion_escala',methods=['GET','POST'])
def calibracion_escala():
    # Creando dinamicamente los inputs de la columna Volumen agregado
    lista = []
    for i in range(int(session.get('nro_marcas_sup'))):
        lista.append(f'vol_sup_{i+1}')
    for e in lista:
        setattr(ModelForm, e, StringField('', validators=[DataRequired()]))

    # Creando dinamicamente los inputs de la columna Volumen removido    
    lista = []
    for i in range(int(session.get('nro_marcas_inf'))):
        lista.append(f'vol_inf_{i+1}')
    for e in lista:
        setattr(ModelForm, e, StringField('', validators=[DataRequired()]))

    # Creando el input para el numero de decimales
    setattr(ModelForm, 'nro_decimales', IntegerField("Número de decimales", validators=[DataRequired(), NumberRange(min=0,max=5)], render_kw={"step": "1"}))

    form = ModelForm()
    if form.validate_on_submit():
        session['vol_agregado_unidad']=form.vol_agregado_unidad.data
        session['vol_removido_unidad']=form.vol_removido_unidad.data

        # Volumen agregado 
        vol_sup = 0
        vol_sup_acumulado = 0
        lista_Vt_sup = []
        vol_sup_ = []

        # la correccion debera estar en las unidades de vol_agregado_unidad
        correccion = datos[session.get('codigo_AUX')]['correccion']
        correccion_unidad = datos[session.get('codigo_AUX')]['correccion_unidad']
        correccion, correccion_unidad = aUnidad(correccion, correccion_unidad, session.get('vol_agregado_unidad'))
        
        for i in range(int(session.get('nro_marcas_sup'))):
            session[f'vol_sup_{i+1}']=getattr(form, f'vol_sup_{i+1}').data
            vol_sup = float(session.get(f'vol_sup_{i+1}').replace(",",".")) + correccion
            vol_sup_.append(session.get(f'vol_sup_{i+1}'))
            vol_sup, vol_sup_unidad = aLitros(vol_sup, session.get('vol_agregado_unidad'))
            vol_sup_acumulado += vol_sup
            lista_Vt_sup.append(float(session.get('Vt'))+vol_sup_acumulado)

        print("vol_sup: ", lista_Vt_sup, vol_sup_unidad)
        agregar_datos(session.get('nombre_calibracion'),"vol_sup_",str(vol_sup_))
        agregar_datos(session.get('nombre_calibracion'),"vol_sup_unidad",session.get('vol_agregado_unidad'))
        # Volumen removido  
        vol_inf = 0
        vol_inf_acumulado = 0
        lista_Vt_inf = []
        vol_inf_ = []
        correccion, correccion_unidad = aUnidad(correccion, correccion_unidad, session.get('vol_removido_unidad'))

        for i in range(int(session.get('nro_marcas_inf'))):
            session[f'vol_inf_{i+1}']=getattr(form, f'vol_inf_{i+1}').data
            vol_inf = float(session.get(f'vol_inf_{i+1}').replace(",",".")) + correccion
            vol_inf_.append(session.get(f'vol_inf_{i+1}'))
            vol_inf, vol_inf_unidad = aLitros(vol_inf, session.get('vol_removido_unidad'))
            vol_inf_acumulado += vol_inf
            lista_Vt_inf.append(float(session.get('Vt'))-vol_inf_acumulado)
        lista_Vt_inf.reverse()
        print("vol_removido: ", lista_Vt_inf, vol_inf_unidad)
        agregar_datos(session.get('nombre_calibracion'),"vol_inf_",str(vol_inf_))
        agregar_datos(session.get('nombre_calibracion'),"vol_inf_unidad",session.get('vol_removido_unidad'))

        x = [i+1 for i in range(int(session.get('nro_marcas_inf')) + 1 + int(session.get('nro_marcas_sup')))]
        y = lista_Vt_inf + [float(session.get('Vt'))] + lista_Vt_sup
        print("Vt de las marcas: ", y, "L")
  
        x = np.array(x)
        y = np.array(y)
        m, b = np.polyfit(x, y, 1)

        resolucion = m
        resolucion_unidad = "L"
        print("resolucion: ", resolucion,"resolucion_unidad: ", resolucion_unidad)
        resolucion_unidad_informacion = extraer_datos("informacion","res_unidad")
        if resolucion_unidad_informacion == "lineas": resolucion_unidad_informacion = "ml"
        resolucion, resolucion_unidad = aUnidad(resolucion,resolucion_unidad, resolucion_unidad_informacion)
        print("resolucion: ", resolucion,"resolucion_unidad: ", resolucion_unidad)
        Vt_valor, Vt_unidad = float(session.get('Vt')), "L"
        Vt_valor, Vt_unidad = aUnidad(Vt_valor, Vt_unidad, resolucion_unidad_informacion)
        resolucion_porcentaje = (resolucion/Vt_valor)*100
        resolucion_porcentaje_unidad = "%"
      
        agregar_datos("resultados", "resolucion", str(resolucion))
        agregar_datos("resultados", "resolucion_unidad", resolucion_unidad)
        agregar_datos("resultados", "resolucion_porcentaje", str(resolucion_porcentaje))
        agregar_datos("resultados", "resolucion_porcentaje_unidad", resolucion_porcentaje_unidad)
        nro_decimales = int(form.nro_decimales.data)
        agregar_datos("informacion", "nro_decimales", nro_decimales)

        print("\n>>> Fin de la calibración de la escala.\n")

        

        # generar el certificado
        ejecutar([session.get('codigo_RS'), session.get('codigo_tRS'), session.get('codigo_tSCM'), session.get('codigo_AUX')], nro_decimales)

        return redirect(url_for('certificado'))

    return render_template('calibracion_escala.html', form=form, nro_marcas_sup=int(session.get('nro_marcas_sup')),
                           nro_marcas_inf=int(session.get('nro_marcas_inf')))

@app.route('/certificado', methods=['GET','POST'])
def certificado():

    def guardar_datos_todo(nombre, nuevos_datos):
        archivo = f"{nombre}.json"
        # Cargar los datos existentes
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as file:
                datos = json.load(file)
        else:
            datos = {}
        
        # Actualizar los datos con los nuevos datos
        datos.update(nuevos_datos)
        
        # Guardar los datos actualizados
        with open(archivo, 'w', encoding='utf-8') as file:
            json.dump(datos, file, ensure_ascii=False, indent=4, cls=DateEncoder)

    # Uso del método guardar_datos
    base_path = "data"

    for filename, key in [
        ('informacion.json', "informacion"),
        ('pre.json', "pre"),
        ('presupuesto_antes_ajuste.json', "presupuesto_antes_ajuste"),
        ('presupuesto.json', "presupuesto"),
        ('resultados_antes_ajuste.json', "resultados_antes_ajuste"),
        ('resultados.json', "resultados"),
        ('calibracion_antes_ajuste.json', "calibracion_antes_ajuste"),
        ('calibracion.json', "calibracion")
    ]:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                guardar_datos_todo(f"{base_path}/{session.get('nro_certificado')}", {key: json.load(file)})
        except:
            pass
    #combinar_archivos(["informacion","pre","presupuesto_antes_ajuste","presupuesto","resultados_antes_ajuste","resultados","calibracion_antes_ajuste","calibracion"], f"{session.get('nro_certificado')}")

    
    flash(f'Se ha almacenado todos los datos de la calibración en "data/{session.get('nro_certificado')}".','info')
    flash(f'Se ha generado el certificado en "certificados/{session.get('nro_certificado')}".','success')
    flash('Ha finalizado la calibración.','success')


    return render_template('certificado.html')

JSON_DIR = os.path.join(os.path.dirname(__file__), 'data')

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    ano_actual = datetime.datetime.now().year
    if request.method == 'POST':
        nro_certificado = request.form['nro_certificado']
        anio = request.form['anio']
        return redirect(url_for('edit', nro_certificado="MT-"+nro_certificado+"-"+anio))
    return render_template('buscar.html',ano_actual = ano_actual)

@app.route('/edit/<nro_certificado>', methods=['GET', 'POST'])
def edit(nro_certificado):
    json_file_path = os.path.join(JSON_DIR, f'{nro_certificado}.json')
    if not os.path.exists(json_file_path):
        flash(f"No se ha encontrado el certificado", 'warning')
        return redirect(url_for('buscar'))

    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if request.method == 'POST':
        # se debe generar una copia del json original y a ese aplicarle la actualizacion 
        archivo_origen = f"data/{nro_certificado}.json"
        nro_certificado_nuevo = request.form['nro_certificado_nuevo']
        archivo_destino = f"data/{nro_certificado_nuevo}.json"

        copiar_json(archivo_origen, archivo_destino)

        json_file_path = os.path.join(JSON_DIR, f'{nro_certificado_nuevo}.json')
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

    
        # Actualizar datos con los valores del formulario
        for section in data:
            for key in data[section]:
                form_key = f"{section}[{key}]"
                if form_key in request.form:
                    data[section][key] = request.form[form_key]

        # Guardar cambios en el archivo JSON
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

        # se deben actualizar los presupuestos y resultados acorde a los datos nuevos
        from actualizar_presupuesto_resultados import actualizar
        actualizar(nro_certificado_nuevo)
        session['nro_certificado_nuevo'] = nro_certificado_nuevo

        comentario = request.form['comentario'].split('\n')
        nro_decimales = extraer_datos(f"data/{nro_certificado_nuevo}","informacion")['nro_decimales']
        comments = []
        for e in comentario:
            if e.strip() != "":
                var = separar_parrafo(130,e)
                comments.append(var)
    
        if 'comentario' in data:
            if data['comentario']['valor'] == "":
                comments = comments
            else:  
                comments = eval(data['comentario']['valor'])+comments

        agregar_datos(f"data/{nro_certificado_nuevo}","comentario",{'valor':str(comments)})
        

        generar_certificado_modificado(session.get('nro_certificado_nuevo'),comments,nro_decimales)


        flash(f"Se ha creado el certificado {nro_certificado_nuevo}",'success')
        return redirect(url_for('edit', nro_certificado=nro_certificado))

    sugerencia = colocamosLetra(nro_certificado,"A")
    return render_template('edit.html', data=data, nro_certificado=nro_certificado,sugerencia = sugerencia)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
