const colorSchemeToggle = async function () {
    document.querySelectorAll("div.mxgraph").forEach(function (div) {
        let style = div.getAttribute("style").replace(/color-scheme: light;/gi, "");
        div.setAttribute("style", style);
    });
};

if (typeof document$ !== "undefined" && typeof document$.subscribe === "function") {
    document$.subscribe(({ body }) => {
        colorSchemeToggle();
      });
} else {
      document.addEventListener("DOMContentLoaded", function () {
        colorSchemeToggle();
    });
}
