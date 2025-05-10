// journal.js — handles tab switching and animated page flips

const flipSound = new Audio('/static/page-flip.mp3');
flipSound.volume = 0.4;

document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.tab');
  const leftPage = document.getElementById('leftPage');
  const rightPage = document.getElementById('rightPage');
  const slot = document.getElementById('active-tab-slot');
  let activeTab = null;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Reset active tab
      if (activeTab) {
        document.body.appendChild(activeTab);
        activeTab.classList.remove('active');
      }

      // Mark current as active
      tab.classList.add('active');
      activeTab = tab;
      slot.appendChild(tab);

      // Play sound and animate
      flipSound.currentTime = 0;
      flipSound.play();
      leftPage.classList.add('flip-left');
      rightPage.classList.add('flip-right');

      // Simulated content change
      setTimeout(() => {
        leftPage.innerHTML = `<em>${tab.dataset.tab} - left page content</em>`;
        rightPage.innerHTML = `<em>${tab.dataset.tab} - right page content</em>`;
        leftPage.appendChild(slot);
        slot.appendChild(tab);
        leftPage.classList.remove('flip-left');
        rightPage.classList.remove('flip-right');
      }, 600);
    });
  });
});