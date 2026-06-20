(function () {
  'use strict';

  function ready(fn) {
    if (document.readyState !== 'loading') {
      fn();
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
  }

  ready(function () {
    var nav = document.querySelector('.main-nav');
    if (!nav) return;

    var stickyNavTop = nav.offsetTop;

    function updateStickyNav() {
      if (window.scrollY > stickyNavTop) {
        nav.classList.add('sticky');
      } else {
        nav.classList.remove('sticky');
      }
    }

    updateStickyNav();
    window.addEventListener('scroll', updateStickyNav, { passive: true });
    window.addEventListener('resize', function () {
      stickyNavTop = nav.offsetTop;
      updateStickyNav();
    });
  });
})();
