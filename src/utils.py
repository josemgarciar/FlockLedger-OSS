"""
Utilidades para FlockLedger
Funciones auxiliares y helpers
"""

from models import Explotacion, Oveja, Alta, Baja
from typing import List, Tuple
from datetime import datetime


class EstadisticasExplotacion:
    """Clase para calcular estadísticas de una explotación"""
    
    @staticmethod
    def total_ovejas(explotacion: Explotacion) -> int:
        """Total de ovejas"""
        return explotacion.total_ovejas()
    
    @staticmethod
    def ovejas_activas(explotacion: Explotacion) -> int:
        """Cantidad de ovejas sin baja"""
        return len(explotacion.obtener_ovejas_activas())
    
    @staticmethod
    def ovejas_bajas(explotacion: Explotacion) -> int:
        """Cantidad de ovejas con baja registrada"""
        return len(explotacion.obtener_ovejas_con_baja())
    
    @staticmethod
    def ovejas_por_raza(explotacion: Explotacion) -> dict:
        """Agrupar ovejas por raza"""
        razas = {}
        for oveja in explotacion.ovejas:
            if oveja.raza not in razas:
                razas[oveja.raza] = []
            razas[oveja.raza].append(oveja)
        return razas
    
    @staticmethod
    def ovejas_por_sexo(explotacion: Explotacion) -> dict:
        """Agrupar ovejas por sexo"""
        sexos = {}
        for oveja in explotacion.ovejas:
            if oveja.sexo not in sexos:
                sexos[oveja.sexo] = []
            sexos[oveja.sexo].append(oveja)
        return sexos
    
    @staticmethod
    def ovejas_por_procedencia(explotacion: Explotacion) -> dict:
        """Agrupar ovejas por procedencia de alta"""
        procedencias = {}
        for oveja in explotacion.ovejas:
            if oveja.alta and oveja.alta.procedencia:
                proc = oveja.alta.procedencia
                if proc not in procedencias:
                    procedencias[proc] = []
                procedencias[proc].append(oveja)
        return procedencias
    
    @staticmethod
    def ovejas_por_destino_baja(explotacion: Explotacion) -> dict:
        """Agrupar ovejas por destino de baja"""
        destinos = {}
        for oveja in explotacion.ovejas:
            if oveja.baja and oveja.baja.destino:
                dest = oveja.baja.destino
                if dest not in destinos:
                    destinos[dest] = []
                destinos[dest].append(oveja)
        return destinos
    
    @staticmethod
    def causas_alta(explotacion: Explotacion) -> dict:
        """Agrupar ovejas por causa de alta"""
        causas = {}
        for oveja in explotacion.ovejas:
            if oveja.alta and oveja.alta.causa:
                causa = oveja.alta.causa
                if causa not in causas:
                    causas[causa] = 0
                causas[causa] += 1
        return causas
    
    @staticmethod
    def causas_baja(explotacion: Explotacion) -> dict:
        """Agrupar ovejas por causa de baja"""
        causas = {}
        for oveja in explotacion.ovejas:
            if oveja.baja and oveja.baja.causa:
                causa = oveja.baja.causa
                if causa not in causas:
                    causas[causa] = 0
                causas[causa] += 1
        return causas


