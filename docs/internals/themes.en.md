# Creating Themes

Not a fan of the default themes? You can create your own. Themes are simple JSON files — no coding required, just pick some colors.

---

## Theme location

Pireal looks for themes in the user data directory:

- **Linux:** `~/.pireal/themes/`
- **Windows / macOS:** in the system's standard app data folder

Any `.json` file you drop there shows up automatically in **Settings → Theme**. That's it.

---

## Theme structure

```json
{
  "name": "My Theme",
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

### `editor` section

| Key            | Description                              |
|----------------|------------------------------------------|
| `background`   | Editor background color                  |
| `foreground`   | Base text color                          |
| `current_line` | Highlight for the line with the cursor   |
| `selection`    | Selected text color                      |
| `keyword`      | Keywords (`select`, `project`, etc.)     |
| `string`       | Quoted strings                           |
| `number`       | Numeric values                           |
| `comment`      | Comments (lines starting with `%`)       |
| `operator`     | Operators (`:=`, `=`, `<`, etc.)         |

### `app` section

| Key          | Description                      |
|--------------|----------------------------------|
| `background` | General app background           |
| `foreground` | Text in panels and sidebar       |
| `accent`     | Emphasis color (buttons, active tabs) |
| `border`     | Borders between panels           |

---

## Example: Catppuccin Mocha

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

Save this as `~/.pireal/themes/catppuccin-mocha.json` and it will appear in the theme list.

---

## Tips for designing themes

- Use tools like [Coolors](https://coolors.co) or [Lospec](https://lospec.com/palette-list) to pick palettes.
- Make sure there's enough contrast between background and text.
- Popular palettes like **Dracula**, **Nord**, **Solarized**, or **Catppuccin** are good starting points.

---

## Sharing your theme

If you put together a theme you like, share it — open a Pull Request or publish it as a GitHub gist and link it in the issues.

Anyone whose theme gets accepted into the repo gets a beer on me 🍺 (or a soda, no pressure).
