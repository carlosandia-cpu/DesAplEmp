productos = [
    {"id": 1, "nombre": "Arroz 1kg", "precio": 4.50, "stock": 30, "categoria": "Abarrotes"},
    {"id": 2, "nombre": "Leche Evaporada", "precio": 3.20, "stock": 0, "categoria": "Lácteos"},
    {"id": 3, "nombre": "Detergente 1L", "precio": 8.90, "stock": 15, "categoria": "Limpieza"},
    {"id": 4, "nombre": "Papel Higiénico x4", "precio": 6.00, "stock": 20, "categoria": "Cuidado personal"},
    {"id": 5, "nombre": "Aceite Vegetal 1L", "precio": 9.50, "stock": 12, "categoria": "Abarrotes"},
]

def obtener_productos():
    return productos

def agregar_producto(nombre, precio, stock, categoria):
    nuevo_id = max([p["id"] for p in productos], default=0) + 1
    productos.append({
        "id": nuevo_id,
        "nombre": nombre,
        "precio": precio,
        "stock": stock,
        "categoria": categoria,
    })