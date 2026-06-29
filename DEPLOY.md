# Deployment — Aj-Link-Website

- **Intended production domain:** https://ajlink.com  ⚠️ **NOT current.**
  The live ajlink.com still shows an OLD version. It has **not** been updated because
  I no longer have access to that hosting, and the owner is difficult to contact.
- **Best / canonical version:** the **Netlify** deployment (this repo). This is the
  most up-to-date, correct version of the site.
- **Repo:** https://github.com/gonzalolyon/Aj-Link-Website
  Branches: `main`, `fix-clients-map`.
- **Type:** hand-coded static site (multi-page HTML/CSS/JS).

## Status / blockers
- Cannot push to ajlink.com (lost hosting access; owner unreachable).
- The Netlify site is the source of truth until ajlink.com access is regained.
- If/when domain access returns: point ajlink.com's DNS at the Netlify site (cleanest),
  or redeploy from this repo.

## Netlify
- **Live (best version):** https://ajlink-18.netlify.app
- Netlify project: `ajlink-18`  ·  admin: https://app.netlify.com/projects/ajlink-18
- The site's internal canonical is set to https://www.ajlink.com/ — so once DNS for
  ajlink.com can be pointed at this Netlify project, the live domain matches with no
  code changes.
- Auto-deploys on push to `main`.
