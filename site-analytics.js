(function () {
  'use strict';
  var id = 'G-4M29ST27KY';
  var hosts = ['japanese', 'chinese', 'biz100', 'baby', 'welfare', 'calc'].map(function (s) { return s + '.luckygrampus.com'; });
  if (hosts.indexOf(location.hostname) < 0 || window.__luckyAnalytics) return;
  try { if (localStorage.getItem('lucky-analytics-disabled') === '1') return; } catch (_) {}
  if (navigator.doNotTrack === '1' || navigator.globalPrivacyControl === true) return;
  window.__luckyAnalytics = true;
  window.dataLayer = window.dataLayer || [];
  function tag() { window.dataLayer.push(arguments); }
  function cleanUrl(value) { try { var u = new URL(value, location.href); return u.origin + u.pathname; } catch (_) { return ''; } }
  var lastPage = '', previousPage = cleanUrl(document.referrer);
  tag('js', new Date());
  tag('config', id, { send_page_view: false, allow_google_signals: false, allow_ad_personalization_signals: false, page_location: cleanUrl(location.href), page_referrer: previousPage });
  function pageView() {
    var current = cleanUrl(location.href);
    if (current === lastPage) return;
    tag('event', 'page_view', { send_to: id, page_location: current, page_title: document.title, page_referrer: previousPage });
    lastPage = current;
    previousPage = current;
  }
  var script = document.createElement('script');
  script.async = true;
  script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
  document.head.appendChild(script);
  pageView();
  ['pushState', 'replaceState'].forEach(function (method) {
    var original = history[method];
    history[method] = function () {
      var result = original.apply(this, arguments);
      window.setTimeout(pageView, 100);
      return result;
    };
  });
  window.addEventListener('popstate', function () { window.setTimeout(pageView, 100); });
  document.addEventListener('click', function (event) {
    var link = event.target instanceof Element ? event.target.closest('a[data-learning-link]') : null;
    if (!link) return;
    var target = new URL(link.href, location.href);
    if (target.origin !== location.origin) return;
    tag('event', 'learning_link_click', { send_to: id, page_location: cleanUrl(location.href), link_url: cleanUrl(link.href) });
  });
})();
