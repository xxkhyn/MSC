function getCSRFToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='));
  return cookieValue ? cookieValue.split('=')[1] : '';
}

// ボタングループの選択処理
document.querySelectorAll('.btn-group').forEach(group => {
  group.addEventListener('click', e => {
    if (e.target.classList.contains('btn')) {
      group.querySelectorAll('.btn').forEach(btn => btn.classList.remove('selected'));
      e.target.classList.add('selected');
    }
  });
});

document.querySelectorAll('.option-group').forEach(group => {
  group.addEventListener('click', e => {
    if (e.target.classList.contains('btn')) {
      group.querySelectorAll('.btn').forEach(btn => btn.classList.remove('selected'));
      e.target.classList.add('selected');
    }
  });
});

// 送信ボタン押下時の処理
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('condition-submit-btn').addEventListener('click', (e) => {

    e.preventDefault();

    // 条件選択の取得
    const getSelectedText = (selector) => {
      const selected = document.querySelector(selector + ' .btn.selected');
      return selected ? selected.textContent.trim() : '';
    };

    const prevalent_wind = getSelectedText('.btn-group:nth-of-type(1)');  // 最初のbtn-group（場風）
    const seat_wind = getSelectedText('.btn-group:nth-of-type(2)');      // 2番目のbtn-group（自風）

    const is_riichi = getSelectedText('.option-group:nth-of-type(1)') !== 'なし';
    const is_double_riichi = getSelectedText('.option-group:nth-of-type(1)') === 'ダブル立直';
    const is_ippatsu = getSelectedText('.option-group:nth-of-type(2)') === '一発';
    const is_rinshan = getSelectedText('.option-group:nth-of-type(3)') === '嶺上開花';
    const is_chankan = getSelectedText('.option-group:nth-of-type(4)') === '搶槓';

    // 漢字→英語へのマッピング
    const wind_map = {
      '東': 'east',
      '南': 'south',
      '西': 'west',
      '北': 'north'
    };

    fetch('/api/condition/submit/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      body: JSON.stringify({
        prevalent_wind: wind_map[prevalent_wind],
        seat_wind: wind_map[seat_wind],
        is_riichi: is_riichi,
        is_double_riichi: is_double_riichi,
        is_ippatsu: is_ippatsu,
        is_rinshan: is_rinshan,
        is_chankan: is_chankan
        // 必要であれば他の条件も追加可能
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert("送信成功！");
      } else {
        alert("送信失敗：" + data.error);
      }
    })
    .catch(error => {
      alert("通信エラー：" + error);
    });
  });
});