# meowtheme

<p align="center">
  <img src="assets/theme.png" alt="meowtheme preview" width="660">
</p>

Light and dark `meow` theme for Chrome, VS Code, Zed, Vim, JetBrains IDEs, macOS Terminal, Codex, Codex Desktop, and opencode.

## Artifacts

Ready-to-use theme artifacts are stored in `output/`.

Chrome themes are generated as unpacked extension directories. To install one, open
`chrome://extensions`, enable Developer mode, choose Load unpacked, and select
`output/chrome/meow-dark/` or `output/chrome/meow-light/`.

## Development

To generate theme artifacts from `meowtheme.yaml`, run:

```sh
just generate
```

To run tests, run:

```sh
just test
```
