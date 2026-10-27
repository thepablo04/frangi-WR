"""Build the self-contained calendar and reproducible download archive."""

from pathlib import Path
import argparse
import io
import zipfile


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"


def build_html():
    template = (SOURCE / "template.html").read_text(encoding="utf-8")
    preflight = (SOURCE / "sync-preflight.js").read_text(encoding="utf-8")
    core = (SOURCE / "sync-core.js").read_text(encoding="utf-8")
    ui = (SOURCE / "sync-ui.js").read_text(encoding="utf-8")
    engine = (SOURCE / "sync-engine.js").read_text(encoding="utf-8")
    for script in (preflight, core, ui, engine):
        if "</script" in script.lower():
            raise ValueError("An embedded script contains an HTML closing tag")
    if template.count("<!-- FRANGI_PREFLIGHT -->") != 1 or template.count("</body>") != 1:
        raise ValueError("The HTML template is incomplete")
    html = template.replace("<!-- FRANGI_PREFLIGHT -->", f"<script>\n{preflight}\n</script>")
    html = html.replace(
        "</body>",
        "\n".join(
            [
                f"<script>{core}</script>",
                f"<script>{ui}</script>",
                f"<script>{engine}</script>",
                "<script>readyTrades.then(window.FrangiStartSync);</script>",
                "</body>",
            ]
        ),
    )
    return html.encode("utf-8")


def build_archive(html):
    result = io.BytesIO()
    with zipfile.ZipFile(result, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in (
            ("frangi.html", html),
            ("LEEME.txt", (ROOT / "LEEME.txt").read_bytes()),
        ):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return result.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Verify committed output without changing it")
    args = parser.parse_args()
    html = build_html()
    outputs = {
        ROOT / "index.html": html,
        ROOT / "frangi.html": html,
        ROOT / "downloads" / "Frangi-sincronizado.zip": build_archive(html),
    }
    for path, data in outputs.items():
        if args.check:
            if not path.is_file() or path.read_bytes() != data:
                raise SystemExit(f"Outdated generated file: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    print("Frangi HTML and ZIP verified." if args.check else "Frangi HTML and ZIP built.")


if __name__ == "__main__":
    main()
