# plesion.com

Static website for the PLESION app, hosted on GitHub Pages from the `main` branch. No build step: every commit to `main` is published as-is.

The `CNAME` file sets the custom domain (plesion.com). DNS stays in Google Cloud DNS: plesion.com has GitHub's four A records, and www.plesion.com is a CNAME to plesion.github.io (GitHub redirects www to plesion.com).

| File | Page |
|---|---|
| `index.html` | Landing page (plesion.com) |
| `data-policy.html` | plesion.com/data-policy |
| `terms-of-service.html` | plesion.com/terms-of-service |
| `download.html` | plesion.com/download: one link for social bios. Phones go straight to the App Store or Google Play (tagged with the platform the visitor came from); computers see the badges and a QR code |
| `styles.css` | Styles shared by all pages |
| `assets/` | Logo, handwritten wordmark, favicons |

Header and footer are repeated in each HTML file, so a change to a link there needs to be made in all three pages.

After changing `styles.css`, bump the `?v=` value on the stylesheet link in all three HTML files, so browsers fetch the new version instead of a cached one.
