"""Build GlazeBook's static pages from the app repo's release docs.

Source of truth lives in the GlazeBook app repo:
  docs/release/privacy-policy.{zh,en}.md
  docs/release/support.{zh,en}.md

Run from this directory:
  python3 build.py
"""
import os
import pathlib

import markdown

HERE = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(
    os.environ.get("GLAZEBOOK_DOCS")
    or HERE.parents[1] / "glazebook" / "docs" / "release"
)
EMAIL = "mfjt55@163.com"

TEMPLATE = """<!DOCTYPE html>
<html lang="@LANG@">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@TITLE@</title>
<meta name="description" content="@DESC@">
<style>
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body { margin:0; font-family: system-ui, -apple-system, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif; line-height:1.75; color:#1c1c1e; background:#fff; }
nav { max-width:760px; margin:0 auto; padding:18px 20px 0; display:flex; justify-content:space-between; align-items:baseline; }
nav .brand { font-weight:700; letter-spacing:.02em; }
nav .links a { margin-left:14px; color:#666; text-decoration:none; font-size:.95em; }
nav .links a:hover { text-decoration:underline; }
main { max-width:760px; margin:0 auto; padding:24px 20px 48px; }
h1 { font-size:1.65em; border-bottom:1px solid #ddd; padding-bottom:.4em; }
h2 { margin-top:2em; font-size:1.22em; }
h3 { font-size:1.05em; }
table { border-collapse:collapse; width:100%; margin:1em 0; font-size:.93em; }
th,td { border:1px solid #ccc; padding:8px 10px; text-align:left; vertical-align:top; }
th { background:#f5f5f7; }
footer { max-width:760px; margin:0 auto; padding:0 20px 44px; color:#888; font-size:.9em; }
a { color:#0366d6; }
ul,ol { padding-left:1.4em; }
@media (prefers-color-scheme: dark) {
  body { background:#111114; color:#e4e4e7; }
  th { background:#1d1d21; }
  th,td { border-color:#3a3a3f; }
  h1 { border-bottom-color:#3a3a3f; }
  nav .links a { color:#999; }
  footer { color:#77777d; }
}
</style>
</head>
<body>
<nav><span class="brand">釉记</span><span class="links">@NAV@</span></nav>
<main>
@BODY@
</main>
<footer>© 2026 Xin Zhou · <a href="mailto:@EMAIL@">@EMAIL@</a></footer>
</body>
</html>
"""


def render(md_name: str, lang: str, title: str, desc: str, nav: str) -> str:
    text = (SRC / md_name).read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables"])
    return (
        TEMPLATE.replace("@LANG@", lang)
        .replace("@TITLE@", title)
        .replace("@DESC@", desc)
        .replace("@NAV@", nav)
        .replace("@BODY@", body)
        .replace("@EMAIL@", EMAIL)
    )


zh_nav = (
    '<a href="/glazebook/support-zh.html">支持</a>'
    '<a href="/glazebook/privacy-zh.html">隐私政策</a>'
    '<a href="/glazebook/index.html">English</a>'
)
en_nav = (
    '<a href="/glazebook/support-en.html">Support</a>'
    '<a href="/glazebook/privacy-en.html">Privacy</a>'
    '<a href="/glazebook/index.html">中文</a>'
)

pages = {
    "privacy-zh.html": render(
        "privacy-policy.zh.md", "zh-CN", "釉记隐私政策",
        "釉记隐私政策：本地优先、无需账号、不收集数据。",
        zh_nav,
    ),
    "privacy-en.html": render(
        "privacy-policy.en.md", "en", "GlazeBook Privacy Policy",
        "GlazeBook privacy policy: local-first, no account, no data collection.",
        en_nav,
    ),
    "support-zh.html": render(
        "support.zh.md", "zh-CN", "釉记支持",
        "釉记使用帮助、常见问题与联系方式。",
        zh_nav,
    ),
    "support-en.html": render(
        "support.en.md", "en", "GlazeBook Support",
        "GlazeBook help, FAQ, and contact information.",
        en_nav,
    ),
}

for name, html in pages.items():
    (HERE / name).write_text(html, encoding="utf-8")

index_body = """<h1>GlazeBook / 釉记</h1>
<p>A local-first pottery studio log: glaze recipes, test tile comparison, piece tracking, and kiln runs. One-time purchase, no account, no cloud.</p>
<p>本地优先的陶艺工作室记录：釉料配方、试片对比、作品状态流、窑次台账。一次买断，无账号，无云端。</p>
<h2>Support / 支持</h2>
<ul>
<li><a href="/glazebook/support-zh.html" lang="zh-CN">支持（简体中文）</a></li>
<li><a href="/glazebook/support-en.html" lang="en">Support (English)</a></li>
</ul>
<h2>Privacy / 隐私</h2>
<ul>
<li><a href="/glazebook/privacy-zh.html" lang="zh-CN">隐私政策（简体中文）</a></li>
<li><a href="/glazebook/privacy-en.html" lang="en">Privacy Policy (English)</a></li>
</ul>
"""

index_html = (
    TEMPLATE.replace("@LANG@", "en")
    .replace("@TITLE@", "GlazeBook / 釉记")
    .replace("@DESC@", "GlazeBook: a local-first pottery studio log.")
    .replace("@NAV@", en_nav)
    .replace("@BODY@", index_body)
    .replace("@EMAIL@", EMAIL)
)
(HERE / "index.html").write_text(index_html, encoding="utf-8")

print(f"built {len(pages) + 1} pages into {HERE}")
