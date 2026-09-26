"""Check that every element script.js looks up exists in the page that loads it.

A missing element makes getElementById return null, and the TypeError that follows stops
every handler registered after it, with nothing visible on the page.
"""
import re
from pathlib import Path

APP = Path(__file__).parent


def page_ids(html):
    return set(re.findall(r'id=["\']([^"\']+)["\']', html)) | \
           set(re.findall(r'class=["\']([^"\']+)["\']', html))


def js_targets(js):
    """IDs and classes the script looks up by literal name."""
    return set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js)), \
           set(re.findall(r'getElementsByClassName\(["\']([^"\']+)["\']\)', js))


def main():
    js = (APP / "static/js/script.js").read_text()
    ids, classes = js_targets(js)

    pages = [p for p in (APP / "templates").glob("*.html")
             if "script.js" in p.read_text()]
    assert pages, "no template loads script.js"

    for page in pages:
        have = page_ids(page.read_text())
        missing = sorted((ids | classes) - have)
        assert not missing, (
            f"script.js looks up {missing} but {page.name} has no such element")
        print(f"{page.name}: all {len(ids | classes)} lookups resolve")

    # Flask serves static/ as is, so a Jinja tag there reaches the browser unrendered.
    assert "{{" not in js, "script.js contains a Jinja tag"
    print("no Jinja tags in static JS")


if __name__ == "__main__":
    main()
    print("OK")
