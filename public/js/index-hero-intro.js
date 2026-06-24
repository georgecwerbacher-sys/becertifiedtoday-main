(function () {
  var cfg = window.SITE_WELCOME_VIDEO;
  var hero = document.getElementById("hero-banner");
  if (!cfg || !hero) return;

  var videoEl = document.getElementById("hero-intro-video");
  var imageEl = hero.querySelector(".hero-banner__image");
  if (!videoEl || !imageEl) return;

  var sessionKey = cfg.sessionKey || "bct_index_intro_seen";
  var title = cfg.title || "Welcome to Be Certified Today";
  var youtubeId = cfg.youtubeId ? String(cfg.youtubeId).trim() : "";
  var localSrc = cfg.localSrc ? String(cfg.localSrc).trim() : "";

  function showImageOnly() {
    hero.classList.add("is-intro-done");
    videoEl.hidden = true;
    videoEl.pause();
    imageEl.hidden = false;
    try {
      sessionStorage.setItem(sessionKey, "1");
    } catch (e) {}
  }

  if (sessionStorage.getItem(sessionKey) === "1") {
    showImageOnly();
    return;
  }

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    showImageOnly();
    return;
  }

  function bindEnd(el) {
    el.addEventListener("ended", showImageOnly, { once: true });
    el.addEventListener("error", showImageOnly, { once: true });
  }

  if (youtubeId) {
    videoEl.remove();
    var iframe = document.createElement("iframe");
    iframe.id = "hero-intro-video";
    iframe.className = "hero-banner__video";
    iframe.src =
      "https://www.youtube-nocookie.com/embed/" +
      encodeURIComponent(youtubeId) +
      "?autoplay=1&mute=1&rel=0&modestbranding=1&playsinline=1";
    iframe.title = title;
    iframe.allow =
      "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    iframe.allowFullscreen = true;
    hero.insertBefore(iframe, imageEl);
    imageEl.hidden = true;
    /* YouTube iframe has no reliable ended event — fall back to image after typical intro length. */
    setTimeout(showImageOnly, 150000);
    return;
  }

  if (!localSrc) {
    showImageOnly();
    return;
  }

  videoEl.title = title;
  if (cfg.poster) {
    videoEl.poster = String(cfg.poster);
  }
  videoEl.defaultMuted = true;
  videoEl.muted = true;
  videoEl.volume = 0;
  videoEl.autoplay = true;
  videoEl.playsInline = true;
  videoEl.setAttribute("playsinline", "");
  videoEl.setAttribute("autoplay", "");
  videoEl.setAttribute("muted", "");
  videoEl.preload = "auto";
  videoEl.controls = false;
  videoEl.disablePictureInPicture = true;
  videoEl.setAttribute("disablepictureinpicture", "");
  videoEl.setAttribute("controlslist", "nodownload nofullscreen noremoteplayback");
  videoEl.addEventListener("volumechange", function () {
    videoEl.muted = true;
    videoEl.volume = 0;
  });

  imageEl.hidden = true;
  bindEnd(videoEl);

  var playAttempt = videoEl.play();
  if (playAttempt && typeof playAttempt.catch === "function") {
    playAttempt.catch(function () {
      showImageOnly();
    });
  }
})();
