/* A polyfill for browsers that don't support ligatures. */
/* The script tag referring to this file must be placed before the ending body tag. */

/* To provide support for elements dynamically added, this script adds
   method 'icomoonLiga' to the window object. You can pass element references to this method.
*/
(function () {
    'use strict';
    function supportsProperty(p) {
        var prefixes = ['Webkit', 'Moz', 'O', 'ms'],
            i,
            div = document.createElement('div'),
            ret = p in div.style;
        if (!ret) {
            p = p.charAt(0).toUpperCase() + p.substr(1);
            for (i = 0; i < prefixes.length; i += 1) {
                ret = prefixes[i] + p in div.style;
                if (ret) {
                    break;
                }
            }
        }
        return ret;
    }
    var icons;
    if (!supportsProperty('fontFeatureSettings')) {
        icons = {
            'phone': '&#xe974;',
            'telephone': '&#xe974;',
            'phone-hang-up': '&#xe975;',
            'telephone2': '&#xe975;',
            'cogs': '&#xe995;',
            'gears': '&#xe995;',
            'menu': '&#xe9bd;',
            'list3': '&#xe9bd;',
            'menu3': '&#xe9bf;',
            'options3': '&#xe9bf;',
            'sphere': '&#xea00;',
            'globe': '&#xea00;',
            'earth': '&#xea01;',
            'globe2': '&#xea01;',
            'link': '&#xe9cb;',
            'chain': '&#xe9cb;',
            'attachment': '&#xe9cd;',
            'paperclip': '&#xe9cd;',
            'plus': '&#xea0a;',
            'add': '&#xea0a;',
            'minus': '&#xea0b;',
            'subtract': '&#xea0b;',
            'info': '&#xea0c;',
            'information': '&#xea0c;',
            'cancel-circle': '&#xea0d;',
            'close': '&#xea0d;',
            'cross': '&#xea0f;',
            'cancel': '&#xea0f;',
            'checkmark': '&#xea10;',
            'tick': '&#xea10;',
            'checkmark2': '&#xea11;',
            'tick2': '&#xea11;',
            'play2': '&#xea15;',
            'player': '&#xea15;',
            'pause': '&#xea16;',
            'player2': '&#xea16;',
            'stop': '&#xea17;',
            'player3': '&#xea17;',
            'previous': '&#xea18;',
            'player4': '&#xea18;',
            'next': '&#xea19;',
            'player5': '&#xea19;',
            'backward': '&#xea1a;',
            'player6': '&#xea1a;',
            'forward2': '&#xea1b;',
            'player7': '&#xea1b;',
            'play3': '&#xea1c;',
            'player8': '&#xea1c;',
            'pause2': '&#xea1d;',
            'player9': '&#xea1d;',
            'stop2': '&#xea1e;',
            'player10': '&#xea1e;',
            'backward2': '&#xea1f;',
            'player11': '&#xea1f;',
            'forward3': '&#xea20;',
            'player12': '&#xea20;',
            'first': '&#xea21;',
            'player13': '&#xea21;',
            'arrow-down2': '&#xea3e;',
            'down2': '&#xea3e;',
            'circle-up': '&#xea41;',
            'up3': '&#xea41;',
            'circle-right': '&#xea42;',
            'right5': '&#xea42;',
            'circle-down': '&#xea43;',
            'down3': '&#xea43;',
            'circle-left': '&#xea44;',
            'left5': '&#xea44;',
            'checkbox-checked': '&#xea52;',
            'checkbox': '&#xea52;',
            'checkbox-unchecked': '&#xea53;',
            'checkbox2': '&#xea53;',
            'radio-checked': '&#xea54;',
            'radio-button': '&#xea54;',
            'radio-checked2': '&#xea55;',
            'radio-button2': '&#xea55;',
            'radio-unchecked': '&#xea56;',
            'radio-button3': '&#xea56;',
            'amazon': '&#xea87;',
            'brand': '&#xea87;',
            'google': '&#xea88;',
            'brand2': '&#xea88;',
            'google3': '&#xea8a;',
            'brand4': '&#xea8a;',
            'google-plus': '&#xea8b;',
            'brand5': '&#xea8b;',
            'hangouts': '&#xea8e;',
            'brand8': '&#xea8e;',
            'google-drive': '&#xea8f;',
            'brand9': '&#xea8f;',
            'facebook': '&#xea90;',
            'brand10': '&#xea90;',
            'facebook2': '&#xea91;',
            'brand11': '&#xea91;',
            'instagram': '&#xea92;',
            'brand12': '&#xea92;',
            'whatsapp': '&#xea93;',
            'brand13': '&#xea93;',
            'spotify': '&#xea94;',
            'brand14': '&#xea94;',
            'telegram': '&#xea95;',
            'brand15': '&#xea95;',
            'twitter': '&#xea96;',
            'brand16': '&#xea96;',
            'feed2': '&#xea9b;',
            'rss': '&#xea9b;',
            'youtube': '&#xea9d;',
            'brand21': '&#xea9d;',
            'youtube2': '&#xea9e;',
            'brand22': '&#xea9e;',
            'twitch': '&#xea9f;',
            'brand23': '&#xea9f;',
            'vimeo': '&#xeaa0;',
            'brand24': '&#xeaa0;',
            'vimeo2': '&#xeaa1;',
            'brand25': '&#xeaa1;',
            'flickr2': '&#xeaa4;',
            'brand28': '&#xeaa4;',
            'dribbble': '&#xeaa7;',
            'brand31': '&#xeaa7;',
            'behance': '&#xeaa8;',
            'brand32': '&#xeaa8;',
            'behance2': '&#xeaa9;',
            'brand33': '&#xeaa9;',
            'deviantart': '&#xeaaa;',
            'brand34': '&#xeaaa;',
            'soundcloud': '&#xeac3;',
            'brand58': '&#xeac3;',
            'soundcloud2': '&#xeac4;',
            'brand59': '&#xeac4;',
            'skype': '&#xeac5;',
            'brand60': '&#xeac5;',
            'linkedin': '&#xeac9;',
            'brand64': '&#xeac9;',
            'linkedin2': '&#xeaca;',
            'brand65': '&#xeaca;',
            'pinterest': '&#xead1;',
            'brand72': '&#xead1;',
            'pinterest2': '&#xead2;',
            'brand73': '&#xead2;',
            'file-pdf': '&#xeadf;',
            'file10': '&#xeadf;',
            'git': '&#xeae7;',
            'brand80': '&#xeae7;',
          '0': 0
        };
        delete icons['0'];
        window.icomoonLiga = function (els) {
            var classes,
                el,
                i,
                innerHTML,
                key;
            els = els || document.getElementsByTagName('*');
            if (!els.length) {
                els = [els];
            }
            for (i = 0; ; i += 1) {
                el = els[i];
                if (!el) {
                    break;
                }
                classes = el.className;
                if (/icon-/.test(classes)) {
                    innerHTML = el.innerHTML;
                    if (innerHTML && innerHTML.length > 1) {
                        for (key in icons) {
                            if (icons.hasOwnProperty(key)) {
                                innerHTML = innerHTML.replace(new RegExp(key, 'g'), icons[key]);
                            }
                        }
                        el.innerHTML = innerHTML;
                    }
                }
            }
        };
        window.icomoonLiga();
    }
}());
