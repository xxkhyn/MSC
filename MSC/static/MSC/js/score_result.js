document.addEventListener('DOMContentLoaded', () => {
  const reloadButton = document.getElementById('reload-button');
  const resultId = document.getElementById('result-id').value;
  const scoreArea = document.getElementById('score-area');

  reloadButton.addEventListener('click', () => {
    // Step 1: サーバーに得点計算を依頼
    fetch(`/api/score/run/${resultId}/`, {
      method: 'POST',
    })
    .then(response => {
      if (!response.ok) throw new Error('計算処理に失敗しました');
      // Step 2: 計算完了後、結果を取得
      return fetch(`/api/score/calculate/${resultId}/`);
    })
    .then(response => {
      if (!response.ok) throw new Error('結果取得に失敗しました');
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
      scoreArea.innerHTML = `<div class="error"><p>⚠ エラー: ${error.message}</p></div>`;
    });
  });
});
