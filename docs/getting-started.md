# Primeros pasos

## Instalación

### Windows

Descargá el instalador desde la [página de releases](https://github.com/centaurialpha/pireal/releases) y seguí los pasos. Next, next, finish.

### Linux

Descargá el AppImage desde la [página de releases](https://github.com/centaurialpha/pireal/releases):

```bash
chmod +x Pireal-x86_64.AppImage
./Pireal-x86_64.AppImage
```

### macOS

Todavía no hay instalador para macOS. Si usás Mac y sabés empaquetar apps Python, ¡tu contribución sería muy bienvenida! Abrí un [issue en GitHub](https://github.com/centaurialpha/pireal/issues) y coordinamos.

### Desde el código fuente

Para cualquier plataforma, con [uv](https://docs.astral.sh/uv/) instalado:

```bash
git clone https://github.com/centaurialpha/pireal
cd pireal
uv run pireal
```

---

## Primeros pasos

Al abrir Pireal por primera vez, vas a ver tres paneles:

- **Barra lateral izquierda** — muestra las relaciones de la base de datos y los resultados de las consultas
- **Área superior** — la vista de la base de datos, donde ves y editás tus relaciones
- **Editor inferior** — donde escribís tus consultas de Álgebra Relacional

### 1. Abrir la base de datos de ejemplo

Ir a **Archivo → Abrir ejemplo** para cargar una base de datos prediseñada. Es la forma más rápida de empezar a escribir consultas sin crear nada desde cero.

El ejemplo incluye relaciones como `alumno`, `curso` e `inscripto` — un escenario académico clásico.

### 2. Crear tu propia base de datos

Ir a **Archivo → Nueva base de datos**. Podés definir relaciones usando la sintaxis de texto directamente en el editor:

```
estudiantes(id, nombre, edad)
1, Gabriel, 25
2, Marisel, 30
3, Rodrigo, 25
```

Cada relación comienza con `nombre(col1, col2, ...)` seguido de una fila por línea.

!!! note "Extensiones de archivo"
    Las bases de datos de Pireal se guardan como `.pdb`. Los archivos de consultas usan `.pqf`.

### 3. Escribir tu primera consulta

En el editor de consultas inferior, escribí:

```
q := select edad = 25 (estudiantes);
```

Presioná **F5** (o **Consulta → Ejecutar**) para ejecutar. El resultado aparece en la barra lateral y se abre en una nueva pestaña.

### 4. Encadenar operaciones

Las consultas se pueden anidar y asignar a nombres:

```
jovenes := select edad < 30 (estudiantes);
nombres  := project nombre (jovenes);
```

Cada asignación crea un nuevo resultado que podés inspeccionar de forma independiente.

---

## Atajos de teclado

| Acción                | Atajo           |
|-----------------------|-----------------|
| Ejecutar consultas    | `F5`            |
| Nueva base de datos   | `Ctrl+N`        |
| Abrir archivo         | `Ctrl+O`        |
| Guardar archivo       | `Ctrl+S`        |
| Modo oscuro           | `Ctrl+Shift+D`  |

---

## Próximos pasos

- Conocer todos los [operadores](relational-algebra/operators.md) disponibles
- Ver [ejemplos](relational-algebra/examples.md) prácticos con consultas reales
- Leer sobre los [archivos de base de datos](user-guide/databases.md) y la sintaxis en detalle
