import './App.css'

const nombreApp = 'GymManager - Investigación'

// Forma de la respuesta de la API (decimales como texto)
const entrenadores = [
  { id: 1, nombre: 'Luis Ramos', especialidad: 'Crossfit', telefono: '987654321' },
  { id: 2, nombre: 'Ana Torres', especialidad: 'Yoga', telefono: '912345678' },
  { id: 3, nombre: 'Marco Díaz', especialidad: 'Spinning', telefono: '955443322' },
  { id: 4, nombre: 'Sofía Paredes', especialidad: 'Funcional', telefono: '944112233' },
]

const clases = [
  {
    id: 1, nombre: 'Yoga matutino', horario: '20/10/2026 07:00',
    cupos_disponibles: 12, entrenador: 2,
    inscripciones: [
      { id: 1, cliente: 'Carlos Andia', fecha_inscripcion: '2026-10-15', estado: 'Activa', sesiones: 4, precio_sesion: '25.00' },
      { id: 2, cliente: 'Noe Quispe', fecha_inscripcion: '2026-10-16', estado: 'Activa', sesiones: 8, precio_sesion: '20.00' },
    ],
  },
  {
    id: 2, nombre: 'Crossfit avanzado', horario: '20/10/2026 18:00',
    cupos_disponibles: 2, entrenador: 1,
    inscripciones: [
      { id: 3, cliente: 'Carlos Andia', fecha_inscripcion: '2026-10-14', estado: 'Completada', sesiones: 10, precio_sesion: '30.50' },
    ],
  },
  {
    id: 3, nombre: 'Spinning', horario: '21/10/2026 19:00',
    cupos_disponibles: 0, entrenador: 3,
    inscripciones: [
      { id: 4, cliente: 'Lucía Rojas', fecha_inscripcion: '2026-10-10', estado: 'Cancelada', sesiones: 2, precio_sesion: '18.00' },
    ],
  },
  {
    id: 4, nombre: 'Funcional', horario: '22/10/2026 08:00',
    cupos_disponibles: 15, entrenador: 4,
    inscripciones: [],
  },
  {
    id: 5, nombre: 'Yoga nocturno', horario: '22/10/2026 20:00',
    cupos_disponibles: 3, entrenador: 2,
    inscripciones: [
      { id: 5, cliente: 'Noe Quispe', fecha_inscripcion: '2026-10-17', estado: 'Activa', sesiones: 5, precio_sesion: '22.00' },
    ],
  },
]

// Total de una clase = suma de sesiones x precio por sesión
function totalClase(clase) {
  return clase.inscripciones.reduce(
    (suma, i) => suma + i.sesiones * Number(i.precio_sesion),
    0
  )
}

function nombreEntrenador(id) {
  const e = entrenadores.find((x) => x.id === id)
  return e ? e.nombre : 'Sin asignar'
}

function App() {
  const ingresosTotales = clases.reduce((suma, c) => suma + totalClase(c), 0)

  return (
    <div className="contenedor">
      <h1 style={{ borderLeft: '6px solid #f97316', paddingLeft: '12px' }}>
        {nombreApp}
      </h1>
      <p className="resumen">
        Clases: {clases.length} | Ingresos estimados: S/ {ingresosTotales.toFixed(2)}
      </p>

      {/* LISTA 1: Entrenadores */}
      <h2>Entrenadores</h2>
      {entrenadores.length === 0 ? (
        <p className="vacio">No hay registros</p>
      ) : (
        <ul className="lista">
          {entrenadores.map((e) => (
            <li key={e.id} className="tarjeta">
              <strong>{e.nombre}</strong> — {e.especialidad} ({e.telefono})
            </li>
          ))}
        </ul>
      )}

      {/* LISTA 2: Clases, con inscripciones anidadas */}
      <h2>Clases</h2>
      {clases.length === 0 ? (
        <p className="vacio">No hay registros</p>
      ) : (
        <ul className="lista">
          {clases.map((clase) => (
            <li key={clase.id} className="tarjeta">
              <h3>{clase.nombre}</h3>
              <p>
                {clase.horario} · Entrenador: {nombreEntrenador(clase.entrenador)}
              </p>

              {/* Ternario */}
              {clase.cupos_disponibles === 0 ? (
                <span className="badge agotado">Sin cupos</span>
              ) : (
                <span className="badge ok">Cupos: {clase.cupos_disponibles}</span>
              )}

              {/* && */}
              {clase.cupos_disponibles > 0 && clase.cupos_disponibles <= 3 && (
                <span className="badge alerta">¡Últimos cupos!</span>
              )}

              <h4>Inscripciones</h4>
              {clase.inscripciones.length === 0 ? (
                <p className="vacio">Sin inscripciones</p>
              ) : (
                <ul className="sublista">
                  {clase.inscripciones.map((i) => (
                    <li key={i.id}>
                      {i.cliente} · {i.estado} · {i.sesiones} sesiones × S/{' '}
                      {Number(i.precio_sesion).toFixed(2)}
                    </li>
                  ))}
                </ul>
              )}

              <p className="total">Total de la clase: S/ {totalClase(clase).toFixed(2)}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default App