class ValidadorDatos:
    """Validar datos de ovejas"""
    
    @staticmethod
    def validar_oveja(oveja: Oveja) -> Tuple[bool, List[str]]:
        """
        Validar datos de una oveja
        Retorna (es_valida, lista_de_errores)
        """
        errores = []
        
        if not oveja.identificacion:
            errores.append("Identificación es requerida")
        
        if oveja.ano_nacimiento <= 0:
            errores.append("Año de nacimiento debe ser mayor a 0")
        
        if oveja.ano_nacimiento > datetime.now().year:
            errores.append("Año de nacimiento no puede ser en el futuro")
        
        if not oveja.raza:
            errores.append("Raza es requerida")
        
        if not oveja.sexo:
            errores.append("Sexo es requerido")
        
        if oveja.sexo not in ['M', 'H', '-']:
            errores.append("Sexo debe ser M (Macho), H (Hembra) o - (no especificado)")
        
        # Validar Alta si existe
        if oveja.alta:
            if not oveja.alta.causa:
                errores.append("Alta: Causa es requerida")
            if not oveja.alta.fecha:
                errores.append("Alta: Fecha es requerida")
        
        # Validar Baja si existe
        if oveja.baja:
            if not oveja.baja.causa:
                errores.append("Baja: Causa es requerida")
            if not oveja.baja.fecha:
                errores.append("Baja: Fecha es requerida")
        
        # Validar consistencia de fechas
        if oveja.alta and oveja.baja:
            try:
                fecha_alta = datetime.strptime(oveja.alta.fecha, "%d/%m/%Y")
                fecha_baja = datetime.strptime(oveja.baja.fecha, "%d/%m/%Y")
                if fecha_baja < fecha_alta:
                    errores.append("Fecha de baja no puede ser anterior a fecha de alta")
            except ValueError:
                errores.append("Formato de fecha inválido (use DD/MM/YYYY)")
        
        return (len(errores) == 0, errores)
    
    @staticmethod
    def validar_explotacion(explotacion: Explotacion) -> Tuple[bool, dict]:
        """
        Validar todos los datos de una explotación
        Retorna (es_valida, diccionario_de_errores_por_oveja)
        """
        errores = {}
        
        for oveja in explotacion.ovejas:
            es_valida, lista_errores = ValidadorDatos.validar_oveja(oveja)
            if not es_valida:
                errores[oveja.numero_orden] = lista_errores
        
        return (len(errores) == 0, errores)


class FormateadorDatos:
    """Formatear datos para presentación"""
    
    @staticmethod
    def formatear_fecha(fecha_str: str) -> str:
        """Formatear fecha a formato estándar DD/MM/YYYY"""
        if not fecha_str:
            return ""
        try:
            fecha = datetime.strptime(str(fecha_str), "%d/%m/%Y")
            return fecha.strftime("%d/%m/%Y")
        except ValueError:
            return str(fecha_str)
    
    @staticmethod
    def traducir_sexo(sexo: str) -> str:
        """Traducir sexo a descripción legible"""
        traducciones = {
            'M': 'Macho',
            'H': 'Hembra',
            '-': 'No especificado'
        }
        return traducciones.get(sexo, sexo)
    
    @staticmethod
    def generar_resumen_explotacion(explotacion: Explotacion) -> str:
        """Generar resumen en texto de una explotación"""
        stats = EstadisticasExplotacion()
        
        resumen = f"""
RESUMEN DE EXPLOTACIÓN
======================
Código: {explotacion.codigo}
Nombre: {explotacion.nombre or 'Sin nombre'}

ESTADÍSTICAS GENERALES:
- Total de ovejas: {stats.total_ovejas(explotacion)}
- Ovejas activas: {stats.ovejas_activas(explotacion)}
- Ovejas con baja: {stats.ovejas_bajas(explotacion)}

DISTRIBUCIÓN POR RAZA:
{FormateadorDatos._generar_tabla_dist(stats.ovejas_por_raza(explotacion))}

DISTRIBUCIÓN POR SEXO:
{FormateadorDatos._generar_tabla_dist(stats.ovejas_por_sexo(explotacion))}

CAUSAS DE ALTA:
{FormateadorDatos._generar_tabla_causas(stats.causas_alta(explotacion))}

CAUSAS DE BAJA:
{FormateadorDatos._generar_tabla_causas(stats.causas_baja(explotacion))}
"""
        return resumen
    
    @staticmethod
    def _generar_tabla_dist(diccionario: dict) -> str:
        """Helper para generar tabla de distribución"""
        if not diccionario:
            return "  (Sin datos)"
        
        tabla = ""
        for clave, ovejas in diccionario.items():
            tabla += f"  - {clave}: {len(ovejas)} ovejas\n"
        return tabla
    
    @staticmethod
    def _generar_tabla_causas(diccionario: dict) -> str:
        """Helper para generar tabla de causas"""
        if not diccionario:
            return "  (Sin datos)"
        
        tabla = ""
        for causa, cantidad in diccionario.items():
            tabla += f"  - {causa}: {cantidad}\n"
        return tabla
