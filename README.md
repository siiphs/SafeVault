# Uso
## Dependencias necesarias
```bash
pip install aiocoap
```
## Montar servidor
```bash
python server.py
```
## Montar actuador
```bash
#En terminales distintas
# SENSOR PISO 1
python sensor_node.py 1 1

# SENSOR PISO 2 
python sensor_node.py 2 2

# SENSOR PISO 3
python sensor_node.py 3 3
```
## Simular cliente
```bash
# En terminales distintas
# ACTUADORES PISO 1
python actuator_node.py ACT_PISO_1 6001

# ACTUADORES PISO 2
python actuator_node.py ACT_PISO_2 6002

# ACTUADORES PISO 3
python actuator_node.py ACT_PISO_3 6003
```
