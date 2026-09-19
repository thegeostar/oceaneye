"""Every element script.js reaches for must exist in the page that loads it.

This is the bug that was live until 15 Sept 2026: script.js called
getElementById('login-btn'), index.html had no such element, so the call returned
null and `.addEventListener` on it threw. The throw happened inside the
DOMContentLoaded handler, which silently killed every handler registered after
it — about a hundred lines of the file, including the camera-stream refresh loop.

Nothing about that failure was visible on the page. Run this instead:

    python test_dom_ids.py
"""
import re
import sys
from pathlib import Path

APP = Path(__file__).parent


def page_ids(html):
    return set(re.findall(r'id=["\']([^"\']+)["\']', html)) | \
           set(re.findall(r'class=["\']([^"\']+)["\']', html))


def js_targets(js):
    """IDs and classes the script looks up. Only unconditional lookups matter —
    those are the ones that throw when they miss."""
    return set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', js)), \
           set(re.findall(r'getElementsByClassName\(["\']([^"\']+)["\']\)', js))


def main():
    js = (APP / "static/js/script.js").read_text()
    ids, classes = js_targets(js)

    # every template that pulls script.js in has to satisfy it
    pages = [p for p in (APP / "templates").glob("*.html")
             if "script.js" in p.read_text()]
    assert pages, "no template loads script.js — has the <script> tag moved?"

    for page in pages:
        have = page_ids(page.read_text())
        missing = sorted((ids | classes) - have)
        assert not missing, (
            f"script.js looks up {missing} but {page.name} has no such element.\n"
            f"getElementById returns null there and the next call throws, taking "
            f"every handler below it with it.")
        print(f"{page.name}: all {len(ids | classes)} lookups resolve")

    # the other half of the same bug: Jinja tags only render in templates/, never
    # in a file served out of static/
    assert "{{" not in js, (
        "script.js contains a Jinja tag. Flask serves this file as a static asset "
        "and never renders it, so the browser gets the literal '{{ ... }}' text.")
    print("no Jinja tags in static JS")


if __name__ == "__main__":
    main()
    print("OK")
    sys.exit(0)
