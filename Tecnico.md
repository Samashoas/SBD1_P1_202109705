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

* API: Una API (Interfaz de Programación de Aplicaciones, por sus siglas en inglés: Application Programming Interface) es un conjunto de reglas y protocolos que permite la comunicación entre diferentes sistemas, aplicaciones o servicios. Es una interfaz que define cómo se deben solicitar y recibir datos o funcionalidades entre software, permitiendo que programas diferentes interactúen sin necesidad de conocer los detalles internos de su implementación.

En este caso la API fue creada con el framework FLASK, framework del la cual conoceremos un poco

* FLASK: Flask es un framework web ligero y de microservicios para Python. Está diseñado para facilitar la creación de aplicaciones web simples o complejas, permitiendo a los desarrolladores crear sitios y servicios con rapidez, sin forzar una estructura o depender de herramientas pesadas.

Para la instalación de flask primero tenemos que tener instalado python, el cual se instala desde la store de extenciones de visual studio code o utilizando el siguiente comando:

```bash
$ python --version
$ pip --version
```

Una vez instaldo python lo que tendremos que realizar es la instalación de nuestro framework, que en este caso es flask


```bash
$ pip install Flask
$ python -m flask --version
```

De esta forma ya podemos empezar a trabajar con la creación de nuestra API.

En este caso la API nos permitirá realizar consultas a nuestra base de datos, cosa que para ello se recomienda utilizar **SQL DEVELOPER** el cual se obtiene desde la store de visual studio code.

De igual forma se recomienda el uso de docker para poder levantar el host que nos servirá para levantar nuestro servidor, para esto necesitaremos lo siguiente:

* Instalar docker, el cual se puede obtener buscando docker en el navegador, de igual forma aquí hay un video para realizar todo el proceso de instalación:

   [Instalacion de docker](https://www.youtube.com/watch?v=ZyBBv1JmnWQ)

* Buscar la imagen oficial de oracle en docker hub

```bash
$ docker search oracle/database
```

* Descargar la iamgen de Oracle

```bash
$ docker pull gvenzl/oracle-xe
```

* Crear y ejecutar el contenedor

```bash
$ docker run -d --name oracle-xe -p 1521:1521 -p 5500:5500 -e ORACLE_PASSWORD=your_password gvenzl/oracle-xe
```

Una vez realizado esto ya se puede proceder a la conexion de la base de datos con nuestra API.

## ENDPOINTS

* ¿Qué es un endpoint?: Un endpoint es una dirección específica de un servicio dentro de una API donde se pueden enviar solicitudes para realizar alguna operación, como obtener o modificar datos. Un endpoint está asociado a una ruta URL y un método HTTP (como GET, POST, PUT, DELETE), que indican qué acción se debe realizar sobre los datos.

En este caso se utilizaron varios metodos y endpoints similares, ya que es principalmente el metodo que se le asigna al endpoint el que importa, y el que estará asignando el trabajo a realizar a la dirección de nuestro endpoint

### Endpoints y metodos de clientes

```bash
>>>>CREAR USUARIO
[@app.route('/api/users/', methods=['POST'])]
http://localhost:5000/api/users

>>>>Login de Clientes
[@app.route('/api/users/login', methods=['POST'])]
(http://localhost:5000/api/users)

>>>>BUSCAR Cliente
[@app.route('/api/users/:<int:id>', methods=['GET'])]
http://localhost:5000/api/users/:id

>>>Actualizar Cliente
[@app.route('/api/users/:<int:id>', methods=['PUT'])]
http://localhost:5000/api/users/:id

>>>Eliminar Cliente
[@app.route('/api/users/:<int:id>', methods=['DELETE'])]
http://localhost:5000/api/users/:id

```

### Endpoints y metodos de Productos

```bash
>>>>CREAR PRODUCTO
[@app.route('/api/products/', methods=['POST'])]
http://localhost:5000/api/products

>>>>LISTAR PRODUCTOS
[@app.route('/api/products/', methods=['GET'])]
(http://localhost:5000/api/products)

>>>>BUSCAR PRODUCTO
[@app.route('/api/products/:<int:id>', methods=['GET'])]
http://localhost:5000/api/products/:id

>>>Actualizar PRODUCTO
[@app.route('/api/products/:<int:id>', methods=['PUT'])]
http://localhost:5000/api/products/:id

>>>Eliminar PRODUCTO
[@app.route('/api/products/:<int:id>', methods=['DELETE'])]
http://localhost:5000/api/products/:id

```

### Endpoints y metodos de Odenes de pago
```bash
>>>>>>>Crear nueva orden
[@app.route('/api/orders/', methods=['POST'])]
http://localhost:5000/api/orders/

>>>>>>Buscar orden de pago por ID
[@app.route('/api/orders/:<int:id>', methods=['GET'])]
http://localhost:5000/api/orders/:ID

>>>>>>Listar ordenes de pago
[@app.route('/api/orders/', methods=['GET'])]
http://localhost:5000/api/orders/

```

### Endpoints y metodos de Pagos
```bash
>>>>>>>>CREAR PAGOS
[@app.route('/api/payments/', methods=['POST'])]
http://localhost:5000/api/payments/

>>>>>>LISTAR PAGOS
[@app.route('/api/payments/', methods=['GET'])]
http://localhost:5000/api/payments/

```
