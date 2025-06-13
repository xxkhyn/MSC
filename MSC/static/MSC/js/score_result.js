document.addEventListener('DOMContentLoaded', () => {
    const reloadButton = document.getElementById('reload-button');
    const resultIdElement = document.getElementById('result-id'); // この input hidden に入れる

    reloadButton.addEventListener('click', () => {
        // ① まず /api/score/calculate/ に POST → 計算開始
        fetch('/api/score/calculate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}) // 今は空のPOSTでOK（hand, conditionはサーバ側で last() を取得している）
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not OK');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const resultId = data.result_id;
                console.log(`取得した result_id: ${resultId}`);
                resultIdElement.value = resultId; // input hidden にセットする（再読込用に保持）

                // ② 取得した result_id で /api/score/result/<result_id>/ をGET
                return fetch(`/api/score/result/${resultId}/`);
            } else {
                throw new Error(data.error || 'スコア計算エラー');
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not OK');
            return response.json();
        })
        .then(data => {
            // ③ 結果を画面に反映
            const scoreArea = document.getElementById('score-area');
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
            const scoreArea = document.getElementById('score-area');
            scoreArea.innerHTML = `<div class="error"><p>⚠ データ取得エラー: ${error.message}</p></div>`;
        });
    });
});
