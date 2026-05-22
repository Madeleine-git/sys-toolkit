#!/usr/bin/env python3
"""
network_models.py
=================
Módulo de modelado de dispositivos de red mediante POO.

Clases:
  - NetworkDevice  → clase base con atributos comunes
  - Router         → clase hija para routers
  - Server         → clase hija para servidores

Conceptos que practicamos:
  - Clases y objetos
  - Herencia
  - Polimorfismo
  - __init__ (constructor)
  - __str__ (representación en texto)
  - super() para llamar al padre
"""


# ─────────────────────────────────────────────────────────────
# CLASE BASE: NetworkDevice
# ─────────────────────────────────────────────────────────────

class NetworkDevice:
    """
    Clase base que representa cualquier dispositivo de red.
    Define los atributos comunes a todos los dispositivos:
    hostname, ip y mac.

    CONCEPTO — __init__:
      Es el constructor. Se ejecuta automáticamente cada vez
      que creas un objeto de esta clase. Recibe los datos
      iniciales y los guarda como atributos del objeto.

    CONCEPTO — self:
      Es una referencia al propio objeto. Cuando escribes
      self.hostname = hostname, estás diciendo "guarda este
      valor EN ESTE objeto específico". Cada objeto tiene
      sus propios valores aunque sean de la misma clase.
    """

    def __init__(self, hostname: str, ip: str, mac: str) -> None:
        """
        Constructor de NetworkDevice.

        Parámetros:
          hostname → nombre del dispositivo (ej: "router-01")
          ip       → dirección IP (ej: "192.168.1.1")
          mac      → dirección MAC (ej: "AA:BB:CC:DD:EE:FF")
        """
        self.hostname: str = hostname
        self.ip: str = ip
        self.mac: str = mac

    def __str__(self) -> str:
        """
        CONCEPTO — __str__:
          Define cómo se muestra el objeto cuando usas print().
          Sin este método, print(router) mostraría algo feo
          como <NetworkDevice object at 0x...>.
          Con él, muestra la información del dispositivo.
        """
        return (
            f"Dispositivo: {self.hostname} | "
            f"IP: {self.ip} | "
            f"MAC: {self.mac}"
        )

    def audit_device(self) -> None:
        """
        Método de auditoría base.
        Las clases hijas lo sobreescriben con sus propias
        directrices de seguridad (polimorfismo).
        """
        print(f"\n  [AUDIT] Dispositivo: {self.hostname}")
        print(f"  [AUDIT] IP:          {self.ip}")
        print(f"  [AUDIT] MAC:         {self.mac}")
        print("  [AUDIT] Directrices generales de seguridad:")
        print("    • Mantener firmware actualizado")
        print("    • Usar contraseñas seguras")
        print("    • Revisar logs periódicamente")

    def mostrar_info(self) -> None:
        """Muestra información básica del dispositivo."""
        print(f"\n  {'─' * 45}")
        print(f"  Hostname : {self.hostname}")
        print(f"  IP       : {self.ip}")
        print(f"  MAC      : {self.mac}")


# ─────────────────────────────────────────────────────────────
# CLASE HIJA: Router
# ─────────────────────────────────────────────────────────────

