
// static/MSC/js/score.js
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('score-calc-btn').addEventListener('click', () => {
    fetch('/api/score/calculate/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const result = data.result;
        document.getElementById('score-han').textContent = `${result.han} 翻`;
        document.getElementById('score-fu').textContent = `${result.fu} 符`;
        document.getElementById('score-point').textContent = `${result.point} 点`;
        document.getElementById('score-yaku').textContent = result.yaku_list.join(', ');
      } else {
        alert("点数計算エラー: " + data.error);
      }
    })
    .catch(error => {
      alert("通信エラー: " + error);
    });
  });
});
