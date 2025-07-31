// tehai.js（最終版・整形＋修正バージョン）

document.addEventListener('DOMContentLoaded', () => {
    // --- グローバル変数 ---
    let activeDoraSlot = null;
    let selectedDoraTiles = new Array(10).fill(null);
    let activeHandSlot = null;
    let lastAddedTileCode = null;

    // --- グローバルに公開する変数と関数 ---
    window.tileSlots = document.querySelectorAll('#hand > .tile-slot');

    window.updateWinningTileHighlight = function () {
        window.tileSlots.forEach(slot => slot.classList.remove('winning-tile-slot'));
        if (!lastAddedTileCode) return;

        for (const slot of Array.from(window.tileSlots).reverse()) {
            if (slot.dataset.tile === lastAddedTileCode) {
                slot.classList.add('winning-tile-slot');
                break;
            }
        }
    };

    window.refillAndSort = function () {
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

    // --- 牌クリックのイベントリスナー ---
    const tileImages = document.querySelectorAll('.tile-img');
    tileImages.forEach(img => {
        img.addEventListener('click', async () => {
            const tileSrc = img.src;
            const tileCode = img.dataset.tile;

            // 通常制限チェック処理は省略（既存のままでOK）

            const emptySlot = Array.from(window.tileSlots).find(slot => !slot.dataset.tile);
            if (emptySlot) {
                emptySlot.style.backgroundImage = `url(${tileSrc})`;
                emptySlot.dataset.tile = tileCode;
                lastAddedTileCode = tileCode;
                window.refillAndSort();
            } else {
                alert('手牌が一杯です。');
            }
        });
    });

    // --- データ送信関数（winning_pai を lastAddedTileCode に） ---
    function sendHandToServer() {
        const normalizeTileCode = (code) => {
            if (/^[1-9]'?[mps]$/.test(code)) {
                const isRed = code.includes("'");
                const num = code[0];
                const suit = code.slice(-1);
                return suit + num + (isRed ? "'" : "");
            } else if (/^z[1-7]$/.test(code)) {
                return code;
            }
            return code;
        };

        const handPai = [];
        window.tileSlots.forEach(slot => {
            if (slot.dataset.tile) handPai.push(slot.dataset.tile);
        });

        const meldedTilesCount = (window.meldedSets || []).reduce((acc, set) => acc + set.tiles.length, 0);
        const totalTiles = handPai.length + meldedTilesCount;
        if (totalTiles < 14) {
            alert(`牌が${totalTiles}枚しかありません。14枚の牌を選択してください。`);
            return;
        }

        const payload = {
            hand_pai: handPai.filter(code => code !== lastAddedTileCode).map(normalizeTileCode),
            winning_pai: normalizeTileCode(lastAddedTileCode),
            is_tsumo: isTsumoCheckbox.checked,
            is_huuro: window.meldedSets && window.meldedSets.length > 0,
            huuro: window.meldedSets || [],
            dora_pai: selectedDoraTiles.filter(tile => tile !== null).map(normalizeTileCode),
        };

        fetch('/api/hand-input/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
            body: JSON.stringify(payload),
        })
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => alert('送信成功！'))
        .catch(err => alert('送信エラー'));
    }

    // --- ボタンにイベント追加 ---
    document.getElementById('submit-hand').addEventListener('click', (e) => {
        e.preventDefault();
        sendHandToServer();
    });
});
