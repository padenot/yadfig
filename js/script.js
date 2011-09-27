/* Author:
 * Paul
 */

function $(e) {
  return document.querySelector(e);
}

function $$(e) {
  return document.querySelectorAll(e);
}

/**
 * indexOf impl for browser that don't support it.
 */
function indexOf(array, element) {
  var i = array.length;
  while(i--) {
    if (array[i] == element)
      return i;
  }
  return -1;
}

function getOffset( el ) {
  var _x = 0;
  var _y = 0;
  while( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
    _x += el.offsetLeft - el.scrollLeft;
    _y += el.offsetTop - el.scrollTop;
    el = el.offsetParent;
  }
  return { top: _y, left: _x };
}


var debug = true;
var zoomed = null;
var mode = "gallery";
var images = [];
var currentImage = -1;

function log(msg) {
  if (debug) {
    console.log(msg);
  }
}

function init() {
  var title = $("hgroup h1").innerHTML;
  $(".rotated").innerHTML = title;
  images = $$('.thumb');
  for (var i = 0; i < images.length; i++) {
    images[i].addEventListener("click", onClickImage, false);
  }

  document.onkeydown = function(e) {
    dispatch(e);
  }
  $("#close").addEventListener("click", function() {
    diaporamaOut();
  }, false);

  $("#prev").addEventListener("click", prev, false);

  $("#next").addEventListener("click", next, false);
}

function onClickImage(e) {
  e.stopPropagation();
  var image = e.target.parentNode;
  if(!image.getAttribute("zoomed")) {
    diaporamaIn(image);
  } else {
    diaporamaOut();
  }
}

function next(e) {
  if (mode == "diaporama") {
    currentImage = (currentImage + 1) % images.length;
    $('.diaporama img').src = getHiResUrl(images[currentImage].src);
    checkImageSize();
  }
}

function prev(e) {
  if (mode == "diaporama") {
    currentImage = currentImage == 0 ? images.length - 1 : currentImage - 1;
    $('.diaporama img').src = getHiResUrl(images[currentImage].src);
    checkImageSize();
  }
}

function diaporamaIn(initialCell) {
  mode = "diaporama";
  backgroundIn();
  currentImage = indexOf(images, initialCell.querySelector('img, video'));
  var d = $('.diaporama');
  var wrap = d.querySelector(".wrapper");
  var ctrl = wrap.querySelector(".ctrlWrap");
  d.removeAttribute("hide");
  var image = document.createElement("img");
  image.src = getHiResUrl(initialCell.querySelector('img').src);
  image.addEventListener("click", clickDiaporama, false);
  wrap.insertBefore(image, ctrl);
  var caption = document.createElement("p");
  caption.innerHTML = initialCell.querySelector("p").innerHTML;
  wrap.insertBefore(caption, ctrl);
  checkImageSize();
}

function clickDiaporama(e) {
  if (e.clientX < getOffset(e.target).left + e.target.offsetWidth/2) {
    prev(e);
  } else {
    next(e);
  }
}

function checkImageSize() {
    var wrapper = $('.diaporama .wrapper');
    wrapper.querySelector("img").addEventListener("load", function () {
    var size = wrapper.querySelector("img").naturalHeight;
    var ratio = wrapper.offsetHeight / window.innerHeight * 0.8;
    wrapper.querySelector("img").style.height = window.innerHeight * 0.8 + "px";
  }, false);
}

function diaporamaOut() {
  var d = $('.diaporama .wrapper');
  d.removeChild(d.querySelector("p"));
  d.removeChild(d.querySelector("img"));
  $('.diaporama').setAttribute("hide", "true");
  mode = "gallery";
  backgroundOut();
}

function backgroundIn() {
  var back = $('.back');
  back.removeAttribute("hide");
}

function backgroundOut() {
  $(".wrapper").style.filter = "";
  var back = $(".back");
  back.setAttribute("hide", "true");
}

/**
 * Keyboard shortcut handler
 */
function dispatch(e) {
  switch(e.keyCode) {
    case 27: // Escape
      if (mode == "diaporama") {
        diaporamaOut();
      }
      break;
    case 32: // Space bar
      break;
    case 74: // J
    case 39: // Right
      next(e);
      break;
    case 75: // K
    case 37: // Left
      prev(e);
      break;
    case 191: // ?
      break;
    default:
      log(e.keyCode);
  }
}

function getHiResUrl(thumbUrl) {
  var regexp = new RegExp("^(.*)\.c/(.*)$");
  var matches = regexp.exec(thumbUrl);
  if (matches.length == 3) {
    return matches[1] + matches[2];
  }
  return "";
}
