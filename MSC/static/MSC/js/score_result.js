document.addEventListener('DOMContentLoaded', () => {
    const reloadButton = document.getElementById('reload-button');
    const resultIdElement = document.getElementById('result-id');
    const scoreArea = document.getElementById('score-area'); // 先に要素を取得

    // ★★★ ページが読み込まれた時に、結果表示エリアを空にする ★★★
    scoreArea.innerHTML = '';

    reloadButton.addEventListener('click', () => {

        // (任意) ユーザー体験向上のため、計算中にメッセージを表示する
        scoreArea.innerHTML = '<p>計算中...</p>';

        // ① まず /api/score/calculate/ に POST → 計算開始
        fetch('/api/score/calculate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not OK');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const resultId = data.result_id;
                console.log(`取得した result_id: ${resultId}`);
                resultIdElement.value = resultId;

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
            if (data.error_message) {
                scoreArea.innerHTML = `<div class="error"><p>⚠ エラー: ${data.error_message}</p></div>`;
            } else {
                let yakuHtml = '';
                data.yaku_list.forEach(([name, value]) => {
                    yakuHtml += `<li>${name}　${value}翻</li>`;  // ← 全角スペース + 翻数
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
});