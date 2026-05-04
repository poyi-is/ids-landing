(function () {
  document.querySelectorAll("[data-copy-btn]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var panel = btn.closest(".code-panel");
      if (!panel) return;
      var code = panel.querySelector("pre code");
      if (!code) return;
      var text = code.textContent || "";
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          var o = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(function () {
            btn.textContent = o;
          }, 1600);
        });
      }
    });
  });
})();
