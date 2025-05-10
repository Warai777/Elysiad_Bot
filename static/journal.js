// journal.js — handles tab switching and animated page flips

const flipSound = new Audio('/static/page-flip.mp3');
flipSound.volume = 0.4;

document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.tab');
  const slot = document.getElementById('active-tab-slot');
  const tabOrder = ['tab-hints', 'tab-lore', 'tab-notes'];

  const hintTab = document.querySelector('.tab-hints');
  hintTab.classList.add('flipped-tab');
  hintTab.style.left = 'calc(5%)';
  hintTab.style.transform = 'translateX(-100%) scaleY(2)';
  hintTab.style.zIndex = '5';
  hintTab.style.backgroundImage = "url('/static/parchment_tab_active.png')";
  slot.appendChild(hintTab);

  function updateTabPositions(activeTabClass) {
    const activeIndex = tabOrder.indexOf(activeTabClass);

    tabs.forEach(tab => {
      const tabClass = [...tab.classList].find(cls => tabOrder.includes(cls));
      if (!tabClass || tabClass === 'tab-hints') return;

      const index = tabOrder.indexOf(tabClass);

      if (index <= activeIndex) {
        // Flip to left
        tab.classList.add('flipped-tab');
        tab.style.left = 'calc(5%)';
        tab.style.transform = 'translateX(-100%) scaleY(2)';
        tab.style.zIndex = '5';
        tab.style.backgroundImage = "url('/static/parchment_tab_active.png')";
        slot.appendChild(tab);
      } else {
        // Return to right
        tab.classList.remove('flipped-tab');
        tab.style.left = '';
        tab.style.transform = '';
        tab.style.zIndex = '';
        tab.style.backgroundImage = "url('/static/parchment_tab.png')";
        document.body.appendChild(tab);
      }
    });
  }

  tabs.forEach(tab => {
    if (tab.classList.contains('tab-hints')) return;

    tab.addEventListener('click', () => {
      const activeTabClass = [...tab.classList].find(cls => tabOrder.includes(cls));
      if (!activeTabClass) return;

      flipSound.currentTime = 0;
      flipSound.play();

      tab.classList.add('flipping');
      setTimeout(() => {
        tab.classList.remove('flipping');
        updateTabPositions(activeTabClass);
      }, 500);
    });
  });
});