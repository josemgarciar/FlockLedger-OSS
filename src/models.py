"""
Modelos de datos para FlockLedger
Define las estructuras de datos para Explotación, Oveja, Alta y Baja
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, List


@dataclass
class Alta:
    """Modelo de datos para el alta de una oveja"""
    causa: str
    fecha: str
    procedencia: str
    guia: str
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Baja:
    """Modelo de datos para la baja de una oveja"""
    causa: str
    fecha: str
    destino: str
    guia: str
    
    def to_dict(self):
        return asdict(self)


@dataclass
class Oveja:
    """Modelo de datos para una oveja"""
    numero_orden: int
    identificacion: str
    ano_nacimiento: int
    fecha_identificacion: str
    raza: str
    sexo: str
    alta: Optional[Alta] = None
    baja: Optional[Baja] = None
    grupo_edad: str = ""
    genotipiado: str = ""  # Campo para indicar si está genotipiado
    
    def to_dict(self):
        """Convertir a diccionario"""
        data = {
            'Nº Orden': self.numero_orden,
            'Identificación': self.identificacion,
            'Año Nacimiento': self.ano_nacimiento,
            'Fecha Identificación': self.fecha_identificacion,
            'Raza': self.raza,
            'Sexo': self.sexo,
            'Genotipiado': self.genotipiado,
            'Grupo Edad': self.grupo_edad,
            'Causa Alta': self.alta.causa if self.alta else '',
            'Fecha Alta': self.alta.fecha if self.alta else '',
            'Procedencia': self.alta.procedencia if self.alta else '',
            'Guía Alta': self.alta.guia if self.alta else '',
            'Causa Baja': self.baja.causa if self.baja else '',
            'Fecha Baja': self.baja.fecha if self.baja else '',
            'Destino': self.baja.destino if self.baja else '',
            'Guía Baja': self.baja.guia if self.baja else '',
        }
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Crear instancia desde diccionario"""
        alta = None
        if data.get('Causa Alta') or data.get('Fecha Alta'):
            alta = Alta(
                causa=str(data.get('Causa Alta', '')),
                fecha=str(data.get('Fecha Alta', '')),
                procedencia=str(data.get('Procedencia', '')),
                guia=str(data.get('Guía Alta', ''))
            )
        
        baja = None
        if data.get('Causa Baja') or data.get('Fecha Baja'):
            baja = Baja(
                causa=str(data.get('Causa Baja', '')),
                fecha=str(data.get('Fecha Baja', '')),
                destino=str(data.get('Destino', '')),
                guia=str(data.get('Guía Baja', ''))
            )
        
        # Conversión segura de número_orden
        try:
            numero_orden = int(data.get('Nº Orden', '0'))
        except (ValueError, TypeError):
            numero_orden = 0
        
        # Conversión segura de año_nacimiento
        try:
            ano_nacimiento = int(data.get('Año Nacimiento', '0'))
        except (ValueError, TypeError):
            ano_nacimiento = 0
        
        return cls(
            numero_orden=numero_orden,
            identificacion=str(data.get('Identificación', '')),
            ano_nacimiento=ano_nacimiento,
            fecha_identificacion=str(data.get('Fecha Identificación', '')),
            raza=str(data.get('Raza', '')),
            sexo=str(data.get('Sexo', '')),
            alta=alta,
            baja=baja,
            grupo_edad=str(data.get('Grupo Edad', '')),
            genotipiado=str(data.get('Genotipiado', ''))
        )


@dataclass
class Explotacion:
    """Modelo de datos para una explotación ganadera"""
    codigo: str
    nombre: Optional[str] = None
    ovejas: List[Oveja] = None
    
    def __post_init__(self):
        if self.ovejas is None:
            self.ovejas = []
    
    def agregar_oveja(self, oveja: Oveja):
        """Agregar una oveja a la explotación"""
        self.ovejas.append(oveja)
    
    def eliminar_oveja(self, numero_orden: int):
        """Eliminar una oveja por número de orden"""
        self.ovejas = [o for o in self.ovejas if o.numero_orden != numero_orden]
    
    def obtener_oveja(self, numero_orden: int) -> Optional[Oveja]:
        """Obtener una oveja por número de orden"""
        for oveja in self.ovejas:
            if oveja.numero_orden == numero_orden:
                return oveja
        return None
    
    def obtener_ovejas_con_alta(self) -> List[Oveja]:
        """Obtener todas las ovejas con alta registrada"""
        return [o for o in self.ovejas if o.alta]
    
    def obtener_ovejas_con_baja(self) -> List[Oveja]:
        """Obtener todas las ovejas con baja registrada"""
        return [o for o in self.ovejas if o.baja]
    
    def obtener_ovejas_activas(self) -> List[Oveja]:
        """Obtener todas las ovejas sin baja registrada"""
        return [o for o in self.ovejas if not o.baja]
    
    def total_ovejas(self) -> int:
        """Obtener total de ovejas"""
        return len(self.ovejas)
    
    def to_dataframe(self):
        """Convertir explotación a DataFrame de pandas"""
        import pandas as pd
        
        if not self.ovejas:
            return pd.DataFrame()
        
        data = [oveja.to_dict() for oveja in self.ovejas]
        return pd.DataFrame(data)
    
    @classmethod
    def from_dataframe(cls, df, codigo: str, nombre: str = None):
        """Crear explotación desde DataFrame de pandas"""
        explotacion = cls(codigo=codigo, nombre=nombre)
        
        for _, row in df.iterrows():
            oveja = Oveja.from_dict(row.to_dict())
            explotacion.agregar_oveja(oveja)
        
        return explotacion


class RepositorioExplotaciones:
    """Repositorio para gestionar múltiples explotaciones"""
    
    def __init__(self):
        self.explotaciones: dict = {}
    
    def agregar_explotacion(self, explotacion: Explotacion):
        """Agregar una explotación al repositorio"""
        self.explotaciones[explotacion.codigo] = explotacion
    
    def obtener_explotacion(self, codigo: str) -> Optional[Explotacion]:
        """Obtener una explotación por código"""
        return self.explotaciones.get(codigo)
    
    def eliminar_explotacion(self, codigo: str):
        """Eliminar una explotación"""
        if codigo in self.explotaciones:
            del self.explotaciones[codigo]
    
    def obtener_todas(self) -> List[Explotacion]:
        """Obtener todas las explotaciones"""
        return list(self.explotaciones.values())
    
    def obtener_codigos(self) -> List[str]:
        """Obtener códigos de todas las explotaciones"""
        return list(self.explotaciones.keys())
    
    def cantidad_explotaciones(self) -> int:
        """Obtener cantidad de explotaciones"""
        return len(self.explotaciones)
