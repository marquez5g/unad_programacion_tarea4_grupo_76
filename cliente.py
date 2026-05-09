# Universidad Nacional Abierta y a Distancia - UNAD
# Curso: Programacion - Codigo: 213023A_2201
# Fase 4 - Sistema Integral de Gestion de Clientes, Servicios y Reservas
# Grupo: 213023_217

import re
import logging
from entidades import EntidadBase
from excepciones import ClienteInvalidoError


class Cliente(EntidadBase):
    """
    Representa un cliente del sistema Software FJ.
    Encapsula datos personales con validaciones estrictas mediante
    atributos privados y propiedades con setter.
    """

    def __init__(self, nombre, identificacion, correo, telefono):
        self.__nombre = None
        self.__identificacion = None
        self.__correo = None
        self.__telefono = None
        self.nombre = nombre
        self.identificacion = identificacion
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ClienteInvalidoError("El nombre del cliente no puede estar vacio.")
        self.__nombre = valor.strip()

    @property
    def identificacion(self):
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, valor):
        if not str(valor).isdigit():
            raise ClienteInvalidoError(
                f"La identificacion '{valor}' debe contener solo digitos."
            )
        self.__identificacion = str(valor)

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        if not re.match(patron, valor):
            raise ClienteInvalidoError(
                f"El correo '{valor}' no tiene un formato valido."
            )
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not str(valor).isdigit() or len(str(valor)) < 7:
            raise ClienteInvalidoError(f"El telefono '{valor}' no es valido.")
        self.__telefono = str(valor)

    def validar(self):
        """Verifica que todos los campos esten correctamente definidos."""
        return all([self.__nombre, self.__identificacion, self.__correo, self.__telefono])

    def mostrar_info(self):
        return (
            f"Cliente: {self.__nombre} | ID: {self.__identificacion} "
            f"| Correo: {self.__correo} | Tel: {self.__telefono}"
        )
