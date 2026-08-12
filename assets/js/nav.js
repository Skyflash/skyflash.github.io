(function () {
  var toggle = document.getElementById('nav-toggle');
  var list = document.getElementById('nav-list');

  if (toggle && list) {
    toggle.addEventListener('click', function () {
      var isOpen = list.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  var blogToggle = document.getElementById('nav-blog-toggle');
  var blogItem = blogToggle ? blogToggle.closest('.nav-item') : null;

  if (blogToggle && blogItem) {
    blogToggle.addEventListener('click', function () {
      var isOpen = blogItem.classList.toggle('is-open');
      blogToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  document.addEventListener('click', function (e) {
    if (blogItem && !blogItem.contains(e.target)) {
      blogItem.classList.remove('is-open');
      if (blogToggle) blogToggle.setAttribute('aria-expanded', 'false');
    }
  });
})();
