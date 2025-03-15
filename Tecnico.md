# MANUAL TECNICO
## Esquema conceptual:
Es una representación abstracta y de alto nivel de la estructura lógica de la base de datos, que describe cómo los datos se organizan y cómo se relacionan entre sí, sin entrar en detalles sobre la implementación física. 

El propósito principal de un esquema conceptual es proporcionar una representación clara y comprensible de los datos de la base de datos desde la perspectiva del negocio o de los usuarios finales.

### Diagrama realizado para el modelo conceptual, realizado con excalidraw:
![Diagrama Modelo Conceptual](https://github.com/Samashoas/SBD1_P1_202109705/blob/main/%5BSDB1%5DDiagramas_P1/%5BSBD1%5DModelo_Conceptual_P1.png?raw=true)

## Esquema logico:
Es una representación más detallada de la estructura de los datos, que especifica cómo se organizarán y almacenarán los datos en términos de tablas, columnas, relaciones y restricciones, pero aún no se ocupa de detalles físicos como la ubicación de los datos o la optimización de rendimiento.

A diferencia del esquema conceptual, el esquema lógico se enfoca en cómo se representarán los datos en un SGBD determinado, pero sigue siendo independiente de detalles físicos como índices o particiones de datos.

### Diagrama realizado para el modelo logico, realizado con datamodeler:
![Diagrama Modelo Logico](https://github.com/Samashoas/SBD1_P1_202109705/blob/main/%5BSDB1%5DDiagramas_P1/%5BSBD1%5DModelo_Logicol_P1.png?raw=true)

## Esquema fisico o relacional:
describe cómo se almacenan realmente los datos en un sistema de gestión de bases de datos (SGBD). Es la representación más detallada y concreta de la base de datos, que especifica cómo se organizarán físicamente los datos, cómo se accederán y cómo se optimizará el rendimiento de la base de datos.

Este esquema es el más cercano a la implementación real y es directamente influenciado por el hardware, las configuraciones del SGBD y los requerimientos de rendimiento de la aplicación.

### Diagrama realizado para el modelo relacional, realizado con datamodeler: 
![Diagrama de arquitectura](https://github.com/Samashoas/SBD1_P1_202109705/blob/main/%5BSDB1%5DDiagramas_P1/%5BSBD1%5DModelo_Relacionall_P1.png?raw=true)

Para poder llegar a obtener estos esquemas primero hay que seguir algunas pautas para la elaboración de las tablas.

## Fases de la normalización
### Primera fase nomral (1NF):

* Elimina los grupos repetitivos o conjuntos de datos dentro de una fila. Cada columna debe contener solo un valor atómico (no debe haber valores múltiples o listas dentro de una misma celda)
* Cada columna debe tener un valor único para cada fila y las filas deben ser únicas.

### Segunda fase normal (2NF):

* Se basa en la 1NF y elimina las dependencias parciales. Es decir, todos los atributos no clave deben depender completamente de la clave primaria.
* Si una tabla tiene una clave primaria compuesta (más de una columna), todos los atributos deben depender de toda la clave primaria, no solo de una parte de ella.

### Tercera fase normal (3FN):
* Se basa en la 2NF y elimina las dependencias transitivas. Un atributo no clave no debe depender de otro atributo no clave.
* Es decir, si A depende de B y B depende de C, entonces A debe depender directamente de C, o no debe depender de B en absoluto.

En este caso la Normalización de las tablas se realizó en base al los siguientes CSV:
* [CSV PROYECTO 1](https://drive.google.com/drive/folders/1gwGvckRx3sAuRtZpQMKZwzTaFL4i7Fa8)

De forma que despues de aplicar las primeras 3 fases de la normalización quedan nuestras tablas normalizadas con las cuales estaremos trabajando durante todo el proyecto
* [Tablas normalizadas Proyecto 1](https://docs.google.com/spreadsheets/d/1shWiuavApTypH0oO4eYShfWLYI0867wxHVzaHkl4IQw/edit?gid=0#gid=0)

## CREACION DE LA API

Antes de continuar con esto primero hay que definir lo que es una api


