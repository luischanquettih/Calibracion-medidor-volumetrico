from forms import *
# Definimos variables y su informacion
informacion_RS = ''
for e in lista_codigo_RS: informacion_RS += e + "\n \t" + 'Descripción: '+ datos[e]['descripcion'] + '\n'

setattr(RegistrationForm, 'codigo_RS', SelectField('Medidor volumétrico patrón', 
                                                       choices=[('','-- Seleccionar --'),('MVP001','MVP001'),('MVP002','MVP002')], 
                                                       validators=[DataRequired()],
                                                       render_kw={"title": informacion_RS}))

informacion_tRS = ''
for e in lista_codigo_tRS: informacion_tRS += e + "\n \t" + 'Descripción: '+ datos[e]['descripcion'] + '\n'
setattr(RegistrationForm, 'codigo_tRS', SelectField('Termómetro patrón en el medidor volumétrico patrón', 
                                                       choices=[('','-- Seleccionar --'),('TP001','TP001')], 
                                                       validators=[DataRequired()],
                                                       render_kw={"title": informacion_tRS}))
informacion_tSCM = ''
for e in lista_codigo_tSCM: informacion_tSCM += e + "\n \t" + 'Descripción: '+ datos[e]['descripcion'] + '\n'
setattr(RegistrationForm, 'codigo_tSCM', SelectField('Termómetro patrón en el calibrando', 
                                                       choices=[('','-- Seleccionar --'),('TP002','TP002')], 
                                                       validators=[DataRequired()],
                                                       render_kw={"title": informacion_tSCM}))    
informacion_AUX = ''
for e in lista_codigo_AUX: informacion_AUX += e + "\n \t" + 'Descripción: '+ datos[e]['descripcion'] + '\n'
setattr(RegistrationForm, 'codigo_AUX', SelectField('Medidor volumétrico auxiliar', 
                                                       choices=[('','-- Seleccionar --'),('MVAP001','MVAP001')], 
                                                       validators=[DataRequired()],
                                                       render_kw={"title": informacion_AUX}))  
informacion_t = ''
for e in lista_codigo_t: informacion_t += e + "\n \t" + 'Descripción: '+ datos[e]['descripcion'] + '\n'
setattr(RegistrationForm, 'codigo_t', SelectField('Termómetro', 
                                                       choices=[('','-- Seleccionar --'),('Termometro001','Termometro001')], 
                                                       validators=[DataRequired()],
                                                       render_kw={"title": informacion_t})) 
informacion_h = ''
for e in lista_codigo_h: informacion_h += e + "\n \t" + 'Descripción: '+ datos[e]['descripcion'] + '\n'
setattr(RegistrationForm, 'codigo_h', SelectField('Higrómetro', 
                                                       choices=[('','-- Seleccionar --'),('Higrometro001','Higrometro001')], 
                                                       validators=[DataRequired()],
                                                       render_kw={"title": informacion_h})) 
informacion_p = ''
for e in lista_codigo_p: informacion_p += e + "\n \t" + 'Descripción: '+ datos[e]['descripcion'] + '\n'
setattr(RegistrationForm, 'codigo_p', SelectField('Barómetro', 
                                                       choices=[('','-- Seleccionar --'),('Barometro001','Barometro001')], 
                                                       validators=[DataRequired()],
                                                       render_kw={"title": informacion_p})) 