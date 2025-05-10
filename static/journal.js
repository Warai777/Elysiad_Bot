// journal.js — handles tab switching and animated page flips

const flipSound = new Audio('/static/page-flip.mp3');
flipSound.volume = 0.4;

document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.tab');
  const leftPage = document.getElementById('leftPage');
  const slot = document.getElementById('active-tab-slot');
  let activeTab = null;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      if (activeTab && activeTab !== tab) {
        activeTab.classList.remove('flipped-tab');
        document.body.appendChild(activeTab);
      }

      flipSound.currentTime = 0;
      flipSound.play();

      const computedTop = getComputedStyle(tab).top;
      tab.style.top = computedTop;

      tab.classList.add('flipping');
      setTimeout(() => {
        tab.classList.remove('flipping');
        tab.classList.add('flipped-tab');
        tab.style.left = 'calc(5%)';
        slot.appendChild(tab);
        activeTab = tab;
      }, 500);
    });
  });
});