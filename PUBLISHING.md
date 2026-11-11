# Publishing StockSignal OSS safely

This folder is an independently authored, minimal public release. It is NOT a copy of private Bandel Scout source or configuration.

## GitHub repository settings

- Repository name: `stocksignal-oss`
- Description: `Privacy-first, dependency-free product availability checker with conservative status reports.`
- Visibility: **Public**, only after checking the preview of all uploaded files.
- Topics: `open-source`, `python`, `stock-monitor`, `privacy`, `availability`, `restock-alerts`
- License: MIT (included). Do not initialize the GitHub repository with an additional README/license/gitignore; these already exist.
- Keep Issues and Discussions optional, enable secret scanning / push protection where available.
- Do not connect the existing Vercel production project.

## Publish using GitHub web UI

1. Create a **new, empty** repository named `stocksignal-oss` at https://github.com/new; use an account whose public profile/username you are comfortable exposing.
2. Open the new repository, select **uploading an existing file**, and upload the *contents* of this package, not any personal files or an old `.git` directory. GitHub's web upload may not reliably handle hidden folders; check `.github/workflows/test.yml` and `.gitignore` afterward.
3. Review the GitHub commit author's **public name, username, email visibility, and avatar** before your first commit. Configure a GitHub no-reply email if desired.
4. Verify that all 13 tracked files are present, with no data other than placeholders and generic project text.
5. Confirm that the Actions test workflow passes. Do not claim a production-ready service; this is an early prototype.
6. Copy your **new public repository URL** into the official application form at https://developers.openai.com/community/codex-for-oss.

## Optional local git steps

Do not run these inside any existing personal project. Configure a public-safe git author before committing:

```sh
cd stocksignal-oss
git init -b main
git config user.name "Your chosen public contributor name"
git config user.email "YOUR_GITHUB_NOREPLY_EMAIL"
git add README.md LICENSE .gitignore .github src tests examples PRIVACY.md SECURITY.md CONTRIBUTING.md APPLICATION.md PUBLISHING.md
git diff --cached --stat
git diff --cached --check
git commit -m "Initial public-safe StockSignal OSS release"
git remote add origin https://github.com/YOUR_PUBLIC_USERNAME/stocksignal-oss.git
git push -u origin main
```

Never publish `.env`, private logs, account data, customer messages, live store integrations, Git history from the private project, or deployment credentials. An open-source release and a new repository alone do not guarantee eligibility for Codex for OSS.
