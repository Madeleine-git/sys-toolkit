# 🛠️ SysAdmin Toolkit

Kit de herramientas de línea de comandos desarrollado en Python para automatizar tareas de administración de sistemas: análisis de logs SSH, gestión de inventarios de red, inteligencia de amenazas y generación de informes Excel ejecutivos.

> **Módulo ASIR — Automatización y análisis de redes con Python**  
> **Entorno:** Ubuntu 22.04 LTS — AWS EC2 t3.micro  
> **Repositorio:** github.com/Madeleine-git/sys-toolkit

---

## 📋 Índice

- [¿Qué hace este proyecto?](#qué-hace-este-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Módulos](#módulos)
- [Mejoras aplicadas](#mejoras-aplicadas)
- [Tests](#tests)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Tecnologías](#tecnologías)

---

## ¿Qué hace este proyecto?

SysAdmin Toolkit automatiza en segundos tareas que un administrador haría manualmente en horas:

| Tarea | Sin toolkit | Con toolkit |
|---|---|---|
| Detectar IPs atacantes en logs SSH | Revisar miles de líneas a mano | 1 segundo |
| Saber de dónde viene un atacante | Buscar la IP en Google | Automático via API |
| Analizar inventario de 1000 servidores | Filtrar en Excel a mano | 1 línea de pandas |
| Generar informe para dirección | Crear Excel manualmente | Automático con formato |
| Comprobar si un servidor está activo | Abrir terminal y hacer ping | Automatizado desde Python |
| Monitorizar espacio en disco | Revisar manualmente | Alerta automática al 20% |

---

## Requisitos

- Python 3.10 o superior
- pip
- Git
- Conexión a internet (para el módulo de geolocalización)

---

## Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/Madeleine-git/sys-toolkit.git
cd sys-toolkit

# 2. Crea el entorno virtual
python3 -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Crea las carpetas necesarias
mkdir -p logs data docs
```

---

## Uso

### Menú interactivo (modo clásico)

```bash
source venv/bin/activate
python3 sys_toolkit.py
```

### CLI profesional con Typer (modo avanzado)

```bash
# Ver todos los comandos disponibles
python3 cli.py --help

# Ping a una IP
python3 cli.py ping ip 8.8.8.8

# Analizar espacio en disco
python3 cli.py ping disco /

# Analizar logs SSH
python3 cli.py logs analizar

# Ver IPs únicas atacantes
python3 cli.py logs ips

# Generar inventario CSV
python3 cli.py inventario generar --total 1000

# Ver servidores vulnerables
python3 cli.py inventario vulnerables

# Ver servidores por departamento
python3 cli.py inventario departamentos

# Generar informe Excel
python3 cli.py informe generar

# Geolocalizar IPs atacantes
python3 cli.py amenazas analizar

# Geolocalizar una IP específica
python3 cli.py amenazas ip 8.8.8.8

# Auditar dispositivos de red
python3 cli.py red auditar
```

### Demonio automático

```bash
python3 daemon.py
```

---

## Módulos

### 1. Automatización del SO — `os_utils.py`
- **`check_ping(ip)`** — ejecuta ping real via `subprocess`. Detecta Windows/Linux automáticamente con `os.name`.
- **`check_disk(ruta)`** — analiza espacio libre con `shutil.disk_usage()`. Alerta si baja del 20%.

### 2. Analizador de logs SSH — `log_parser.py`
Lee `auth.log` línea a línea con `with open`, filtra `Failed password`, extrae IPs con `.split()`. Usa `collections.Counter` para contar intentos y `logging` para registrar eventos.

```
REPORTE DE SEGURIDAD SSH
IPs únicas atacantes:    4
Total intentos fallidos: 25
185.220.101.45    8    ⚠ PELIGROSA
91.241.19.77      7    ⚠ PELIGROSA
45.33.32.156      5    ⚠ PELIGROSA
193.32.126.150    5    ⚠ PELIGROSA
```

### 3. Inteligencia de amenazas — `threat_intel.py`
Consulta [ipinfo.io](https://ipinfo.io) para geolocalizar IPs atacantes. Manejo robusto de errores de red con `try/except`.

```
IP               Intentos  País  Ciudad    Organización
185.220.101.45      8       DE   Berlin    AS60729 Stiftung...
91.241.19.77        7       RU   Lugansk   AS47550 Bratinov...
45.33.32.156        5       US   Fremont   AS63949 Akamai...
193.32.126.150      5       FR   Paris     AS39351 31173 Services
```

### 4. Modelos de red con POO — `network_models.py`
Jerarquía de clases con `@dataclass`, herencia y polimorfismo:
- `NetworkDevice` (base): `hostname`, `ip`, `mac`
- `Router` (hija): añade `interfaces`, `gateway`
- `Server` (hija): añade `sistema_operativo`, `ram_gb`, `servicios`

El método `audit_device()` demuestra polimorfismo: mismo nombre, comportamiento distinto según el tipo de objeto.

### 5. Generador de inventario — `generate_inventory.py`
Genera `data/inventory.csv` con 1000 servidores ficticios usando `Faker` y `random`. Columnas: hostname, ip, mac, SO, RAM, CPU, departamento, rol, estado, fechas.

### 6. Gestor de inventario — `inventory_manager.py`
Carga el CSV con `pandas`. Filtra vulnerables (Windows o RAM < 4GB) y agrupa por departamento con barras visuales.

### 7. Generador de informes Excel — `report_generator.py`
Genera `informe_servidores_YYYYMMDD.xlsx` con 4 hojas formateadas con `openpyxl`:
- Resumen Ejecutivo
- Inventario Completo
- Vulnerables
- Por Departamento

### 8. CLI profesional — `cli.py`
Interfaz de comandos con `Typer`. Subcomandos: `ping`, `logs`, `inventario`, `informe`, `amenazas`, `red`.

### 9. Demonio automático — `daemon.py`
Ejecuta el ciclo completo cada hora con `schedule`.

### 10. Logger centralizado — `logger.py`
Sistema de logging con niveles INFO/WARNING/ERROR. Escribe en consola y en `logs/toolkit.log`.

---

## Mejoras aplicadas

Mejoras profesionales aplicadas sobre el proyecto base:

| # | Mejora | Fichero | Descripción |
|---|---|---|---|
| 01 | `collections.Counter` | `log_parser.py` | Reemplaza diccionario manual con contador automático |
| 02 | `logging` centralizado | `logger.py` | Sustituye `print()` del sistema por logging con niveles y timestamps |
| 03 | `@dataclass` | `network_models.py` | Genera `__init__`, `__repr__` y `__eq__` automáticamente |
| 04 | CLI con `Typer` | `cli.py` | Subcomandos profesionales tipo `docker` o `kubectl` |

---

## Tests

```bash
pytest test_toolkit.py -v
```

Resultado:

```
collected 13 items

test_toolkit.py::TestLogParser::test_detecta_ips_correctamente PASSED
test_toolkit.py::TestLogParser::test_cuenta_intentos_correctamente PASSED
test_toolkit.py::TestLogParser::test_log_sin_fallos_devuelve_vacio PASSED
test_toolkit.py::TestLogParser::test_fichero_inexistente_no_explota PASSED
test_toolkit.py::TestLogParser::test_fichero_vacio_no_explota PASSED
test_toolkit.py::TestLogParser::test_no_cuenta_logins_exitosos PASSED
test_toolkit.py::TestOsUtils::test_ping_localhost_responde PASSED
test_toolkit.py::TestOsUtils::test_ping_ip_inexistente_devuelve_false PASSED
test_toolkit.py::TestOsUtils::test_ping_devuelve_bool PASSED
test_toolkit.py::TestEstructurasDatos::test_set_elimina_duplicados PASSED
test_toolkit.py::TestEstructurasDatos::test_diccionario_conteo_manual PASSED
test_toolkit.py::TestManejoErrores::test_parsear_log_maneja_ruta_invalida PASSED
test_toolkit.py::TestManejoErrores::test_parsear_log_maneja_fichero_vacio PASSED

13 passed in 5.07s
```

La salida completa está documentada en `docs/pytest_output.txt`.

---

## Estructura del proyecto

```
sys-toolkit/
├── sys_toolkit.py          # Menú CLI interactivo
├── cli.py                  # CLI profesional con Typer
├── logger.py               # Logging centralizado
├── os_utils.py             # Ping y monitor de disco
├── log_parser.py           # Análisis de logs SSH
├── network_models.py       # POO con @dataclass
├── threat_intel.py         # Geolocalización via API REST
├── generate_inventory.py   # Generador CSV (1000 filas)
├── inventory_manager.py    # Análisis con pandas
├── report_generator.py     # Informes Excel con openpyxl
├── daemon.py               # Demonio automático cada hora
├── test_toolkit.py         # 13 tests unitarios con pytest
├── requirements.txt        # Dependencias fijadas con pip freeze
├── .gitignore              # Excluye venv/, __pycache__/
├── data/
│   ├── inventory.csv               # Inventario generado
│   └── informe_servidores_*.xlsx   # Informes Excel
├── logs/
│   └── auth.log            # Log SSH de entrada
└── docs/
    ├── python-sysadmin.md  # Por qué Python además de Bash
    ├── poo-inventario.md   # POO en inventarios de red
    └── pytest_output.txt   # Salida documentada de tests
```

---

## Tecnologías

| Librería | Versión | Uso en el proyecto |
|---|---|---|
| pandas | 2.3.3 | Carga, filtrado y agrupación del inventario CSV |
| openpyxl | 3.1.5 | Formato profesional del informe Excel |
| requests | 2.34.2 | Peticiones HTTP a la API ipinfo.io |
| typer | 0.26.3 | CLI profesional con subcomandos |
| faker | 40.19.1 | Generación de datos ficticios realistas |
| pytest | 9.0.3 | Framework de tests unitarios |
| mypy | 2.1.0 | Verificación estática de type hints |
| schedule | 1.2.2 | Programación de tareas automáticas |

---

## Entorno de despliegue

```
PC local (Windows 11)
  └── VS Code + Remote SSH
        └── AWS EC2 t3.micro (Ubuntu 22.04 LTS)
              └── /home/ubuntu/sys-toolkit/
```

El entorno virtual está excluido del repositorio via `.gitignore`. Para reproducir el entorno exacto:

```bash
pip install -r requirements.txt
```

---

## Próximas mejoras

- [ ] Usar `cron` o `systemd timers` en lugar de `schedule`
- [ ] Empaquetar con `pyproject.toml` para instalar con `pip install`

---

*Desarrollado como proyecto Automatización y análisis de redes con Python.*