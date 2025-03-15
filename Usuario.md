# MANUAL DE USUARIO
## Herramienta recomendada
En este caso para el mejor uso del programa se recomienda utilziar postam para realizar las peticiones de la API y de la API a la base de datos

* ¿Qué es POSTMAN?: Postman es una herramienta popular para probar APIs de manera fácil y eficiente. Es utilizada principalmente por desarrolladores y testers para realizar solicitudes HTTP (como GET, POST, PUT, DELETE) y verificar las respuestas de una API. Permite enviar solicitudes, examinar las respuestas, automatizar pruebas y gestionar diferentes entornos de trabajo.

 [Link para descargar POSTMAN](https://www.postman.com/downloads/)

Una vez instalado POSTMAN, ya se pueden hacer peticiones a la API, estas son PETICIONES de ejemplo que se pueden realizar:

### CLIENTES

```bash
>>>>CREAR USUARIO
http://localhost:5000/api/users

{
  "Documento_nacional": "606060606",
  "Nombre_Cliente": "Emilio",
  "Apellido_Cliente": "Pérez",
  "correo": "emilio.perez@example.com",
  "correo_confirmado": "FALSE",
  "password": "segura123",
  "numero": "555123456"
}

{
  "Documento_nacional": "6060644406",
  "Nombre_Cliente": "Antonio",
  "Apellido_Cliente": "Manuel",
  "correo": "antonio.manuel@example.com",
  "correo_confirmado": "TRUE",
  "password": "4854454545",
  "numero": "555123456"
}

>>>>Login de Clientes
http://localhost:5000/api/users/login

{
    "correo": "emilio.perez@example.com",
    "password": "segura123"
}

{
    "correo": "antonio.manuel@example.com",
    "password": "4854454545"
}

{
  "correo": "juan.perez@example.com",
  "password": "passkey123"
}

>>>>BUSCAR USUARIO
http://localhost:5000/api/test/:id

>>>Actualizar Cliente
http://localhost:5000/api/users/:id

{
    "correo": "emilio.perezLOLLOLOL@example.com",
    "numero": "+505 56565656"
}

{
    "correo": "MiNuevoCorreo@example.com",
    "numero": "+502 25259696"
}

>>>Eliminar Cliente
http://localhost:5000/api/users/:11
```

### PRODUCTOS

```bash
>>>>>Crear producto
http://localhost:5000/api/products/

{
  "sku": "LAPTOP-XPS-001",
  "nombre_producto": "Laptop Dell XPS",
  "descripcion_producto": "Laptop ultradelgada con Intel i7",
  "precio_producto": 1200.99,
  "descripcion_slug": "laptop-dell-xps",
  "id_categoria": 2
}

>>>>>Listar producto
http://localhost:5000/api/products/

>>>>Buscar producto
http://localhost:5000/api/products/:ID

>>>>Actualizar producto
http://localhost:5000/api/products/:ID

{
  "precio_producto": 999.99,
  "id_categoria": 3
}

>>>>Eliminar producto
http://localhost:5000/api/products/:ID

```
### ORDENES DE PAGO

```bash
>>>>>>>Crear nueva orden
http://localhost:5000/api/orders/
{
  "id_orden": 2,
  "cantidad_ordenada": 3,
  "id_producto": 1
}

>>>>>>Buscar orden de pago por ID
http://localhost:5000/api/orders/:ID

>>>>>>Listar ordenes de pago
http://localhost:5000/api/orders/
```

### PAGOS

```bash
>>>>>>>>CREAR PAGOS
http://localhost:5000/api/payments/

{
  "id_cliente": 1,
  "monto": 500,
  "Metodo_pago": "Tarjeta"
}

>>>>>>LISTAR PAGOS
http://localhost:5000/api/payments/
```
