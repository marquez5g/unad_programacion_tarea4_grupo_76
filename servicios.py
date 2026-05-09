# Universidad Nacional Abierta y a Distancia - UNAD
# Curso: Programacion - Codigo: 213023A_2201
# Fase 4 - Sistema Integral de Gestion de Clientes, Servicios y Reservas
# Grupo: 213023_217

from abc import abstractmethod
from entidades import EntidadBase
from excepciones import (
    ServicioNoDisponibleError,
    CapacidadExcedidaError,
    ReservaInvalidaError,
    DuracionInvalidaError,
)


class Servicio(EntidadBase):
    """Clase abstracta que representa un servicio ofrecido por Software FJ."""

    def __init__(self, nombre, disponible=True):
        self.__nombre = nombre
        self.__disponible = disponible

    @property
    def nombre(self):
        return self.__nombre

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        self.__disponible = bool(valor)

    def verificar_disponibilidad(self):
        if not self.__disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.__nombre}' no esta disponible en este momento."
            )

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        pass

    @abstractmethod
    def describir(self):
        pass

    def validar(self):
        return bool(self.__nombre)

    def mostrar_info(self):
        estado = "Disponible" if self.__disponible else "No disponible"
        return f"Servicio: {self.__nombre} | Estado: {estado}"


class ReservaSala(Servicio):
    """
    Servicio de reserva de salas de trabajo o reunion.
    El costo se calcula multiplicando el precio por hora por la duracion en horas.
    """

    def __init__(self, nombre_sala, capacidad, precio_por_hora, equipamiento="Basico"):
        super().__init__(nombre_sala)
        if capacidad <= 0:
            raise ReservaInvalidaError("La capacidad de la sala debe ser mayor que cero.")
        if precio_por_hora <= 0:
            raise ReservaInvalidaError("El precio por hora debe ser mayor que cero.")
        self.__capacidad = capacidad
        self.__precio_por_hora = precio_por_hora
        self.__equipamiento = equipamiento

    def verificar_capacidad(self, num_personas):
        if num_personas > self.__capacidad:
            raise CapacidadExcedidaError(
                f"La sala tiene capacidad para {self.__capacidad} personas; "
                f"se solicitaron {num_personas}."
            )

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        """
        Calcula el costo de la reserva de sala.
        duracion: numero de horas.
        impuesto: porcentaje de IVA (ej. 0.19 para 19%).
        descuento: porcentaje de descuento (ej. 0.10 para 10%).
        """
        if duracion <= 0:
            raise DuracionInvalidaError("La duracion debe ser mayor que cero.")
        costo_base = self.__precio_por_hora * duracion
        costo_con_descuento = costo_base * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)
        return round(costo_final, 2)

    def describir(self):
        return (
            f"Sala: {self.nombre} | Capacidad: {self.__capacidad} personas "
            f"| Precio: ${self.__precio_por_hora}/hora | Equipamiento: {self.__equipamiento}"
        )


class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos tecnologicos.
    El costo se calcula multiplicando el precio por dia por la duracion en dias.
    """

    def __init__(self, nombre_equipo, tipo_equipo, precio_por_dia, estado="Disponible"):
        super().__init__(nombre_equipo)
        if precio_por_dia <= 0:
            raise ReservaInvalidaError("El precio por dia debe ser mayor que cero.")
        self.__tipo_equipo = tipo_equipo
        self.__precio_por_dia = precio_por_dia
        self.__estado_equipo = estado

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        """
        Calcula el costo del alquiler de equipo.
        duracion: numero de dias.
        impuesto: porcentaje de IVA.
        descuento: porcentaje de descuento.
        """
        if duracion <= 0:
            raise DuracionInvalidaError("La duracion en dias debe ser mayor que cero.")
        costo_base = self.__precio_por_dia * duracion
        costo_con_descuento = costo_base * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)
        return round(costo_final, 2)

    def describir(self):
        return (
            f"Equipo: {self.nombre} | Tipo: {self.__tipo_equipo} "
            f"| Precio: ${self.__precio_por_dia}/dia | Estado: {self.__estado_equipo}"
        )


class AsesoriaEspecializada(Servicio):
    """
    Servicio de asesoria profesional especializada.
    El costo se calcula multiplicando el precio por hora por la duracion en horas.
    """

    def __init__(self, area, nombre_asesor, precio_por_hora, nivel_expertise="Junior"):
        super().__init__(f"Asesoria en {area}")
        if precio_por_hora <= 0:
            raise ReservaInvalidaError("El precio por hora debe ser mayor que cero.")
        self.__area = area
        self.__nombre_asesor = nombre_asesor
        self.__precio_por_hora = precio_por_hora
        self.__nivel_expertise = nivel_expertise

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
        """
        Calcula el costo de la asesoria.
        duracion: numero de horas.
        impuesto: porcentaje de IVA.
        descuento: porcentaje de descuento.
        """
        if duracion <= 0:
            raise DuracionInvalidaError("La duracion de la asesoria debe ser mayor que cero.")
        costo_base = self.__precio_por_hora * duracion
        costo_con_descuento = costo_base * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)
        return round(costo_final, 2)

    def describir(self):
        return (
            f"Asesoria: {self.__area} | Asesor: {self.__nombre_asesor} "
            f"| Precio: ${self.__precio_por_hora}/hora | Nivel: {self.__nivel_expertise}"
        )
