# πireal

**Pireal** es un intérprete de Álgebra Relacional libre y de código abierto, diseñado para aprender los fundamentos de las bases de datos. Permite crear relaciones, escribir consultas en Álgebra Relacional y ver los resultados al instante, sin SQL, sin configuración, sin ruido.

Ideal para estudiantes y docentes que quieren entender cómo funcionan las bases de datos desde sus cimientos matemáticos.

---

## ¿Por qué Pireal?

La mayoría de los cursos de bases de datos arrancan directo con SQL. Pireal da un paso atrás y permite trabajar con **Álgebra Relacional**, la base matemática sobre la que SQL está construido. Entender esta capa hace que SQL (y las bases de datos en general) tengan mucho más sentido.

Con Pireal podés:

- Escribir consultas de Álgebra Relacional y ver los resultados al instante en una tabla interactiva
- **Visualizar relaciones** - explorá la estructura y los datos de cada relación en el panel lateral
- **Ver el árbol de sintaxis (AST)** - Pireal puede mostrarte el árbol que genera internamente al parsear tu consulta, ideal para entender cómo funciona un intérprete
- **Generar SQL equivalente** - cada consulta se puede traducir automáticamente a SQL para comparar ambos lenguajes
- **Escribir tu base de datos como texto** - definí relaciones en texto plano, sin formularios
- Comparar múltiples resultados lado a lado
- Cargar bases de datos de ejemplo para arrancar rápido
- Usar el **modo terminal** si preferís trabajar desde la línea de comandos

---

## Ejemplo rápido

Dada la relación `estudiantes`:

| id | nombre  | edad |
|----|---------|------|
| 1  | Gabriel | 25   |
| 2  | Marisel | 30   |
| 3  | Rodrigo | 25   |

Esta consulta selecciona los estudiantes de 25 años y muestra solo sus nombres:

```
q := project nombre (select edad = 25 (estudiantes));
```

Resultado:

| nombre  |
|---------|
| Gabriel |
| Rodrigo |

---

## Instalación

Descargá el instalador desde la [página de releases](https://github.com/centaurialpha/pireal/releases), o corré desde el código fuente con [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/centaurialpha/pireal
cd pireal
uv run pireal
```

Para más opciones de instalación, ver [Primeros pasos](getting-started.md).
