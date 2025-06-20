// static/MSC/js/jouken.js

document.addEventListener('DOMContentLoaded', () => {
    const getSelectedValue = (selector, attribute) => {
      const btn = document.querySelector(`${selector}.selected`);
      return btn ? btn.getAttribute(attribute) : null;
    };

    document.getElementById('condition-submit-btn').addEventListener('click', () => {
      const playerType = getSelectedValue('.player-type-btn', 'data-player');
      const riichi = getSelectedValue('.riichi-btn', 'data-riichi');
      const prevalentWind = getSelectedValue('.wind-btn[data-wind-type="prevalent"]', 'data-wind');
      const seatWind = getSelectedValue('.wind-btn[data-wind-type="seat"]', 'data-wind');
      const ippatsu = document.querySelector('.ippatsu-btn.selected')?.textContent === '一発';

      const payload = {
        is_riichi: riichi === 'riichi',
        is_double_riichi: riichi === 'double',
        is_ippatsu: ippatsu,
        prevalent_wind: prevalentWind,
        seat_wind: seatWind,
        player_type: playerType,
      };

      console.log('送信内容:', payload);

      fetch('/api/condition/submit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
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
      });
    });
  });