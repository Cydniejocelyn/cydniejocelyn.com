// The section 53 hero composite, as one script. Paste into a real browser on
// any page with a .hero (or serve it and eval a fetch of it) and it returns
// the worst contrast under each run of hero text: the real image mapping,
// both scrim gradients per pixel, 3:1 for the h1 and 4.5:1 for the rest.
// Written 12 September 2026 for the /retreats/ hero. It returns without
// timers on purpose: in a hidden preview pane setTimeout never fires.
(async () => {
  const st = document.createElement('style');
  st.textContent = '.hero-copy *, .hero-copy{transform:none!important;transition:none!important;animation:none!important;opacity:1!important}';
  document.head.appendChild(st);
  const hero = document.querySelector('.hero');
  const img = hero.querySelector('.hero-water img');
  if (!img.complete || !img.naturalWidth) return {err:'image not loaded', src: img.currentSrc};
  const H = hero.getBoundingClientRect();
  const W = Math.round(H.width), Ht = Math.round(H.height);
  const cv = document.createElement('canvas'); cv.width = W; cv.height = Ht;
  const cx = cv.getContext('2d');
  // the image box without the parallax transform
  const saved = img.style.transform; img.style.setProperty('transform', 'none', 'important');
  const B = img.getBoundingClientRect();
  img.style.transform = saved;
  const nw = img.naturalWidth, nh = img.naturalHeight;
  const cs = getComputedStyle(img);
  const [px, py] = cs.objectPosition.split(' ').map(v => parseFloat(v) / 100);
  const sc = Math.max(B.width / nw, B.height / nh);
  const rw = nw * sc, rh = nh * sc;
  const ox = B.left - H.left + (B.width - rw) * px, oy = B.top - H.top + (B.height - rh) * py;
  cx.fillStyle = '#0B1D22'; cx.fillRect(0, 0, W, Ht);
  cx.drawImage(img, ox, oy, rw, rh);
  const data = cx.getImageData(0, 0, W, Ht).data;
  // scrim, parsed from the live computed background
  const bg = getComputedStyle(hero.querySelector('.hero-scrim')).backgroundImage;
  const grads = bg.split(/,\s*(?=linear-gradient)/);
  const parse = g => {
    const dir = /90deg/.test(g) ? 'x' : 'y';
    const stops = [...g.matchAll(/rgba?\(([^)]+)\)\s*([\d.]+)%/g)].map(m => {
      const p = m[1].split(',').map(Number); return { c: p.slice(0, 3), a: p[3] === undefined ? 1 : p[3], at: +m[2] / 100 };
    });
    return { dir, stops };
  };
  const G = grads.map(parse); // first listed is on top
  const at = (stops, t) => {
    if (t <= stops[0].at) return stops[0];
    for (let i = 1; i < stops.length; i++) if (t <= stops[i].at) {
      const a = stops[i - 1], b = stops[i], f = (t - a.at) / (b.at - a.at || 1);
      return { c: a.c.map((v, k) => v + (b.c[k] - v) * f), a: a.a + (b.a - a.a) * f };
    }
    return stops[stops.length - 1];
  };
  const lin = v => { v /= 255; return v <= .04045 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); };
  const L = c => .2126 * lin(c[0]) + .7152 * lin(c[1]) + .0722 * lin(c[2]);
  const ground = (x, y) => {
    const i = (y * W + x) * 4; let c = [data[i], data[i + 1], data[i + 2]];
    for (let g = G.length - 1; g >= 0; g--) { // bottom layer first
      const s = at(G[g].stops, G[g].dir === 'x' ? x / W : y / Ht);
      c = c.map((v, k) => s.c[k] * s.a + v * (1 - s.a));
    }
    return c;
  };
  const parseInk = s => s.match(/[\d.]+/g).slice(0, 3).map(Number);
  const out = [];
  const tw = document.createTreeWalker(hero.querySelector('.hero-copy'), NodeFilter.SHOW_TEXT);
  let n;
  while ((n = tw.nextNode())) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement; if (el.closest('.vh')) continue;
    const ink = parseInk(getComputedStyle(el).color), li = L(ink);
    const fs = parseFloat(getComputedStyle(el).fontSize);
    const big = !!el.closest('h1');
    const r = document.createRange(); r.selectNodeContents(n);
    let worst = 99;
    for (const q of r.getClientRects()) {
      for (let y = Math.max(0, Math.floor(q.top - H.top)); y < Math.min(Ht, q.bottom - H.top); y += 2)
        for (let x = Math.max(0, Math.floor(q.left - H.left)); x < Math.min(W, q.right - H.left); x += 2) {
          const lg = L(ground(x, y));
          const cr = (Math.max(li, lg) + .05) / (Math.min(li, lg) + .05);
          if (cr < worst) worst = cr;
        }
    }
    const key = (el.closest('h1') ? 'h1' : el.closest('.hero-sub') ? 'sub' : el.closest('.hero-go') ? 'link' : el.closest('dt') ? 'dt' : el.closest('dd') ? 'dd' : el.className || el.tagName);
    const need = big ? 3 : 4.5;
    const prev = out.find(o => o.key === key);
    if (!prev) out.push({ key, worst, need, fs });
    else prev.worst = Math.min(prev.worst, worst);
  }
  st.remove();
  return { vw: innerWidth, rows: out.map(o => [o.key, +o.worst.toFixed(2), o.need, o.worst >= o.need ? 'ok' : 'FAIL']) };
})()
