document.addEventListener("DOMContentLoaded", function () {
  const circularTabs = document.querySelectorAll(".circle-tabs .nav-link");
  const currentPath = window.location.pathname;

    circularTabs.forEach((tab) => {
        if (tab.getAttribute("href") === currentPath) {
            tab.classList.add("active");
        } else {
            tab.classList.remove("active");
        }
    });
});
