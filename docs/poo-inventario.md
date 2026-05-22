# Cómo la POO ayuda a mantener un inventario de red estructurado

## El problema sin POO

Sin programación orientada a objetos, gestionar un inventario de red implica variables sueltas y desorganizadas:

    # Sin POO — caótico y difícil de mantener
    hostname1 = "router-01"
    ip1 = "192.168.1.1"
    mac1 = "AA:BB:CC:DD:EE:01"

    hostname2 = "server-01"
    ip2 = "192.168.1.10"
    mac2 = "AA:BB:CC:DD:EE:02"

Con 500 dispositivos esto se vuelve imposible de gestionar.
No hay estructura, no hay garantías de que cada dispositivo tenga los mismos campos, y el código se vuelve un caos.

## La solución con POO

Cada dispositivo es un objeto que lleva sus propios datos:

    # Con POO — limpio, organizado, escalable
    router = Router("router-01", "192.168.1.1", "AA:BB:CC:DD:EE:01",
                    interfaces=8, gateway="10.0.0.1")

    server = Server("server-01", "192.168.1.10", "AA:BB:CC:DD:EE:02",
                    sistema_operativo="Ubuntu 22.04", ram_gb=16,
                    servicios=["nginx", "ssh"])

## Ventajas concretas para el inventario

### 1. Escalabilidad

Añadir 1000 dispositivos es tan simple como crear 1000 objetos.
Todos comparten la misma estructura definida en la clase base.
No importa si tienes 10 o 10.000 dispositivos, el código que los gestiona es exactamente el mismo.

### 2. Consistencia

Todos los dispositivos tienen garantizados los atributos hostname, ip y mac porque los hereda de NetworkDevice.
Es imposible crear un dispositivo sin esos datos básicos.
El constructor __init__ lo exige obligatoriamente.

### 3. Polimorfismo en auditorías

El mismo comando audit_device() genera directrices distintas según el tipo de dispositivo. No hay que escribir código diferente para cada tipo. Python sabe automáticamente qué versión del método ejecutar según la clase del objeto.

    for dispositivo in inventario:
        dispositivo.audit_device()
        # Router     → directrices de router
        # Server     → directrices de servidor

### 4. Mantenimiento

Si mañana necesitas añadir un nuevo atributo a todos los dispositivos, solo lo añades en NetworkDevice y automáticamente lo heredan Router y Server.
Un solo cambio afecta a toda la jerarquía.

### 5. Legibilidad

El código se lee casi como lenguaje natural:

    router1 = Router("router-core-01", "192.168.1.1", ...)
    server1 = Server("server-web-01", "192.168.1.10", ...)

    router1.audit_device()   # audita el router
    server1.mostrar_info()   # muestra info del servidor

Cualquier programador entiende qué hace este código
sin necesidad de comentarios adicionales.

### 6. Reutilización

Las clases Router y Server pueden importarse en cualquier otro script del proyecto. Una vez definidas, están disponibles para siempre sin reescribir nada.

## Jerarquía de clases del proyecto

    NetworkDevice  (clase base)
    |
    |-- hostname : str
    |-- ip       : str
    |-- mac      : str
    |-- audit_device()    → directrices generales
    |-- mostrar_info()    → información básica
    |
    |── Router  (clase hija)
    |   |-- interfaces : int
    |   |-- gateway    : str
    |   |-- audit_device()  → directrices de router
    |   |-- mostrar_info()  → info completa del router
    |
    └── Server  (clase hija)
        |-- sistema_operativo : str
        |-- ram_gb            : int
        |-- servicios         : list[str]
        |-- audit_device()  → directrices de servidor
        |-- mostrar_info()  → info completa del servidor

## Comparación directa

| Aspecto | Sin POO | Con POO |
|---|---|---|
| Estructura | Variables sueltas | Objetos organizados |
| Escalabilidad | Difícil | Muy fácil |
| Consistencia | No garantizada | Garantizada por __init__ |
| Auditoría | Código repetido | Polimorfismo automático |
| Mantenimiento | Cambios en muchos sitios | Cambio en un solo lugar |
| Legibilidad | Confusa | Clara y natural |

## Conclusión

La POO transforma un inventario de red de una colección de variables sueltas en una jerarquía estructurada de objetos inteligentes. Cada dispositivo sabe quién es, qué atributos tiene y cómo auditarse a sí mismo.

Esto hace el código más limpio, más fácil de mantener y más fácil de escalar. Es exactamente como funcionan las herramientas profesionales de gestión de redes como Cisco Network Assistant o SolarWinds: cada dispositivo es un objeto con sus propios datos y comportamientos.