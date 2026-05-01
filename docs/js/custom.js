document.addEventListener("DOMContentLoaded", function () {
  // Preserva preferencia do usuario e mantem tema escuro como padrao inicial.
  var stored = localStorage.getItem("__palette");
  if (!stored) {
    var palette = {
      color: {
        media: "(prefers-color-scheme)",
        scheme: "slate",
        primary: "red",
        accent: "orange"
      }
    };
    localStorage.setItem("__palette", JSON.stringify(palette));
  }
});
