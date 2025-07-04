// naki.js (最終版)
// 機能：鳴き（ポン・チー・カン）に関する全ての処理を担当します。
// tehai.jsの後に読み込まれる必要があります。

// グローバルスコープに鳴きデータを定義
window.meldedSets = [];
let currentNaki = null;

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM要素の取得 ---
    const nakiButtons = document.querySelectorAll('.naki-btn');
    const tileImagesForNaki = document.querySelectorAll('.tile-img');
    const handContainer = document.getElementById('hand');

    // --- イベントリスナー ---
    nakiButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // 鳴きボタンを押した時点で回数チェックを行う
            if (window.meldedSets.length >= 4) {
                alert('鳴きは4回までです。');
                return; // 5回目は鳴きモードに移行させない
            }
            const nakiType = btn.dataset.naki;
            currentNaki = nakiType;
            alert(`「${btn.textContent}」する牌を1枚、下の牌セレクターから選んでください。`);
        });
    });

    // --- tehai.jsから呼び出されるメイン関数 ---
    window.handleNaki = function(tileCode, tileSrc) {
        if (!currentNaki) {
            return false; // 鳴きモードでなければtehai.jsに処理を戻す
        }

        // 念のため、牌を選択した時点でも回数チェック
        if (window.meldedSets.length >= 4) {
            alert('鳴きは4回までです。');
            currentNaki = null; // 鳴き状態をリセット
            return true;
        }

        // 現在の手牌と副露の状況を把握
        const allTilesInHand = Array.from(window.tileSlots).map(s => s.dataset.tile).filter(Boolean);
        const meldedTiles = (window.meldedSets || []).flatMap(s => s.tiles);
        const allCurrentTiles = allTilesInHand.concat(meldedTiles);
        const getCount = (code) => allCurrentTiles.filter(c => c === code).length;

        // 各種鳴きの妥当性チェック
        if (currentNaki === 'pon') {
            if (getCount(tileCode) > 1) {
                alert(`「${tileCode}」を既に2枚以上持っているため、ポンはできません。`);
                currentNaki = null;
                return true;
            }
        } else if (currentNaki === 'mkan' || currentNaki === 'akan') {
            if (getCount(tileCode) > 0) {
                alert(`「${tileCode}」を既に持っているため、カンはできません。`);
                currentNaki = null;
                return true;
            }
        } else if (currentNaki === 'chi') {
            const suit = tileCode.slice(-1);
            const num = parseInt(tileCode[0], 10);
            if (suit === 'z' || num >= 8) {
                alert('その牌からはチーできません。');
                currentNaki = null;
                return true;
            }
            const tile1 = tileCode;
            const tile2 = getNextTileCode(tileCode, 1);
            const tile3 = getNextTileCode(tileCode, 2);
            if (getCount(tile1) >= 4 || getCount(tile2) >= 4 || getCount(tile3) >= 4) {
                alert(`チーを構成する牌（${tile1}, ${tile2}, ${tile3}）の中に、既に4枚あるものが含まれています。`);
                currentNaki = null;
                return true;
            }
        }

        // チェックをパスしたら各種鳴き処理を実行
        if (currentNaki === 'pon') handlePon(tileCode, tileSrc);
        else if (currentNaki === 'chi') handleChi(tileCode, tileSrc);
        else if (currentNaki === 'mkan') handleMkan(tileCode, tileSrc);
        else if (currentNaki === 'akan') handleAkan(tileCode, tileSrc);

        currentNaki = null; // 鳴きモードを解除
        return true; // tehai.jsの処理を中断
    };

    /**
     * 副露（鳴き）を取り消す関数
     * @param {HTMLElement} meldGroupElement - クリックされた副露グループのDOM要素
     */
    function undoMeld(meldGroupElement) {
        const meldData = JSON.parse(meldGroupElement.dataset.meld);
        const meldIndex = window.meldedSets.findIndex(set =>
            JSON.stringify(set) === JSON.stringify(meldData)
        );
        if (meldIndex > -1) {
            window.meldedSets.splice(meldIndex, 1);
        }
        meldGroupElement.remove();
        addSlotsToHand(3);
    }

    /**
     * 手牌エリアにスロットを追加する関数
     * @param {number} count - 追加するスロットの数
     */
    function addSlotsToHand(count) {
        const fixedTilesContainer = document.getElementById('fixed-tiles');
        for (let i = 0; i < count; i++) {
            const newSlot = document.createElement('div');
            newSlot.classList.add('tile-slot');
            handContainer.insertBefore(newSlot, fixedTilesContainer);
        }
        window.tileSlots = document.querySelectorAll('#hand > .tile-slot');
        if (window.addClickToDeleteHandlers) {
            window.addClickToDeleteHandlers();
        }
        window.refillAndSort();
    }

    // --- 共通のスロット削除関数 ---
    function removeSlotsFromHand(count) {
        const children = Array.from(handContainer.children);
        const handSlots = children.filter(child => child.classList.contains('tile-slot'));
        let removeCount = count;
        for (let i = handSlots.length - 1; i >= 0 && removeCount > 0; i--) {
            const slotToRemove = handSlots[i];
            slotToRemove.parentNode.removeChild(slotToRemove);
            removeCount--;
        }
        window.tileSlots = document.querySelectorAll('#hand > .tile-slot');
    }

    // --- 各種鳴き処理 ---
    function handlePon(tileCode) {
        removeSlotsFromHand(3);
        const newMeld = { type: 'pon', tiles: [tileCode, tileCode, tileCode] };
        window.meldedSets.push(newMeld);
        renderSingleMeld(newMeld);
        window.refillAndSort();
    }
    function handleChi(tileCode) {
        removeSlotsFromHand(3);
        const meldData = [tileCode, getNextTileCode(tileCode, 1), getNextTileCode(tileCode, 2)];
        const newMeld = { type: 'chi', tiles: meldData };
        window.meldedSets.push(newMeld);
        renderSingleMeld(newMeld);
        window.refillAndSort();
    }
    function handleMkan(tileCode) {
        removeSlotsFromHand(3); // カンは手牌が3枚減る
        const newMeld = { type: 'mkan', tiles: [tileCode, tileCode, tileCode, tileCode] };
        window.meldedSets.push(newMeld);
        renderSingleMeld(newMeld);
        window.refillAndSort();
    }
    function handleAkan(tileCode) {
        removeSlotsFromHand(3); // カンは手牌が3枚減る
        const newMeld = { type: 'akan', tiles: [tileCode, tileCode, tileCode, tileCode] };
        window.meldedSets.push(newMeld);
        renderSingleMeld(newMeld);
        window.refillAndSort();
    }

    // --- ヘルパー関数 ---
    function getNextTileCode(tileCode, offset = 1) {
        const suit = tileCode.slice(-1);
        const num = parseInt(tileCode[0], 10);
        if (isNaN(num) || num + offset > 9) return null;
        return (num + offset) + suit;
    }

    /**
     * 1つの副露グループを画面に描画する共通関数
     * @param {object} meld - 副露の情報（type, tilesを持つオブジェクト）
     */
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

    // --- リセット処理 ---
    window.resetNakiState = function() {
        window.meldedSets = [];
        currentNaki = null;
    };
});