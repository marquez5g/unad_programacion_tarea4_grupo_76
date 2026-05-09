# Universidad Nacional Abierta y a Distancia - UNAD
# Curso: Programacion - Codigo: 213023A_2201
# Fase 4 - Sistema Integral de Gestion de Clientes, Servicios y Reservas
# Grupo: 213023_217

import logging
from excepciones import ReservaInvalidaError, ServicioNoDisponibleError, DuracionInvalidaError


class Reserva:
    """
    Integra un cliente, un servicio, una duracion y un estado.
    Implementa confirmacion, cancelacion y procesamiento con manejo de excepciones.
    """

    ESTADOS_VALIDOS = ("pendiente", "confirmada", "cancelada")

    def __init__(self, cliente, servicio, duracion):
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "pendiente"
        self.__costo_total = None

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    def confirmar(self):
        """Confirma la reserva si el servicio esta disponible y los datos son validos."""
        if self.__estado != "pendiente":
            raise ReservaInvalidaError(
                f"No se puede confirmar una reserva en estado '{self.__estado}'."
            )
        try:
            self.__servicio.verificar_disponibilidad()
            self.__costo_total = self.__servicio.calcular_costo(self.__duracion)
            self.__estado = "confirmada"
        except ServicioNoDisponibleError as e:
            logging.error(f"Confirmacion fallida - servicio no disponible: {e}")
            raise
        except DuracionInvalidaError as e:
            logging.error(f"Confirmacion fallida - duracion invalida: {e}")
            raise

    def cancelar(self):
        """Cancela la reserva si aun no esta cancelada."""
        if self.__estado == "cancelada":
            raise ReservaInvalidaError("La reserva ya esta cancelada.")
        self.__estado = "cancelada"
        logging.info(f"Reserva del cliente '{self.__cliente.nombre}' cancelada.")

    def procesar(self, impuesto=0.0, descuento=0.0):
        """Procesa la reserva calculando el costo con impuestos y descuentos."""
        try:
            self.__servicio.verificar_disponibilidad()
            self.__costo_total = self.__servicio.calcular_costo(
                self.__duracion, impuesto=impuesto, descuento=descuento
            )
            self.__estado = "confirmada"
            logging.info(
                f"Reserva procesada para '{self.__cliente.nombre}'. "
                f"Costo total: ${self.__costo_total}"
            )
        except (ServicioNoDisponibleError, DuracionInvalidaError, ReservaInvalidaError) as e:
            logging.error(f"Error al procesar reserva: {e}")
            raise
        finally:
            print(f"[Proceso finalizado] Estado de la reserva: {self.__estado}")

    def mostrar_info(self):
        costo = f"${self.__costo_total}" if self.__costo_total is not None else "No calculado"
        return (
            f"Reserva - Cliente: {self.__cliente.nombre} "
            f"| Servicio: {self.__servicio.nombre} "
            f"| Duracion: {self.__duracion} | Estado: {self.__estado} "
            f"| Costo total: {costo}"
        )