class Router(NetworkDevice):
    """
    Clase hija que representa un router de red.
    Hereda de NetworkDevice y añade atributos específicos.

    CONCEPTO — Herencia (Router hereda de NetworkDevice):
      Router tiene automáticamente hostname, ip y mac
      sin necesidad de redefinirlos. Solo añade lo suyo:
      interfaces y gateway.

    CONCEPTO — super():
      Llama al constructor del padre (NetworkDevice).
      Evita repetir el código de inicialización de
      hostname, ip y mac.
    """

    def __init__(
        self,
        hostname: str,
        ip: str,
        mac: str,
        interfaces: int,
        gateway: str
    ) -> None:
        """
        Constructor de Router.

        Parámetros heredados de NetworkDevice:
          hostname, ip, mac

        Parámetros propios de Router:
          interfaces → número de interfaces de red
          gateway    → IP de la puerta de enlace
        """
        # super() llama al __init__ del padre (NetworkDevice)
        # para inicializar hostname, ip y mac
        super().__init__(hostname, ip, mac)

        # Atributos propios del Router
        self.interfaces: int = interfaces
        self.gateway: str = gateway

    def __str__(self) -> str:
        """Representación en texto del Router."""
        base: str = super().__str__()
        return (
            f"{base} | Interfaces: {self.interfaces} | "
            f"Gateway: {self.gateway}"
        )

    def mostrar_info(self) -> None:
        """Muestra información completa del router."""
        super().mostrar_info()  # muestra hostname, ip, mac
        print(f"  Tipo     : Router")
        print(f"  Interfaces: {self.interfaces}")
        print(f"  Gateway  : {self.gateway}")
        print(f"  {'─' * 45}")

    def audit_device(self) -> None:
        """
        CONCEPTO — Polimorfismo:
          Este método tiene el MISMO nombre que en NetworkDevice
          pero hace algo DIFERENTE. Muestra directrices
          específicas de seguridad para routers.
          Python sabe qué versión usar según el tipo de objeto.
        """
        print(f"\n  {'═' * 45}")
        print(f"  AUDITORÍA DE ROUTER: {self.hostname}")
        print(f"  {'═' * 45}")
        print(f"  IP:         {self.ip}")
        print(f"  MAC:        {self.mac}")
        print(f"  Interfaces: {self.interfaces}")
        print(f"  Gateway:    {self.gateway}")
        print(f"\n  Directrices de seguridad para ROUTER:")
        print("    • Deshabilitar servicios no usados (Telnet, HTTP)")
        print("    • Usar SSH v2 en lugar de Telnet")
        print("    • Configurar ACLs para filtrar tráfico")
        print("    • Activar logging de eventos de red")
        print("    • Cambiar credenciales por defecto")
        print("    • Actualizar IOS/firmware regularmente")
        print(f"  {'═' * 45}")


# ─────────────────────────────────────────────────────────────
# CLASE HIJA: Server
# ─────────────────────────────────────────────────────────────

class Server(NetworkDevice):
    """
    Clase hija que representa un servidor de red.
    Hereda de NetworkDevice y añade atributos específicos.
    """

    def __init__(
        self,
        hostname: str,
        ip: str,
        mac: str,
        sistema_operativo: str,
        ram_gb: int,
        servicios: list[str]
    ) -> None:
        """
        Constructor de Server.

        Parámetros heredados:
          hostname, ip, mac

        Parámetros propios de Server:
          sistema_operativo → SO del servidor (ej: "Ubuntu 22.04")
          ram_gb            → RAM en gigabytes
          servicios         → lista de servicios activos
        """
        super().__init__(hostname, ip, mac)

        self.sistema_operativo: str = sistema_operativo
        self.ram_gb: int = ram_gb
        self.servicios: list[str] = servicios

    def __str__(self) -> str:
        """Representación en texto del Server."""
        base: str = super().__str__()
        servicios_str: str = ", ".join(self.servicios)
        return (
            f"{base} | SO: {self.sistema_operativo} | "
            f"RAM: {self.ram_gb}GB | Servicios: {servicios_str}"
        )

    def mostrar_info(self) -> None:
        """Muestra información completa del servidor."""
        super().mostrar_info()
        servicios_str: str = ", ".join(self.servicios)
        print(f"  Tipo     : Servidor")
        print(f"  SO       : {self.sistema_operativo}")
        print(f"  RAM      : {self.ram_gb} GB")
        print(f"  Servicios: {servicios_str}")
        print(f"  {'─' * 45}")

    def audit_device(self) -> None:
        """
        Versión del método audit_device() para servidores.
        Muestra directrices específicas de seguridad
        para servidores, distintas a las del router.
        """
        servicios_str: str = ", ".join(self.servicios)
        print(f"\n  {'═' * 45}")
        print(f"  AUDITORÍA DE SERVIDOR: {self.hostname}")
        print(f"  {'═' * 45}")
        print(f"  IP:       {self.ip}")
        print(f"  MAC:      {self.mac}")
        print(f"  SO:       {self.sistema_operativo}")
        print(f"  RAM:      {self.ram_gb} GB")
        print(f"  Servicios: {servicios_str}")
        print(f"\n  Directrices de seguridad para SERVIDOR:")
        print("    • Aplicar actualizaciones de seguridad")
        print("    • Deshabilitar servicios innecesarios")
        print("    • Configurar firewall (ufw/iptables)")
        print("    • Usar autenticación por clave SSH")
        print("    • Configurar fail2ban contra fuerza bruta")
        print("    • Realizar backups periódicos")
        print("    • Monitorizar logs con herramientas SIEM")
        print(f"  {'═' * 45}")


