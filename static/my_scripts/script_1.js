  document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("pills-home-tab").classList.add("active");
    document.getElementById("pills-home").classList.add("show", "active");
  });

  document.querySelectorAll(".tab-pofile-link").forEach(function(tab) {
    tab.addEventListener("click", function(e) {
      e.preventDefault();
      const target = e.target.getAttribute("data-bs-target");
      document.querySelectorAll(".tab-pofile-link").forEach(function(link) {
        link.classList.remove("active");
      });
      document.querySelectorAll(".tab-pane").forEach(function(pane) {
        pane.classList.remove("show", "active");
      });
      tab.classList.add("active");
      document.querySelector(target).classList.add("show", "active");
    });
  });
