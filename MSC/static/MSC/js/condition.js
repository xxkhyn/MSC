// condition.js (リセット機能付き)

function getCSRFToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1]; // Optional chaining for safety
  return cookieValue || '';
}

document.addEventListener('DOMContentLoaded', () => {

  // --- ★★★ 1. リセット＆送信ロジックを追加 ★★★ ---

  const resetButton = document.getElementById('condition-reset-btn'); // HTMLに <button id="condition-reset-btn">リセット</button> を追加してください

  /**
   * フォームのUIをデフォルト状態にリセットする関数
   */
  const resetUI = () => {
    // ボタンの選択をリセット
    const resetToggleButtons = (selector, defaultValue) => {
      document.querySelectorAll(selector).forEach(btn => {
        btn.classList.remove('selected');
        if (btn.getAttribute('data-value') === defaultValue) {
          btn.classList.add('selected');
        }
      });
    };

    resetToggleButtons('.wind-btn[data-wind-type="prevalent"]', 'east');
    resetToggleButtons('.wind-btn[data-wind-type="seat"]', 'east');
    resetToggleButtons('.player-type-btn', 'child');
    resetToggleButtons('.riichi-btn', 'none');
    resetToggleButtons('.ippatsu-btn', 'false');
    resetToggleButtons('.rinshan-btn', 'false');
    resetToggleButtons('.chankan-btn', 'false');
    resetToggleButtons('.haitei-btn', 'false');
    resetToggleButtons('.tenho-btn', 'false');

    // カウンターをリセット
    document.getElementById('kyotaku-count').value = 0;
    document.getElementById('honba-count').value = 0;

    console.log('UIをリセットしました。');
  };

  /**
   * デフォルトの場況データをサーバーに送信する関数
   */
  const sendDefaultConditions = () => {
    const payload = {
      prevalent_wind: 'east',
      seat_wind: 'east',
      player_type: 'child',
      is_riichi: false,
      is_double_riichi: false,
      is_ippatsu: false,
      kyotaku: 0,
      honba: 0,
      is_rinshan: false,
      is_chankan: false,
      is_haitei: false,
      is_tenho: false,
    };

    console.log('デフォルトの場況をサーバーに送信します:', payload);

    fetch('/api/condition/submit/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      body: JSON.stringify(payload)
    })
    .then(res => {
      if(res.ok) {
        console.log('サーバー側の場況をリセットしました。');
      } else {
        res.json().then(err => console.error('サーバー側のリセットに失敗:', err));
      }
    })
    .catch(error => {
      console.error('通信エラー:', error);
    });
  };

  // --- 汎用選択処理 (変更なし) ---
  const setupToggleButtons = (selector) => {
    document.querySelectorAll(selector).forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll(selector).forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
      });
    });
  };

  setupToggleButtons('.wind-btn[data-wind-type="prevalent"]');
  setupToggleButtons('.wind-btn[data-wind-type="seat"]');
  setupToggleButtons('.player-type-btn');
  setupToggleButtons('.riichi-btn');
  setupToggleButtons('.ippatsu-btn');
  setupToggleButtons('.rinshan-btn');
  setupToggleButtons('.chankan-btn');
  setupToggleButtons('.haitei-btn');
  setupToggleButtons('.tenho-btn');

  // --- カウンター処理 (変更なし) ---
  document.querySelectorAll('.count-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-target');
      const action = btn.getAttribute('data-action');
      const input = document.getElementById(`${target}-count`);
      let value = parseInt(input.value, 10);
      if (action === 'increase') {
        value += 1;
      } else if (action === 'decrease' && value > 0) {
        value -= 1;
      }
      input.value = value;
    });
  });

  // --- ★★★ 2. 送信処理を data-value を使うように修正 ★★★ ---
  document.getElementById('condition-submit-btn').addEventListener('click', (e) => {
    e.preventDefault();

    // data-value属性から値を取得する方が確実
    const getValue = (selector) => document.querySelector(`${selector}.selected`)?.getAttribute('data-value');

    const riichiValue = getValue('.riichi-btn') || 'none';

    const payload = {
      prevalent_wind: getValue('.wind-btn[data-wind-type="prevalent"]') || 'east',
      seat_wind: getValue('.wind-btn[data-wind-type="seat"]') || 'east',
      player_type: getValue('.player-type-btn') || 'child',
      is_riichi: riichiValue === 'riichi',
      is_double_riichi: riichiValue === 'double',
      is_ippatsu: getValue('.ippatsu-btn') === 'true',
      kyotaku: parseInt(document.getElementById('kyotaku-count').value, 10),
      honba: parseInt(document.getElementById('honba-count').value, 10),
      is_rinshan: getValue('.rinshan-btn') === 'true',
      is_chankan: getValue('.chankan-btn') === 'true',
      is_haitei: getValue('.haitei-btn') === 'true',
      is_tenho: getValue('.tenho-btn') === 'true',
    };

    console.log('送信内容:', payload);

    fetch('/api/condition/submit/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert('送信成功！');
      } else {
        alert('送信失敗: ' + (data.error || '不明なエラー'));
      }
    })
    .catch(error => {
      alert('通信エラー: ' + error);
    });
  });

  // --- ★★★ 3. リセットボタンとページ読み込み時の処理 ★★★ ---
  if (resetButton) {
    resetButton.addEventListener('click', () => {
      resetUI();
      sendDefaultConditions();
    });
  }

  // ページ読み込み時にUIをリセットし、サーバーにもデフォルト値を送信
  resetUI();
  sendDefaultConditions();

});