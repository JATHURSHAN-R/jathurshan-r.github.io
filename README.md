# 0xFlame77 Portfolio

Jathurshan Rasathurai's cybersecurity portfolio. Static HTML, CSS and JavaScript, with a small Python build script. No npm install, database, paid hosting service or private API token is required.

## Publish under your own GitHub account

1. Create a repository under `JATHURSHAN-R` called `jathurshan-r.github.io`. Public repositories support GitHub Pages on GitHub Free. Publishing this repo makes the source, CV and bundled screenshots public, so review them first.
2. Extract the download. Upload the contents of `portfolio-github` to the repository root. Include the `.github/workflows/pages.yml` file (the `.github` folder may be hidden by your file manager). Do not upload the ZIP itself. Enable Add README when creating the repository if you want an initial `main` branch, then replace it with this README during upload.
3. In repository Settings > Pages > Build and deployment, choose **GitHub Actions** as Source.
4. Open Actions > Publish portfolio > Run workflow, selecting `main` if the initial upload happened before Pages was configured.
5. Wait for build and deploy to succeed. GitHub will show the live URL in Settings > Pages. The intended address is https://jathurshan-r.github.io — it is not live until deployment succeeds.

Alternatively, clone the new repo, copy these files into it, then use Git to add, commit and push to `main`.

## Everyday edits

| Change | File |
| --- | --- |
| Name, introduction, contact links, achievement counts and dates | `content.json` |
| Existing project titles and descriptions | `content.json` |
| Replace downloadable CV | `site/assets/Jathurshan_Rasathurai_CV.pdf` |
| Add projects, writeups or badges; edit other page text | `src/index.template.html` |
| Colours, spacing, font sizes and responsive layout | `site/style.css` |
| Animation, mobile navigation and evidence dialogs | `site/app.js` |
| Replace evidence screenshots | The corresponding PNG under `site/assets/` |

Edit `content.json` directly in GitHub using the pencil button. Keep the double quotes and commas. Commit to `main`. The workflow rebuilds and publishes the site automatically. A failed build does not replace the previous working deployment.

To replace the CV, upload the new PDF under the exact existing path and filename. If you change its filename, update `cv_path` in `content.json` too. This PDF contains your phone number and email address; review what you want to publish.

For achievement updates, update the numbers and `updated_date` together. Screenshot evidence has its own historical date. Replace screenshots and their captions if you want new evidence; changing statistics does not update old screenshots.

To add a project or writeup, duplicate its `<article>` or link card in `src/index.template.html`, then edit the copy. The `{{key}}` markers pull values from `content.json`. Plain text can also be edited directly in the template. Do not edit `site/index.html` directly: the next build replaces it.

## Local preview

From this folder:

```bash
python3 build.py
python3 -m http.server 8000 --directory site
```

On Windows you can use `py` instead of `python3`. Open http://localhost:8000. Stop with Ctrl+C.

## Recover an earlier version

Git stores your change history. Revert the commit that introduced a problem, then push to `main`. The publishing workflow deploys the restored version. Keep a copy of the old CV if you need easy comparisons.

## What is automatic

- Website deployment after a push to `main`.
- Content validation before deployment.

HTB and THM statistics are manual snapshots. No live API integration is enabled. Automatic platform syncing requires a verified, permitted data feed and a separate scheduled update workflow. Never put account passwords, session cookies or API tokens into these public files.

The original terminal has been removed. The site includes a lightweight abstract canvas animation, standard navigation, expandable project details and evidence dialogs. No ChatGPT login or Sites service is needed on GitHub Pages.

## Validation and known limitation

The package passes the Python build, local asset and anchor checks, and JavaScript syntax validation. Desktop/mobile browser rendering has not been verified in this environment. The previously reported missing visual was not identified by a screenshot, so its cause is not confirmed. After publishing, check the graphic, evidence images and CV download on your browser and mobile device.

## Official setup references

- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
