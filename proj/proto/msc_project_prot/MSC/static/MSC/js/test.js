document.addEventListener('DOMContentLoaded', () => {
  const tileImages = document.querySelectorAll('.tile-img');
  const tileSlots = document.querySelectorAll('.tile-slot');
  const resetButton = document.getElementById('reset-button');
  const submitButton = document.getElementById('submit-hand');

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
    console.log('sendHandToServer called');
    
    const hand = [];
    tileSlots.forEach(slot => {
      if (slot.dataset.tile) hand.push(slot.dataset.tile);
    });

    if (hand.length === 0) {
      alert("手牌を選択してください。");
      return;
    }

    const payload = {
      hand_pai: hand.join(','),
      winning_pai: "1m",
      is_huuro: false,
      huuro: "",
      dora_pai: "1z",
    };

    console.log('Sending to:', 'http://127.0.0.1:8000/api/hand-input/');
    console.log('Payload:', payload);

    fetch('/api/hand-input/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify(payload),
    })
    .then(response => {
      console.log('Response status:', response.status);
      console.log('Response URL:', response.url);
      
      if (!response.ok) {
        return response.text().then(text => {
          console.log('Error response body:', text);
          throw new Error(`HTTP ${response.status}: ${text}`);
        });
      }
      
      return response.json();
    })
    .then(data => {
      console.log('送信成功:', data);
      alert('送信成功！');
    })
    .catch(error => {
      console.error('送信エラー:', error);
      alert(`送信に失敗しました: ${error.message}`);
    });
  }

  // タイル選択のイベントリスナー
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
      }
    });
  });

  // タイルスロットのクリック（削除）
  tileSlots.forEach(slot => {
    slot.addEventListener('click', () => {
      slot.style.backgroundImage = '';
      delete slot.dataset.tile;
      refillAndSort();
    });
  });

  // リセットボタン
  resetButton.addEventListener('click', () => {
    tileSlots.forEach(slot => {
      slot.style.backgroundImage = '';
      delete slot.dataset.tile;
    });
  });

  // 送信ボタン（重複削除・event.preventDefault追加）
  submitButton.addEventListener('click', (event) => {
    event.preventDefault();  // フォーム送信を阻止
    console.log('Submit button clicked');
    sendHandToServer();
  });

  // ヘルパー関数
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




reloadButton.addEventListener('click', () => {
      fetch(`/api/score/calculate/${resultId}/`)
        .then(response => {
          if (!response.ok) throw new Error('Network response was not OK');
          return response.json();
        })
        .then(data => {
          if (data.error_message) {
            scoreArea.innerHTML = `<div class="error"><p>⚠ エラー: ${data.error_message}</p></div>`;
          } else {
            let yakuHtml = '';
            data.yaku_list.forEach(yaku => {
              yakuHtml += `<li>${yaku}</li>`;
            });
  
            scoreArea.innerHTML = `
              <div class="score-block">
                <p><strong>翻数:</strong> ${data.han} 翻</p>
                <p><strong>符数:</strong> ${data.fu} 符</p>
                <p><strong>得点:</strong> ${data.point} 点</p>
                <p><strong>役:</strong></p>
                <ul class="yaku-list">${yakuHtml}</ul>
              </div>
            `;
          }
        })
        .catch(error => {
          scoreArea.innerHTML = `<div class="error"><p>⚠ データ取得エラー: ${error.message}</p></div>`;
        });
    });