from __future__ import annotations

import unittest

from meowtheme.renderers import artifact_set

from tests.helpers import palette


class VimRendererTest(unittest.TestCase):
    def test_artifact_set_includes_vim_colorscheme(self) -> None:
        artifacts = artifact_set(palette())

        self.assertIn("vim/meowdark.vim", artifacts)

    def test_vim_colorscheme_sets_core_options_and_highlights(self) -> None:
        body = artifact_set(palette())["vim/meowdark.vim"]

        self.assertIn("let g:colors_name = 'meowdark'", body)
        self.assertIn("set background=dark", body)
        self.assertIn("if has('termguicolors')\n  set termguicolors\nendif", body)
        self.assertIn("highlight Normal guifg=#d0d0d0 guibg=#121212", body)
        self.assertIn("highlight Comment guifg=#686868 gui=italic", body)
        self.assertIn("highlight String guifg=#c3e88d", body)
        self.assertIn("highlight Visual guibg=#303030", body)

    def test_vim_colorscheme_maps_zed_markup_syntax_to_vim_groups(self) -> None:
        body = artifact_set(palette())["vim/meowdark.vim"]

        self.assertIn("highlight Title guifg=#82aaff gui=bold", body)
        self.assertIn("highlight Italic guifg=#82aaff gui=italic", body)
        self.assertIn("highlight Bold guifg=#ffcb6b gui=bold", body)
        self.assertIn("highlight BoldItalic guifg=#ffcb6b gui=bold,italic", body)
        self.assertIn("highlight markdownUrl guifg=#89ddff", body)
        self.assertIn("highlight markdownCode guifg=#c3e88d", body)
        self.assertIn("highlight markdownStrike guifg=#686868 gui=strikethrough", body)
        self.assertIn("highlight htmlLink guifg=#82aaff gui=underline", body)


if __name__ == "__main__":
    unittest.main()
