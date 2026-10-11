"""Wrap the tracker (../index.html) in the Pákó page shell and write pako-site/taper.html.

    python3 -I pako/build.py [path/to/pako-site]

The app itself is identical in both places. Only the shell and theme differ.
The nav, footer, menu and its toggle come from pako-site/build/partials, and the
footer's subscribe script from audit.html, so the page matches the rest of the site.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Downloads/pako-site'))

def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()

def partial(name):
    return re.sub(r'^<!--[\s\S]*?-->\s*', '', read(os.path.join(SITE, 'build', 'partials', name))).strip()

app = read(os.path.join(HERE, '..', 'index.html'))
style = re.search(r'<style>[\s\S]*?</style>', app).group(0)
body = re.search(r'<body>([\s\S]*)</body>', app).group(1).strip()
sub = re.search(r'<script>\s*\(function\(\)\{[\s\S]*?pk-subscribe[\s\S]*?</script>', read(os.path.join(SITE, 'audit.html'))).group(0)

out = read(os.path.join(HERE, 'shell.html'))
for k, v in {
    'APP_STYLE': style, 'THEME': read(os.path.join(HERE, 'theme.css')).strip(),
    'NAV': partial('nav.html'), 'MENU': partial('mobile-menu.html'),
    'FOOTER': partial('footer.html'), 'TOGGLE': partial('menu-toggle.html'),
    'SUBSCRIBE': sub, 'APP': body,
}.items():
    out = out.replace('{{' + k + '}}', v)
assert '{{' not in out, 'unfilled placeholder'
with open(os.path.join(SITE, 'taper.html'), 'w', encoding='utf-8') as f:
    f.write(out)
print('wrote', os.path.join(SITE, 'taper.html'))
