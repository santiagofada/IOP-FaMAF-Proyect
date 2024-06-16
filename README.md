# Modelado de Torneos en Formato Round Robin

## Proyecto de Investigación de Operaciones
### Licenciatura en Matemática Aplicada

Este programa resuelve el problema de la organización de torneos en formato Single Round Robin (SRR) utilizando tres 
formulaciones diferentes: tradicional, basada en permutaciones y basada en emparejamientos (matching).

## Descripción del Proyecto

Los torneos en formato round robin, también conocidos como "todos contra todos", son ampliamente utilizados en diversas
competiciones deportivas y en situaciones que requieren una organización similar. 
Este proyecto presenta tres enfoques diferentes basados en programación lineal entera para resolver el problema de 
programación de estos torneos.

### Formulaciones Implementadas

1. **Formulación Tradicional**: Esta formulación es intuitiva y eficiente en términos de cantidad de variables, proporcionando un modelo más fácil de entender y trabajar.
   
2. **Formulación Basada en Permutaciones**: Aunque presenta problemas de escalabilidad debido a la alta cantidad de variables y restricciones a medida que aumenta el número de equipos, ofrece una estructura flexible para modelar variantes de torneos round robin.

3. **Formulación Basada en Emparejamientos (Matching)**: Proporciona un mayor valor funcional en la relajación lineal asociada, lo que puede ser beneficioso cuando la dimensión del problema impide el uso de métodos como branch-and-cut.


## Ejecución del Script

Para ejecutar el script que resuelve el problema SRR (Single Round Robin), se utilizan varios parámetros que se describen a continuación. El script se ejecuta utilizando `argparse` para manejar estos parámetros.

### Parámetros

- `--variant`: Define la variante del problema a resolver. Puede tomar los valores `traditional`, `matching`, o `permutation`. Por defecto, es `traditional`.
- `--entera`: Indica si las variables deben ser binarias (enteras) en lugar de continuas. Toma un valor booleano (`True` o `False`). Por defecto, es `True`.
- `--file`: Especifica el archivo de configuración que contiene los datos del problema. Este parámetro es requerido.
- `--seed`: Establece la semilla para la generación de números aleatorios, lo cual es útil para reproducibilidad. Por defecto, es `42`.


## Formato de Archivos de Entrada

Para resolver el problema de programación de torneos en formato Single Round Robin (SRR),
se requiere un archivo de configuración que contenga la información necesaria sobre los equipos
y los costos asociados a cada partido en cada ronda.
A continuación, se detalla el formato que debe tener este archivo de entrada.

### Estructura del Archivo

El archivo de configuración debe estar estructurado de la siguiente manera:

1. **Primera línea**: Indica la cantidad de equipos.
2. **Líneas siguientes**: Cada línea contiene una tupla `(i, j), r, c` que especifica el costo `c` de que el equipo `i` juegue contra el equipo `j` en la ronda `r`.

### Ejemplo de Archivo de Configuración

archivo 4_teams.srr

- **Primera línea**: `4` (Número de equipos).
- **Líneas siguientes**:
  - `(0, 1), 0, 3`: Si el equipo `0` juega contra el equipo `1` en la ronda `0` con un costo de `3`.
  - `(0, 2), 0, 8`: Si el equipo `0` juega contra el equipo `2` en la ronda `0` con un costo de `8`.
  - `(0, 3), 0, 1`: Si el equipo `0` juega contra el equipo `3` en la ronda `0` con un costo de `1`.
  - `(0, 1), 1, 4`: Si el equipo `0` juega contra el equipo `1` en la ronda `1` con un costo de `4`.
  - `(0, 2), 1, 6`: Si el equipo `0` juega contra el equipo `2` en la ronda `1` con un costo de `6`.
  - `(0, 3), 1, 9`: Si el equipo `0` juega contra el equipo `3` en la ronda `1` con un costo de `9`.
  - `(0, 1), 2, 2`: Si el equipo `0` juega contra el equipo `1` en la ronda `2` con un costo de `2`.
  - `(0, 2), 2, 4`: Si el equipo `0` juega contra el equipo `2` en la ronda `2` con un costo de `4`.
  - `(0, 3), 2, 7`: Si el equipo `0` juega contra el equipo `3` en la ronda `2` con un costo de `7`.
  - `(1, 2), 0, 5`: Si el equipo `1` juega contra el equipo `2` en la ronda `0` con un costo de `5`.
  - `(1, 3), 0, 1`: Si el equipo `1` juega contra el equipo `3` en la ronda `0` con un costo de `1`.
  - `(1, 2), 1, 3`: Si el equipo `1` juega contra el equipo `2` en la ronda `1` con un costo de `3`.
  - `(1, 3), 1, 9`: Si el equipo `1` juega contra el equipo `3` en la ronda `1` con un costo de `9`.
  - `(1, 2), 2, 4`: Si el equipo `1` juega contra el equipo `2` en la ronda `2` con un costo de `4`.
  - `(1, 3), 2, 8`: Si el equipo `1` juega contra el equipo `3` en la ronda `2` con un costo de `8`.
  - `(2, 3), 0, 6`: Si el equipo `2` juega contra el equipo `3` en la ronda `0` con un costo de `6`.
  - `(2, 3), 1, 9`: Si el equipo `2` juega contra el equipo `3` en la ronda `1` con un costo de `9`.
  - `(2, 3), 2, 4`: Si el equipo `2` juega contra el equipo `3` en la ronda `2` con un costo de `4`.




### Consideraciones

- **Cantidad de Equipos**: Asegúrate de que la cantidad de equipos sea un numero par.
- **Rondas**: El número de rondas debe ser `n-1` donde `n` es el número de equipos.
- **Costos**: Los costos son arbitrarios y pueden ajustarse según las necesidades del problema.


### Instalacion de librerias
```sh
  pip install -r requirements.txt
```
### Ejemplo de Ejecución

Para ejecutar el script, utiliza el siguiente comando en la terminal. Asegúrate de especificar el archivo de configuración adecuado y los parámetros necesarios:

```sh
python main.py --variant traditional --entera True --file example.srr
```