# Zhangshuai Hou (侯章帅) — Academic Webpage

Live site URL once deployed on GitHub Pages: `https://lewis-hou.github.io`

## Quick Deploy to GitHub Pages (Lewis-Hou)

1. Go to GitHub and create a new **public** repository named **`Lewis-Hou.github.io`**.
2. Upload all files and folders from this package (`index.html`, `.nojekyll`, `images/`, `data/`, `scripts/`, `.github/`) to the root of the repository (via `git push` or GitHub's **Add file → Upload files**).
3. Open **Settings → Pages**, set **Source** to **Deploy from a branch**, choose **`main`** and **`/ (root)`**, and click **Save**.
4. Within 1–2 minutes, your site will be live at `https://lewis-hou.github.io`.

## How to Add Fieldwork Photos (添加野外照片)

1. Upload your photo (JPG/WebP) into the `images/` folder (e.g., `images/junggar-2025.jpg`).
2. Open `data/gallery.json` on GitHub and add a new entry at the top of the list (set `"isSample": false` and `"src": "images/junggar-2025.jpg"`).
3. Commit your change — the live gallery updates automatically.
4. To add your personal headshot, upload `images/portrait.jpg` and set `PORTRAIT_URL = "images/portrait.jpg"` inside `index.html`.

## Automatic Citation Metrics (自动更新引用指标)

- **Weekly GitHub Action**: `.github/workflows/update-metrics.yml` runs every Monday (or anytime via **Actions → Update Academic Metrics → Run workflow**) to refresh `data/metrics.json` from Google Scholar (`4TMRXlUAAAAJ`) with an automatic OpenAlex ORCID (`0009-0009-1897-5811`) fallback.
- **Live Browser Refresh**: `index.html` loads `data/metrics.json` on startup and also checks the public OpenAlex ORCID API (`https://api.openalex.org/authors/orcid:0009-0009-1897-5811`) as a live supplement without exposing any API keys.
