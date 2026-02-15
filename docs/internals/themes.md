# Crear temas

¿No te convence ninguno de los temas que vienen por defecto? Podés crear el tuyo. Los temas son archivos JSON simples — no hace falta saber programar, solo elegir colores.

---

## Ubicación de los temas

Pireal busca temas en el directorio de datos del usuario:

- **Linux:** `~/.pireal/themes/`
- **Windows / macOS:** en la carpeta de datos de aplicación estándar del sistema

Cualquier archivo `.json` que pongas en ese directorio aparece automáticamente en **Ajustes → Tema**. Así de simple.

---

## Estructura de un tema

Un tema es un archivo JSON con la siguiente estructura:

```json
{
  "name": "Mi Tema",
  "editor": {
    "background": "#1e1e2e",
    "foreground": "#cdd6f4",
    "current_line": "#313244",
    "selection": "#45475a",
    "keyword": "#cba6f7",
    "string": "#a6e3a1",
    "number": "#fab387",
    "comment": "#6c7086",
    "operator": "#89dceb"
  },
  "app": {
    "background": "#1e1e2e",
    "foreground": "#cdd6f4",
    "accent": "#cba6f7",
    "border": "#313244"
  }
}
```

### Sección `editor`

Controla el aspecto del editor de consultas y la vista de base de datos.

| Clave          | Descripción                              |
|----------------|------------------------------------------|
| `background`   | Color de fondo del editor                |
| `foreground`   | Color del texto base                     |
| `current_line` | Resaltado de la línea donde está el cursor |
| `selection`    | Color del texto seleccionado             |
| `keyword`      | Palabras clave (`select`, `project`, etc.) |
| `string`       | Strings entre comillas                   |
| `number`       | Valores numéricos                        |
| `comment`      | Comentarios (líneas con `%`)             |
| `operator`     | Operadores (`:=`, `=`, `<`, etc.)        |

### Sección `app`

Controla los colores generales de la interfaz.

| Clave        | Descripción                      |
|--------------|----------------------------------|
| `background` | Fondo general de la aplicación   |
| `foreground` | Texto en paneles y barra lateral |
| `accent`     | Color de énfasis (botones, tabs activos) |
| `border`     | Bordes entre paneles             |

---

## Ejemplo: tema Catppuccin Mocha

```json
{
  "name": "Catppuccin Mocha",
  "editor": {
    "background": "#1e1e2e",
    "foreground": "#cdd6f4",
    "current_line": "#313244",
    "selection": "#45475a",
    "keyword": "#cba6f7",
    "string": "#a6e3a1",
    "number": "#fab387",
    "comment": "#6c7086",
    "operator": "#89dceb"
  },
  "app": {
    "background": "#181825",
    "foreground": "#cdd6f4",
    "accent": "#cba6f7",
    "border": "#313244"
  }
}
```

Guardá este archivo como `~/.pireal/themes/catppuccin-mocha.json` y aparecerá en la lista de temas.

---

## Ejemplo: tema claro

```json
{
  "name": "Claro",
  "editor": {
    "background": "#ffffff",
    "foreground": "#383a42",
    "current_line": "#f0f0f0",
    "selection": "#c8e1ff",
    "keyword": "#a626a4",
    "string": "#50a14f",
    "number": "#986801",
    "comment": "#a0a1a7",
    "operator": "#0184bc"
  },
  "app": {
    "background": "#fafafa",
    "foreground": "#383a42",
    "accent": "#4078f2",
    "border": "#e0e0e0"
  }
}
```

---

## Tips para diseñar temas

- Usá herramientas como [Coolors](https://coolors.co) o [Lospec](https://lospec.com/palette-list) para elegir paletas de colores.
- Asegurate de que haya suficiente contraste entre el fondo y el texto para que sea legible.
- Los paletas populares como **Dracula**, **Nord**, **Solarized** o **Catppuccin** son buenos puntos de partida.
- Podés verificar el contraste con herramientas de accesibilidad como [Contrast Checker](https://webaim.org/resources/contrastchecker/).

---

## Compartir tu tema

Si creás un tema que te quedó bueno, compartilo — abrí un Pull Request o publicalo como gist en GitHub y linkealo en las issues.

A los que compartan un tema y sea aceptado al repo les invito una cerveza 🍺 (o una gaseosa, sin presiones).
