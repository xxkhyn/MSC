// naki.js (最終版)

// グローバルスコープに鳴きデータを定義
window.meldedSets = [];
let currentNaki = null;

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM要素の取得 ---
    const nakiButtons = document.querySelectorAll('.naki-btn');
    const tileImagesForNaki = document.querySelectorAll('.tile-img');
    const handContainer = document.getElementById('hand');

    // --- モーダル関連の要素とロジック ---
    const modal = document.getElementById('red-five-selection-modal');
    const normalBtn = document.getElementById('use-normal-btn');
    const redBtn = document.getElementById('use-red-btn');
    let resolvePromise = null;

    function askForRedFive(tileSuit) {
        return new Promise(resolve => {
            resolvePromise = resolve;
            modal.style.display = 'flex';
            normalBtn.dataset.value = `5${tileSuit}`;
            redBtn.dataset.value = `5'${tileSuit}`;
        });
    }

    normalBtn.addEventListener('click', () => {
        if (resolvePromise) {
            resolvePromise(normalBtn.dataset.value);
            modal.style.display = 'none';
            resolvePromise = null;
        }
    });

    redBtn.addEventListener('click', () => {
        if (resolvePromise) {
            const redTileCode = redBtn.dataset.value;
            const allTilesInHand = Array.from(window.tileSlots).map(s => s.dataset.tile).filter(Boolean);
            const meldedTiles = (window.meldedSets || []).flatMap(s => s.tiles);
            const doraTiles = (window.selectedDoraTiles || []).filter(Boolean);
            const allCurrentTiles = allTilesInHand.concat(meldedTiles, doraTiles);
            if (allCurrentTiles.includes(redTileCode)) {
                alert(`赤ドラの「${redTileCode}」は既に使われています。`);
                return;
            }
            resolvePromise(redTileCode);
            modal.style.display = 'none';
            resolvePromise = null;
        }
    });

    // --- イベントリスナー ---
    nakiButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            if (window.meldedSets.length >= 4) {
                alert('鳴きは4回までです。');
                return;
            }
            const nakiType = btn.dataset.naki;
            currentNaki = nakiType;
            alert(`「${btn.textContent}」する牌を1枚、下の牌セレクターから選んでください。`);
        });
    });

    // --- tehai.jsから呼び出されるメイン関数 (asyncに変更) ---
    window.handleNaki = async function(tileCode, tileSrc) {
        if (!currentNaki) {
            return false;
        }
        if (window.meldedSets.length >= 4) {
            alert('鳴きは4回までです。');
            currentNaki = null;
            return true;
        }

        const isRedFive = tileCode.includes("'");
        if (isRedFive && currentNaki !== 'chi') {
            alert('赤ドラはチー以外で鳴くことはできません。');
            currentNaki = null;
            return true;
        }

        let nakiHandled = false;
        if (currentNaki === 'pon') {
            handlePon(tileCode);
            nakiHandled = true;
        } else if (currentNaki === 'chi') {
            await handleChi(tileCode); // handleChiの完了を待つ
            nakiHandled = true;
        } else if (currentNaki === 'mkan') {
            handleMkan(tileCode);
            nakiHandled = true;
        } else if (currentNaki === 'akan') {
            handleAkan(tileCode);
            nakiHandled = true;
        }

        if (nakiHandled) {
            currentNaki = null; // 全ての鳴き処理が終わってからリセット
            return true;
        }
        return false;
    };

    // --- 各鳴き処理 ---
    async function handleChi(tileCode) {
        let meldData = [tileCode, getNextTileCode(tileCode, 1), getNextTileCode(tileCode, 2)];
        const fiveIndex = meldData.findIndex(t => t && t.startsWith('5'));

        if (fiveIndex !== -1) {
            const tileSuit = meldData[fiveIndex].slice(-1);
            const chosenFive = await askForRedFive(tileSuit);
            meldData[fiveIndex] = chosenFive;
        }

        removeSlotsFromHand(3);
        const newMeld = { type: 'chi', tiles: meldData };
        window.meldedSets.push(newMeld);
        renderSingleMeld(newMeld);
        window.refillAndSort();
        window.updateWinningTileHighlight();
    }

    function handlePon(tileCode) {
        removeSlotsFromHand(3);
        const newMeld = { type: 'pon', tiles: [tileCode, tileCode, tileCode] };
        window.meldedSets.push(newMeld);
        renderSingleMeld(newMeld);
        window.refillAndSort();
        window.updateWinningTileHighlight();
    }

    function handleMkan(tileCode) {
        removeSlotsFromHand(3);
        const newMeld = { type: 'mkan', tiles: [tileCode, tileCode, tileCode, tileCode] };
        window.meldedSets.push(newMeld);
        renderSingleMeld(newMeld);
        window.refillAndSort();
        window.updateWinningTileHighlight();
    }

    function handleAkan(tileCode) {
        removeSlotsFromHand(3);
        const newMeld = { type: 'akan', tiles: [tileCode, tileCode, tileCode, tileCode] };
        window.meldedSets.push(newMeld);
        renderSingleMeld(newMeld);
        window.refillAndSort();
        window.updateWinningTileHighlight();
    }

    // --- ヘルパー関数 ---
    function getNextTileCode(tileCode, offset = 1) {
        const suit = tileCode.slice(-1);
        const num = parseInt(tileCode[0], 10);
        if (isNaN(num) || num + offset > 9) return null;
        return (num + offset) + suit;
    }
    
    function undoMeld(meldGroupElement) {
        const meldData = JSON.parse(meldGroupElement.dataset.meld);
        const meldIndex = window.meldedSets.findIndex(set =>
            JSON.stringify(set) === JSON.stringify(meldData)
        );
        if (meldIndex > -1) {
            window.meldedSets.splice(meldIndex, 1);
        }
        meldGroupElement.remove();
        addSlotsToHand(3); // カンでもチー・ポンでも3枚だけ戻す
    }

    function addSlotsToHand(count) {
        const fixedTilesContainer = document.getElementById('fixed-tiles');
        for (let i = 0; i < count; i++) {
            const newSlot = document.createElement('div');
            newSlot.classList.add('tile-slot');
            handContainer.insertBefore(newSlot, fixedTilesContainer);
        }
        window.tileSlots = document.querySelectorAll('#hand > .tile-slot');
        if (window.addClickToSelectHandlers) {
            window.addClickToSelectHandlers();
        }
        window.refillAndSort();
        if (window.updateWinningTileHighlight) {
            window.updateWinningTileHighlight();
        }
    }

    function removeSlotsFromHand(count) {
        const handSlots = Array.from(handContainer.children).filter(child => child.classList.contains('tile-slot'));
        let removeCount = count;
        for (let i = handSlots.length - 1; i >= 0 && removeCount > 0; i--) {
            const slotToRemove = handSlots[i];
            slotToRemove.parentNode.removeChild(slotToRemove);
            removeCount--;
        }
        window.tileSlots = document.querySelectorAll('#hand > .tile-slot');
    }

    function renderSingleMeld(meld) {
        const fixedTilesContainer = document.getElementById('fixed-tiles');
        if (!fixedTilesContainer) return;
        const meldGroup = document.createElement('div');
        meldGroup.classList.add('meld-group');
        meldGroup.dataset.meld = JSON.stringify(meld);
        meldGroup.addEventListener('click', () => undoMeld(meldGroup));
        meld.tiles.forEach((tileCode, index) => {
            const tileDiv = document.createElement('div');
            tileDiv.classList.add('tile-slot');
            tileDiv.dataset.tile = tileCode;
            if (meld.type === 'akan' && (index === 0 || index === 3)) {
                tileDiv.style.backgroundImage = `url('../../static/MSC/images/p_bk_1.gif')`;
                tileDiv.classList.add('naki-closed-tile');
            } else {
                const imgElement = Array.from(tileImagesForNaki).find(img => img.dataset.tile === tileCode);
                if (imgElement) {
                    tileDiv.style.backgroundImage = `url(${imgElement.src})`;
                }
            }
            if ((meld.type === 'chi' && index === 0) ||
                (meld.type === 'pon' && index === 1) ||
                (meld.type === 'mkan' && index === 3)) {
                tileDiv.classList.add('naki-claimed-tile');
            }
            meldGroup.appendChild(tileDiv);
        });
        fixedTilesContainer.appendChild(meldGroup);
    }

    window.resetNakiState = function() {
        window.meldedSets = [];
        currentNaki = null;
    };
});
