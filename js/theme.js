window.ReaderTheme = (() => {
  function init(){ const saved = localStorage.getItem('reader-theme'); if(saved === 'dark') document.body.classList.add('dark'); sync(); document.getElementById('themeToggle').addEventListener('click',()=>{ document.body.classList.toggle('dark'); localStorage.setItem('reader-theme', document.body.classList.contains('dark') ? 'dark' : 'light'); sync(); }); }
  function sync(){ document.getElementById('themeToggle').textContent = document.body.classList.contains('dark') ? 'Light' : 'Dark'; }
  return { init };
})();
