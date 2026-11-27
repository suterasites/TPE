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
// It also 301s every /page.html to the clean /page (TPE's marketer asked for
// a 301 specifically, 2026-11-27). Cloudflare already answered those with a
// 308, which is just as permanent, but a _redirects file cannot take over:
// Pages does not apply _redirects to routes a Function serves, and this
// middleware serves every non-asset route. Doing both here also makes
// tpe-12t.pages.dev/about.html one hop to www/about instead of two.
//
// _routes.json keeps static assets out of this function, so a page view on
// the live domain costs one invocation, not one per image.

const OLD_HOST = "tpe-12t.pages.dev";
const LIVE_HOST = "www.totalpilingandexcavations.com.au";

export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  let moved = false;
  if (url.hostname === OLD_HOST) {
    url.protocol = "https:";
    url.hostname = LIVE_HOST;
    url.port = "";
    moved = true;
  }
  if (url.pathname.endsWith(".html")) {
    // /index.html and /x/index.html -> the folder; /about.html -> /about
    url.pathname = url.pathname.endsWith("/index.html")
      ? url.pathname.slice(0, -"index.html".length)
      : url.pathname.slice(0, -".html".length);
    moved = true;
  }
  // The query string rides along untouched, so a gclid on an ad click survives.
  return moved ? Response.redirect(url.toString(), 301) : next();
}
