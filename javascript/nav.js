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
    var flexmenu = document.getElementById('flexmenu');
    if (!flexmenu) return;

    var toggle = flexmenu.querySelector('.navbutton-menu');
    var mainmenu = flexmenu.querySelector('#main-menu');
    var mediasize = 768;

    if (toggle) {
      toggle.setAttribute('role', 'button');
      toggle.setAttribute('aria-label', 'Toggle navigation menu');
      toggle.setAttribute('tabindex', '0');
      toggle.setAttribute('aria-expanded', 'false');

      function toggleMainMenu() {
        if (!mainmenu) return;
        var isOpen = mainmenu.classList.contains('open');
        toggle.classList.toggle('menu-opened', !isOpen);
        toggle.setAttribute('aria-expanded', isOpen ? 'false' : 'true');
        mainmenu.style.display = isOpen ? 'none' : 'block';
        mainmenu.classList.toggle('open', !isOpen);
      }

      toggle.addEventListener('click', toggleMainMenu);
      toggle.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggleMainMenu();
        }
      });
    }

    flexmenu.querySelectorAll('li').forEach(function (li) {
      if (li.querySelector(':scope > ul')) {
        li.classList.add('has-sub');
      }
    });

    flexmenu.querySelectorAll('.has-sub').forEach(function (li) {
      if (li.querySelector(':scope > .submenu-button')) return;

      var btn = document.createElement('span');
      btn.className = 'submenu-button';
      btn.setAttribute('role', 'button');
      btn.setAttribute('aria-label', 'Toggle submenu');
      btn.setAttribute('tabindex', '0');
      li.insertBefore(btn, li.firstChild);

      function toggleSubmenu() {
        var sub = li.querySelector(':scope > ul');
        if (!sub) return;
        var isOpen = sub.classList.contains('open');
        btn.classList.toggle('submenu-opened', !isOpen);
        sub.style.display = isOpen ? 'none' : 'block';
        sub.classList.toggle('open', !isOpen);
      }

      btn.addEventListener('click', toggleSubmenu);
      btn.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggleSubmenu();
        }
      });
    });

    function resizeFix() {
      var lists = flexmenu.querySelectorAll('ul');
      if (window.innerWidth > mediasize) {
        lists.forEach(function (ul) {
          ul.style.display = '';
        });
      } else {
        lists.forEach(function (ul) {
          if (ul.id !== 'main-menu' || !ul.classList.contains('open')) {
            ul.style.display = 'none';
          }
        });
        lists.forEach(function (ul) {
          ul.classList.remove('open');
        });
        if (toggle) {
          toggle.classList.remove('menu-opened');
          toggle.setAttribute('aria-expanded', 'false');
        }
      }
    }

    resizeFix();
    window.addEventListener('resize', resizeFix);
  });
})();
