# El intérprete

> *"Si no sabes cómo funcionan los compiladores, entonces no sabes cómo funcionan las computadoras. Si no estás 100% seguro de cómo funcionan los compiladores, entonces no sabes cómo funcionan las computadoras."*
> -- Steve Yegge

El núcleo de Pireal es su intérprete de Álgebra Relacional, construido completamente desde cero en Python. No depende de ninguna librería de parsing externa — cada componente fue diseñado e implementado a mano.

Entender cómo funciona un intérprete es uno de los temas más valiosos en la carrera de Ingeniería de Software. Pireal es un ejemplo real, pequeño y legible de estos conceptos en acción.

---

## ¿Por qué construir un intérprete desde cero?

Existen librerías que generan parsers automáticamente (ANTLR, PLY, Lark). Usarlas hubiera sido más rápido, pero el objetivo de Pireal no es solo funcionar — es ser un **ejemplo didáctico** de cómo se procesa un lenguaje formal.

Además, el Álgebra Relacional tiene una gramática relativamente simple que se puede implementar con un parser recursivo descendente sin demasiada complejidad. Esto lo hace ideal para entender los conceptos sin ahogarse en casos edge.

---

## Arquitectura del pipeline

Una consulta como esta:

```
q := project nombre (select edad = 25 (estudiantes));
```

Pasa por cuatro etapas antes de producir un resultado:

```
Texto fuente
    |
    v
┌─────────┐
│ Scanner │  Convierte el texto en una secuencia de caracteres con contexto
└─────────┘
    |
    v
┌───────┐
│ Lexer │  Agrupa los caracteres en tokens con significado
└───────┘
    |
    v
┌────────┐
│ Parser │  Construye el AST (árbol de sintaxis abstracta)
└────────┘
    |
    v
┌───────────┐
│ Evaluator │  Recorre el AST y ejecuta las operaciones relacionales
└───────────┘
    |
    v
Relation (resultado)
```

---

## Scanner

El `Scanner` es la capa más baja. Recibe el texto fuente como string y lo envuelve para exponer una interfaz de navegación: avanzar carácter a carácter, mirar el siguiente sin consumirlo (*peek*), y llevar el número de línea actual.

```python
scanner = Scanner("select edad = 25 (estudiantes)")
scanner.current_char   # 's'
scanner.advance()
scanner.current_char   # 'e'
scanner.lineno         # 1
```

Su responsabilidad es única: navegación sobre el texto. No sabe nada de tokens ni de gramática.

---

## Lexer (tokenizador)

El `Lexer` usa el Scanner para agrupar caracteres en **tokens** -- las unidades mínimas con significado del lenguaje.

Por ejemplo, el texto `select edad = 25` produce:

| Token    | Tipo        |
|----------|-------------|
| `select` | `SELECT`    |
| `edad`   | `ID`        |
| `=`      | `EQUAL`     |
| `25`     | `INTEGER`   |

El Lexer reconoce palabras clave (`select`, `project`, `njoin`, etc.), identificadores, números, strings entre comillas simples, fechas, operadores y símbolos de puntuación.

```python
lexer = Lexer(Scanner("select edad = 25"))
lexer.next_token()  # Token(SELECT, 'select')
lexer.next_token()  # Token(ID, 'edad')
lexer.next_token()  # Token(EQUAL, '=')
lexer.next_token()  # Token(INTEGER, '25')
```

---

## Parser

El `Parser` es el corazón del intérprete. Consume tokens del Lexer y construye un **AST (Abstract Syntax Tree)** -- una representación en árbol de la estructura lógica de la consulta.

Implementa un **parser recursivo descendente**: cada regla de la gramática se corresponde con un método de Python.

La gramática (simplificada) de Pireal es:

```
programa      ::= asignación+
asignación    ::= ID ':=' expresión ';'
expresión     ::= expresión_binaria | proyección | selección | variable
proyección    ::= 'project' atributos '(' expresión ')'
selección     ::= 'select' condición '(' expresión ')'
expresión_bin ::= expresión operador expresión
condición     ::= operando comparador operando
operador      ::= 'union' | 'intersect' | 'difference' | 'njoin' | ...
```

Para la consulta `q := project nombre (select edad = 25 (estudiantes))`, el AST resultante es:

```
Compound
└── Assignment(name='q')
    └── ProjectExpr(attrs=['nombre'])
        └── SelectExpr
            ├── Condition(op1='edad', op='=', op2='25')
            └── Variable('estudiantes')
```

---

## Evaluator

El `Evaluator` implementa el patrón **Visitor** sobre el AST. Recorre el árbol de arriba hacia abajo y ejecuta cada nodo llamando al método correspondiente.

```python
class Evaluator(NodeVisitor):
    def visit_Assignment(self, node):
        relation = self.visit(node.query)
        self._results[node.rname.value] = relation

    def visit_ProjectExpr(self, node):
        relation = self.visit(node.expr)
        attrs = [attr.value for attr in node.attrs]
        return relation.project(*attrs)

    def visit_SelectExpr(self, node):
        relation = self.visit(node.expr)
        condition = self.visit(node.condition)
        return relation.select(condition)

    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return getattr(left, BINARY_OP_MAP[node.op])(right)
```

El resultado de cada `visit_*` es una `Relation`. Al final de la evaluación, `_results` contiene todas las relaciones nombradas que se muestran al usuario.

!!! note "¿Por qué Visitor?"
    El patrón Visitor permite agregar operaciones nuevas sobre el AST sin modificar los nodos. Por ejemplo, Pireal también tiene un `SQLGenerator` que recorre el mismo árbol y genera SQL equivalente -- sin tocar el código del evaluador ni del parser.

---

## La clase Relation

`Relation` es el tipo de dato que fluye entre todos los operadores. Internamente almacena:

- `header`: lista de nombres de columnas
- `content`: conjunto de tuplas (set de Python, garantiza unicidad)

```python
r = Relation()
r.header = ["id", "nombre", "edad"]
r.insert(("1", "Gabriel", "25"))
r.insert(("2", "Marisel", "30"))

r.degree()       # 3  (cantidad de columnas)
r.cardinality()  # 2  (cantidad de filas)
```

Cada operación relacional (`.project()`, `.select()`, `.njoin()`, etc.) devuelve una nueva `Relation` sin modificar la original.

---

## Para profundizar

Si querés explorar el código:

- `src/pireal/interpreter/scanner.py` -- navegación sobre el texto
- `src/pireal/interpreter/lexer.py` -- tokenización
- `src/pireal/interpreter/parser.py` -- construcción del AST
- `src/pireal/interpreter/rast.py` -- definición de los nodos del AST
- `src/pireal/interpreter/evaluator.py` -- ejecución
- `src/pireal/core/relation.py` -- el tipo de dato central

Los tests de integración en `tests/integration/` muestran el pipeline completo de punta a punta.
