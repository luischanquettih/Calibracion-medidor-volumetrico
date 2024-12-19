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
import numpy as np

def ajuste_lineal(lista_x,lista_y):
    return np.polyfit(np.array(lista_x),np.array(lista_y),1)

class Certificado:
    def __init__(self, nombre_pdf, ruta_fondo, ruta_firma, ruta_sello, nro_paginas, texto_revision):
        self.nombre_pdf = nombre_pdf
        self.ruta_fondo = ruta_fondo
        self.ruta_firma = ruta_firma
        self.ruta_sello = ruta_sello
        self.nro_paginas = nro_paginas
        self.texto_revision = texto_revision
        self.width, self.height = 595.276, 841.89#letter  # width = 612, height = 792
        self.pdf_canvas = canvas.Canvas(self.nombre_pdf, pagesize=A4)
        self.contador = 1
        self.agregarFijas()
        
    def agregarFijas(self):
        self.colocarFondo()
        self.agregarPaginacion()
        self.agregarRevision()

    def colocarFondo(self):
        current_directory = os.path.dirname(__file__)
        background_image = os.path.join(current_directory, self.ruta_fondo)
        self.pdf_canvas.drawImage(background_image, 0, 0, self.width, self.height)

    def agregarPaginacion(self):
        self.agregarTexto(f"Página {self.contador} de {self.nro_paginas}", 530, 77, bold=False)

    def agregarPaginacionCertificado(self, nro_expediente, x, y):
        self.agregarTexto(f"Certificado : {nro_expediente}", x, y)


    def agregarRevision(self):
        self.agregarTexto(self.texto_revision, 40, 75, font_size=8, bold=False)


    def agregarLineaHorizontal(self, x_position, y_position, line_length, line_thickness, line_color):
        self.pdf_canvas.setStrokeColor(line_color)
        self.pdf_canvas.setLineWidth(line_thickness)
        self.pdf_canvas.line(x_position, y_position, x_position + line_length, y_position)


    def agregarImagen(self, image_path, x, y, width, height):
        self.pdf_canvas.drawImage(image_path, x, y, width, height)

    def agregarHoja(self):
        if self.contador <= self.nro_paginas-1:
            self.pdf_canvas.showPage()
            self.colocarFondo()
            self.contador = self.contador + 1
            self.agregarTexto(f"Página {self.contador} de {self.nro_paginas}", 530, 77,bold=False)
            self.agregarRevision()
        else:
            print("No es posible crear una página más")


    def crearTablaPersonalizada(self, titulo, datos, ancho_celda, x=54 , y=222, alto_celda=10, con_grilla=False, span=None, background_color=None,
                         text_color=None, align=None, valign=None, font_name=None, font_size=None):
        
        n_row = len(datos)
        n_col = len(datos[0])

        if titulo != False: self.agregarTexto(titulo, 60, alto_celda*n_row+y + 10)

        data_table = datos
        if isinstance(alto_celda,int):
            row_heights = [alto_celda] * len(data_table)  
        
        if isinstance(ancho_celda,float or int):
            col_widths = [ancho_celda]
        col_widths = ancho_celda


        table_style = [
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0,0),(-1,-1), 8)
                ]
        if isinstance(con_grilla,bool):
            if con_grilla != False:
                table_style = [
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ('FONTSIZE', (0,0),(-1,-1), 8)
                ]
        else:
            table_style.append(('GRID',con_grilla[0],con_grilla[1], 0.5, colors.black))


        if span != None: 
            for i,e in enumerate(span):
                table_style.append(('SPAN',span[i][0],span[i][1]))

        if background_color != None:
            for e in background_color:
                for clave, valor in e.items():
                    table_style.append(('BACKGROUND', valor[0], valor[1], HexColor(clave)))
                    
                    
        if text_color != None:
            for e in text_color:
                for clave, valor in e.items():
                    table_style.append(('TEXTCOLOR', valor[0], valor[1], HexColor(clave)))

        if align != None:
            for e in align:
                for clave, valor in e.items():
                    table_style.append(('ALIGN', valor[0], valor[1], clave))


        if valign != None:
            for e in valign:
                for clave, valor in e.items():
                    table_style.append(('VALIGN', valor[0], valor[1], clave))

        if font_name != None:
            for e in font_name:
                for clave, valor in e.items():
                    table_style.append(('FONTNAME', valor[0], valor[1], clave))

        if font_size != None:
            for e in font_size:
                for clave, valor in e.items():
                    table_style.append(('FONTSIZE', valor[0], valor[1], int(clave)))

    
        table = Table(data_table, style=table_style, rowHeights=alto_celda, colWidths=ancho_celda)
        table.wrapOn(self.pdf_canvas, self.width, self.height)
        if x == "CENTER": 
            if isinstance(ancho_celda,list):
                ancho_total = sum(ancho_celda)
            else:
                ancho_total = ancho_celda*n_col
            x = self.width/2 - ancho_total/2
        table.drawOn(self.pdf_canvas, x, y) 


    def agregarTexto(self, text, x, y, font_size=8, font_name="Helvetica",bold=True, subrayado=False):
        if bold:
            self.pdf_canvas.setFont(font_name + "-Bold", font_size)
        else:
            self.pdf_canvas.setFont(font_name, font_size)
        if x=="CENTER": x=self.width/2
        self.pdf_canvas.drawString(x, y, text)

        if subrayado==True:
            text_width = self.pdf_canvas.stringWidth(text, font_name + ("-Bold" if bold else ""), font_size)
            line_y = y - 2  # Adjust the position of the underline
            self.pdf_canvas.line(x, line_y, x + text_width, line_y)
        elif subrayado == "superior":
            text_width = self.pdf_canvas.stringWidth(text, font_name + ("-Bold" if bold else ""), font_size)
            line_y = y + 8  # Adjust the position of the underline
            self.pdf_canvas.line(x, line_y, x + text_width, line_y)
        elif subrayado == "ambos":
            text_width = self.pdf_canvas.stringWidth(text, font_name + ("-Bold" if bold else ""), font_size)
            line_y = y + 8  # Adjust the position of the underline
            self.pdf_canvas.line(x, line_y, x + text_width, line_y) 
            line_y = y - 2  # Adjust the position of the underline
            self.pdf_canvas.line(x, line_y, x + text_width, line_y)


    def agregarParrafo(self, texto, x, y, width, height, font_size=8, alignment=4, auto_direccion=False, auto_solicitante=False):
        style = getSampleStyleSheet()['Normal']
        style.fontName = "Helvetica"
        style.fontSize = font_size
        style.alignment = alignment
        paragraph = Paragraph(texto, style=style)
        paragraph.wrapOn(self.pdf_canvas, width, height)
        
        ancho_parrafo, alto_parrafo = paragraph.wrap(width, height)
        fila_height = style.fontSize * 1.2  # Asumiendo una altura de fila basada en el tamaño de fuente
        
        # Calcular la cantidad de filas completas del párrafo
        cantidad_filas_completas = int(alto_parrafo / fila_height)

        extra = 0

        if auto_direccion:
            if cantidad_filas_completas > 3:
                cantidad_filas_completas = cantidad_filas_completas - 1
                extra = 0
            elif cantidad_filas_completas == 2: extra = 15
            elif cantidad_filas_completas == 1: extra = 25

            y = -12*cantidad_filas_completas + 557 +10


        if auto_solicitante:
            
            if cantidad_filas_completas == 1: y = 569 + 10
            
            elif cantidad_filas_completas == 2: y = 557 + 10

        
        paragraph.drawOn(self.pdf_canvas, x, y)
    
        return y, extra, cantidad_filas_completas

    def __repr__(self):
        return f'PDF(certificado.pdf,ruta_fondo.png,nro_páginas,titulo)'
    
    def __str__(self):
        return f'PDF(Nombre del certificado, ruta del fondo del pdf, número de páginas, titulo del pdf)'

    def guardar(self):
        self.pdf_canvas.save()
        print(f"Hay un total de {self.contador} páginas")


