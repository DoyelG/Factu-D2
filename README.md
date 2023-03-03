Facturador: Script para no tener que facturar manualmente

# Facturito

## Introduction

Un script para facturarlos a todos. Un script para facilitarnos la vida, para quitarnos la fiaca y terminar con las manualidades.

## Requirements

Para poder correr el script, necesitamos:

- Python 3
- Selenium
- PIP
- Realizar "pip install {dependencia}" de las dependencias del script que son:
  - selenium
  - webdriver-manager
  - pandas

- CSV con nombre "account" con usuario y contraseña en la misma carpeta que nuestro script, con el formato:
  CUIL       | PASSWORD
  {Nro Cuil} | {Password}
- CSV con nombre "clients" con clientes a facturar en la misma carpeta que nuestro script, con el formato:
  CUIL       | CONDICION
  {Nro Cuil} | {Nro Condicion}
  {Nro Cuil} | {Nro Condicion}
  {Nro Cuil} | {Nro Condicion}
### Los numeros de condicion para tener referencia son:
### Responsable Inscripto = 1
### Consumidor Final = 3
### Si queremos hacer una factura a consumidor final sin especificar a quien, dejamos el Nro de Cuil vacio y Condicion = 3

# Installation

# Python
https://www.python.org/downloads/

# Selenium
https://www.geeksforgeeks.org/how-to-install-selenium-in-python/

# PIP
Mac -> https://www.geeksforgeeks.org/how-to-install-pip-in-macos/?ref=rp
Windows -> https://www.geeksforgeeks.org/how-to-install-pip-on-windows/?ref=rp
Linux -> https://www.geeksforgeeks.org/how-to-install-pip-in-linux/?ref=rp

## Usage
```
SCENARIO User open the terminal console
THEN User goes into the folder where the script is placed `cd {folderPath}`
THEN User runs the script `python3 facturar.py`
```
