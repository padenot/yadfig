/* Author:
 * Paul
 */

function $(e) {
  return document.querySelector(e);
}

function $$(e) {
  return document.querySelectorAll(e);
}

var debug = true;
var zoomed = null;
var mode = "gallery";

function log(msg) {
  if (debug) {
    console.log(msg);
  }
}

function init() {
  var images = $$('img');
  for (var i = 0; i < images.length; i++) {
    images[i].addEventListener("click", onClickImage, false);
  }

  document.onkeydown = function(e) {
    dispatch(e);
  }
  $(".close").addEventListener("click", function() {
    diaporamaOut();
  }, false);
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

function diaporamaIn(initialCell) {
  mode = "diaporama";
  backgroundIn();
  var d = $('.diaporama');
  d.removeAttribute("hide");
  var wrap = document.createElement("div");
  wrap.className = "wrapper";
  d.appendChild(wrap);
  var image = document.createElement("img");
  image.src = getHiResUrl(initialCell.querySelector('img').src);
  wrap.appendChild(image);
  var caption = document.createElement("p");
  caption.innerHTML = initialCell.querySelector("p").innerHTML;
  wrap.appendChild(caption);
}

function diaporamaOut() {
  var d = $('.diaporama');
  d.setAttribute("hide", "true");
  d.removeChild(d.querySelector(".wrapper"));
  backgroundOut();
  mode = "gallery";
}

function backgroundIn() {
  var back = $('.back');
  back.style.width = window.innerWidth + "px";
  back.style.height = window.innerHeight + "px";
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
      break;
    case 75: // K
      break;
    case 191: // ?
      break;
  }
}

function getHiResUrl(thumbUrl) {
  log(thumbUrl);
  var regexp = new RegExp("^(.*)\.c/(.*)$");
  var matches = regexp.exec(thumbUrl);
  if (matches.length == 3) {
    return matches[1] + matches[2];
  }
  return "";
}