# ─────────────────────────────────────────────────────────────
# FUNCIÓN INTERACTIVA: MENÚ DEL MÓDULO
# ─────────────────────────────────────────────────────────────

def menu_network_models() -> None:
    """
    Submenú interactivo del módulo de modelos de red.
    Crea dispositivos de ejemplo y demuestra el polimorfismo.
    """

    # Creamos objetos de ejemplo
    # Cada objeto es una instancia de su clase
    router1 = Router(
        hostname="router-core-01",
        ip="192.168.1.1",
        mac="AA:BB:CC:DD:EE:01",
        interfaces=8,
        gateway="10.0.0.1"
    )

    server1 = Server(
        hostname="server-web-01",
        ip="192.168.1.10",
        mac="AA:BB:CC:DD:EE:02",
        sistema_operativo="Ubuntu 22.04 LTS",
        ram_gb=16,
        servicios=["nginx", "ssh", "postgresql"]
    )

    server2 = Server(
        hostname="server-db-01",
        ip="192.168.1.11",
        mac="AA:BB:CC:DD:EE:03",
        sistema_operativo="Windows Server 2019",
        ram_gb=32,
        servicios=["sqlserver", "rdp", "iis"]
    )

    # Lista de todos los dispositivos
    # CONCEPTO: podemos mezclar Router y Server en la misma
    # lista porque ambos heredan de NetworkDevice
    dispositivos: list[NetworkDevice] = [router1, server1, server2]

    while True:
        print("\n  ── Modelos de red (POO) ────────────────────")
        print("  a.  Ver inventario de dispositivos")
        print("  b.  Auditar todos los dispositivos")
        print("  c.  Auditar un dispositivo específico")
        print("  v.  Volver al menú principal")
        print("  ────────────────────────────────────────────")

        opcion: str = input("\n  Elige una opción [a/b/c/v]: ").strip().lower()

        if opcion == "a":
            print("\n  INVENTARIO DE RED")
            for dispositivo in dispositivos:
                dispositivo.mostrar_info()

        elif opcion == "b":
            print("\n  AUDITORÍA COMPLETA DE RED")
            print("  CONCEPTO: polimorfismo en acción.")
            print("  El mismo método audit_device() hace")
            print("  cosas distintas según el tipo de objeto.")
            for dispositivo in dispositivos:
                dispositivo.audit_device()

        elif opcion == "c":
            print("\n  Dispositivos disponibles:")
            for i, dispositivo in enumerate(dispositivos):
                print(f"    {i + 1}. {dispositivo.hostname} ({dispositivo.ip})")

            seleccion: str = input("\n  Elige un número: ").strip()
            try:
                indice: int = int(seleccion) - 1
                if 0 <= indice < len(dispositivos):
                    dispositivos[indice].audit_device()
                else:
                    print("  [!] Número fuera de rango.")
            except ValueError:
                print("  [!] Introduce un número válido.")

        elif opcion == "v":
            break

        else:
            print("  [!] Opción no reconocida.")