document.addEventListener('DOMContentLoaded', () => {
  let currentNaki = null;

  // 鳴きボタン処理（ポン以外は拡張予定）
  document.querySelectorAll('.naki-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      currentNaki = btn.dataset.naki;  // "pon", "chi", "mkan", "akan" etc.
    });
  });

  // 牌画像クリック処理
  document.querySelectorAll('.tile-img').forEach(img => {
    img.addEventListener('click', (e) => {
      const tileCode = img.dataset.tile;
      const tileSrc = img.src;

      if (currentNaki === 'pon') {
        const hand = document.getElementById('hand');
        const fixed = document.getElementById('fixed-tiles');

        // 手牌スロットから3つ削除
        let removed = 0;
        const slots = Array.from(hand.querySelectorAll('.tile-slot'));
        for (let i = slots.length - 1; i >= 0 && removed < 3; i--) {
          hand.removeChild(slots[i]);
          removed++;
        }

        // 副露欄に3つ追加
        for (let i = 0; i < 3; i++) {
          const slot = document.createElement('div');
          slot.classList.add('hand-slot');
          slot.dataset.tile = tileCode;
          slot.style.backgroundImage = `url(${tileSrc})`;
          fixed.appendChild(slot);
        }

        currentNaki = null;

        // サーバーに送る関数が定義されていれば実行
        if (typeof sendHandToServer === 'function') {
          sendHandToServer();
        }

        e.stopImmediatePropagation();
        return;
      }

      // 通常選択は今後拡張（必要に応じてここに追加）
    });
  });
});
