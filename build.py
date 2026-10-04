"""Build the portfolio with Python's standard library. Run: python3 build.py"""
from pathlib import Path
import html
import json
import re
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent
content = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
template = (ROOT / 'src/index.template.html').read_text(encoding='utf-8')

def substitute(match):
    key = match.group(1)
    if key not in content or not isinstance(content[key], str):
        raise ValueError(f'Missing or non-text content value: {key}')
    return html.escape(content[key], quote=True)

result = re.sub(r'\{\{([a-z0-9_]+)\}\}', substitute, template)
if '{{' in result:
    raise ValueError('Unresolved template marker')

class Validator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                raise ValueError('Duplicate element ID: ' + a['id'])
            self.ids.add(a['id'])
        for key in ('src', 'href'):
            if a.get(key):
                self.refs.append(a[key])
        if a.get('data-evidence'):
            self.refs.append('assets/' + a['data-evidence'])

check = Validator()
check.feed(result)
for ref in check.refs:
    if ref.startswith('#'):
        if ref[1:] not in check.ids:
            raise ValueError('Missing anchor: ' + ref)
    elif re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', ref):
        if not ref.startswith(('https://', 'mailto:')):
            raise ValueError('Only HTTPS and email links are allowed: ' + ref)
    elif not (ROOT / 'site' / ref).is_file():
        raise ValueError('Missing local asset: ' + ref)

(ROOT / 'site/index.html').write_text(result, encoding='utf-8')
print('Built site/index.html. Content, anchors and local assets validated.')
