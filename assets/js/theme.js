(function () {
  var buttons = document.querySelectorAll('.theme-switch__btn');
  if (!buttons.length) return;

  function currentChoice() {
    try {
      var stored = localStorage.getItem('theme');
      if (stored === 'light' || stored === 'dark') return stored;
    } catch (e) {}
    return 'auto';
  }

  function applyAttribute(choice) {
    if (choice === 'auto') {
      document.documentElement.removeAttribute('data-theme');
    } else {
      document.documentElement.setAttribute('data-theme', choice);
    }
  }

  function updateButtons(choice) {
    buttons.forEach(function (btn) {
      var isActive = btn.getAttribute('data-theme-choice') === choice;
      btn.classList.toggle('is-active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });
  }

  function apply(choice) {
    applyAttribute(choice);
    try {
      if (choice === 'auto') {
        localStorage.removeItem('theme');
      } else {
        localStorage.setItem('theme', choice);
      }
    } catch (e) {}
    updateButtons(choice);
    // Giscus vive in un iframe cross-origin: cambiare tema sull'host non lo
    // aggiorna da solo, va detto esplicitamente via postMessage.
    var giscusFrame = document.querySelector('iframe.giscus-frame');
    if (giscusFrame) {
      giscusFrame.contentWindow.postMessage({
        giscus: { setConfig: { theme: choice === 'auto' ? 'preferred_color_scheme' : choice } }
      }, 'https://giscus.app');
    }
  }

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      apply(btn.getAttribute('data-theme-choice'));
    });
  });

  // Riapplica sempre sia l'attributo che lo stato dei pulsanti alla preferenza
  // salvata: non fidarsi che lo script inline nell'<head> sia riuscito a farlo
  // prima del paint (alcuni browser/estensioni orientati alla privacy bloccano
  // gli script inline pur permettendo file esterni come questo).
  var initialChoice = currentChoice();
  applyAttribute(initialChoice);
  updateButtons(initialChoice);
})();
