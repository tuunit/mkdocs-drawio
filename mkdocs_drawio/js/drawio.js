const colorize = async function () {
    document.querySelectorAll("div.mxgraph").forEach(function (div) {
        let style = div.getAttribute("style").replace(/color-scheme: light;/gi, "");
        div.setAttribute("style", style);
    });
};

if (typeof document$ !== "undefined" && typeof document$.subscribe === "function") {
    document$.subscribe(({ body }) => {
        GraphViewer.processElements()
        colorize();
      });
} else {
    document.addEventListener("DOMContentLoaded", function () {
        colorize();
    });
}
