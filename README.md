# Research website (Jekyll + GitHub Pages)

A self-contained Jekyll site — no external theme gem, so every layout, style,
and piece of content is in this repo and editable. Built to be hosted free on
GitHub Pages.

---

## 1. Preview it locally

You need Ruby (3.0+) and Bundler installed.

```bash
bundle install
bundle exec jekyll serve
```

Open <http://localhost:4000>. The site rebuilds as you edit; refresh the page.
(Restart the command after editing `_config.yml`.)

---

## 2. Put it on GitHub Pages

**For a personal site at `https://<username>.github.io`:**

1. Create a repository named exactly `<username>.github.io`.
2. Push this folder's contents to the `main` branch.
3. In the repo: **Settings → Pages → Build and deployment → Source →
   "Deploy from a branch"**, branch `main`, folder `/ (root)`. Save.
4. Wait ~1 minute. Your site is live.

In `_config.yml`, set `url` to your address and leave `baseurl: ""`.

**For a project site at `https://<username>.github.io/<repo-name>`:**
set `baseurl: "/<repo-name>"` in `_config.yml` instead. Every link in the
site already uses Jekyll's `relative_url`, so both work without edits.

> There are two deploy methods. The branch method above is simplest.
> The `.github/workflows/pages.yml` file is an *alternative* (set Source to
> "GitHub Actions"). Use one or the other — not both. Delete the workflow
> file if you use the branch method.

---

## 3. Where to edit things

| To change… | Edit this |
|---|---|
| Your name, role, email, ORCID, GitHub, site address | `_config.yml` |
| Colours and fonts | the `:root` block at the top of `assets/css/style.scss` |
| The top menu | `_data/navigation.yml` |
| Research threads | `_data/projects.yml` |
| Software / tools | `_data/tools.yml` |
| Publications | `_data/publications.yml` |
| Group members & collaborators | `_data/people.yml` |
| Your headshot | add the file to `assets/img/`, then set `author.photo` in `_config.yml` |
| Field photos & captions | `_data/photos.yml` (add image path + caption per photo) |
| Home page hero text | `index.html` (the `.hero` section) |
| Teaching page prose | `teaching.md` |

Set `featured: true` on a project, tool, or publication to surface it on the
home page.

---

## Notes

- **Publications** and **people** files contain placeholder / draft entries.
  Replace the publications with real references, and confirm names with people
  before listing them.
- Drop a profile photo or figures into `assets/img/` and reference them as
  `{{ '/assets/img/yourfile.jpg' | relative_url }}`.
- The palette and fonts come from your Claude Design tokens: an ice-blue
  scale for structure and interaction, a rock-grey neutral for text, and amber
  reserved as a sparing personal accent (it appears once, as the tick above the
  home hero). Type is Source Serif 4 (display), Public Sans (body), IBM Plex
  Mono (code). The `:root` block in `style.scss` holds the full scale as the
  single source of truth — the "Site roles" section below it decides which
  scale value each part of the page uses, so you can restyle by repointing a
  role rather than hunting through the CSS.
