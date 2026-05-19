// Search tracking
function trackSearch(query) {
  if (typeof gtag !== 'undefined') {
    gtag('event', 'search', { search_term: query });
  }
}

// Post click tracking
function trackPostClick(postTitle, postUrl) {
  if (typeof gtag !== 'undefined') {
    gtag('event', 'select_content', {
      content_type: 'post',
      item_id: postUrl,
      content_id: postTitle
    });
  }
}

// Outbound link tracking (bokjiro, work24, gov.kr etc)
// Auto-attach on DOMContentLoaded:
// - Listen for clicks on .post-card elements → trackPostClick
// - Listen for form submit / search button click → trackSearch
// - Listen for external links (target="_blank") → track outbound
document.addEventListener('DOMContentLoaded', function() {
  // post card clicks
  document.querySelectorAll('a.post-card, a.related-card').forEach(function(el) {
    el.addEventListener('click', function() {
      trackPostClick(el.querySelector('.post-title, .rc-title')?.textContent?.trim() || '', el.href);
    });
  });

  // search button / form
  var searchBtn = document.querySelector('.search-box button, #searchBtn, button[onclick*="doSearch"]');
  if (searchBtn) {
    searchBtn.addEventListener('click', function() {
      var input = document.querySelector('.search-box input, #searchInput');
      if (input && input.value) trackSearch(input.value);
    });
  }

  // outbound links
  document.querySelectorAll('a[target="_blank"]').forEach(function(el) {
    el.addEventListener('click', function() {
      if (typeof gtag !== 'undefined') {
        gtag('event', 'click', { event_category: 'outbound', event_label: el.href });
      }
    });
  });

  // FAQ opens
  document.querySelectorAll('.faq-q').forEach(function(el) {
    el.addEventListener('click', function() {
      var question = el.textContent.trim().slice(0, 50);
      if (typeof gtag !== 'undefined') {
        gtag('event', 'faq_open', { question: question });
      }
    });
  });
});
