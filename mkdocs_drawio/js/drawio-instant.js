(function () {
  "use strict";

  var loading = false;

  function render() {
    document
      .querySelectorAll(".mxgraph[data-mxgraph]:not([data-drawio-rendered])")
      .forEach(function (el) {
        el.dataset.drawioRendered = "true";
        try {
          el.innerText = "";
          GraphViewer.createViewerForElement(el);
        } catch (error) {
          el.innerText = error.message;
          console.error(error);
        }
      });
  }

  // Called by the viewer when it loads, instead of rendering every diagram.
  window.onDrawioViewerLoad = render;

  if (typeof document$ === "undefined") return;

  document$.subscribe(function () {
    if (window.GraphViewer) {
      render();
      return;
    }
    var diagram = document.querySelector(".mxgraph[data-viewer-js]");
    if (diagram && !loading) {
      loading = true;
      var script = document.createElement("script");
      script.src = diagram.dataset.viewerJs;
      document.body.appendChild(script);
    }
  });
})();
