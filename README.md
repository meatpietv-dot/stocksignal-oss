# StockSignal OSS

Privacy-first, community-maintained product availability checker, inspired by the core idea of a personal restock dashboard. This is a **new, isolated OSS edition**, not a byte-for-byte clone of any private production application.

## What works

- Check a user-provided list of **public HTTPS product pages** from a local JSON file.
- Classify results conservatively: `unavailable`, `possible_stock`, `uncertain`, `unknown`, `check_failed`.
- Output a JSON report, useful for integrations.
- Synthetic demo, built-in unit tests and a CI workflow.
- Zero external Python packages, no user accounts, no analytics, no tracking.

## Quick start

Requires Python 3.10+.

```bash
python -m unittest discover -s tests -v
python -m src.monitor --demo --out demo-results.json
```

To monitor actual public pages, replace `examples/products.json` with your own list and run:

```bash
python -m src.monitor --config examples/products.json --out results.json
```

### Important limits

- `possible_stock` **does not prove** a listing can actually be purchased.
- Some shops render inventory in JavaScript, block automated checks, or change their wording. This scanner does not bypass security measures.
- Honor merchant terms, robots policies and rate limits. Avoid frequent polling.
- For production deployments, add hostname-to-IP validation and redirect controls to prevent DNS-rebinding / SSRF. Do not expose arbitrary URL scanning as a public API without them.
- No alert delivery, payment, waitlist sign-up or e-mail synchronization is included in this public version.

## Roadmap

1. Opt-in site-specific parsers and JSON-LD structured availability detection.
2. Safeguarded HTTP client with DNS / redirect validation, persistent local state and differential alerts.
3. Accessible offline dashboard and documented plugin interface.
4. Integration tests using synthetic fixtures; community contributions.

## Security and privacy

The public edition contains only sample items and generic code. Never commit `.env` files, auth tokens, real cookies, personal inbox data, waitlist records, production Edge Config exports or API keys. Run a secret scanner before publishing and review Git history. See `SECURITY.md` and `PRIVACY.md`.

## Contributing

Issues and pull requests are welcome. See `CONTRIBUTING.md`. Project is licensed under MIT (`LICENSE`).

## Publishing and applying

For a privacy review and setup of a **separate** GitHub repository, see [PUBLISHING.md](PUBLISHING.md). The existing private application, user accounts, connected services, and deployments are not part of this project.
