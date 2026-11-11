"""StockSignal OSS: privacy-first, conservative product availability scanner.

No cookies, email integrations, user identities or API credentials are stored.
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.parse import urlparse

NEGATIVE = [r'out\s*of\s*stock', r'sold\s*out', r'nicht\s*lieferbar', r'ausverkauft', r'currently\s*unavailable']
POSITIVE = [r'in\s*stock', r'auf\s*lager', r'sofort\s*lieferbar', r'add\s*to\s*cart', r'in\s*den\s*warenkorb']


def classify(html: str) -> str:
    """Classify unverified page text; never assert stock from weak or mixed evidence."""
    body = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', ' ', html, flags=re.I | re.S)
    text = unescape(re.sub(r'<[^>]+>', ' ', body)).lower()
    text = re.sub(r'\s+', ' ', text)
    negatives = any(re.search(p, text, flags=re.I) for p in NEGATIVE)
    positives = any(re.search(p, text, flags=re.I) for p in POSITIVE)
    if negatives:
        return 'unavailable' if not positives else 'uncertain'
    return 'possible_stock' if positives else 'unknown'


def safe_url(url: str) -> bool:
    parsed = urlparse(url)
    host = parsed.hostname or ''
    if parsed.scheme != 'https' or not host or parsed.username or parsed.password:
        return False
    if host.lower() in {'localhost', 'localhost.localdomain'} or host.endswith('.local'):
        return False
    try:
        import ipaddress
        ipaddress.ip_address(host)
        return False  # Public hostname only; DNS security requires network-level controls.
    except ValueError:
        pass
    return True


def check_product(item: dict, *, fetch=None) -> dict:
    url = item.get('url', '')
    if not safe_url(url):
        return {'name': item.get('name', ''), 'url': '', 'status': 'invalid_url'}
    try:
        if fetch is None:
            request = urllib.request.Request(url, headers={'User-Agent': 'StockSignalOSS/0.1 (+public-open-source-checker)'})
            with urllib.request.urlopen(request, timeout=12) as response:
                content_type = response.headers.get('content-type', '')
                if 'text/html' not in content_type:
                    raise ValueError('Unexpected response type')
                html = response.read(500_000).decode('utf-8', 'replace')
        else:
            html = fetch(url)
        return {'name': item.get('name', ''), 'url': url, 'status': classify(html)}
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        return {'name': item.get('name', ''), 'url': url, 'status': 'check_failed', 'error': type(exc).__name__}


def main() -> int:
    parser = argparse.ArgumentParser(description='Conservative stock check with explicitly supplied public URLs')
    parser.add_argument('--config', default='examples/products.json')
    parser.add_argument('--out', default='results.json')
    parser.add_argument('--demo', action='store_true', help='Generate synthetic demonstration without networking')
    args = parser.parse_args()
    items = json.loads(Path(args.config).read_text(encoding='utf8'))['products']
    fetch = (lambda url: '<main>Sample product: out of stock</main>') if args.demo else None
    results = [check_product(item, fetch=fetch) for item in items]
    output = {'generated_at': datetime.now(timezone.utc).isoformat(), 'note': 'possible_stock is not a confirmed purchasable offer', 'results': results}
    Path(args.out).write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf8')
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
