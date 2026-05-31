function initSlider() {
  TweenMax.set(".h3-slider", {
    css: {
      opacity: 0,
      y: -20
    }
  });
  TweenMax.set(".icon-slider, .slide-list", {
    css: {
      opacity: 0,
      y: -20
    }
  });


}

function changeSlide() {
  $el = $(".slide").last();
  t = new TimelineMax();
  t
    // show text of slide
    .to($el.find(".h3-slider"), 1, {
      opacity: 1,
      y: 0
    })
    .to($el.find(".icon-slider, .slide-list"), 1, {
      opacity: 1,
      y: 0
    }, .5)

    // hide slide
    .to($el.find(".icon-slider, .slide-list"), 1, {
      opacity: 0,
      y: 20,
      ease: Expo.easeIn
    }, 4)
    .to($el.find(".h3-slider"), 1, {
      opacity: 0,
      y: 20,
      ease: Expo.easeIn
    }, 4.5)
    .to($el, 1.5, {
      opacity: 0,
      onComplete: function () {
        TweenMax.set($el.find(".h3-slider"), {
          css: {
            opacity: 0,
            y: -20
          }
        });
        TweenMax.set($el.find(".icon-slider, .slide-list"), {
          css: {
            opacity: 0,
            y: -20
          }
        });
        $el.prependTo($('.slider')).css('opacity', '1');
        changeSlide();
      }
    }, 5);
}

initSlider();
changeSlide();

$('.switch').click(function (e) {
  ix = $(this).index('.switch') + 1;
  t.kill();
  $('.s' + ix).nextAll().prependTo('.slider');
  initSlider();
  changeSlide();
})
$('.next').click(function (e) {
  t.kill();
  $('.slide').last().prependTo('.slider');
  initSlider();
  changeSlide();
})
$('.prev').click(function (e) {
  t.kill();
  $('.slide').first().appendTo('.slider');
  initSlider();
  changeSlide();
})

$('.pause').click(function (e) {
  t.pause();
  $('.slider').addClass("paused");
})
$('.play').click(function (e) {
  t.play();
  $('.slider').removeClass("paused");
})
