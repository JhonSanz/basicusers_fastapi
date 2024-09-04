##### Add alembic to fastapi
1. desde /backend correr `alembic init app/alembic`
2. ir a `app/alembic/env.py` y agregar el siguiente código, para traer la DATABASE_URL de variables de entorno
```python
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
DATABASE_URL = os.getenv("DATABASE_URL")

config = context.config
config.set_main_option('sqlalchemy.url', DATABASE_URL)
```
3. donde esté nuestro alembic.ini correr `alembic revision --autogenerate -m "Initial migration"` para generar las migraciones
4. correr `alembic upgrade head` para aplicar las migraciones

