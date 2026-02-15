# Bases de datos

Una base de datos de Pireal (archivo `.pdb`) es un archivo de texto plano que define una o más relaciones. Podés crearla y editarla directamente en la interfaz de Pireal o con cualquier editor de texto.

---

## Formato del archivo

Cada relación comienza con una línea de encabezado que define el nombre y las columnas, seguida de una fila por línea:

```
nombre_relacion(col1, col2, col3)
valor1, valor2, valor3
valor4, valor5, valor6
```

Una base de datos completa con múltiples relaciones:

```
estudiantes(id, nombre, edad)
1, Gabriel, 25
2, Marisel, 30
3, Rodrigo, 25

cursos(id_curso, nombre_curso, valor)
10, Bases de Datos, 2500
20, Redes, 3500
30, Python, 1500

inscripto(id, id_curso)
1, 10
1, 30
2, 20
```

---

## Crear una base de datos

### Desde la interfaz

Ir a **Archivo → Nueva base de datos**. Se abre un editor donde podés escribir la base de datos usando la sintaxis de texto. Al guardar, Pireal escribe el archivo `.pdb`.

### Con el diálogo de creación de relaciones

Ir a **Base de datos → Nueva relación** para abrir un formulario donde podés definir columnas e ingresar filas sin escribir la sintaxis manualmente.

### Abrir un archivo existente

Ir a **Archivo → Abrir** y seleccionar un archivo `.pdb`.

---

## Editar relaciones

Podés editar el texto de la base de datos directamente en el editor. Los cambios se aplican después de guardar el archivo.

!!! note "Indicador de cambios sin guardar"
    Cuando una base de datos tiene cambios sin guardar, la pestaña muestra un `*` antes del nombre del archivo. Usá `Ctrl+S` para guardar.

---

## Tipos de datos

Todos los valores en Pireal se almacenan como texto internamente, pero el intérprete maneja las comparaciones correctamente para:

| Tipo    | Ejemplos                             |
|---------|--------------------------------------|
| Números | `25`, `3500`, `3.14`                 |
| Strings | `'Gabriel'`, `'Bases de Datos'`      |
| Fechas  | `'15/03/2017'`, `'2024-01-01'`       |
| Horas   | `'10:30'`, `'23:59:00'`              |

Al comparar en una condición `select`, los strings y fechas van entre comillas simples:

```
resultado := select nombre = 'Gabriel' (estudiantes);
resultado := select fecha_inicio > '01/03/2017' (cursos);
```

Los números se comparan sin comillas:

```
resultado := select valor >= 2000 (cursos);
```

---

## Base de datos de ejemplo

Pireal incluye una base de datos de ejemplo. Abrila desde **Archivo → Abrir ejemplo** para ver un escenario académico listo para usar con estudiantes, cursos e inscripciones.
