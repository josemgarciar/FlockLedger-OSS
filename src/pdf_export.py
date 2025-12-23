"""
Módulo de exportación a PDF para FlockLedger
Genera reportes en PDF con la estructura de "Hoja de Identificación Individual"
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from models import Explotacion


class ExportadorPDF:
    """Clase para exportar datos a PDF"""
    
    def __init__(self, explotacion: Explotacion):
        self.explotacion = explotacion
        self.styles = getSampleStyleSheet()
        
    def generar_pdf(self, ruta_archivo: str):
        """Generar PDF con la hoja de identificación"""
        doc = SimpleDocTemplate(
            ruta_archivo,
            pagesize=landscape(A4),
            rightMargin=5*mm,
            leftMargin=5*mm,
            topMargin=15*mm,
            bottomMargin=10*mm
        )
        
        # Construir el documento
        elementos = []
        
        # Título principal - más grande y prominente
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#000000'),
            spaceAfter=12,
            alignment=1,  # Center
            fontName='Helvetica-Bold'
        )
        
        titulo = Paragraph(
            "HOJA DE IDENTIFICACIÓN INDIVIDUAL DEL GANADO OVINO-CAPRINO",
            titulo_style
        )
        elementos.append(titulo)
        
        # Información de la explotación
        info_text = f"Nº REGISTRO DE EXPLOTACIÓN: <b>{self.explotacion.codigo}</b>"
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            fontName='Helvetica'
        )
        elementos.append(Paragraph(info_text, info_style))
        elementos.append(Spacer(1, 3*mm))
        
        # Crear tabla de datos
        tabla_datos = self._construir_tabla_datos()
        elementos.append(tabla_datos)
        
        # Información de generación
        footer_text = f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            spaceAfter=2,
            topPadding=15
        )
        elementos.append(Spacer(1, 12*mm))
        elementos.append(Paragraph(footer_text, footer_style))
        
        # Generar PDF
        try:
            doc.build(elementos)
            return True, f"PDF generado correctamente: {ruta_archivo}"
        except Exception as e:
            return False, f"Error al generar PDF: {str(e)}"
    
    def _construir_tabla_datos(self):
        """Construir tabla con datos de las ovejas"""
        
        # Encabezados más cortos para mejor presentación
        encabezados = [
            'Nº Orden',
            'Identificación',
            'Año Nac.',
            'Fecha Ident.',
            'Raza',
            'Genotipiado',
            'Sexo',
            'Causa Alta',
            'Fecha Alta',
            'Procedencia',
            'Guía',
            'Causa Baja',
            'Fecha Baja',
            'Destino',
            'Guía',
            'Incidencias'
        ]
        
        # Datos
        datos_tabla = [encabezados]
        
        for oveja in self.explotacion.ovejas:
            fila = [
                str(oveja.numero_orden),
                oveja.identificacion,
                str(oveja.ano_nacimiento),
                oveja.fecha_identificacion,
                oveja.raza,
                oveja.genotipiado,
                oveja.sexo,
                oveja.alta.causa if oveja.alta else '',
                oveja.alta.fecha if oveja.alta else '',
                oveja.alta.procedencia if oveja.alta else '',
                oveja.alta.guia if oveja.alta else '',
                oveja.baja.causa if oveja.baja else '',
                oveja.baja.fecha if oveja.baja else '',
                oveja.baja.destino if oveja.baja else '',
                oveja.baja.guia if oveja.baja else '',
                ''  # Incidencias (vacío por ahora)
            ]
            datos_tabla.append(fila)
        
        # Crear tabla con mejores proporciones
        tabla = Table(
            datos_tabla,
            colWidths=[
                11*mm,   # Nº Orden
                19*mm,   # Identificación
                14*mm,   # Año Nac
                17*mm,   # Fecha Ident
                14*mm,   # Raza
                15*mm,   # Genotipiado
                11*mm,   # Sexo
                14*mm,   # Causa Alta
                15*mm,   # Fecha Alta
                15*mm,   # Procedencia
                13*mm,   # Guía
                14*mm,   # Causa Baja
                15*mm,   # Fecha Baja
                15*mm,   # Destino
                13*mm,   # Guía
                14*mm    # Incidencias
            ]
        )
        
        # Estilos mejorados - más profesionales
        tabla.setStyle(TableStyle([
            # Encabezado: fondo azul, texto blanco, negrita
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8.5),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
            ('TOPPADDING', (0, 0), (-1, 0), 7),
            
            # Bordes para encabezado
            ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.HexColor('#4472C4')),
            
            # Datos: alineación, bordes y espaciado
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7.5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
            ('LEFTPADDING', (0, 1), (-1, -1), 5),
            ('RIGHTPADDING', (0, 1), (-1, -1), 5),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
            
            # Bordes - Grid completo
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#999999')),
            
            # Línea especial debajo de encabezado
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#4472C4')),
        ]))
        
        return tabla
    
    def generar_pdf_simple(self, ruta_archivo: str):
        """Generar PDF de forma más simple usando canvas directamente"""
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        
        c = canvas.Canvas(ruta_archivo, pagesize=landscape(A4))
        c.setFont("Helvetica-Bold", 12)
        
        # Título
        c.drawString(20, 550, "HOJA DE IDENTIFICACIÓN INDIVIDUAL DEL GANADO OVINO-CAPRINO")
        
        # Información de explotación
        c.setFont("Helvetica", 10)
        c.drawString(20, 520, f"Nº REGISTRO DE EXPLOTACIÓN: {self.explotacion.codigo}")
        
        # Tabla de datos (usando reportlab Table)
        y_position = 500
        x_start = 20
        
        # Ancho de columnas
        col_widths = [30, 60, 35, 50, 30, 30, 25, 35, 40, 40, 35, 35, 40, 40, 35, 30]
        
        # Encabezados
        headers = [
            'Nº O', 'Nº Ident.', 'Año N.', 'Fecha Ident.', 'Raza', 'Genot.', 'Sexo',
            'Causa A', 'Fecha A', 'Proc.', 'Guía A', 'Causa B', 'Fecha B', 'Dest.', 'Guía B', 'Inc.'
        ]
        
        c.setFont("Helvetica-Bold", 7)
        c.setFillColor(colors.HexColor('#4472C4'))
        
        # Dibujar encabezados
        x_pos = x_start
        for i, header in enumerate(headers):
            c.drawString(x_pos, y_position, header)
            x_pos += col_widths[i]
        
        # Dibujar datos
        y_position -= 12
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.black)
        
        for oveja in self.explotacion.ovejas:
            fila_datos = [
                str(oveja.numero_orden),
                oveja.identificacion,
                str(oveja.ano_nacimiento),
                oveja.fecha_identificacion,
                oveja.raza,
                oveja.genotipiado,
                oveja.sexo,
                oveja.alta.causa if oveja.alta else '',
                oveja.alta.fecha if oveja.alta else '',
                oveja.alta.procedencia if oveja.alta else '',
                oveja.alta.guia if oveja.alta else '',
                oveja.baja.causa if oveja.baja else '',
                oveja.baja.fecha if oveja.baja else '',
                oveja.baja.destino if oveja.baja else '',
                oveja.baja.guia if oveja.baja else '',
                ''
            ]
            
            x_pos = x_start
            for i, dato in enumerate(fila_datos):
                c.drawString(x_pos, y_position, str(dato)[:10])  # Limitar longitud
                x_pos += col_widths[i]
            
            y_position -= 10
            
            # Nueva página si se alcanza el final
            if y_position < 50:
                c.showPage()
                y_position = 550
        
        # Footer
        c.setFont("Helvetica", 8)
        c.drawString(20, 20, f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        c.save()
        return True, f"PDF generado correctamente: {ruta_archivo}"


def exportar_explotacion_a_pdf(explotacion: Explotacion, ruta_archivo: str = None) -> tuple:
    """
    Función auxiliar para exportar una explotación a PDF
    
    Args:
        explotacion: Instancia de Explotacion
        ruta_archivo: Ruta del archivo PDF (si no se especifica, usa el código de la explotación)
    
    Returns:
        (exitoso: bool, mensaje: str)
    """
    if ruta_archivo is None:
        ruta_archivo = f"Explotacion_{explotacion.codigo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    exportador = ExportadorPDF(explotacion)
    return exportador.generar_pdf(ruta_archivo)
