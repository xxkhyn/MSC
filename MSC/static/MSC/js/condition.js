function getCSRFToken() {
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='));
  return cookieValue ? cookieValue.split('=')[1] : '';
}

document.addEventListener('DOMContentLoaded', () => {

  // ボタングループの汎用選択処理
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

  // 供託・積棒のカウンター処理
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

  // 送信処理
  document.getElementById('condition-submit-btn').addEventListener('click', (e) => {
    e.preventDefault();

    const windMap = { '東': 'east', '南': 'south', '西': 'west', '北': 'north' };

    const prevalentText = document.querySelector('.wind-btn[data-wind-type="prevalent"].selected')?.textContent.trim();
    const seatText = document.querySelector('.wind-btn[data-wind-type="seat"].selected')?.textContent.trim();
    const prevalent_wind = windMap[prevalentText] || 'east';
    const seat_wind = windMap[seatText] || 'east';

    const playerTypeText = document.querySelector('.player-type-btn.selected')?.textContent.trim();
    const player_type = (playerTypeText === '親') ? 'parent' : 'child';

    const riichiText = document.querySelector('.riichi-btn.selected')?.getAttribute('data-riichi') || 'none';
    const is_riichi = riichiText === 'riichi';
    const is_double_riichi = riichiText === 'double';

    const is_ippatsu = document.querySelector('.ippatsu-btn.selected')?.textContent.trim() === '一発';

    const is_rinshan = document.querySelector('.rinshan-btn.selected')?.textContent.trim() === 'あり';
    const is_chankan = document.querySelector('.chankan-btn.selected')?.textContent.trim() === 'あり';
    const is_haitei = document.querySelector('.haitei-btn.selected')?.textContent.trim() === 'あり';
    const is_tenho = document.querySelector('.tenho-btn.selected')?.textContent.trim() === 'あり';

    const kyotaku = parseInt(document.getElementById('kyotaku-count').value, 10);
    const honba = parseInt(document.getElementById('honba-count').value, 10);

    const payload = {
      prevalent_wind: prevalent_wind,
      seat_wind: seat_wind,
      player_type: player_type,
      is_riichi: is_riichi,
      is_double_riichi: is_double_riichi,
      is_ippatsu: is_ippatsu,
      kyotaku: kyotaku,
      honba: honba,
      is_rinshan: is_rinshan,
      is_chankan: is_chankan,
      is_haitei: is_haitei,
      is_tenho: is_tenho,
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
        alert('送信失敗: ' + data.error);
      }
    })
    .catch(error => {
      alert('通信エラー: ' + error);
    });
  });

});