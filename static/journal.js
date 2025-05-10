// journal.js — handles tab switching and animated page flips

const flipSound = new Audio('/static/page-flip.mp3');
flipSound.volume = 0.4;

document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.tab');
  const slot = document.getElementById('active-tab-slot');
  let activeTab = null;
  let tabZIndex = 10; // incrementing to keep newest tab on top

  const topMap = {
    'tab-hints': '11.5%',
    'tab-lore': '25%',
    'tab-notes': '45%'
  };

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      if (activeTab && activeTab !== tab) {
        activeTab.classList.remove('flipped-tab');
        document.body.appendChild(activeTab);
      }

      flipSound.currentTime = 0;
      flipSound.play();

      const tabClass = [...tab.classList].find(cls => topMap[cls]);
      const topValue = topMap[tabClass] || '20%';

      tab.classList.add('flipping');
      setTimeout(() => {
        tab.classList.remove('flipping');
        tab.classList.add('flipped-tab');
        tab.style.top = topValue;
        tab.style.left = 'calc(5%)';
        tab.style.transform = 'translateX(-100%) scaleY(2)';
        tab.style.zIndex = tabZIndex++;
        slot.appendChild(tab);
        activeTab = tab;
      }, 500);
    });
  });
});