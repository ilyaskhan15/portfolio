# Google AdSense Troubleshooting

If your AdSense account shows "Getting ready" even after adding `ads.txt` and the AdSense script, try the following checklist:

- Ensure `ads.txt` is accessible at `https://yourdomain.com/ads.txt` (no trailing slash)
- Make sure the `ads.txt` contains your correct publisher ID: `pub-xxxxxxxxxxxxxxxx`
- Keep only a single AdSense script on the site (add it in `templates/base.html`).
- Create at least one ad unit in your AdSense account and place it on a content page (e.g., `post_detail.html`) with the correct `data-ad-slot`.
- Wait up to 2-4 weeks; sometimes review can take longer. If it's been longer than 30 days, contact AdSense support.
- Check the site is reachable and not blocking Googlebot via `robots.txt` or other server settings.
- Check that the domain in AdSense exactly matches the site domain (with/without www) and that HTTPS is used.

Quick tips:
- If you want to display ads automatically, enable Auto ads in AdSense and keep the `script` with `data-ad-client` in `base.html`.
- To display specific ad units, create them in AdSense and paste the `data-ad-slot` value into the `<ins class="adsbygoogle">` tag.

If you want, I can add an example ad unit to `post_detail.html` that uses a site setting or context variable to enable it safely.
