(function () {
  var toggleBtn = document.getElementById('nav-search-toggle');
  var panel = document.getElementById('search-panel');
  var input = document.getElementById('search-input');
  var results = document.getElementById('search-results');

  if (!toggleBtn || !panel || !input || !results) return;

  var baseurlMeta = document.querySelector('meta[name="baseurl"]');
  var baseurl = baseurlMeta ? baseurlMeta.getAttribute('content') : '';
  var data = null;

  function loadData() {
    if (data) return Promise.resolve(data);
    return fetch(baseurl + '/search.json')
      .then(function (res) { return res.json(); })
      .then(function (json) {
        data = (json && json.data) || [];
        return data;
      })
      .catch(function () {
        data = [];
        return data;
      });
  }

  function openPanel() {
    panel.hidden = false;
    toggleBtn.setAttribute('aria-expanded', 'true');
    input.value = '';
    results.innerHTML = '';
    loadData();
    input.focus();
  }

  function closePanel() {
    panel.hidden = true;
    toggleBtn.setAttribute('aria-expanded', 'false');
  }

  toggleBtn.addEventListener('click', function () {
    if (panel.hidden) {
      openPanel();
    } else {
      closePanel();
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closePanel();
  });

  // Punteggio di un elemento rispetto alle parole della query: le parole
  // trovate nel titolo pesano di più di quelle trovate solo in descrizione/
  // tag/categoria. Ritorna null se anche una sola parola non è presente
  // in nessun campo (match "AND", non "OR").
  function scoreItem(item, words) {
    var title = (item.title || '').toLowerCase();
    var rest = [item.description, item.tags, item.categories]
      .filter(Boolean)
      .join(' ')
      .toLowerCase();

    var score = 0;
    for (var i = 0; i < words.length; i++) {
      var word = words[i];
      var inTitle = title.indexOf(word) !== -1;
      var inRest = rest.indexOf(word) !== -1;
      if (!inTitle && !inRest) return null;
      score += inTitle ? 3 : 1;
    }
    return score;
  }

  function renderResults(matches) {
    results.innerHTML = '';
    matches.forEach(function (item) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = item.url;

      var title = document.createElement('span');
      title.className = 'search-results__title';
      title.textContent = item.title;
      a.appendChild(title);

      if (item.description) {
        var desc = document.createElement('span');
        desc.className = 'search-results__desc';
        desc.textContent = item.description;
        a.appendChild(desc);
      }

      li.appendChild(a);
      results.appendChild(li);
    });
  }

  input.addEventListener('input', function () {
    var words = input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    results.innerHTML = '';
    if (!words.length || !data) return;

    var scored = data
      .map(function (item) {
        var score = scoreItem(item, words);
        return score === null ? null : { item: item, score: score };
      })
      .filter(Boolean)
      .sort(function (a, b) { return b.score - a.score; })
      .slice(0, 8)
      .map(function (entry) { return entry.item; });

    renderResults(scored);
  });
})();
