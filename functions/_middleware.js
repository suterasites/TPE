// Retire the test copy at tpe-12t.pages.dev (Tom asked, 2026-11-27).
//
// The Cloudflare Pages project behind tpe-12t.pages.dev is the SAME project
// that serves www.totalpilingandexcavations.com.au, so it cannot be deleted
// without taking the live site down. A _redirects rule cannot do it either:
// Pages matches _redirects on path only, never on hostname. So the old host
// is 301'd here to the same path on the real domain.
//
// Only the exact production host is redirected. <deployment>.tpe-12t.pages.dev
// and <branch>.tpe-12t.pages.dev previews keep working (Cloudflare already
// serves those with X-Robots-Tag: noindex), because staged pages on focus/
// branches are reviewed there before they are published.
//
// _routes.json keeps static assets out of this function, so a page view on
// the live domain costs one invocation, not one per image.

const OLD_HOST = "tpe-12t.pages.dev";
const LIVE_HOST = "www.totalpilingandexcavations.com.au";

export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (url.hostname === OLD_HOST) {
    url.protocol = "https:";
    url.hostname = LIVE_HOST;
    url.port = "";
    return Response.redirect(url.toString(), 301);
  }
  return next();
}
