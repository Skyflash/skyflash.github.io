// Lightbox minimale per le immagini dei post (.post-image): click o Invio
// aprono l'immagine a schermo intero. Nessuna dipendenza; l'overlay viene
// creato al primo utilizzo. Se la pagina non ha immagini di post, non fa nulla.
(function () {
  var images = document.querySelectorAll('.post-image');
  if (!images.length) return;

  var box, boxImg, lastFocus;

  function build() {
    box = document.createElement('div');
    box.className = 'lightbox';
    box.hidden = true;
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.innerHTML =
      '<button type="button" class="lightbox__close" aria-label="Chiudi">×</button>' +
      '<img class="lightbox__img" alt="">';
    boxImg = box.querySelector('.lightbox__img');

    // Click sullo sfondo o sul pulsante: chiude. Click sull'immagine: no.
    box.addEventListener('click', function (e) {
      if (e.target !== boxImg) close();
    });
    document.body.appendChild(box);
  }

  function onKey(e) {
    if (e.key === 'Escape') close();
  }

  function open(src, alt) {
    if (!box) build();
    boxImg.src = src;
    boxImg.alt = alt || '';
    lastFocus = document.activeElement;
    box.hidden = false;
    box.offsetWidth; // forza un reflow: la transizione di opacità parte da 0
    box.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    document.addEventListener('keydown', onKey);
    box.querySelector('.lightbox__close').focus();
  }

  function close() {
    if (!box || box.hidden) return;
    box.classList.remove('is-open');
    box.hidden = true;
    boxImg.removeAttribute('src');
    document.body.style.overflow = '';
    document.removeEventListener('keydown', onKey);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  images.forEach(function (img) {
    img.setAttribute('role', 'button');
    img.setAttribute('tabindex', '0');
    img.addEventListener('click', function () {
      open(img.currentSrc || img.src, img.alt);
    });
    img.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        open(img.currentSrc || img.src, img.alt);
      }
    });
  });
})();
