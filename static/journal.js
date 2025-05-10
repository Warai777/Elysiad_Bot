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

      const tabClass = tab.classList.contains('tab-lore') ? 'top: 25%;' :
                       tab.classList.contains('tab-notes') ? 'top: 45%;' :
                       'top: 11.5%;';

      tab.classList.add('flipping');
      setTimeout(() => {
        tab.classList.remove('flipping');
        tab.classList.add('flipped-tab');
        tab.style.top = tabClass.match(/top: (.*?);/)[1];
        tab.style.left = '2%';
        slot.appendChild(tab);
        activeTab = tab;
      }, 500);
    });
  });
});