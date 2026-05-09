# Universidad Nacional Abierta y a Distancia - UNAD
# Curso: Programacion - Codigo: 213023A_2201
# Fase 4 - Sistema Integral de Gestion de Clientes, Servicios y Reservas
# Grupo: 213023_217


class SistemaReservasError(Exception):
    """Excepcion base del sistema Software FJ."""
    pass


class ClienteInvalidoError(SistemaReservasError):
    """Se lanza cuando los datos del cliente no superan la validacion."""
    pass


class ServicioNoDisponibleError(SistemaReservasError):
    """Se lanza cuando se intenta reservar un servicio no disponible."""
    pass


class ReservaInvalidaError(SistemaReservasError):
    """Se lanza cuando los parametros de una reserva son incorrectos."""
    pass


class DuracionInvalidaError(SistemaReservasError):
    """Se lanza cuando la duracion es cero, negativa o supera el limite permitido."""
    pass


class CapacidadExcedidaError(SistemaReservasError):
    """Se lanza cuando el numero de personas supera la capacidad de una sala."""
    pass
