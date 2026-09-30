// Shows release version, last-modified date and commit link from build.json
// (written by the Pages deploy, scripts/build-site-info.py). Renders into
// #build-info if the page has one, else a small fixed badge. data-artifact="graph"
// reports the graphify graph's own last-rebuild commit instead of the deploy's.
(function () {
  var script = document.currentScript;
  var artifact = (script && script.dataset.artifact) || "site";

  function link(href, text) {
    var a = document.createElement("a");
    a.href = href;
    a.textContent = text;
    a.style.color = "var(--primary,#c8a858)";  // never browser-default blue (graph.html has no link styles)
    return a;
  }

  fetch("build.json").then(function (r) {
    if (!r.ok) { throw new Error("HTTP " + r.status); }
    return r.json();
  }).then(function (info) {
    var c = (artifact === "graph" && info.graph) ? info.graph : info.site;
    if (!c) { return; }
    var box = document.getElementById("build-info");
    if (!box) {
      box = document.createElement("div");
      box.id = "build-info";
      box.style.cssText = "position:fixed;left:8px;bottom:8px;z-index:10;padding:2px 8px;" +
        // Fallbacks are the EyeRest dark tokens: only graph.html (dark, no CSS vars) needs them.
        "font:12px/1.6 Inter,system-ui,sans-serif;background:var(--surface,#242018);" +
        "color:var(--text-muted,#a89878);border:1px solid var(--border,#383428);border-radius:4px;";
      document.body.appendChild(box);
    }
    box.textContent = "";
    if (info.version) { box.appendChild(document.createTextNode("v" + info.version + " · ")); }
    box.appendChild(document.createTextNode(
      (artifact === "graph" ? "graph rebuilt " : "updated ") + c.date + " · "));
    box.appendChild(link(c.url, c.short));
  }).catch(function () { /* no build.json (local preview): show nothing */ });
})();
