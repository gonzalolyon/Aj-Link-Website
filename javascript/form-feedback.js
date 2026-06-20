(function () {
  var params = new URLSearchParams(window.location.search);
  var enviado = params.get('enviado');
  var success = params.get('success');
  var error = params.get('error');
  var container = document.getElementById('contactos');

  if (!container || (!enviado && !success && !error)) {
    return;
  }

  var isSpanish = document.documentElement.lang === 'es';
  var alert = document.createElement('div');
  alert.className = 'form-alert';

  if (enviado === '1' || success === '1') {
    alert.className += ' form-alert--success';
    alert.textContent = isSpanish
      ? '¡Gracias! Su mensaje fue enviado correctamente. Nos pondremos en contacto pronto.'
      : 'Thank you! Your message was sent successfully. We will get back to you soon.';
  } else {
    alert.className += ' form-alert--error';
    var messages = {
      campos: isSpanish
        ? 'Por favor complete todos los campos obligatorios.'
        : 'Please fill in all required fields.',
      email: isSpanish
        ? 'Ingrese una dirección de correo válida.'
        : 'Please enter a valid email address.',
      largo: isSpanish
        ? 'Su mensaje es demasiado largo. Intente con un texto más breve.'
        : 'Your message is too long. Please shorten it and try again.',
      envio: isSpanish
        ? 'No pudimos enviar su mensaje. Inténtelo de nuevo o llámenos directamente.'
        : 'We could not send your message. Please try again or call us directly.'
    };
    alert.textContent = messages[error] || messages.envio;
  }

  container.insertBefore(alert, container.firstChild);

  if (window.history && window.history.replaceState) {
    window.history.replaceState({}, document.title, window.location.pathname + window.location.hash);
  }
})();
