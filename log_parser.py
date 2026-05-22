#!/usr/bin/env python3
"""
log_parser.py
=============
Módulo de análisis de logs SSH.

Lee auth.log línea a línea, extrae IPs que han fallado
al autenticarse y genera un reporte de amenazas.

Conceptos que practicamos:
  - with open     → abrir ficheros de forma segura
  - .split()      → dividir texto en partes
  - .strip()      → limpiar espacios y saltos de línea
  - set           → colección sin duplicados
  - dict          → tabla clave-valor para contar intentos
"""

import os


# ─── CONSTANTES ──────────────────────────────────────────────
# Ruta al fichero de log.
# En Windows usamos la barra invertida doble \\.
RUTA_LOG: str = "logs\\auth.log"

# Texto que identifica un intento fallido en el log
PATRON_FALLO: str = "Failed password"

# Número mínimo de intentos para considerar una IP peligrosa
UMBRAL_ATAQUES: int = 5


# ─── FUNCIÓN 1: LEER Y PARSEAR EL LOG ────────────────────────

def parsear_log(ruta: str = RUTA_LOG) -> dict[str, int]:
    """
    Lee auth.log línea a línea y cuenta los intentos
    fallidos por IP.

    Devuelve:
      dict[str, int] → diccionario {ip: numero_de_intentos}
      Ejemplo: {"185.220.101.45": 8, "45.33.32.156": 5}

    CONCEPTO — with open:
      Abre el fichero de forma segura. Cuando el bloque
      'with' termina, Python cierra el fichero solo,
      aunque haya ocurrido un error. Evita fugas de memoria.

    CONCEPTO — encoding="utf-8":
      Los ficheros de log pueden tener caracteres especiales.
      Especificar utf-8 evita errores de codificación.
    """

    # El diccionario que contará los intentos por IP
    # Empieza vacío y se va llenando línea a línea
    conteo_ips: dict[str, int] = {}

    # Verificamos que el fichero existe antes de abrirlo
    if not os.path.exists(ruta):
        print(f"  [!] Error: no se encontró el fichero '{ruta}'")
        print(f"  [!] Asegúrate de que logs\\auth.log existe.")
        return conteo_ips  # devuelve diccionario vacío

    # ── EL GESTOR DE CONTEXTO with open ──────────────────
    # 'r' = modo lectura (read)
    # encoding='utf-8' = codificación de caracteres
    with open(ruta, "r", encoding="utf-8") as fichero:

        # Iteramos línea a línea
        # Python lee una línea, la procesa y pasa a la siguiente
        # Nunca carga todo el fichero en RAM de golpe
        for linea in fichero:

            # .strip() elimina el salto de línea \n del final
            linea = linea.strip()

            # ── FILTRO PRINCIPAL ──────────────────────────
            # Solo nos interesan las líneas con "Failed password"
            # Si la línea no contiene ese texto → la saltamos
            if PATRON_FALLO not in linea:
                continue  # salta a la siguiente línea

            # ── EXTRAER LA IP ─────────────────────────────
            # Una línea típica tiene esta estructura:
            # "May 19 03:21:04 servidor sshd[1235]: Failed password for root from 185.220.101.45 port 22 ssh2"
            #
            # .split() divide el texto por espacios y crea una lista:
            # ["May", "19", "03:21:04", "servidor", "sshd[1235]:",
            #  "Failed", "password", "for", "root", "from",
            #  "185.220.101.45", "port", "22", "ssh2"]
            #
            # La IP siempre está justo DESPUÉS de la palabra "from"
            # que está en la posición 9 → la IP está en posición 10

            partes: list[str] = linea.split()

            # Comprobamos que la línea tiene suficientes partes
            # y que contiene "from" donde esperamos
            if len(partes) > 10 and "from" in partes:
                # Buscamos el índice de "from" y cogemos el siguiente
                indice_from: int = partes.index("from")
                ip: str = partes[indice_from + 1]

                # ── CONTAR EN EL DICCIONARIO ──────────────
                # Si la IP ya está en el diccionario → sumamos 1
                # Si es nueva → la añadimos con valor 1
                if ip in conteo_ips:
                    conteo_ips[ip] += 1
                else:
                    conteo_ips[ip] = 1

    return conteo_ips


