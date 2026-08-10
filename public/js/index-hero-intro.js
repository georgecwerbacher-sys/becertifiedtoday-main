(function () {
  var cfg = window.SITE_WELCOME_VIDEO;
  var hero = document.getElementById("hero-banner");
  if (!cfg || !hero) return;

  var videoEl = document.getElementById("hero-intro-video");
  if (!videoEl) return;

  var sessionKey = cfg.sessionKey || "bct_index_intro_seen";
  var title = cfg.title || "Welcome to Be Certified Today";
  var youtubeId = cfg.youtubeId ? String(cfg.youtubeId).trim() : "";
  var localSrc = cfg.localSrc ? String(cfg.localSrc).trim() : "";

  function seekToLastFrame() {
    try {
      var d = videoEl.duration;
      if (Number.isFinite(d) && d > 0) {
        videoEl.currentTime = Math.max(0, d - 0.04);
      }
    } catch (e) {}
  }

  /** Pause on the final logo frame - keep video visible, no static header image. */
  function freezeIntro() {
    hero.classList.add("is-intro-done");
    videoEl.hidden = false;
    seekToLastFrame();
    videoEl.pause();
    try {
      sessionStorage.setItem(sessionKey, "1");
    } catch (e) {}
  }

  function whenMetadataReady(fn) {
    if (videoEl.readyState >= 1) {
      fn();
      return;
    }
    videoEl.addEventListener("loadedmetadata", fn, { once: true });
  }

  if (sessionStorage.getItem(sessionKey) === "1") {
    videoEl.autoplay = false;
    videoEl.preload = "auto";
    whenMetadataReady(freezeIntro);
    return;
  }

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    videoEl.autoplay = false;
    whenMetadataReady(freezeIntro);
    return;
  }

  function bindEnd(el) {
    el.addEventListener("ended", freezeIntro, { once: true });
    el.addEventListener("error", function () {
      whenMetadataReady(freezeIntro);
    }, { once: true });
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
    hero.appendChild(iframe);
    setTimeout(function () {
      hero.classList.add("is-intro-done");
      try {
        sessionStorage.setItem(sessionKey, "1");
      } catch (e) {}
    }, 150000);
    return;
  }

  if (!localSrc) {
    freezeIntro();
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

  bindEnd(videoEl);

  var playAttempt = videoEl.play();
  if (playAttempt && typeof playAttempt.catch === "function") {
    playAttempt.catch(function () {
      whenMetadataReady(freezeIntro);
    });
  }
})();
