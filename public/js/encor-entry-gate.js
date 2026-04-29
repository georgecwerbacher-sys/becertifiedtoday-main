(function () {
  var entry = document.getElementById("encor-entry-link");
  var modal = document.getElementById("encor-purchase-modal");
  var closeBtn = document.getElementById("encor-purchase-close");

  if (!entry || !modal || !closeBtn) return;

  function openModal() {
    modal.classList.add("is-open");
  }

  function closeModal() {
    modal.classList.remove("is-open");
  }

  async function hasAccess() {
    var response = await fetch("/api/auth/access-status", { credentials: "include" });
    if (!response.ok) return false;
    var data = await response.json();
    return data && data.has_access === true;
  }

  entry.addEventListener("click", async function (event) {
    event.preventDefault();
    try {
      var allowed = await hasAccess();
      if (allowed) {
        window.location.href = entry.href;
        return;
      }
      openModal();
    } catch (_error) {
      openModal();
    }
  });

  closeBtn.addEventListener("click", closeModal);
  modal.addEventListener("click", function (event) {
    if (event.target === modal) closeModal();
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeModal();
  });
})();