# ─── FUNCIÓN 2: OBTENER IPs ÚNICAS CON SET ───────────────────

def obtener_ips_sospechosas(conteo: dict[str, int]) -> set[str]:
    """
    A partir del diccionario de conteo, devuelve un Set
    con las IPs únicas que han tenido al menos 1 intento fallido.

    CONCEPTO — set:
      Colección sin duplicados. Aunque una IP aparezca
      500 veces en el log, en el set aparece solo una vez.
      Útil para saber CUÁNTAS IPs distintas nos atacaron.
    """
    # set() convierte las claves del diccionario en un conjunto
    return set(conteo.keys())


# ─── FUNCIÓN 3: MOSTRAR EL REPORTE ───────────────────────────

def mostrar_reporte(conteo: dict[str, int]) -> None:
    """
    Muestra en pantalla el reporte completo de intentos fallidos.
    Ordena las IPs de mayor a menor número de intentos.
    """

    if not conteo:
        print("\n  [INFO] No se encontraron intentos fallidos.")
        return

    # Obtenemos el set de IPs únicas
    ips_unicas: set[str] = obtener_ips_sospechosas(conteo)

    # Total de intentos fallidos (suma de todos los valores)
    total_intentos: int = sum(conteo.values())

    # Ordenamos por número de intentos de mayor a menor
    # sorted() con key=lambda ordena por el valor del diccionario
    ips_ordenadas = sorted(
        conteo.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # ── CABECERA DEL REPORTE ──────────────────────────────
    print("\n  " + "═" * 52)
    print("  REPORTE DE SEGURIDAD SSH")
    print("  " + "═" * 52)
    print(f"  IPs únicas atacantes:  {len(ips_unicas)}")
    print(f"  Total intentos fallidos: {total_intentos}")
    print(f"  Umbral de peligro:     ≥ {UMBRAL_ATAQUES} intentos")
    print("  " + "─" * 52)

    # ── CABECERA DE LA TABLA ──────────────────────────────
    print(f"  {'IP':<20} {'Intentos':>10}   {'Estado'}")
    print("  " + "─" * 52)

    # ── FILAS DE LA TABLA ────────────────────────────────
    for ip, intentos in ips_ordenadas:
        if intentos >= UMBRAL_ATAQUES:
            estado: str = "⚠  PELIGROSA"
        else:
            estado = "●  Revisar"

        print(f"  {ip:<20} {intentos:>10}   {estado}")

    print("  " + "═" * 52)


# ─── FUNCIÓN PRINCIPAL DEL MÓDULO ────────────────────────────

def menu_log_parser() -> None:
    """
    Submenú interactivo del módulo de análisis de logs.
    Se llama desde el menú principal de sys_toolkit.py.
    """
    while True:
        print("\n  ── Analizador de logs SSH ──────────────────")
        print("  a.  Analizar auth.log y ver reporte")
        print("  b.  Ver solo IPs únicas detectadas")
        print("  v.  Volver al menú principal")
        print("  ────────────────────────────────────────────")

        opcion: str = input("\n  Elige una opción [a/b/v]: ").strip().lower()

        if opcion == "a":
            print(f"\n  Analizando {RUTA_LOG}...")
            conteo: dict[str, int] = parsear_log()
            mostrar_reporte(conteo)

        elif opcion == "b":
            conteo_b: dict[str, int] = parsear_log()
            ips: set[str] = obtener_ips_sospechosas(conteo_b)
            print(f"\n  IPs únicas que intentaron acceso: {len(ips)}")
            for ip in sorted(ips):
                print(f"    → {ip}")

        elif opcion == "v":
            break

        else:
            print("  [!] Opción no reconocida.")