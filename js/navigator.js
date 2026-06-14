window.ReaderNavigator = (() => {
  let observer;
  function build(sections) {
    const list = document.getElementById('sectionList');
    list.replaceChildren(...sections.map((section, index) => {
      const li = document.createElement('li'); const a = document.createElement('a');
      a.href = `#${section.id}`; a.textContent = section.text?.trim() || `Section ${index + 1}`; a.dataset.target = section.id;
      a.addEventListener('click', closeDrawer); li.appendChild(a); return li;
    }));
    trackActive();
  }
  function init() {
    const drawer = document.getElementById('drawer'); const toggle = document.getElementById('drawerToggle'); const close = document.getElementById('drawerClose'); const scrim = document.getElementById('scrim');
    toggle.addEventListener('click', () => openDrawer()); close.addEventListener('click', closeDrawer); scrim.addEventListener('click', closeDrawer);
    document.getElementById('backToTop').addEventListener('click', () => scrollTo({ top: 0, behavior: 'smooth' }));
    addEventListener('scroll', updateProgress, { passive: true });
  }
  function openDrawer(){ document.getElementById('drawer').classList.add('open'); document.getElementById('scrim').hidden = false; document.getElementById('drawerToggle').setAttribute('aria-expanded','true'); }
  function closeDrawer(){ document.getElementById('drawer').classList.remove('open'); document.getElementById('scrim').hidden = true; document.getElementById('drawerToggle').setAttribute('aria-expanded','false'); }
  function updateProgress(){ const max = document.documentElement.scrollHeight - innerHeight; document.getElementById('progressBar').style.width = `${max > 0 ? (scrollY / max) * 100 : 0}%`; document.getElementById('backToTop').classList.toggle('hidden', scrollY < 600); }
  function trackActive(){ if (observer) observer.disconnect(); const links = [...document.querySelectorAll('.drawer-list a')]; observer = new IntersectionObserver(entries => entries.forEach(entry => { if(entry.isIntersecting){ document.querySelectorAll('.active,.active-section').forEach(el=>el.classList.remove('active','active-section')); document.querySelector(`[data-target="${entry.target.id}"]`)?.classList.add('active'); entry.target.classList.add('active-section'); }}), { rootMargin: '-20% 0px -65% 0px' }); links.forEach(a => { const el = document.getElementById(a.dataset.target); if(el) observer.observe(el); }); }
  return { init, build, updateProgress };
})();
