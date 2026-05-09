# Universidad Nacional Abierta y a Distancia - UNAD
# Curso: Programacion - Codigo: 213023A_2201
# Fase 4 - Sistema Integral de Gestion de Clientes, Servicios y Reservas
# Grupo: 213023_217

from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad del sistema."""

    @abstractmethod
    def validar(self):
        """Valida que la entidad tenga datos correctos."""
        pass

    @abstractmethod
    def mostrar_info(self):
        """Retorna una representacion textual de la entidad."""
        pass
