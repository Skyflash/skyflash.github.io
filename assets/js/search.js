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

  input.addEventListener('input', function () {
    var query = input.value.trim().toLowerCase();
    results.innerHTML = '';
    if (!query || !data) return;

    var matches = data.filter(function (item) {
      return item.title.toLowerCase().indexOf(query) !== -1 ||
        (item.description && item.description.toLowerCase().indexOf(query) !== -1);
    }).slice(0, 8);

    matches.forEach(function (item) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = item.url;
      a.textContent = item.title;
      li.appendChild(a);
      results.appendChild(li);
    });
  });
})();
