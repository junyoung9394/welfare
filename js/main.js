// 검색 기능
function doSearch() {
  const q = document.getElementById('searchInput').value.trim();
  if (!q) return;
  window.location.href = 'search.html?q=' + encodeURIComponent(q);
}

document.getElementById('searchInput')?.addEventListener('keydown', function(e) {
  if (e.key === 'Enter') doSearch();
});

// 카테고리 클릭 → 검색 페이지
document.querySelectorAll('.cat-card[data-cat]').forEach(function(el) {
  el.addEventListener('click', function() {
    window.location.href = 'search.html?cat=' + encodeURIComponent(el.dataset.cat);
  });
});
