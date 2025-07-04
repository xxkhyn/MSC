// tehai.js (ハイライト修正版)

document.addEventListener('DOMContentLoaded', () => {
    // --- グローバル変数 ---
    let activeDoraSlot = null;
    let selectedDoraTiles = new Array(10).fill(null);
    let activeHandSlot = null;

    // --- ★★★ ここからが修正箇所 ★★★ ---
    /**
     * アガリ牌のハイライトを更新するグローバル関数
     */
    window.updateWinningTileHighlight = function() {
        // まず全てのスロットからハイライトを消す
        window.tileSlots.forEach(slot => slot.classList.remove('winning-tile-slot'));

        // 牌の合計枚数を計算
        const handTilesCount = Array.from(window.tileSlots).filter(s => s.dataset.tile).length;
        const meldedTilesCount = (window.meldedSets || []).reduce((acc, set) => acc + set.tiles.length, 0);
        const totalTiles = handTilesCount + meldedTilesCount;

        // 合計が14枚の時だけ、一番右の牌をハイライトする
        if (totalTiles === 14) {
            const filledSlots = Array.from(window.tileSlots).filter(s => s.dataset.tile);
            if (filledSlots.length > 0) {
                const winningSlot = filledSlots[filledSlots.length - 1];
                winningSlot.classList.add('winning-tile-slot');
            }
        }
    };
    // ★★★ 修正ここまで ★★★

    // --- グローバルに公開する変数と関数 ---
    window.tileSlots = document.querySelectorAll('#hand > .tile-slot');
    window.refillAndSort = function() {
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

        // ソート後にハイライトを更新
        window.updateWinningTileHighlight();
    };

    // (省略: DOM取得, CSRFトークン, sendHandToServer は変更なし)
    const tileImages = document.querySelectorAll('.tile-img');
    const resetButton = document.getElementById('reset-button');
    const submitButton = document.getElementById('submit-hand');
    const doraSlots = document.querySelectorAll('.dora-slot');
    const isTsumoCheckbox = document.getElementById('is-tsumo-checkbox');
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
    function sendHandToServer() {
        if (activeHandSlot) {
            activeHandSlot.classList.remove('selecting');
            activeHandSlot = null;
        }
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
            hand_pai: handPai,
            winning_pai: winningPai,
            is_tsumo: isTsumoCheckbox.checked,
            is_huuro: window.meldedSets && window.meldedSets.length > 0,
            huuro: window.meldedSets || [],
            dora_pai: selectedDoraTiles.filter(tile => tile !== null),
        };
        console.log('送信するデータ:', payload);
        fetch('/api/hand-input/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken, },
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
            slot.style.backgroundImage = '';
            delete slot.dataset.tile;
            slot.classList.remove('selecting');
            activeHandSlot = null;
            window.refillAndSort(); // この中でハイライトも更新される
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
                    slot.classList.remove('selecting');
                    activeDoraSlot = null;
                }
            } else {
                doraSlots.forEach(s => s.classList.remove('selecting'));
                slot.classList.add('selecting');
                activeDoraSlot = slot;
            }
        });
    });

    tileImages.forEach(img => {
        img.addEventListener('click', () => {
            const tileSrc = img.src;
            const tileCode = img.dataset.tile;
            const handTiles = Array.from(window.tileSlots).map(s => s.dataset.tile).filter(Boolean);
            const meldTiles = (window.meldedSets || []).flatMap(s => s.tiles);
            let doraTiles = selectedDoraTiles.filter(tile => tile !== null);
            if (activeDoraSlot) {
                const doraIndex = parseInt(activeDoraSlot.dataset.doraIndex, 10);
                doraTiles = selectedDoraTiles.filter((tile, index) => tile !== null && index !== doraIndex);
            }
            const allCurrentTiles = handTiles.concat(meldTiles).concat(doraTiles);
            const currentTileCount = allCurrentTiles.filter(c => c === tileCode).length;
            if (currentTileCount >= 4) {
                alert(`「${tileCode}」は既に4枚選択されています。`);
                if (activeDoraSlot) {
                    activeDoraSlot.classList.remove('selecting');
                    activeDoraSlot = null;
                }
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
            if (window.handleNaki && window.handleNaki(tileCode, tileSrc)) {
                return;
            }
            const emptySlot = Array.from(window.tileSlots).find(slot => !slot.dataset.tile);
            if (emptySlot) {
                emptySlot.style.backgroundImage = `url(${tileSrc})`;
                emptySlot.dataset.tile = tileCode;
                window.refillAndSort(); // この中でハイライトも更新される
                updateEmptyHandHighlight();
            } else {
                alert('手牌が一杯です。');
            }
        });
    });

    window.addClickToSelectHandlers();
    updateEmptyHandHighlight();
    window.updateWinningTileHighlight(); // 初期読み込み時にも実行

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
        window.updateWinningTileHighlight(); // リセット後にも実行
    });

    submitButton.addEventListener('click', (event) => {
        event.preventDefault();
        sendHandToServer();
    });
});
