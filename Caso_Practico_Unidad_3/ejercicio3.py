from datetime import datetime

class Cliente:
    # Atributo de clase para el conteo global de clientes
    _contador_clientes = 0

    def __init__(self, nombre: str, apellidos: str, fecha_nacimiento_str: str):
        # Conversión de la cadena de texto a un objeto tipo datetime/date
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y/%m/%d").date()
        except ValueError:
            raise ValueError("El formato de fecha debe ser YYYY/MM/DD")

        # Validación de la mayoría de edad (asumiendo años de 365 días)
        fecha_actual = datetime.now().date()
        dias_vividos = (fecha_actual - fecha_nacimiento).days
        edad_anos = dias_vividos // 365

        if edad_anos < 18:
            raise ValueError(f"El cliente {nombre} {apellidos} es menor de edad ({edad_anos} años). Registro denegado.")

        # Asignación de atributos de instancia
        self.nombre = nombre
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.saldo = 0.0

        # Incremento del contador global y asignación del ID único con formato de 6 dígitos
        Cliente._contador_clientes += 1
        self.id_cliente = str(Cliente._contador_clientes).zfill(6)

        # Mensaje de bienvenida
        print(f"[ALTA EXITOSA] ¡Bienvenido/a al banco, {self.nombre} {self.apellidos}! Tu ID asignado es: {self.id_cliente}")

    def saludo(self):
        """Muestra un mensaje institucional con el saldo actual del cliente."""
        print(f"Hola {self.nombre} {self.apellidos} (ID: {self.id_cliente}). Tu saldo disponible es: {self.saldo:.2f}€")

    def deposito(self, cantidad: float):
        """Ingresa dinero en la cuenta del cliente."""
        if cantidad <= 0:
            print("La cantidad a depositar debe ser superior a 0€.")
            return
        self.saldo += cantidad
        print(f"Depósito realizado: +{cantidad:.2f}€. Nuevo saldo de {self.nombre}: {self.saldo:.2f}€")

    def retirada(self, cantidad: float) -> bool:
        """Retira dinero de la cuenta si se dispone de fondos suficientes."""
        if cantidad <= 0:
            print("La cantidad a retirar debe ser positiva.")
            return False

        if self.saldo >= cantidad:
            self.saldo -= cantidad
            print(f"Retirada exitosa: -{cantidad:.2f}€. Nuevo saldo de {self.nombre}: {self.saldo:.2f}€")
            return True
        else:
            print(f"[ERROR EN RETIRADA] Saldo insuficiente para {self.nombre}. Intento de retiro: {cantidad:.2f}€ | Saldo disponible: {self.saldo:.2f}€")
            return False

    @staticmethod
    def transferencia(emisor: 'Cliente', receptor: 'Cliente', cantidad: float):
        """
        Método estático que realiza la transferencia entre dos instancias de Cliente.
        """
        print(f"\n--- Procesando Transferencia: {emisor.nombre} -> {receptor.nombre} por {cantidad:.2f}€ ---")
        if emisor.retirada(cantidad):
            receptor.deposito(cantidad)
            print("Transferencia completada con éxito.")
        else:
            print("No se pudo completar la transferencia debido a saldo insuficiente en la cuenta emisora.")


# Script de prueba y validación del sistema bancario
if __name__ == "__main__":
    print("=== PRUEBAS DEL SISTEMA BANCARIO ===")

    # 1. Creación de clientes (dos mayores de edad y uno menor de edad)
    try:
        c1 = Cliente("Carlos", "Gómez", "1995/04/12")
        c2 = Cliente("Ana", "Martínez", "2001/11/30")
    except ValueError as e:
        print(e)

    try:
        c3_menor = Cliente("Lucas", "Pérez", "2010/08/15")
    except ValueError as e:
        print(f"[EXCEPCIÓN CAPTURADA CORRECTAMENTE]: {e}")

    # Mostrar estados iniciales
    print("\n--- Estado Inicial ---")
    c1.saludo()
    c2.saludo()

    # 2. Realizar depósito y retirada válidos
    print("\n--- Operaciones de Depósito y Retirada ---")
    c1.deposito(500.0)
    c1.retirada(150.0)

    # 3. Intento de retirada sin saldo suficiente
    print("\n--- Pruebas de Retirada sin Saldo ---")
    c2.retirada(100.0)

    # 4. Realizar transferencia entre dos clientes
    Cliente.transferencia(emisor=c1, receptor=c2, cantidad=200.0)

    # 5. Saldo final de los clientes
    print("\n--- ESTADO FINAL DE CUENTAS ---")
    c1.saludo()
    c2.saludo()
