// journal.js — handles tab switching and animated page flips

const flipSound = new Audio('/static/page-flip.mp3');
flipSound.volume = 0.4;

document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.tab');
  const leftPage = document.getElementById('leftPage');
  const rightPage = document.getElementById('rightPage');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Remove active from all tabs
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      // Play page flip sound
      flipSound.currentTime = 0;
      flipSound.play();

      // Animate flip effect
      leftPage.classList.add('flip-left');
      rightPage.classList.add('flip-right');

      // Fake page change (could replace with real fetch/update)
      setTimeout(() => {
        leftPage.innerHTML = `<em>${tab.dataset.tab} - left page content</em>`;
        rightPage.innerHTML = `<em>${tab.dataset.tab} - right page content</em>`;
        leftPage.classList.remove('flip-left');
        rightPage.classList.remove('flip-right');
      }, 600);
    });
  });
});