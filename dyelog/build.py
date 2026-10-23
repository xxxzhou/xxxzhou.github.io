"""Build DyeLog's static pages from the app repo's release docs.

Source of truth lives in the DyeLog app repo:
  docs/release/privacy-policy.<lang>.md
  docs/release/support.<lang>.md

Run from this directory:
  DYELOG_DOCS=/path/to/dyelog/docs/release python3 build.py

One page per store locale so each App Store storefront points at its own
language (privacyPolicyUrl / supportUrl), matching Metadata/metadata.json.
"""
import os
import pathlib

import markdown

HERE = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(
    os.environ.get("DYELOG_DOCS")
    or HERE.parents[1] / "dyelog" / "docs" / "release"
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
<nav><span class="brand">DyeLog</span><span class="links">@NAV@</span></nav>
<main>
@BODY@
</main>
<footer>© 2026 Xin Zhou · <a href="mailto:@EMAIL@">@EMAIL@</a></footer>
</body>
</html>
"""

# code -> (html lang, ui label, support label, privacy label, all-languages label,
#          privacy meta desc, support meta desc)
LANGS = {
    "en": ("en", "English", "Support", "Privacy Policy", "All languages",
           "DyeLog privacy policy: local-first, no account, no data collection.",
           "DyeLog help, FAQ, and contact information."),
    "zh": ("zh-CN", "简体中文", "支持", "隐私政策", "全部语言",
           "染记隐私政策：本地优先、无需账号、不收集数据。",
           "染记使用帮助、常见问题与联系方式。"),
    "zh-Hant": ("zh-Hant", "繁體中文", "支援", "隱私權政策", "全部語言",
           "染記隱私權政策：本地優先、無需帳號、不收集資料。",
           "染記使用說明、常見問題與聯絡方式。"),
    "ja": ("ja", "日本語", "サポート", "プライバシーポリシー", "すべての言語",
           "DyeLog プライバシーポリシー：ローカルファースト、アカウント不要、データ収集なし。",
           "DyeLog のヘルプ、よくある質問、お問い合わせ。"),
    "ko": ("ko", "한국어", "지원", "개인정보 처리방침", "전체 언어",
           "DyeLog 개인정보 처리방침: 로컬 퍼스트, 계정 없음, 데이터 수집 없음.",
           "DyeLog 도움말, FAQ, 연락처."),
    "de": ("de", "Deutsch", "Support", "Datenschutz", "Alle Sprachen",
           "DyeLog Datenschutzerklärung: lokal, ohne Konto, keine Datensammlung.",
           "DyeLog Hilfe, FAQ und Kontakt."),
    "fr": ("fr", "Français", "Assistance", "Confidentialité", "Toutes les langues",
           "Politique de confidentialité de DyeLog : local, sans compte, sans collecte.",
           "Aide, FAQ et contact pour DyeLog."),
    "es": ("es", "Español", "Soporte", "Privacidad", "Todos los idiomas",
           "Política de privacidad de DyeLog: local, sin cuenta, sin recopilación.",
           "Ayuda, preguntas frecuentes y contacto de DyeLog."),
    "it": ("it", "Italiano", "Assistenza", "Privacy", "Tutte le lingue",
           "Informativa sulla privacy di DyeLog: locale, senza account, senza raccolta.",
           "Assistenza, FAQ e contatti per DyeLog."),
    "pt-BR": ("pt-BR", "Português (Brasil)", "Suporte", "Privacidade", "Todos os idiomas",
           "Política de privacidade do DyeLog: local, sem conta, sem coleta.",
           "Ajuda, perguntas frequentes e contato do DyeLog."),
    "ru": ("ru", "Русский", "Поддержка", "Конфиденциальность", "Все языки",
           "Политика конфиденциальности DyeLog: локально, без аккаунта, без сбора данных.",
           "Поддержка, вопросы и контакты DyeLog."),
    "nl": ("nl", "Nederlands", "Ondersteuning", "Privacy", "Alle talen",
           "DyeLog Privacybeleid: lokaal, geen account, geen gegevensverzameling.",
           "DyeLog hulp, FAQ en contact."),
    "pl": ("pl", "Polski", "Wsparcie", "Prywatność", "Wszystkie języki",
           "Polityka prywatności DyeLog: lokalnie, bez konta, bez zbierania danych.",
           "Pomoc, FAQ i kontakt DyeLog."),
    "tr": ("tr", "Türkçe", "Destek", "Gizlilik", "Tüm diller",
           "DyeLog Gizlilik Politikası: yerel, hesapsız, veri toplamıyor.",
           "DyeLog yardım, SSS ve iletişim."),
    "sv": ("sv", "Svenska", "Support", "Integritet", "Alla språk",
           "DyeLog integritetspolicy: lokalt, inget konto, ingen datainsamling.",
           "DyeLog hjälp, FAQ och kontakt."),
    "da": ("da", "Dansk", "Support", "Privatliv", "Alle sprog",
           "DyeLog privatlivspolitik: lokalt, ingen konto, ingen dataindsamling.",
           "DyeLog hjælp, ofte stillede spørgsmål og kontakt."),
}


def nav_for(code: str) -> str:
    _, _, s_label, p_label, all_label, _, _ = LANGS[code]
    return (
        f'<a href="/dyelog/support-{code}.html">{s_label}</a>'
        f'<a href="/dyelog/privacy-{code}.html">{p_label}</a>'
        f'<a href="/dyelog/index.html">{all_label}</a>'
    )


def page_title(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


built = []
for code, (html_lang, _, _, _, _, p_desc, s_desc) in LANGS.items():
    for kind, md_name, url_name, desc in (
        ("privacy", f"privacy-policy.{code}.md", f"privacy-{code}.html", p_desc),
        ("support", f"support.{code}.md", f"support-{code}.html", s_desc),
    ):
        md_path = SRC / md_name
        if not md_path.exists():
            raise SystemExit(f"missing source: {md_path}")
        text = md_path.read_text(encoding="utf-8")
        body = markdown.markdown(text, extensions=["tables"])
        html = (
            TEMPLATE.replace("@LANG@", html_lang)
            .replace("@TITLE@", page_title(text, f"DyeLog {kind}"))
            .replace("@DESC@", desc)
            .replace("@NAV@", nav_for(code))
            .replace("@BODY@", body)
            .replace("@EMAIL@", EMAIL)
        )
        (HERE / url_name).write_text(html, encoding="utf-8")
        built.append(url_name)

intro_en = (
    "<p>DyeLog is a local-first hair color formula archive for hairstylists and colorists. "
    "No account, no tracking, one-time purchase.</p>"
)
intro_zh = (
    "<p>染记是面向发型师与染色师的本地优先配色档案。无账号、零追踪、一次买断。</p>"
)
entries = "".join(
    f"<li><a href=\"/dyelog/privacy-{c}.html\">{p}</a> · "
    f"<a href=\"/dyelog/support-{c}.html\">{s}</a></li>"
    for c, (_, label, s, p, _, _, _) in LANGS.items()
)
index_body = (
    f"<h1>DyeLog / 染记</h1>{intro_en}{intro_zh}"
    "<h2>Privacy Policy &amp; Support / 隐私政策与支持</h2><ul>" + entries + "</ul>"
)
(HERE / "index.html").write_text(
    TEMPLATE.replace("@LANG@", "en")
    .replace("@TITLE@", "DyeLog / 染记")
    .replace("@DESC@", "DyeLog: a local-first hair color formula archive.")
    .replace("@NAV@", nav_for("en"))
    .replace("@BODY@", index_body)
    .replace("@EMAIL@", EMAIL),
    encoding="utf-8",
)
built.append("index.html")

print("built:", ", ".join(sorted(built)))
