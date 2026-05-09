# Universidad Nacional Abierta y a Distancia - UNAD
# Curso: Programacion - Codigo: 213023A_2201
# Fase 4 - Sistema Integral de Gestion de Clientes, Servicios y Reservas
# Grupo: 213023_217

import logging
from excepciones import (
    ClienteInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    DuracionInvalidaError,
    CapacidadExcedidaError,
)
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva

# Configuracion del sistema de logs
logging.basicConfig(
    filename="sistema_logs.txt",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
)

if __name__ == "__main__":
    print("=" * 60)
    print("  SISTEMA SOFTWARE FJ - GESTION DE CLIENTES Y RESERVAS")
    print("=" * 60)

    # OPERACION 1: Registro valido de cliente 1
    print("\n[OP 1] Registrando cliente valido...")
    try:
        cliente1 = Cliente("Ana Torres", "1001234567", "ana.torres@email.com", "3101234567")
        logging.info(f"Cliente creado: {cliente1.mostrar_info()}")
        print("OK:", cliente1.mostrar_info())
    except ClienteInvalidoError as e:
        logging.error(f"Error al crear cliente 1: {e}")
        print("ERROR:", e)

    # OPERACION 2: Registro valido de cliente 2
    print("\n[OP 2] Registrando cliente valido...")
    try:
        cliente2 = Cliente("Carlos Ruiz", "9876543210", "carlos.ruiz@empresa.com", "3209876543")
        logging.info(f"Cliente creado: {cliente2.mostrar_info()}")
        print("OK:", cliente2.mostrar_info())
    except ClienteInvalidoError as e:
        logging.error(f"Error al crear cliente 2: {e}")
        print("ERROR:", e)

    # OPERACION 3: Intento de registro con nombre vacio (debe fallar)
    print("\n[OP 3] Registrando cliente con nombre vacio (debe fallar)...")
    try:
        cliente_invalido = Cliente("", "1112223334", "invalido@email.com", "3001112233")
        print("OK:", cliente_invalido.mostrar_info())
    except ClienteInvalidoError as e:
        logging.error(f"ClienteInvalidoError capturada: {e}")
        print("EXCEPCION CAPTURADA:", e)

    # OPERACION 4: Intento de registro con correo malformado (debe fallar)
    print("\n[OP 4] Registrando cliente con correo invalido (debe fallar)...")
    try:
        cliente_correo_malo = Cliente("Luis Gomez", "4445556667", "no-es-un-correo", "3004445566")
        print("OK:", cliente_correo_malo.mostrar_info())
    except ClienteInvalidoError as e:
        logging.error(f"ClienteInvalidoError (correo invalido): {e}")
        print("EXCEPCION CAPTURADA:", e)

    # OPERACION 5: Creacion correcta de los tres tipos de servicio
    print("\n[OP 5] Creando servicios validos...")
    try:
        sala_a = ReservaSala(
            "Sala A - Ejecutiva",
            capacidad=10,
            precio_por_hora=80000,
            equipamiento="Proyector y videoconferencia",
        )
        equipo_laptop = AlquilerEquipo(
            "Laptop HP ProBook",
            tipo_equipo="Portatil",
            precio_por_dia=50000,
        )
        asesoria_dev = AsesoriaEspecializada(
            "Desarrollo de software",
            "Ing. Fernanda Perez",
            precio_por_hora=150000,
            nivel_expertise="Senior",
        )
        logging.info("Servicios creados correctamente.")
        print("OK:", sala_a.describir())
        print("OK:", equipo_laptop.describir())
        print("OK:", asesoria_dev.describir())
    except Exception as e:
        logging.error(f"Error al crear servicios: {e}")
        print("ERROR:", e)

    # OPERACION 6: Intento de crear servicio con precio negativo
    # Encadenamiento de excepciones: ValueError convertido a ReservaInvalidaError
    print("\n[OP 6] Creando sala con precio negativo (debe fallar)...")
    try:
        try:
            precio_entrada = int("-1000")
        except ValueError as e:
            raise ReservaInvalidaError(
                "El precio ingresado no es un numero valido."
            ) from e
        sala_invalida = ReservaSala("Sala B", capacidad=5, precio_por_hora=precio_entrada)
        print("OK:", sala_invalida.describir())
    except ReservaInvalidaError as e:
        logging.error(f"ReservaInvalidaError al crear servicio: {e}")
        print("EXCEPCION CAPTURADA:", e)

    # OPERACION 7: Reserva exitosa con confirmacion (try/except/else)
    print("\n[OP 7] Creando y confirmando reserva valida...")
    try:
        reserva1 = Reserva(cliente1, sala_a, duracion=3)
        reserva1.confirmar()
    except (ServicioNoDisponibleError, ReservaInvalidaError, DuracionInvalidaError) as e:
        logging.error(f"Error al confirmar reserva 1: {e}")
        print("ERROR:", e)
    else:
        logging.info(f"Reserva confirmada: {reserva1.mostrar_info()}")
        print("OK:", reserva1.mostrar_info())

    # OPERACION 8: Reserva con procesamiento, IVA 19% y descuento 10% (try/except/finally)
    print("\n[OP 8] Procesando reserva con IVA 19% y descuento 10%...")
    try:
        reserva2 = Reserva(cliente2, asesoria_dev, duracion=2)
        reserva2.procesar(impuesto=0.19, descuento=0.10)
    except Exception as e:
        logging.error(f"Error al procesar reserva 2: {e}")
        print("ERROR:", e)
    else:
        logging.info(f"Reserva procesada: {reserva2.mostrar_info()}")
        print("OK:", reserva2.mostrar_info())

    # OPERACION 9: Reserva fallida - servicio no disponible (try/except/finally)
    print("\n[OP 9] Intentando reservar servicio marcado como no disponible...")
    try:
        equipo_laptop.disponible = False
        reserva3 = Reserva(cliente1, equipo_laptop, duracion=5)
        reserva3.confirmar()
    except ServicioNoDisponibleError as e:
        logging.error(f"ServicioNoDisponibleError en reserva 3: {e}")
        print("EXCEPCION CAPTURADA:", e)
    finally:
        equipo_laptop.disponible = True  # restaurar disponibilidad

    # OPERACION 10: Cancelar una reserva y luego reintentar la cancelacion
    print("\n[OP 10] Cancelando reserva y reintentando cancelacion...")
    try:
        reserva1.cancelar()
        print("OK: Reserva cancelada.")
        reserva1.cancelar()  # debe lanzar excepcion
    except ReservaInvalidaError as e:
        logging.error(f"ReservaInvalidaError al cancelar reserva ya cancelada: {e}")
        print("EXCEPCION CAPTURADA:", e)

    print("\n" + "=" * 60)
    print("Ejecucion completa. Revisar 'sistema_logs.txt' para el registro de eventos.")
    print("=" * 60)
