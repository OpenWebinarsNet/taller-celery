### Mock Aplicacion Banco

Esta aplicación format parte del taller sobre tareas asíncronas de openwebinars e intenta simular el comporatmiento de 
una aplicación de un banco la cual solo realiza las operaciones de retirada de dinero y transferencia,
pero con grandes problemas de rendimiento.

#### Instalar dependencias

Para ejecutar esta aplicación necesitarás >= python 3.7

```shell
pip install -r requirements.txt
```

#### Estructura

La aplicación es un servicio hecho en django que se compone de una aplicación accounts, que gestiona
las transferencias y la retirada de efectivo.


En el módulo views de la app de accounts nos encontramos con los endpoints de:
- withdraw_view: Endpoint que se encarga de la retirada de dinero de nuestra aplicación
- transfer_view: Endpoint que se encarga de la transferencia de dinero a otra cuenta

Contamos con una base de datos en el repositorio que también deberá ser descargada.


#### Solución
Para probar la solución tenemos que ejecutar redis en nuestro local

```shell
docker run --publish 6379:6379 -d redis
```

Instalar de nuevo todas las dependencias

```shell
pip install -r requirements.txt
```

Ejecutar migraciones en nuestra bbdd

```shell
python manage.py migrate
```

Y levantar el proceso de celery

```shell
celery -A bank.celery_app worker -l INFO
```
