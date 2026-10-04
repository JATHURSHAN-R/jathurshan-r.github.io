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

## Automatic HTB updates

The publishing workflow refreshes HTB progress every six hours (00:23, 06:23, 12:23 and 18:23 UTC), on pushes to main, and through Actions > Publish portfolio > Run workflow. Scheduled start times may be delayed by GitHub. It is polling, not an instant HTB webhook.

Required repository secret: `HTB_API_TOKEN`. Set it under Settings > Secrets and variables > Actions. Never put its value in source files, issues or screenshots. The secret is available only to the sync step, not the deployed website.

The sync reads three fixed profile endpoints on `labs.hackthebox.com` for user `2170950`:

- `GET /api/v4/user/profile/basic/2170950`: system owns and user owns.
- `GET /api/v4/user/profile/progress/challenges/2170950`: solved challenges.
- `GET /api/v5/user/profile/activity/2170950`: recent user/root machine-flag activity from the returned page.

These routes were verified with this account; they are not treated as a guaranteed stable public API. Rank and level are deliberately not copied: the v4 rank differed from the newer profile display. Rank, level, season, streak, THM statistics, and screenshots remain manual snapshots. A user flag is explicitly labelled as user activity, not full machine completion.

Only the allowlisted counts, machine activity name/label, and UTC sync time are merged into content.json in the temporary runner workspace. Raw API responses and the token are never written to disk or logged. Sync values are not committed back to GitHub. The site's displayed timestamp is the last successful fetch; editing content.json still controls all manual fields.

If the token expires, requests fail, or response validation fails, the build stops before publishing, preserving the last successful live deployment. Fix the secret or integration and run the workflow again. The existing timestamp lets visitors see how old the data is. Check Actions for failures. GitHub can disable scheduled workflows in inactive public repositories; re-enable the workflow if necessary.

The workflow uses read-only repository access and commit-pinned official GitHub Actions. Only the deploy job receives Pages write and OIDC permissions. API redirects are refused. To pause automation, remove the schedule entry; pushes will still sync. To fully disconnect HTB, remove the refresh step and revoke the HTB token, then maintain the counts manually.

No terminal interface, database, or third-party runtime script is required.

## Validation and known limitation

The package passes the Python build, local asset and anchor checks, and JavaScript syntax validation. Desktop/mobile browser rendering has not been verified in this environment. The previously reported missing visual was not identified by a screenshot, so its cause is not confirmed. After publishing, check the graphic, evidence images and CV download on your browser and mobile device.

## Official setup references

- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
