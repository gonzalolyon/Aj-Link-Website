(function () {
  'use strict';

  function isNetlifyHost() {
    return /\.netlify\.app$/i.test(window.location.hostname);
  }

  function configureContactForms() {
    document.querySelectorAll('form.form-contact[data-success-url]').forEach(function (form) {
      if (isNetlifyHost()) {
        form.action = form.getAttribute('data-success-url');
      } else {
        form.action = 'mail.php';
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', configureContactForms);
  } else {
    configureContactForms();
  }
})();
