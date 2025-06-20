// tehai.js
// 機能：手牌の基本的な操作（追加・削除・ソート）、サーバーへのデータ送信を担当します。
// naki.jsと連携して動作します。

document.addEventListener('DOMContentLoaded', () => {
    // --- グローバルに公開する変数と関数 ---
    // naki.jsから参照されるため、windowオブジェクトに格納します。
    window.tileSlots = document.querySelectorAll('#hand > .tile-slot');
    window.refillAndSort = function() {

        const currentHandSlots = window.tileSlots; 

        const tiles = [];
        window.tileSlots.forEach(slot => {
            if (slot.dataset.tile) {
                tiles.push({
                    code: slot.dataset.tile,
                    src: slot.style.backgroundImage
                });
            }
        });

        const suitOrder = { m: 1, p: 2, s: 3, z: 4 };

        function normalize(tileCode) {
            if (/^[1-9]'?[mps]$/.test(tileCode)) {
                const isRed = tileCode.includes("'");
                const num = parseInt(tileCode[0]);
                const suit = tileCode.slice(-1);
                return { suit, num, isRed };
            } else if (/^z[1-7]$/.test(tileCode)) {
                const num = parseInt(tileCode.slice(1));
                return { suit: 'z', num, isRed: false };
            }
            return { suit: 'z', num: 99, isRed: false }; // エラーケース
        }

        tiles.sort((a, b) => {
            const A = normalize(a.code);
            const B = normalize(b.code);
            if (A.suit !== B.suit) return suitOrder[A.suit] - suitOrder[B.suit];
            if (A.num !== B.num) return A.num - B.num;
            return A.isRed - B.isRed;
        });

        window.tileSlots.forEach((slot, i) => {
            if (i < tiles.length) {
                slot.dataset.tile = tiles[i].code;
                slot.style.backgroundImage = tiles[i].src;
            } else {
                delete slot.dataset.tile;
                slot.style.backgroundImage = '';
            }
        });
    };

    // --- DOM要素の取得 ---
    const tileImages = document.querySelectorAll('.tile-img');
    const resetButton = document.getElementById('reset-button');
    const submitButton = document.getElementById('submit-hand');

    // --- CSRFトークン取得 ---
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // --- サーバーへのデータ送信 ---
    function sendHandToServer() {
        console.log('sendHandToServer called');

        const handPai = [];
        window.tileSlots.forEach(slot => {
            if (slot.dataset.tile) handPai.push(slot.dataset.tile);
        });

        const meldedTilesCount = (window.meldedSets || []).reduce((acc, set) => acc + set.tiles.length, 0);
        const totalTiles = handPai.length + meldedTilesCount;

        if (totalTiles === 0) {
            alert("手牌を選択してください。");
            return;
        }

        if (totalTiles < 14) {
            alert(`牌が${totalTiles}枚しかありません。14枚の牌を選択してください。`);
            return;
        }

        const winningPai = handPai.pop(); // 手牌の最後の1枚をアガリ牌とする

        const payload = {
            hand_pai: handPai,
            winning_pai: winningPai,
            is_huuro: window.meldedSets && window.meldedSets.length > 0,
            huuro: window.meldedSets || [],
            dora_pai: "1z", // TODO: ドラ選択機能を実装
        };

        console.log('Sending to:', '/api/hand-input/');
        console.log('Payload:', payload);

        fetch('/api/hand-input/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(payload),
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(`HTTP ${response.status}: ${text}`); });
            }
            return response.json();
        })
        .then(data => {
            console.log('送信成功:', data);
            alert('送信成功！');
        })
        .catch(error => {
            console.error('送信エラー:', error);
            alert(`送信に失敗しました: ${error.message}`);
        });
    }

    // --- イベントリスナー ---

    // タイル選択（追加）
function addClickToDeleteHandlers() {
    window.tileSlots.forEach(slot => {
        slot.addEventListener('click', () => {
            if (slot.dataset.tile) {
                // 鳴き処理が有効な場合は何もしない（鳴き牌のクリック誤操作防止）
                if (window.isNakiActive && window.isNakiActive()) {
                    return;
                }
                slot.style.backgroundImage = '';
                delete slot.dataset.tile;
                window.refillAndSort();
            }
        });
    });
}

// --- イベントリスナーの初期設定 ---

// タイル選択（追加）
tileImages.forEach(img => {
    img.addEventListener('click', () => {
        const tileSrc = img.src;
        const tileCode = img.dataset.tile;

        // naki.jsの鳴き処理を先に呼び出す
        if (window.handleNaki && window.handleNaki(tileCode, tileSrc)) {
            return;
        }

        const allTiles = Array.from(window.tileSlots).map(s => s.dataset.tile).filter(Boolean);
        const meldedTiles = (window.meldedSets || []).flatMap(s => s.tiles);
        const currentTileCount = allTiles.concat(meldedTiles).filter(c => c === tileCode).length;

        if (currentTileCount >= 4) {
            alert(`「${tileCode}」は4枚までしか選べません`);
            return;
        }

        const emptySlot = Array.from(window.tileSlots).find(slot => !slot.dataset.tile);
        if (emptySlot) {
            emptySlot.style.backgroundImage = `url(${tileSrc})`;
            emptySlot.dataset.tile = tileCode;
            window.refillAndSort();
        } else {
            alert('手牌が一杯です。');
        }
    });
});

// タイルスロットのクリック（削除）イベントを初回設定
addClickToDeleteHandlers();

// リセットボタン
resetButton.addEventListener('click', () => {
    // 1. 鳴きの内部データをリセット
    if (window.resetNakiState) {
        window.resetNakiState();
    }

    // 2. 手牌の表示エリアを一度更地にする
    const handContainer = document.getElementById('hand');
    handContainer.innerHTML = ''; // 中身をすべて削除

    // 3. 14枚のタイル・スロットを再生成する
    for (let i = 0; i < 14; i++) {
        const newSlot = document.createElement('div');
        newSlot.classList.add('tile-slot');
        newSlot.dataset.index = i;
        handContainer.appendChild(newSlot);
    }

    // 4. 鳴き牌用のコンテナも再生成する
    const fixedTilesDiv = document.createElement('div');
    fixedTilesDiv.id = 'fixed-tiles';
    fixedTilesDiv.classList.add('fixed-tiles');
    handContainer.appendChild(fixedTilesDiv);

    // 5. グローバル変数のスロット情報を新しいものに更新
    window.tileSlots = document.querySelectorAll('#hand > .tile-slot');

    // 6. 新しく作ったスロットにクリックイベントを再設定
    addClickToDeleteHandlers();
});

// 送信ボタン
submitButton.addEventListener('click', (event) => {
    event.preventDefault();
    sendHandToServer();
});
});