(function initApp(){
  function showReader(parsed) {
    const sections = DocumentRenderer.render(parsed);
    ReaderNavigator.build(sections);
    document.getElementById('upload').classList.add('hidden');
    document.getElementById('reader').classList.remove('hidden');
    document.getElementById('drawerToggle').classList.remove('hidden');
    document.getElementById('newDocument').classList.remove('hidden');
    requestAnimationFrame(() => { scrollTo({ top: 0 }); ReaderNavigator.updateProgress(); });
  }
  document.addEventListener('DOMContentLoaded', () => {
    ReaderTheme.init(); ReaderNavigator.init(); DocumentUploader.init(showReader);
    document.getElementById('newDocument').addEventListener('click', () => location.reload());
  });
})();
