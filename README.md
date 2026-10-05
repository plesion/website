# plesion.com

Static website for the PLESION app, hosted on GitHub Pages from the `main` branch. No build step: every commit to `main` is published as-is.

The `CNAME` file sets the custom domain (plesion.com). DNS stays in Google Cloud DNS: plesion.com has GitHub's four A records, and www.plesion.com is a CNAME to plesion.github.io (GitHub redirects www to plesion.com).

| File | Page |
|---|---|
| `index.html` | Landing page (plesion.com), in English. The source for the translated home pages |
| `fr/index.html`, `it/index.html` | French and Italian home pages (plesion.com/fr/, plesion.com/it/). Generated: don't edit by hand |
| `_i18n/build.py` | Builds the translated home pages from `index.html` and fills in the footer language switcher |
| `data-policy.html` | plesion.com/data-policy |
| `terms-of-service.html` | plesion.com/terms-of-service |
| `download.html` | plesion.com/download: one link for social bios. Phones go straight to the App Store or Google Play (tagged with the platform the visitor came from); computers see the badges and a QR code |
| `404.html` | Shown for any address that doesn't exist |
| `robots.txt`, `sitemap.xml` | Tell search engines which pages exist |
| `styles.css` | Styles shared by all pages |
| `assets/` | Logo, handwritten wordmark, favicons |

Header and footer are repeated in each HTML file, so a change to a link there needs to be made in all three pages.

After changing `styles.css`, bump the `?v=` value on the stylesheet link in all three HTML files, so browsers fetch the new version instead of a cached one.

## Languages

English is the source. After any change to `index.html`, run `python3 _i18n/build.py` from the repository root and commit the regenerated `fr/` and `it/` pages with it. The script stops if an English string it translates has changed, so update its translation in `_i18n/build.py` at the same time. Jekyll doesn't publish the `_i18n` folder.

To add a language: add a line to `LANGS` and a list of translations to `T` in `_i18n/build.py`, add it to `PAGES` and `HINT` in the language script at the bottom of `index.html` and to the date names in the live strip script, add its `hreflang` link in the head of `index.html` and to `sitemap.xml`, then run the script.

The legal pages stay in English for now; the translated footers link to them with translated link text.

## Analytics

Cloudflare Web Analytics (cookieless, free). The beacon snippet sits just before `</body>` on every page.
