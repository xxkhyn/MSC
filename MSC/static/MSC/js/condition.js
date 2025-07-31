// condition.js

function getCSRFToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
  return cookieValue || '';
}

// 一番上のボタンに .selected を付ける（まだ選ばれていない場合）
const autoSelectFirstButton = (groupSelector) => {
  document.querySelectorAll(groupSelector).forEach(group => {
    // ← 追加: 除外マークが付いていたらスキップ
    if (group.hasAttribute('data-skip-auto-select')) return;

    const alreadySelected = group.querySelector('.btn.selected');
    const firstBtn = group.querySelector('.btn');
    if (!alreadySelected && firstBtn) {
      firstBtn.classList.add('selected');
    }
  });
};

document.addEventListener('DOMContentLoaded', () => {

  const resetButton = document.getElementById('condition-reset-btn');

  /**
   * UIの選択状態をデフォルトに戻す
   */
  const resetUI = () => {
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
    resetToggleButtons('.player-type-btn', 'parent');
    resetToggleButtons('.riichi-btn', 'none');
    resetToggleButtons('.ippatsu-btn', 'false');
    resetToggleButtons('.rinshan-btn', 'false');
    resetToggleButtons('.chankan-btn', 'false');
    resetToggleButtons('.haitei-btn', 'false');
    resetToggleButtons('.tenho-btn', 'false');

    document.getElementById('kyotaku-count').value = 0;
    document.getElementById('honba-count').value = 0;

    console.log('UIをリセットしました。');
  };

  /**
   * 初期データをサーバーに送信
   */
  const sendDefaultConditions = () => {
    const payload = {
      prevalent_wind: 'east',
      seat_wind: 'east',
      player_type: 'parent',
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
      if (res.ok) {
        console.log('サーバー側の場況をリセットしました。');
      } else {
        res.json().then(err => console.error('サーバー側のリセットに失敗:', err));
      }
    })
    .catch(error => {
      console.error('通信エラー:', error);
    });
  };

  /**
   * ボタンの選択切り替え（クリックで .selected 切り替え）
   */
  const setupToggleButtons = (selector) => {
    document.querySelectorAll(selector).forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll(selector).forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
      });
    });
  };

  // 各カテゴリごとにボタン制御を設定
  setupToggleButtons('.wind-btn[data-wind-type="prevalent"]');
  setupToggleButtons('.wind-btn[data-wind-type="seat"]');
  setupToggleButtons('.player-type-btn');
  setupToggleButtons('.riichi-btn');
  setupToggleButtons('.ippatsu-btn');
  setupToggleButtons('.rinshan-btn');
  setupToggleButtons('.chankan-btn');
  setupToggleButtons('.haitei-btn');
  setupToggleButtons('.tenho-btn');

  // カウンター操作（+/-）
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

  // 送信ボタン押下時
  document.getElementById('condition-submit-btn').addEventListener('click', (e) => {
    e.preventDefault();

    const getValue = (selector) =>
      document.querySelector(`${selector}.selected`)?.getAttribute('data-value');

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

  // リセットボタン押下時
  if (resetButton) {
    resetButton.addEventListener('click', () => {
      resetUI();
      autoSelectFirstButton('.btn-group');
      autoSelectFirstButton('.btnn-group');
      sendDefaultConditions();
    });
  }

  // ページ読み込み時に初期化処理を実行
  resetUI();
  autoSelectFirstButton('.btn-group');
  autoSelectFirstButton('.btnn-group');
  sendDefaultConditions();
});
