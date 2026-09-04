"""Launch the Prompt Ops Gradio app: python app.py"""

from __future__ import annotations

from gradio_prompt_ops.ui import build_app


def main() -> None:
    demo = build_app()
    demo.launch()


if __name__ == "__main__":
    main()
