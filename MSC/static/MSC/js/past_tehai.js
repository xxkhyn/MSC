document.addEventListener('DOMContentLoaded', () => {
  const tileImages = document.querySelectorAll('.tile-img');
  const tileSlots = document.querySelectorAll('.tile-slot');
  const resetButton = document.getElementById('reset-button');
  const submitButton = document.getElementById('submit-hand'); // 追加

  // CSRFトークンをCookieから取得する関数
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  function sendHandToServer() {
    const hand = [];
    tileSlots.forEach(slot => {
      if (slot.dataset.tile) hand.push(slot.dataset.tile);
    });

    const formData = new FormData();
    formData.append('hand_pai', hand.join(','));

    fetch('/index/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
      },
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      console.log('送信成功:', data);
      // 必要ならここで画面更新など
    })
    .catch(error => {
      console.error('送信エラー:', error);
    });
  }

  // --- ▼ 自動送信の呼び出しを削除 ▼ ---
  tileImages.forEach(img => {
    img.addEventListener('click', () => {
      const tileSrc = img.src;
      const tileCode = img.dataset.tile;

      const count = Array.from(tileSlots).filter(slot => slot.dataset.tile === tileCode).length;
      if (count >= 4) {
        alert(`「${tileCode}」は4枚までしか選べません`);
        return;
      }

      if (tileCode.includes("'")) {
        const redCount = Array.from(tileSlots).filter(slot => slot.dataset.tile && slot.dataset.tile.includes("'")).length;
        if (redCount >= 1) {
          alert('赤牌は1枚までしか選べません');
          return;
        }
      }

      const emptySlot = findNextEmptySlot();
      if (emptySlot) {
        emptySlot.style.backgroundImage = `url(${tileSrc})`;
        emptySlot.dataset.tile = tileCode;

        refillAndSort();

        // sendHandToServer(); ← 削除
      }
    });
  });

  tileSlots.forEach(slot => {
    slot.addEventListener('click', () => {
      slot.style.backgroundImage = '';
      delete slot.dataset.tile;

      refillAndSort();

      // sendHandToServer(); ← 削除
    });
  });

  resetButton.addEventListener('click', () => {
    tileSlots.forEach(slot => {
      slot.style.backgroundImage = '';
      delete slot.dataset.tile;
    });

    // sendHandToServer(); ← 削除
  });

  // ✅ 「送信」ボタンが押されたときだけ送る！
  submitButton.addEventListener('click', () => {
    sendHandToServer();
  });

  function findNextEmptySlot() {
    return Array.from(tileSlots).find(slot => !slot.dataset.tile);
  }

  function refillAndSort() {
    const tiles = [];
    tileSlots.forEach(slot => {
      if (slot.dataset.tile) {
        tiles.push({
          code: slot.dataset.tile,
          src: slot.style.backgroundImage
        });
      }
    });

    const suitOrder = { m: 1, p: 2, s: 3, z: 4 };

    function normalize(tileCode) {
      if (/^[1-9]'?[mps]$/.test(tileCode)) {
        const isRed = tileCode.includes("'");
        const num = parseInt(tileCode[0]);
        const suit = tileCode.slice(-1);
        return { suit, num, isRed };
      } else if (/^z[1-7]$/.test(tileCode)) {
        const num = parseInt(tileCode.slice(1));
        return { suit: 'z', num, isRed: false };
      } else {
        return { suit: 'z', num: 99, isRed: false };
      }
    }

    tiles.sort((a, b) => {
      const A = normalize(a.code);
      const B = normalize(b.code);
      if (A.suit !== B.suit) return suitOrder[A.suit] - suitOrder[B.suit];
      if (A.num !== B.num) return A.num - B.num;
      return A.isRed - B.isRed;
    });

    tileSlots.forEach((slot, i) => {
      if (i < tiles.length) {
        slot.dataset.tile = tiles[i].code;
        slot.style.backgroundImage = tiles[i].src;
      } else {
        delete slot.dataset.tile;
        slot.style.backgroundImage = '';
      }
    });
  }
});
