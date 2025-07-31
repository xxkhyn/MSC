// tehai.js (最終版・完全版)

document.addEventListener('DOMContentLoaded', () => {
    // --- グローバル変数 ---
    let activeDoraSlot = null;
    let selectedDoraTiles = new Array(10).fill(null);
    let activeHandSlot = null;
    let lastSelectedTileCode = null;
    let lastSelectedSlot = null;



    // --- グローバルに公開する変数と関数 ---
    window.tileSlots = document.querySelectorAll('#hand > .tile-slot');

    window.updateWinningTileHighlight = function () {
        window.tileSlots.forEach(slot => slot.classList.remove('winning-tile-slot'));

        const meldedCount = (window.meldedSets || []).reduce((acc, set) => acc + set.tiles.length, 0);
        const totalTiles = Array.from(window.tileSlots).filter(s => s.dataset.tile).length + meldedCount;

        if (totalTiles !== 14 || !lastSelectedTileCode) return;

            // スロットインデックスでの和了牌位置を決定（0-based）
            const highlightIndex = 14 - Math.floor(meldedCount / 3) - 1;

            const slot = window.tileSlots[highlightIndex];

        // tileCodeの一致だけでなく、スロット自体が lastSelectedSlot かどうかも見る
        if (slot && slot.dataset.tile === lastSelectedTileCode) {
                slot.classList.add('winning-tile-slot');
        } else if (lastSelectedSlot && lastSelectedSlot.dataset.tile === lastSelectedTileCode) {
            lastSelectedSlot.classList.add('winning-tile-slot');
        }
    };


    // 和了方法ボタン（ツモ / ロン）の選択処理
    const agariTypeButtons = document.querySelectorAll('.agari-type-btn');
    window.isTsumoSelected = true; // 初期値はツモ

    agariTypeButtons.forEach(button => {
        button.addEventListener('click', () => {
            // すべてのボタンから選択クラスを除去
            agariTypeButtons.forEach(btn => btn.classList.remove('selected'));
            // クリックされたボタンに選択クラスを付与
            button.classList.add('selected');

            // 状態をグローバル変数に記録
            window.isTsumoSelected = button.dataset.agari === 'tsumo';
        });
    });






    window.refillAndSort = function () {
    const tiles = [];
    let winningTile = null;

    // 全tileを取得
    window.tileSlots.forEach(slot => {
        if (slot.dataset.tile) {
            tiles.push({
                code: slot.dataset.tile,
                src: slot.style.backgroundImage,
                slot: slot
            });
        }
    });

    const meldedCount = (window.meldedSets || []).reduce((acc, set) => acc + set.tiles.length, 0);
    const totalTiles = tiles.length + meldedCount;

    // 和了牌を右端に除外する条件：牌が14枚あるときだけ
    if (totalTiles === 14 && lastSelectedTileCode) {
        const index = tiles.findIndex(tile => tile.code === lastSelectedTileCode);
        if (index !== -1) {
            winningTile = tiles.splice(index, 1)[0]; // ソート対象から除外
        }
    }

    // ソート処理（数字・種類・赤ドラ）
    const suitOrder = { m: 1, p: 2, s: 3, z: 4 };
    function normalize(tileCode) {
        if (!tileCode) return null;
        if (/^[1-9]'?[mps]$/.test(tileCode)) {
            const isRed = tileCode.includes("'");
            const num = parseInt(tileCode[0]);
            const suit = tileCode.slice(-1);
            return { suit, num, isRed };
        } else if (/^z[1-7]$/.test(tileCode)) {
            const num = parseInt(tileCode.slice(1));
            return { suit: 'z', num, isRed: false };
        }
        return { suit: 'z', num: 99, isRed: false };
    }

    tiles.sort((a, b) => {
        const A = normalize(a.code);
        const B = normalize(b.code);
        if (A.suit !== B.suit) return suitOrder[A.suit] - suitOrder[B.suit];
        if (A.num !== B.num) return A.num - B.num;
        return A.isRed - B.isRed;
    });

    // 和了牌があるなら右端に追加
    if (winningTile) {
        tiles.push(winningTile);
    }

    // UIに反映
    window.tileSlots.forEach((slot, i) => {
        if (i < tiles.length) {
            slot.dataset.tile = tiles[i].code;
            slot.style.backgroundImage = tiles[i].src;
            slot.style.cursor = 'pointer';
        } else {
            delete slot.dataset.tile;
            slot.style.backgroundImage = '';
            slot.style.cursor = 'default';
        }
    });

    window.updateWinningTileHighlight();
};



    // --- DOM取得とCSRFトークン ---
    const tileImages = document.querySelectorAll('.tile-img');
    const resetButton = document.getElementById('reset-button');
    const submitButton = document.getElementById('submit-hand');
    const doraSlots = document.querySelectorAll('.dora-slot');

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

    // --- サーバーへのデータ送信関数 ---
    function sendHandToServer() {
        if (activeHandSlot) {
            activeHandSlot.classList.remove('selecting');
            activeHandSlot = null;
        }

        const normalizeTileCode = (code) => {
            if (/^[1-9]'?[mps]$/.test(code)) {
                // 赤牌含む数字牌 → 5'm → m5'
                const isRed = code.includes("'");
                const num = code[0];
                const suit = code.slice(-1);
                return (suit + num + (isRed ? "'" : ""));
            } else if (/^z[1-7]$/.test(code)) {
                return code; // 字牌はそのまま
            }
            return code;
        };
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

        const winningPai = handPai.pop();

        const payload = {
            hand_pai: handPai.map(normalizeTileCode),
            winning_pai: normalizeTileCode(winningPai),
            is_tsumo: window.isTsumoSelected,
            is_huuro: window.meldedSets && window.meldedSets.length > 0,
            huuro: window.meldedSets || [],
            dora_pai: selectedDoraTiles.filter(tile => tile !== null).map(normalizeTileCode),
        };


        console.log('送信するデータ:', payload);
        fetch('/api/hand-input/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
            body: JSON.stringify(payload),
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(`HTTP ${response.status}: ${text}`); });
            }
            return response.json();
        })
        .then(data => {
            console.log('サーバーからの応答:', data);
            alert('送信成功！');
        })
        .catch(error => {
            console.error('送信エラー:', error);
            alert(`送信に失敗しました: ${error.message}`);
        });
    }

    function sendEmptyStateToServer() {
        const payload = {
            hand_pai: [],
            winning_pai: '',
            is_tsumo: true,
            is_huuro: false,
            huuro: [],
            dora_pai: []
        };

        console.log('空の状態をサーバーに送信します。');
        fetch('/api/hand-input/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
            body: JSON.stringify(payload),
        })
        .then(response => {
            if (response.ok) {
                console.log('サーバー側の状態をクリアしました。');
            } else {
                response.text().then(text => {
                   console.error('サーバー側の状態クリアに失敗しました:', text);
                });
            }
        })
        .catch(error => {
            console.error('状態クリアのための通信エラー:', error);
        });
    }

    // --- イベントリスナー ---
    function updateEmptyHandHighlight() {
        const isHandEmpty = Array.from(window.tileSlots).every(slot => !slot.dataset.tile);
        const firstSlot = window.tileSlots[0];
        if (firstSlot) {
            if (isHandEmpty) {
                firstSlot.classList.add('selecting');
            } else if (firstSlot !== activeHandSlot) {
                firstSlot.classList.remove('selecting');
            }
        }
    }

    window.addClickToSelectHandlers = function() {
        window.tileSlots.forEach(slot => {
            slot.removeEventListener('click', handleSlotClick);
            slot.addEventListener('click', handleSlotClick);
        });
    }

    function handleSlotClick() {
        const slot = this;
        if (window.isNakiActive && window.isNakiActive()) return;
        if (activeDoraSlot) {
            activeDoraSlot.classList.remove('selecting');
            activeDoraSlot = null;
        }
        if (slot === activeHandSlot) {
            if (slot === lastSelectedSlot) {
                lastSelectedSlot = null;
                lastSelectedTileCode = null;
            }
            slot.style.backgroundImage = '';
            delete slot.dataset.tile;
            slot.classList.remove('selecting');
            activeHandSlot = null;
            window.refillAndSort();
        } else if (slot.dataset.tile) {
            if (activeHandSlot) {
                activeHandSlot.classList.remove('selecting');
            }
            slot.classList.add('selecting');
            activeHandSlot = slot;
        }
        updateEmptyHandHighlight();
    }

    doraSlots.forEach(slot => {
        slot.addEventListener('click', () => {
            if (activeHandSlot) {
                activeHandSlot.classList.remove('selecting');
                activeHandSlot = null;
            }
            const doraIndex = parseInt(slot.dataset.doraIndex, 10);
            if (selectedDoraTiles[doraIndex] !== null) {
                selectedDoraTiles[doraIndex] = null;
                slot.style.backgroundImage = '';
                if (activeDoraSlot === slot) {
                    activeDoraSlot.classList.remove('selecting');
                    activeDoraSlot = null;
                }
            } else {
                doraSlots.forEach(s => s.classList.remove('selecting'));
                slot.classList.add('selecting');
                activeDoraSlot = slot;
            }
        });
    });

    // 牌クリックのイベントリスナー (asyncに対応)
    tileImages.forEach(img => {
        img.addEventListener('click', async () => {
            const tileSrc = img.src;
            const tileCode = img.dataset.tile;

            // 牌の選択枚数チェック
            const isRedFive = tileCode.includes("'");
            const handTiles = Array.from(window.tileSlots).map(s => s.dataset.tile).filter(Boolean);
            const meldTiles = (window.meldedSets || []).flatMap(s => s.tiles);
            let doraTiles = selectedDoraTiles.filter(tile => tile !== null);
            if (activeDoraSlot) {
                const doraIndex = parseInt(activeDoraSlot.dataset.doraIndex, 10);
                doraTiles = selectedDoraTiles.filter((tile, index) => tile !== null && index !== doraIndex);
            }
            const allCurrentTiles = handTiles.concat(meldTiles).concat(doraTiles);
            const normalVersion = tileCode.replace("'", "");
            const redVersion = `5'${normalVersion.slice(-1)}`;
            const countOfNormal = allCurrentTiles.filter(c => c === normalVersion).length;
            const countOfRed = allCurrentTiles.filter(c => c === redVersion).length;

            if (countOfNormal + countOfRed >= 4) {
                alert(`「${normalVersion.slice(0, -1)}」牌は既に4枚選択されています。`);
                if (activeDoraSlot) { activeDoraSlot.classList.remove('selecting'); activeDoraSlot = null; }
                return;
            }
            if (isRedFive && countOfRed >= 1) {
                alert(`赤ドラの「${tileCode}」は1枚しか選択できません。`);
                if (activeDoraSlot) { activeDoraSlot.classList.remove('selecting'); activeDoraSlot = null; }
                return;
            }

            if (activeDoraSlot) {
                activeDoraSlot.style.backgroundImage = `url(${tileSrc})`;
                const doraIndex = parseInt(activeDoraSlot.dataset.doraIndex, 10);
                selectedDoraTiles[doraIndex] = tileCode;
                activeDoraSlot.classList.remove('selecting');
                activeDoraSlot = null;
                return;
            }

            // handleNakiの呼び出しをawaitに変更
            if (window.handleNaki && await window.handleNaki(tileCode, tileSrc)) {
                return;
            }

            const emptySlot = Array.from(window.tileSlots).find(slot => !slot.dataset.tile);
            if (emptySlot) {
                emptySlot.style.backgroundImage = `url(${tileSrc})`;
                emptySlot.dataset.tile = tileCode;

                // 和了牌情報を更新（←ソートの前に行うのが重要）
                lastSelectedTileCode = tileCode;
                lastSelectedSlot = emptySlot;
            }

            // 牌が入らなくても和了牌情報を更新したならソート・ハイライトを即時実行
            setTimeout(() => {
                window.refillAndSort();
                updateEmptyHandHighlight();
            }, 0);

            if (!emptySlot) {
                alert('手牌が一杯です。');
                }   
        });
    });

    // --- 初期化処理 ---
    window.addClickToSelectHandlers();
    updateEmptyHandHighlight();
    window.updateWinningTileHighlight();

    resetButton.addEventListener('click', () => {
        if (window.resetNakiState) {
            window.resetNakiState();
        }
        doraSlots.forEach(slot => {
            slot.style.backgroundImage = '';
            slot.classList.remove('selecting');
        });
        selectedDoraTiles.fill(null);
        activeDoraSlot = null;
        activeHandSlot = null;
        isTsumoCheckbox.checked = true;
        const handContainer = document.getElementById('hand');
        handContainer.innerHTML = '';
        for (let i = 0; i < 14; i++) {
            const newSlot = document.createElement('div');
            newSlot.classList.add('tile-slot');
            newSlot.dataset.index = i;
            handContainer.appendChild(newSlot);
        }
        const fixedTilesDiv = document.createElement('div');
        fixedTilesDiv.id = 'fixed-tiles';
        fixedTilesDiv.classList.add('fixed-tiles');
        handContainer.appendChild(fixedTilesDiv);
        window.tileSlots = document.querySelectorAll('#hand > .tile-slot');
        window.addClickToSelectHandlers();
        updateEmptyHandHighlight();
        window.updateWinningTileHighlight();
        sendEmptyStateToServer();
    });

    submitButton.addEventListener('click', (event) => {
        event.preventDefault();
        sendHandToServer();
    });

    // ページ読み込み時にリセットを実行
    resetButton.click();
});
