document.addEventListener('DOMContentLoaded', () => {
  let currentNaki = null;

  document.querySelectorAll('.naki-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      if (btn.dataset.naki === 'pon') {
        currentNaki = 'pon';
      }
    });
  });

  document.querySelectorAll('.tile-img').forEach(img => {
    img.addEventListener('click', (e) => {
      const tileCode = img.dataset.tile;
      const tileSrc = img.src;

      if (currentNaki === 'pon') {
        const hand = document.getElementById('hand');
        const fixed = document.getElementById('fixed-tiles');

        // tile-slot を 3 個削除
        let removed = 0;
        const slots = Array.from(hand.querySelectorAll('.tile-slot'));
        for (let i = slots.length - 1; i >= 0 && removed < 3; i--) {
          hand.removeChild(slots[i]);
          removed++;
        }

        // hand-slot を 3 個作って追加
        for (let i = 0; i < 3; i++) {
          const slot = document.createElement('div');
          slot.classList.add('hand-slot');
          slot.dataset.tile = tileCode;
          slot.style.backgroundImage = `url(${tileSrc})`;
          fixed.appendChild(slot);
        }

        currentNaki = null;

        if (typeof sendHandToServer === 'function') {
          sendHandToServer(); // 手牌変更送信
        }

        e.stopImmediatePropagation();
        return;
      }

      // 通常の選択処理は script2.js 側
    });
  });
});
