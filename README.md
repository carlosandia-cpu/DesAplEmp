## Laboratorio 08: API REST con Django REST Framework

La aplicación expone sus datos como una API REST en formato JSON, bajo `/api/`, con Django REST Framework. La API reutiliza los modelos y los QuerySets personalizados de la Semana 7.

### Recursos expuestos
| URL | Recurso | Tipo | Operaciones |
|---|---|---|---|
| `/api/membresias/` | Membresía | ModelViewSet | GET, POST, PUT, PATCH, DELETE |
| `/api/pagos/` | Pago | ModelViewSet | GET, POST, PUT, PATCH, DELETE |
| `/api/clases/` | Clase | ModelViewSet | GET, POST, PUT, PATCH, DELETE |
| `/api/clientes/` | Cliente con sus inscripciones anidadas | ReadOnlyModelViewSet | GET |
| `/api/inscripciones/` | Inscripción con cliente y clase anidados | ReadOnlyModelViewSet | GET |

### Serializers (`gimnasio/serializers.py`)
- `MembresiaSerializer`, con `validate_precio` (el precio debe ser mayor que cero).
- `PagoSerializer`, con `validate_monto` (el monto debe ser mayor que cero).
- `ClaseSerializer` y `EntrenadorSerializer`.
- `ClienteDetalleSerializer` e `InscripcionAnidadaSerializer`: el cliente con sus inscripciones anidadas.
- `InscripcionDetalleSerializer`, con `ClienteResumenSerializer` y `ClaseResumenSerializer` anidados.

### ViewSets y rutas (`gimnasio/api_views.py` y `gimnasio/api_urls.py`)
Los ViewSets se registran en un `DefaultRouter` y `config/urls.py` los incluye bajo `/api/`.

### Filtros y acciones
| URL | Técnica |
|---|---|
| `/api/membresias/?search=...&ordering=...` | `SearchFilter` (tipo y cliente) y `OrderingFilter` (precio y fechas) |
| `/api/clases/?search=...&ordering=...` | `SearchFilter` (nombre y entrenador) y `OrderingFilter` (nombre, horario y cupos) |
| `/api/clientes/?estado=...` | Filtro por parámetro en `get_queryset()` |
| `/api/inscripciones/?estado=...` | Filtro por parámetro en `get_queryset()` |
| `/api/clientes/activos/` | `@action` que reutiliza `Cliente.objects.con_inscripciones_activas()` |
| `/api/clases/proximas/` | `@action` que reutiliza `Clase.objects.proximas().con_cupos()` |

### Optimización de consultas
| Recurso | Técnica | Antes | Después |
|---|---|---|---|
| Clientes con inscripciones | `prefetch_related('inscripciones__clase')` | 16 | 3 |
| Inscripciones con cliente y clase | `select_related('cliente', 'clase')` | 21 | 1 |