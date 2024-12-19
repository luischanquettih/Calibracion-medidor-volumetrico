from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, DateField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, InputRequired, NumberRange
from unidades import *
from datetime import date


class RegistrationForm(FlaskForm):
    ajuste = SelectField('¿Se realizará ajuste?', choices=[('','-- Seleccionar --'),('NO', 'NO'),('SI', 'SI')], validators=[DataRequired()])
    valvula_drenaje = SelectField('¿Posee válvula de drenaje?', choices=[('','-- Seleccionar --'),('NO', 'NO'),('SI', 'SI')], validators=[DataRequired()])
    nro_certificado = StringField('N° Certificado', validators=[DataRequired()])
    cotizacion = StringField('Cotizacion', validators=[DataRequired()])
    solicitante = StringField('Solicitante', validators=[DataRequired()])
    direccion = StringField('Direccion', validators=[DataRequired()])
    marca = StringField('Marca', validators=[DataRequired()])
    modelo = StringField('Modelo', validators=[DataRequired()])
    nro_serie = StringField('N° de Serie', validators=[DataRequired()])
    proced = StringField('Procedencia', validators=[DataRequired()])
    cod_id = StringField('Código de identificación', validators=[DataRequired()])
    cod_id_unidad = SelectField('Asignación', choices=[('','-- Seleccionar --'),('(*)','(*)')])
    color = StringField('Color', validators=[DataRequired()])
    valor_nominal = StringField('Valor nominal', validators=[DataRequired()])
    valor_nominal_unidad = SelectField('Unidad', choices=[('L','L'),('gal','gal')], validators=[DataRequired()])
    interval_ind = StringField('Intervalo de indicación ±', validators=[DataRequired()])
    interval_ind_unidad = SelectField('Unidad', choices=[('ml','ml'),('L','L'),('gal','gal'),('lineas','lineas')], validators=[DataRequired()])
    clase = StringField('Clase', validators=[DataRequired()])
    resolucion = StringField('Resolucion', validators=[DataRequired()])
    resolucion_unidad = SelectField('Unidad',choices=[('ml','ml'),('L','L'),('gal','gal'),('lineas','lineas')], validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[('','-- Seleccionar --'),('Ex','Ex'),('In','In')], validators=[DataRequired()])
    fecha_cal = DateField('Fecha de calibración', validators=[DataRequired()], default=date.today)
    fecha_emi = DateField('Fecha de emisión', validators=[DataRequired()], default=date.today)
    material = SelectField('Material', choices=alternativas_materiales, validators=[DataRequired()])
    

    #ancho_escala = FloatField('Ancho de escala', validators=[DataRequired()], render_kw={"step": "0.1"})
    ancho_escala = StringField('Ancho de escala', validators=[DataRequired()])
    ancho_escala_unidad = SelectField('Unidad',choices=[('cm','cm'),('mm','mm')], validators=[DataRequired()])
    diametro_cuello =  StringField('Diametro de cuello interno', validators=[DataRequired()])
    diametro_cuello_unidad = SelectField('Unidad',choices=[('cm','cm'),('mm','mm')], validators=[DataRequired()])
    espaciamiento_marcas = StringField('Espaciamiento entre marcas', validators=[DataRequired()])
    espaciamiento_marcas_unidad = SelectField('Unidad',choices=[('cm','cm'),('mm','mm')], validators=[DataRequired()])
    usar_valores_por_defecto = BooleanField('Valores por defecto')
                                            
    submit = SubmitField('Guardar')


class PreForm(FlaskForm):
    p1 = BooleanField('La variación máxima de la temperatura del agua este dentro de ± 1°C (laboratorio).')
    p2 = BooleanField('La variación máxima de la temperatura del agua este dentro de ± 2°C (campo).')
    p3 = BooleanField('La variación máxima de la temperatura del aire este dentro de ± 3°C.')
    p4 = BooleanField('Los recipientes deben almacenarse en el área de calibración durante al menos 6 horas antes de la calibración.')
    p5 = BooleanField('Se debe evitar la exposición a la radiación solar directa, viento y lluvia.')
    p6 = BooleanField('Los equipos para medir condiciones ambientales, deberán estar en el área de calibración y encenderse al menos 1 hora antes.')
    p7 = BooleanField('El calibrando debe ser limpiado por el cliente o por el laboratorio.')
    p8 = BooleanField('La inspección y limpieza del calibrando debe realizarse antes de la calibración.')
    p9 = BooleanField('Se debe comprobar la legibilidad y seguridad de la escala, el mecanismo de nivelación y los sellos pertinentes.')
    p10 = BooleanField('Se debe anotar la existencia de golpes, fugas en los tubos o daños.')
    p11 = BooleanField('Se recomienda realizar una verificación de fugas.')
    p12 = BooleanField('Se debe garantizar que los líquidos se entreguen fácilmente hacia y desde el estándar y que no haya bolsas, abolladuras o grietas capaces de atrapar el líquido, aire o vapor.')
    p13 = BooleanField('El calibrando se nivelará antes de que comience su calibración.')
    p14 = BooleanField('El recipiente patrón debe calibrarse con una incertidumbre al menos 3 veces menor que la incertidumbre del calibrando.')
    c1 = TextAreaField('')
    c2 = TextAreaField('')
    c3 = TextAreaField('')
    c4 = TextAreaField('')
    c5 = TextAreaField('')
    c6 = TextAreaField('')
    c7 = TextAreaField('')
    c8 = TextAreaField('')
    c9 = TextAreaField('')
    c10 = TextAreaField('')
    c11 = TextAreaField('')
    c12 = TextAreaField('')
    c13 = TextAreaField('')
    c14 = TextAreaField('')

    submit = SubmitField('Guardar')

class CalibracionForm(FlaskForm):

    t_inicial = StringField('', validators=[DataRequired()])
    t_final = StringField('', validators=[DataRequired()])
    t_unidad = SelectField('Temperatura', choices=[('°C','°C'),('K','K')])
    h_inicial = StringField('', validators=[DataRequired()])
    h_final = StringField('', validators=[DataRequired()])
    h_unidad = SelectField('Humedad', choices=[('%','%')])
    p_inicial = StringField('', validators=[DataRequired()])
    p_final = StringField('', validators=[DataRequired()])
    p_unidad = SelectField('Presión', choices=[('mbar','mbar'),('hPa','hPa')])

    t1_unidad = SelectField('',choices=[('°C','°C'),('K','K')])
    t2_unidad = SelectField('',choices=[('°C','°C'),('K','K')])
    deltaV_unidad = SelectField('',choices=[('L','L'),('gal','gal'),('ml','ml')])
    
    submit = SubmitField('Guardar')

class ModelForm(FlaskForm):
    vol_agregado_unidad = SelectField('Unidad',choices=[('','-- Seleccionado --'),('ml','ml')], validators=[DataRequired()])
    vol_removido_unidad = SelectField('Unidad',choices=[('','-- Seleccionado --'),('ml','ml')], validators=[DataRequired()])

    submit = SubmitField('Guardar')

class CertificadoForm(FlaskForm):
    submit = SubmitField('Nueva Calibración')

class EditForm(FlaskForm):
    submit2 = SubmitField('Generar Nuevo Certificado')