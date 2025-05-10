// journal.js — handles tab switching and animated page flips with infinite inner flipping per tab

const flipSound = new Audio('/static/page-flip.mp3');
flipSound.volume = 0.4;

let currentSection = 'tab-hints';
let currentPageIndex = {
  'tab-hints': 0,
  'tab-lore': 0,
  'tab-notes': 0
};

document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.tab');
  const slot = document.getElementById('active-tab-slot');
  const leftPage = document.getElementById('leftPage');
  const rightPage = document.getElementById('rightPage');
  const tabOrder = ['tab-hints', 'tab-lore', 'tab-notes'];

  const hintTab = document.querySelector('.tab-hints');
  hintTab.classList.add('flipped-tab');
  hintTab.style.left = 'calc(5%)';
  hintTab.style.transform = 'translateX(-100%) scaleY(2)';
  hintTab.style.zIndex = '5';
  hintTab.style.backgroundImage = "url('/static/parchment_tab_active.png')";
  slot.appendChild(hintTab);

  function updateTabPositions(activeTabClass) {
    currentSection = activeTabClass;

    const activeIndex = tabOrder.indexOf(activeTabClass);
    tabs.forEach(tab => {
      const tabClass = [...tab.classList].find(cls => tabOrder.includes(cls));
      if (!tabClass || tabClass === 'tab-hints') return;

      const index = tabOrder.indexOf(tabClass);

      if (index <= activeIndex) {
        tab.classList.add('flipped-tab');
        tab.style.left = 'calc(5%)';
        tab.style.transform = 'translateX(-100%) scaleY(2)';
        tab.style.zIndex = '5';
        tab.style.backgroundImage = "url('/static/parchment_tab_active.png')";
        slot.appendChild(tab);
      } else {
        tab.classList.remove('flipped-tab');
        tab.style.left = '';
        tab.style.transform = '';
        tab.style.zIndex = '';
        tab.style.backgroundImage = "url('/static/parchment_tab.png')";
        document.body.appendChild(tab);
      }
    });
    renderCurrentPages();
  }

  async function fetchLorePage(pageIndex) {
    const response = await fetch(`/get_lore_page?page=${pageIndex}`);
    const data = await response.json();
    if (data.left !== undefined && data.right !== undefined) {
      leftPage.innerHTML = `<div>${data.left}</div>`;
      rightPage.innerHTML = `<div>${data.right}</div>`;
      currentPageIndex[currentSection] = data.current_page;
    }
  }

  function renderCurrentPages() {
    if (currentSection === 'tab-lore') {
      fetchLorePage(currentPageIndex[currentSection]);
    } else {
      const index = currentPageIndex[currentSection];
      leftPage.innerHTML = `<div>Section: ${currentSection}, Page: ${index * 2 + 1}</div>`;
      rightPage.innerHTML = `<div>Section: ${currentSection}, Page: ${index * 2 + 2}</div>`;
    }
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

  document.querySelector('.parchment-button.next').addEventListener('click', () => {
    currentPageIndex[currentSection]++;
    flipSound.currentTime = 0;
    flipSound.play();
    renderCurrentPages();
  });

  document.querySelector('.parchment-button.prev').addEventListener('click', () => {
    if (currentPageIndex[currentSection] > 0) currentPageIndex[currentSection]--;
    flipSound.currentTime = 0;
    flipSound.play();
    renderCurrentPages();
  });

  renderCurrentPages();
});