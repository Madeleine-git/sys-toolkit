#!/usr/bin/env python3
"""
log_parser.py
=============
Módulo de análisis de logs SSH.

Lee auth.log línea a línea, extrae IPs que han fallado
al autenticarse y genera un reporte de amenazas.

Mejora aplicada (sugerencia profesor):
  - Usa collections.Counter en lugar de diccionario manual
    para contar intentos por IP de forma más pythónica.

Conceptos:
  - with open     → abrir ficheros de forma segura
  - .split()      → dividir texto en partes
  - .strip()      → limpiar espacios y saltos de línea
  - Counter       → conteo automático sin if/else manual
  - set           → colección sin duplicados
"""

import os
from collections import Counter


# ─── CONSTANTES ──────────────────────────────────────────────
RUTA_LOG: str = "logs/auth.log"
PATRON_FALLO: str = "Failed password"
UMBRAL_ATAQUES: int = 5


# ─── FUNCIÓN 1: LEER Y PARSEAR EL LOG ────────────────────────

def parsear_log(ruta: str = RUTA_LOG) -> Counter[str]:
    """
    Lee auth.log línea a línea y cuenta los intentos
    fallidos por IP usando collections.Counter.

    Devuelve:
      Counter[str] → {ip: numero_de_intentos}
      Ejemplo: Counter({"185.220.101.45": 8, "45.33.32.156": 5})

    MEJORA — collections.Counter:
      Antes contábamos manualmente con if/else:
        if ip in conteo: conteo[ip] += 1
        else: conteo[ip] = 1

      Ahora recopilamos todas las IPs en una lista
      y Counter las cuenta automáticamente en una línea.
      Es más legible, más pythónico y menos propenso a errores.
    """

    # Verificamos que el fichero existe antes de abrirlo
    if not os.path.exists(ruta):
        print(f"  [!] Error: no se encontró el fichero '{ruta}'")
        print(f"  [!] Asegúrate de que logs/auth.log existe.")
        return Counter()  # devuelve Counter vacío

    # Lista donde acumulamos cada IP que falla
    # Al final Counter la cuenta de golpe
    ips_fallidas: list[str] = []

    with open(ruta, "r", encoding="utf-8") as fichero:
        for linea in fichero:

            linea = linea.strip()

            # Solo nos interesan líneas con "Failed password"
            if PATRON_FALLO not in linea:
                continue

            # Dividimos la línea por espacios
            # La IP está siempre justo después de "from"
            partes: list[str] = linea.split()

            if len(partes) > 10 and "from" in partes:
                indice_from: int = partes.index("from")
                ip: str = partes[indice_from + 1]

                # Añadimos la IP a la lista (con duplicados)
                # Counter se encarga de contar al final
                ips_fallidas.append(ip)

    # Counter cuenta cuántas veces aparece cada IP
    # Counter(["1.2.3.4", "1.2.3.4", "5.6.7.8"])
    # → Counter({"1.2.3.4": 2, "5.6.7.8": 1})
    return Counter(ips_fallidas)


# ─── FUNCIÓN 2: OBTENER IPs ÚNICAS CON SET ───────────────────

def obtener_ips_sospechosas(conteo: Counter[str]) -> set[str]:
    """
    Devuelve un Set con las IPs únicas que han fallado.
    Counter tiene .keys() igual que un diccionario normal.
    """
    return set(conteo.keys())


# ─── FUNCIÓN 3: MOSTRAR EL REPORTE ───────────────────────────

def mostrar_reporte(conteo: Counter[str]) -> None:
    """
    Muestra el reporte completo de intentos fallidos.
    Counter es compatible con .items(), .values() y sorted()
    igual que un diccionario normal.
    """

    if not conteo:
        print("\n  [INFO] No se encontraron intentos fallidos.")
        return

    ips_unicas: set[str] = obtener_ips_sospechosas(conteo)
    total_intentos: int = sum(conteo.values())

    # Counter tiene método .most_common() que ordena
    # automáticamente de mayor a menor sin necesidad de sorted()
    ips_ordenadas = conteo.most_common()

    print("\n  " + "═" * 52)
    print("  REPORTE DE SEGURIDAD SSH")
    print("  " + "═" * 52)
    print(f"  IPs únicas atacantes:    {len(ips_unicas)}")
    print(f"  Total intentos fallidos: {total_intentos}")
    print(f"  Umbral de peligro:       ≥ {UMBRAL_ATAQUES} intentos")
    print("  " + "─" * 52)
    print(f"  {'IP':<20} {'Intentos':>10}   {'Estado'}")
    print("  " + "─" * 52)

    for ip, intentos in ips_ordenadas:
        if intentos >= UMBRAL_ATAQUES:
            estado: str = "⚠  PELIGROSA"
        else:
            estado = "●  Revisar"
        print(f"  {ip:<20} {intentos:>10}   {estado}")

    print("  " + "═" * 52)


# ─── MENÚ INTERACTIVO ────────────────────────────────────────

def menu_log_parser() -> None:
    """Submenú del módulo de análisis de logs SSH."""
    while True:
        print("\n  ── Analizador de logs SSH ──────────────────")
        print("  a.  Analizar auth.log y ver reporte")
        print("  b.  Ver solo IPs únicas detectadas")
        print("  v.  Volver al menú principal")
        print("  ────────────────────────────────────────────")

        opcion: str = input("\n  Elige una opción [a/b/v]: ").strip().lower()

        if opcion == "a":
            print(f"\n  Analizando {RUTA_LOG}...")
            conteo: Counter[str] = parsear_log()
            mostrar_reporte(conteo)

        elif opcion == "b":
            conteo_b: Counter[str] = parsear_log()
            ips: set[str] = obtener_ips_sospechosas(conteo_b)
            print(f"\n  IPs únicas que intentaron acceso: {len(ips)}")
            for ip in sorted(ips):
                print(f"    → {ip}")

        elif opcion == "v":
            break

        else:
            print("  [!] Opción no reconocida.")