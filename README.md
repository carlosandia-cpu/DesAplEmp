# djyango-lb02

## Problemática
Muchas tiendas de barrio llevan el control de sus productos de forma manual, lo que dificulta saber qué hay disponible y su precio actual. Esta app permite a un pequeño comerciante registrar y consultar productos.

## Requisitos funcionales
1. El sistema debe permitir listar los productos disponibles.
2. El sistema debe permitir registrar un nuevo producto (nombre, precio, stock, categoría).
3. El sistema debe mostrar precio y stock actual de cada producto.
4. El sistema debe indicar si un producto está disponible o agotado.
5. El sistema debe permitir clasificar productos por categoría.
6. El sistema debe validar que precio y stock sean valores numéricos positivos.

## App creada
`store`: contiene el modelo de datos estático (lista de diccionarios en `models.py`), las vistas de listado y creación, el formulario `ProductoForm` y los templates `lista.html` y `formulario.html`, heredando de `base.html`.

Nota: al no usar base de datos, los productos agregados se pierden al reiniciar el servidor. Esto es esperado según el enunciado del laboratorio.

## Cómo correr el proyecto
\`\`\`
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
\`\`\`