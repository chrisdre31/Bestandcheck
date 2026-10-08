"""Baut die iPad-Version (GitHub Pages) aus template.html + appdata.json."""
import hashlib, json, os, sys
from PIL import Image, ImageDraw, ImageFont
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/bestandcheck"
PIN = "4141"
t = open("template.html", encoding="utf-8").read()
data = open("appdata.json", encoding="utf-8").read()
ver = hashlib.sha1((t + data).encode()).hexdigest()[:10]
pin_hash = hashlib.sha256(PIN.encode()).hexdigest()

head_extra = '''<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-180.png">
<meta name="theme-color" content="#2f5275">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
'''
pin_css = '''<style>
#pinGate{position:fixed;inset:0;z-index:100;background:var(--bg);display:grid;place-items:center;padding:16px}
#pinGate .card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:28px 24px;width:min(360px,100%);display:grid;gap:16px;text-align:center}
#pinGate h1{font-size:28px}
#pinGate p{margin:0;color:var(--muted)}
#pinDots{display:flex;gap:14px;justify-content:center}
#pinDots i{width:16px;height:16px;border-radius:50%;border:2px solid var(--accent)}
#pinDots i.on{background:var(--accent)}
#pinPad{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
#pinPad button{min-height:62px;border-radius:12px;border:1px solid var(--line);background:var(--bg);font-size:26px;font-family:var(--display)}
#pinPad button:active{background:var(--accent-soft)}
#pinErr{color:var(--bad);min-height:1.4em;font-weight:500}
</style>'''
pin_html = '''<div id="pinGate" hidden><div class="card">
  <h1>KTW Bestandscheck</h1><p>Bitte PIN eingeben</p>
  <div id="pinDots"><i></i><i></i><i></i><i></i></div>
  <div id="pinErr" role="alert"></div>
  <div id="pinPad">
    <button type="button">1</button><button type="button">2</button><button type="button">3</button>
    <button type="button">4</button><button type="button">5</button><button type="button">6</button>
    <button type="button">7</button><button type="button">8</button><button type="button">9</button>
    <span></span><button type="button">0</button><button type="button" aria-label="Löschen">⌫</button>
  </div></div></div>'''
pin_js = '''
/* ---------- PIN + Offline ---------- */
const PIN_HASH = "%s", LS_PIN = "ktn-bc-pin";
async function sha(s){ const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2,"0")).join(""); }
function startApp(){
  const id = ls.get(LS_VEH);
  const v = APP.veh.find(x => x.id === id);
  if(v) openVehicle(v); else showStart();
}
(function gate(){
  if(ls.get(LS_PIN) === PIN_HASH){ startApp(); flushOutbox(); return; }
  const g = $("#pinGate"); g.hidden = false;
  let code = "";
  const dots = [...document.querySelectorAll("#pinDots i")];
  const draw = () => dots.forEach((d,i) => d.classList.toggle("on", i < code.length));
  $("#pinPad").addEventListener("click", async e => {
    const b = e.target.closest("button"); if(!b) return;
    $("#pinErr").textContent = "";
    if(b.textContent === "⌫") code = code.slice(0,-1); else if(code.length < 4) code += b.textContent;
    draw();
    if(code.length === 4){
      if(await sha(code) === PIN_HASH){ ls.set(LS_PIN, PIN_HASH); g.hidden = true; startApp(); flushOutbox(); }
      else { $("#pinErr").textContent = "Falsche PIN"; code = ""; setTimeout(draw, 250); }
    }
  });
})();
if("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
''' % pin_hash

boot_old = t[t.index("/* ---------- boot ---------- */"):t.index("</script>", t.index("/* ---------- boot ---------- */"))]
site = t.replace(boot_old, pin_js).replace("__DATA__", data)
site = site.replace('<meta name="apple-mobile-web-app-title" content="Bestandscheck">', '<meta name="apple-mobile-web-app-title" content="Bestandscheck">\n' + head_extra, 1)
site = site.replace("<style>", '<script>window.KTN_UPLOAD_TOKEN = "491dbb552b424a77a62b";</script>\n' + pin_css + "\n<style>", 1)
site = site.replace('<div class="wrap">', pin_html + '\n<div class="wrap">', 1)
reset = "<style>*,*::before,*::after{box-sizing:border-box}html{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px/1.4 system-ui,-apple-system,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>"
cut = site.index('<div id="pinGate"')
doc = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' + reset + '\n'
       + site[:cut] + '</head><body>\n' + site[cut:] + '\n</body></html>')
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(doc)

json.dump({"name": "KTW Bestandscheck", "short_name": "Bestandscheck", "start_url": "./", "scope": "./",
           "display": "standalone", "background_color": "#eef1f4", "theme_color": "#2f5275", "lang": "de",
           "icons": [{"src": "icon-180.png", "sizes": "180x180", "type": "image/png"},
                     {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]},
          open(os.path.join(OUT, "manifest.webmanifest"), "w"), ensure_ascii=False, indent=1)

open(os.path.join(OUT, "sw.js"), "w").write('''// Offline-Unterstützung: erst Netz (immer aktuelle Version), sonst Kopie aus dem Speicher
const CACHE = "bestandscheck-%s";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-180.png", "icon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES))); self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))); self.clients.claim(); });
self.addEventListener("fetch", e => {
  if(e.request.method !== "GET" || new URL(e.request.url).origin !== self.location.origin) return;   // nur eigene App-Dateien
  e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(CACHE).then(ca => ca.put(e.request, c)); return r; })
    .catch(() => caches.match(e.request, {ignoreSearch: true}).then(r => r || caches.match("index.html"))));
});
''' % ver)

def icon(size, path):
    s = 4  # supersample
    W = size * s
    im = Image.new("RGB", (W, W), (47, 82, 117))
    d = ImageDraw.Draw(im)
    # clipboard
    m = int(W * .2); top = int(W * .17)
    d.rounded_rectangle([m, top, W - m, W - int(W * .14)], radius=int(W * .06), fill=(255, 255, 255))
    d.rounded_rectangle([int(W * .37), int(W * .11), int(W * .63), int(W * .23)], radius=int(W * .03), fill=(214, 226, 238))
    # check lines
    for i, y in enumerate((.38, .54, .70)):
        yy = int(W * y); x0 = int(W * .29)
        d.line([(x0, yy), (x0 + int(W*.05), yy + int(W*.05)), (x0 + int(W*.13), yy - int(W*.05))], fill=(29, 116, 71), width=int(W*.035), joint="curve")
        d.rounded_rectangle([int(W*.48), yy - int(W*.018), int(W*.71), yy + int(W*.018)], radius=int(W*.018), fill=(160, 176, 192))
    im.resize((size, size), Image.LANCZOS).save(path)
icon(180, os.path.join(OUT, "icon-180.png"))
icon(512, os.path.join(OUT, "icon-512.png"))
print("Site gebaut:", OUT, "Version", ver)
