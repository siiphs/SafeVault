# Uso
Primero se debe iniciar el servidor para luego iniciar los actuadores y los nodos correspondientes a los pisos del sistema.
Cuando ocurre una situación de peligro, los datos de la misma quedan guardados en un archivo .csv dentro de la carpeta de data.
## Dependencias necesarias
```bash
pip install cryptography 
pip install aiocoap
```
## Montar servidor
```bash
python server.py
```
## Montar actuador
Desde el directorio raiz:
```bash
cd actor
```
Luego, dentro de la carpeta actor:
```bash
#En terminales distintas

# ACTUADORES PISO 1
python actuator_node.py ACT_PISO_1 6001

# ACTUADORES PISO 2
python actuator_node.py ACT_PISO_2 6002

# ACTUADORES PISO 3
python actuator_node.py ACT_PISO_3 6003
```
## Simular cliente
Desde el directorio raiz:
```bash
cd client
```
Luego, dentro de la carpeta client:
```bash
# En terminales distintas

# SENSOR PISO 1
python sensor_node.py 1 1

# SENSOR PISO 2 
python sensor_node.py 2 2

# SENSOR PISO 3
python sensor_node.py 3 3
```

## Para el conserje
```bash
#Segun las alertas eliga que piso proviene la alerta, digitando el numero de dicho piso
#Luego acepta la alerta con s para activar las medidas de emergencia o n en caso de detectar falso positivo.
