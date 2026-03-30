"""
Renders the final HTML report from computed stats + LLM narrative.
"""

from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


TEMPLATE_DIR = Path(__file__).parent
TEMPLATE_FILE = "report_template.html"


def render_html_report(stats: dict, narrative: dict, output_path: str = None) -> str:
    """
    Merge stats and LLM narrative into the Jinja2 HTML template.
    Returns the rendered HTML string and optionally writes to output_path.
    """
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template(TEMPLATE_FILE)

    html = template.render(
        stats=stats,
        narrative=narrative,
        generated_at=datetime.now().strftime("%B %d, %Y at %I:%M %p"),
    )

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Report saved → {output_path}")

    return html
