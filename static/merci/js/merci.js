/* Merci Media & Digitals: page behaviour. No dependencies. */
(function () {
    'use strict';

    var doc = document;
    var root = doc.documentElement;
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var isPhone = function () { return window.matchMedia('(max-width: 700px)').matches; };
    var $ = function (sel, ctx) { return (ctx || doc).querySelector(sel); };
    var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); };

    root.classList.add('js-ready');

    var yearEl = $('#m-year');
    if (yearEl) { yearEl.textContent = new Date().getFullYear(); }

    /* ---------- Sticky header ---------- */
    var header = $('#site-header');
    function onScroll() {
        if (header) { header.classList.toggle('is-stuck', window.scrollY > 24); }
    }
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    /* ---------- Body scroll lock (shared by menu and modals) ---------- */
    var locks = 0;
    function lockScroll() { locks++; doc.body.classList.add('m-lock'); }
    function unlockScroll() { locks = Math.max(0, locks - 1); if (!locks) { doc.body.classList.remove('m-lock'); } }

    /* ---------- Mobile menu ---------- */
    var menu = $('#mobile-menu');
    var menuBtn = $('#menu-btn');
    var menuClose = $('#menu-close');
    function setMenu(open) {
        if (!menu) { return; }
        if (open === !menu.hidden) { return; }
        menu.hidden = !open;
        if (menuBtn) { menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false'); }
        if (open) { lockScroll(); if (menuClose) { menuClose.focus(); } }
        else { unlockScroll(); if (menuBtn) { menuBtn.focus(); } }
    }
    if (menuBtn) { menuBtn.addEventListener('click', function () { setMenu(true); }); }
    if (menuClose) { menuClose.addEventListener('click', function () { setMenu(false); }); }
    if (menu) {
        $$('a', menu).forEach(function (a) {
            a.addEventListener('click', function () { if (!menu.hidden) { menu.hidden = true; unlockScroll(); menuBtn.setAttribute('aria-expanded', 'false'); } });
        });
    }

    /* ---------- Tabs ---------- */
    function initTabs(btnAttr, panelAttr) {
        var btns = $$('[' + btnAttr + ']');
        var panels = $$('[' + panelAttr + ']');
        if (!btns.length) { return; }
        function show(key) {
            btns.forEach(function (b) { b.setAttribute('aria-selected', b.getAttribute(btnAttr) === key ? 'true' : 'false'); });
            panels.forEach(function (p) { p.classList.toggle('is-active', p.getAttribute(panelAttr) === key); });
        }
        btns.forEach(function (b, i) {
            b.addEventListener('click', function () { show(b.getAttribute(btnAttr)); });
            b.addEventListener('keydown', function (e) {
                if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') { return; }
                var next = btns[(i + (e.key === 'ArrowRight' ? 1 : btns.length - 1)) % btns.length];
                next.focus(); next.click();
            });
        });
        show(btns[0].getAttribute(btnAttr));
    }
    initTabs('data-seg', 'data-seg-panel');
    initTabs('data-seg-pkg', 'data-pkg-panel');
    // A panel with no tab buttons (no photos) must still show.
    $$('[data-seg-panel="films"]').forEach(function (p) { p.classList.add('is-active'); });

    /* ---------- Category filters ---------- */
    function initFilter(filterSel, itemSel) {
        var wrap = $(filterSel);
        if (!wrap) { return; }
        var chips = $$('.m-chip', wrap);
        var items = $$(itemSel);
        chips.forEach(function (chip) {
            chip.addEventListener('click', function () {
                chips.forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
                var cat = chip.getAttribute('data-cat');
                items.forEach(function (it) { it.hidden = !(cat === 'all' || it.getAttribute('data-cat') === cat); });
            });
        });
    }
    initFilter('#work-filter', '#work-grid .m-work');
    initFilter('#photo-filter', '#photo-grid .m-photo');

    /* ---------- Video lightbox ---------- */
    var vModal = $('#video-modal');
    var vPanel = $('#video-panel');
    var vStage = $('#video-stage');
    var vClose = $('#video-close');
    var vTrigger = null;

    function openVideo(btn) {
        if (!vModal) { return; }
        var phone = isPhone();
        var src = (phone && btn.getAttribute('data-embed-m')) || btn.getAttribute('data-embed');
        if (!src) { return; }
        vTrigger = btn;
        vPanel.classList.toggle('is-portrait', phone && btn.getAttribute('data-vertical') === '1');
        var frame = doc.createElement('iframe');
        frame.src = src;
        frame.title = btn.getAttribute('data-title') || 'Video';
        frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen';
        frame.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin'); // YouTube needs a referrer to play
        frame.allowFullscreen = true;
        vStage.innerHTML = '';
        vStage.appendChild(frame);
        vModal.hidden = false;
        void vModal.offsetWidth; // let the browser paint the hidden state first so the fade runs
        vModal.classList.add('is-open');
        lockScroll();
        vClose.focus();
        track('video_play', { video_title: frame.title });
    }
    function closeVideo() {
        if (!vModal || vModal.hidden) { return; }
        vModal.classList.remove('is-open');
        vStage.innerHTML = ''; // removing the iframe stops playback
        unlockScroll();
        setTimeout(function () { vModal.hidden = true; }, reduceMotion ? 0 : 250);
        if (vTrigger) { vTrigger.focus(); }
    }
    $$('.js-play').forEach(function (b) { b.addEventListener('click', function () { openVideo(b); }); });
    if (vClose) { vClose.addEventListener('click', closeVideo); }
    if (vModal) { vModal.addEventListener('click', function (e) { if (!vPanel.contains(e.target)) { closeVideo(); } }); }

    /* ---------- Photo lightbox ---------- */
    var pModal = $('#photo-modal');
    var pImg = $('#photo-img');
    var pCap = $('#photo-cap');
    var pIndex = 0;
    var pList = [];
    var pTrigger = null;

    function showPhoto(i) {
        if (!pList.length) { return; }
        pIndex = (i + pList.length) % pList.length;
        var el = pList[pIndex];
        pImg.src = el.getAttribute('data-full');
        pImg.alt = el.getAttribute('data-alt') || '';
        pCap.textContent = el.getAttribute('data-caption') || '';
    }
    function openPhoto(el) {
        if (!pModal) { return; }
        pTrigger = el;
        pList = $$('#photo-grid .js-photo').filter(function (p) { return !p.hidden; });
        showPhoto(pList.indexOf(el));
        pModal.hidden = false;
        void pModal.offsetWidth;
        pModal.classList.add('is-open');
        lockScroll();
        $('#photo-close').focus();
    }
    function closePhoto() {
        if (!pModal || pModal.hidden) { return; }
        pModal.classList.remove('is-open');
        unlockScroll();
        setTimeout(function () { pModal.hidden = true; pImg.src = ''; }, reduceMotion ? 0 : 250);
        if (pTrigger) { pTrigger.focus(); }
    }
    $$('.js-photo').forEach(function (p) { p.addEventListener('click', function () { openPhoto(p); }); });
    if (pModal) {
        $('#photo-close').addEventListener('click', closePhoto);
        $('#photo-prev').addEventListener('click', function () { showPhoto(pIndex - 1); });
        $('#photo-next').addEventListener('click', function () { showPhoto(pIndex + 1); });
        pModal.addEventListener('click', function (e) { if (e.target === pModal) { closePhoto(); } });
    }

    doc.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { closeVideo(); closePhoto(); setMenu(false); }
        if (pModal && !pModal.hidden) {
            if (e.key === 'ArrowRight') { showPhoto(pIndex + 1); }
            if (e.key === 'ArrowLeft') { showPhoto(pIndex - 1); }
        }
    });

    /* ---------- Prefill the form from service / package buttons ---------- */
    var serviceSel = $('#id_service');
    var descBox = $('#id_project_description');
    var nameBox = $('#id_full_name');
    $$('a[data-service]').forEach(function (a) {
        a.addEventListener('click', function (e) {
            var target = $('#inquiry');
            if (!serviceSel || !target) { return; }
            e.preventDefault();
            serviceSel.value = a.getAttribute('data-service');
            var pkg = a.getAttribute('data-package');
            if (pkg && descBox && !descBox.value.trim()) {
                descBox.value = 'I’m interested in the ' + pkg + ' package.\n';
                var more = $('.m-more-fields');
                if (more) { more.open = true; }
            }
            target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
            setTimeout(function () { if (nameBox) { nameBox.focus({ preventScroll: true }); } }, reduceMotion ? 0 : 600);
            track('select_service', { service: a.getAttribute('data-service'), package: pkg || '' });
        });
    });

    /* ---------- Hero showreel (loads only when useful) ---------- */
    var hv = $('#hero-video');
    var heroClock = null;
    if (hv) {
        var saveData = navigator.connection && navigator.connection.saveData;
        if (!reduceMotion && !saveData) {
            var phone = isPhone();
            var src = (phone && hv.getAttribute('data-src-mobile')) || hv.getAttribute('data-src-desktop');
            var posterM = hv.getAttribute('data-poster-mobile');
            if (phone && posterM) { hv.poster = posterM; }
            hv.src = src;
            if ('IntersectionObserver' in window) {
                new IntersectionObserver(function (entries) {
                    entries.forEach(function (en) {
                        if (en.isIntersecting) { var p = hv.play(); if (p && p.catch) { p.catch(function () {}); } }
                        else { hv.pause(); }
                    });
                }, { threshold: 0.25 }).observe(hv);
            } else { var pp = hv.play(); if (pp && pp.catch) { pp.catch(function () {}); } }
        }
        heroClock = hv;
    }

    /* ---------- Viewfinder timecode ---------- */
    var tc = $('#timecode');
    if (tc && !reduceMotion) {
        var t0 = performance.now();
        var pad = function (n) { return (n < 10 ? '0' : '') + n; };
        setInterval(function () {
            if (doc.hidden) { return; }
            var secs = (heroClock && !heroClock.paused && heroClock.currentTime) ? heroClock.currentTime : (performance.now() - t0) / 1000;
            var h = Math.floor(secs / 3600), m = Math.floor(secs / 60) % 60, s = Math.floor(secs) % 60, f = Math.floor((secs % 1) * 25);
            tc.textContent = pad(h) + ':' + pad(m) + ':' + pad(s) + ':' + pad(f);
        }, 80);
    }

    /* ---------- Reveal on scroll ---------- */
    var reveals = $$('[data-reveal]');
    if (reveals.length) {
        if ('IntersectionObserver' in window && !reduceMotion) {
            var io = new IntersectionObserver(function (entries) {
                entries.forEach(function (en) {
                    if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
                });
            }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
            reveals.forEach(function (el, i) { el.style.transitionDelay = ((i % 3) * 90) + 'ms'; io.observe(el); });
        } else {
            reveals.forEach(function (el) { el.classList.add('is-in'); });
        }
    }

    /* ---------- Mobile action bar: step aside while the form is on screen ---------- */
    var bar = $('.m-actionbar');
    var form = $('#inquiry');
    if (bar && form && 'IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
            bar.classList.toggle('is-hidden', entries[0].isIntersecting);
        }, { threshold: 0.15 }).observe(form);
    }

    /* ---------- Success toast and form errors ---------- */
    var toast = $('#m-toast');
    if (toast) {
        requestAnimationFrame(function () { toast.classList.add('is-shown'); });
        var hide = function () { toast.classList.remove('is-shown'); setTimeout(function () { toast.remove(); }, 400); };
        setTimeout(hide, 7000);
        toast.addEventListener('click', hide);
        if (window.history.replaceState) { window.history.replaceState(null, '', window.location.pathname + '#inquiry'); }
        track('generate_lead', { method: 'inquiry_form' });
    }
    if ($('#inquiry [role="alert"]')) { var f = $('#inquiry'); if (f) { f.scrollIntoView(); } }

    /* ---------- Analytics (only if Google Analytics is on the page) ---------- */
    function track(name, params) {
        try { if (typeof window.gtag === 'function') { window.gtag('event', name, params || {}); } } catch (err) { /* ignore */ }
    }
    doc.addEventListener('click', function (e) {
        var a = e.target.closest && e.target.closest('a[href]');
        if (!a) { return; }
        var href = a.getAttribute('href') || '';
        if (href.indexOf('wa.me') > -1) { track('contact_click', { method: 'whatsapp' }); }
        else if (href.indexOf('tel:') === 0) { track('contact_click', { method: 'phone' }); }
        else if (href.indexOf('mailto:') === 0) { track('contact_click', { method: 'email' }); }
        else if (href.indexOf('t.me') > -1) { track('contact_click', { method: 'telegram' }); }
        else if (a.hasAttribute('data-track')) { track('cta_click', { location: a.getAttribute('data-track') }); }
    });
})();
