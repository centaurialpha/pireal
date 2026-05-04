# Creating themes

Not happy with the built-in themes? You can create your own. Themes are simple JSON files -- no programming knowledge needed, just pick some colors.

---

## Theme location

Pireal looks for themes in the user data directory:

- **Linux:** `~/.pireal/themes/`
- **Windows / macOS:** in the system's standard application data folder

Any `.json` file you put in that directory automatically appears in **Settings -> Theme**. That simple.

---

## Theme structure

A theme is a JSON file with two sections: `editor` and `app`.

```json
{
  "name": "My Theme",
  "editor": {
    "background": "#1e1e2e",
    "foreground": "#cdd6f4",
    "current_line": "#313244",
    "line_number_fg": "#585b70",
    "line_number_bg": "#1e1e2e",
    "selection_bg": "#45475a",
    "selection_fg": "#ffffff",
    "keyword": "#cba6f7",
    "variable": "#f38ba8",
    "string": "#a6e3a1",
    "number": "#fab387",
    "comment": "#6c7086",
    "operator": "#89dceb",
    "bracket_match": "#a6e3a1",
    "bracket_mismatch": "#f38ba8",
    "sidebar_background": "#181825",
    "sidebar_foreground": "#585b70",
    "error": "#f38ba8",
    "success": "#a6e3a1"
  },
  "app": {
    "background": "#1e1e2e",
    "foreground": "#cdd6f4",
    "accent": "#cba6f7",
    "border": "#313244"
  }
}
```

### `editor` section

Controls the appearance of the query editor and database view.

| Key                  | Description                                         |
|----------------------|-----------------------------------------------------|
| `background`         | Editor background color                             |
| `foreground`         | Base text color                                     |
| `current_line`       | Highlight for the line where the cursor is          |
| `line_number_fg`     | Line number text color                              |
| `line_number_bg`     | Line number margin background                       |
| `selection_bg`       | Selected text background                            |
| `selection_fg`       | Selected text color                                 |
| `keyword`            | Keywords (`select`, `project`, `njoin`, etc.)       |
| `variable`           | Relation names and variables                        |
| `string`             | Single-quoted strings                               |
| `number`             | Numeric values                                      |
| `comment`            | Comments (lines starting with `%`)                  |
| `operator`           | Operators (`:=`, `=`, `<`, etc.)                    |
| `bracket_match`      | Parenthesis that matches the one at the cursor      |
| `bracket_mismatch`   | Unmatched parenthesis (balance error)               |
| `sidebar_background` | Sidebar background                                  |
| `sidebar_foreground` | Sidebar text                                        |
| `error`              | Semantic color for errors and negative feedback     |
| `success`            | Semantic color for successful actions (e.g. query ran successfully) |

!!! note "error and success"
    `error` and `success` are **semantic** colors -- they are not part of syntax highlighting. They are used in the interface to communicate results: `error` for failure messages and `success` for positive confirmations like a query that ran successfully. They do not affect code coloring in the editor.

### `app` section

Controls the general interface colors.

| Key          | Description                              |
|--------------|------------------------------------------|
| `background` | General application background          |
| `foreground` | Text in panels and sidebar               |
| `accent`     | Emphasis color (buttons, active tabs)    |
| `border`     | Borders between panels                   |

---

## Example: Catppuccin Mocha theme

```json
{
  "name": "Catppuccin Mocha",
  "editor": {
    "background": "#1e1e2e",
    "foreground": "#cdd6f4",
    "current_line": "#313244",
    "line_number_fg": "#585b70",
    "line_number_bg": "#1e1e2e",
    "selection_bg": "#45475a",
    "selection_fg": "#ffffff",
    "keyword": "#cba6f7",
    "variable": "#f38ba8",
    "string": "#a6e3a1",
    "number": "#fab387",
    "comment": "#6c7086",
    "operator": "#89dceb",
    "bracket_match": "#a6e3a1",
    "bracket_mismatch": "#f38ba8",
    "sidebar_background": "#181825",
    "sidebar_foreground": "#585b70",
    "error": "#f38ba8",
    "success": "#a6e3a1"
  },
  "app": {
    "background": "#181825",
    "foreground": "#cdd6f4",
    "accent": "#cba6f7",
    "border": "#313244"
  }
}
```

Save this file as `~/.pireal/themes/catppuccin-mocha.json` and it will appear in the theme list.

---

## Example: light theme

```json
{
  "name": "Light",
  "editor": {
    "background": "#ffffff",
    "foreground": "#383a42",
    "current_line": "#f0f0f0",
    "line_number_fg": "#8c959f",
    "line_number_bg": "#f6f8fa",
    "selection_bg": "#3f51b5",
    "selection_fg": "#ffffff",
    "keyword": "#a626a4",
    "variable": "#953800",
    "string": "#50a14f",
    "number": "#986801",
    "comment": "#a0a1a7",
    "operator": "#0184bc",
    "bracket_match": "#50a14f",
    "bracket_mismatch": "#cf222e",
    "sidebar_background": "#f6f8fa",
    "sidebar_foreground": "#8c959f",
    "error": "#cf222e",
    "success": "#2d7a2d"
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

## Tips for designing themes

- Use tools like [Coolors](https://coolors.co) or [Lospec](https://lospec.com/palette-list) to pick color palettes.
- Make sure there is enough contrast between the background and text to keep things readable.
- Popular palettes like **Dracula**, **Nord**, **Solarized** or **Catppuccin** are great starting points.
- You can check contrast with accessibility tools like [Contrast Checker](https://webaim.org/resources/contrastchecker/).

---

## Sharing your theme

If you create a theme you are happy with, share it -- open a Pull Request or publish it as a GitHub gist and link it in the issues.

Anyone who shares a theme that gets merged into the repo gets a beer on me 🍺 (or a soda, no pressure).
