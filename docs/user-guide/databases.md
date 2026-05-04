# Bases de datos

Una base de datos de Pireal (archivo `.pdb`) es un archivo de texto plano que define una o más relaciones. Podés crearla desde la interfaz gráfica o escribirla directamente con cualquier editor de texto.

---

## Formato del archivo

Cada relación empieza con una línea de encabezado que define el nombre y las columnas, seguida de una fila por línea:

```
@nombre_relacion:col1,col2,col3
valor1,valor2,valor3
valor4,valor5,valor6
```

Una base de datos completa con múltiples relaciones:

```
@estudiantes:id,nombre,edad
1,Gabriel,25
2,Marisel,30
3,Rodrigo,25

@cursos:id_curso,nombre_curso,valor
10,Bases de Datos,2500
20,Redes,3500
30,Python,1500

@inscripto:id,id_curso
1,10
1,30
2,20
```

!!! note "Formato del encabezado"
    El nombre de la relación va precedido por `@` y separado de las columnas por `:`. Las columnas se separan con `,` sin espacios.

---

## Crear una base de datos

### Desde la interfaz

Ir a **Archivo -> Nueva base de datos**. Se abre un editor donde podés escribir la base de datos usando la sintaxis de texto. Al guardar, Pireal escribe el archivo `.pdb`.

### Con el diálogo de nueva relación

Ir a **Base de datos -> Nueva relación** para abrir un formulario donde podés definir columnas e ingresar filas sin escribir la sintaxis manualmente.

### Abrir un archivo existente

Ir a **Archivo -> Abrir** y seleccionar un archivo `.pdb`. Los archivos recientes también aparecen en **Archivo -> Recientes**.

---

## Editar relaciones

Podés editar el contenido de la base de datos directamente en el editor. Los cambios se aplican al guardar.

!!! note "Indicador de cambios sin guardar"
    Cuando una base de datos tiene cambios sin guardar, la pestaña muestra un `*` antes del nombre del archivo. Usá `Ctrl+S` para guardar.

---

## Tipos de datos

Todos los valores se almacenan como texto, pero Pireal los interpreta correctamente al comparar en una consulta:

| Tipo    | Ejemplos                          |
|---------|-----------------------------------|
| Números | `25`, `3500`, `3.14`              |
| Strings | `'Gabriel'`, `'Bases de Datos'`   |
| Fechas  | `'15/03/2017'`, `'2024-01-01'`    |
| Horas   | `'10:30'`, `'23:59'`              |

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

Pireal incluye una base de datos de ejemplo lista para usar. Abrila desde **Archivo → Abrir ejemplo** para explorar un escenario académico con estudiantes, cursos e inscripciones, sin tener que crear nada desde cero.
