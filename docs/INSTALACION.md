# Guía de Instalación - FlockLedger

## Requisitos Previos

- **Python**: 3.7 o superior
- **Sistema Operativo**: macOS, Linux o Windows
- **pip**: Gestor de paquetes de Python (incluido con Python)

## Instalación Paso a Paso

### 1. Descargar o Clonar el Proyecto

```bash
# Opción A: Si tienes Git
git clone https://github.com/tu-usuario/FlockLedger-OSS.git
cd FlockLedger-OSS

# Opción B: Si descargaste el ZIP
unzip FlockLedger-OSS.zip
cd FlockLedger-OSS
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar la Aplicación

### Opción 1: Desde la Raíz (Recomendado)

```bash
python3 main.py
```

### Opción 2: Desde la Carpeta src

```bash
cd src
python3 app.py
```

### Opción 3: Con Python Directly

```bash
python3 -m src.app
```