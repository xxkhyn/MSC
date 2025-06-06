// static/MSC/js/jouken.js

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('condition-submit-btn').addEventListener('click', () => {
    fetch('/api/condition/submit/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()  // 別途CSRF取得関数定義が必要
      },
      body: JSON.stringify({
        is_riichi: true,
        is_ippatsu: false,
        prevalent_wind: 'east',
        seat_wind: 'south'
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert("送信成功！");
      } else {
        alert("送信失敗：" + data.error);
      }
    });
  });
});
