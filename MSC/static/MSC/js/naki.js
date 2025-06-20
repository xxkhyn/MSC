// naki.js
// 機能：鳴き（ポン・チー・カン）に関する全ての処理を担当します。
// tehai.jsの後に読み込まれる必要があります。

// グローバルスコープに鳴きデータを定義
window.meldedSets = [];
let currentNaki = null;

document.addEventListener('DOMContentLoaded', () => {
    // --- DOM要素の取得 ---
    const nakiButtons = document.querySelectorAll('.naki-btn');
    const fixedTilesContainer = document.getElementById('fixed-tiles');
    const tileImagesForNaki = document.querySelectorAll('.tile-img');
    const handContainer = document.getElementById('hand'); 

    // --- イベントリスナー ---
    nakiButtons.forEach(btn => {
        btn.addEventListener('click', () => {
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

    // --- 現在の手牌と副露の状況を把握 ---
    const allTilesInHand = Array.from(window.tileSlots).map(s => s.dataset.tile).filter(Boolean);
    const meldedTiles = (window.meldedSets || []).flatMap(s => s.tiles);
    const allCurrentTiles = allTilesInHand.concat(meldedTiles);
    const getCount = (code) => allCurrentTiles.filter(c => c === code).length;

    // ★★★ ここから検証ロジックを強化 ★★★

    // --- ポンの場合のチェック ---
    if (currentNaki === 'pon') {
        // ポンは牌を3枚追加する扱いのため、実行前に2枚以上持っていると5枚になってしまう。
        // ※「既に鳴いている」状態も、この条件で検知できます。
        if (getCount(tileCode) > 1) {
            alert(`「${tileCode}」を既に2枚以上持っているため、ポンはできません。`);
            currentNaki = null; // 鳴き状態をリセット
            return true;      // tehai.jsの処理を中断
        }
    }
    // --- カンの場合のチェック ---
    else if (currentNaki === 'mkan' || currentNaki === 'akan') {
        // カンは牌を4枚追加する扱いのため、実行前に1枚でも持っていると5枚になってしまう。
        if (getCount(tileCode) > 0) {
            alert(`「${tileCode}」を既に持っているため、カンはできません。`);
            currentNaki = null;
            return true;
        }
    }
    // --- チーの場合のチェック ---
    else if (currentNaki === 'chi') {
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
        // チーを構成する3枚が、それぞれ既に4枚持っていないかチェック
        if (getCount(tile1) >= 4 || getCount(tile2) >= 4 || getCount(tile3) >= 4) {
            alert(`チーを構成する牌（${tile1}, ${tile2}, ${tile3}）の中に、既に4枚あるものが含まれています。`);
            currentNaki = null;
            return true;
        }
    }
    // ★★★ 検証ロジックここまで ★★★

    // 検証をパスした場合、各種鳴き処理を実行
    if (currentNaki === 'pon') {
        handlePon(tileCode, tileSrc);
    } else if (currentNaki === 'chi') {
        handleChi(tileCode, tileSrc);
    } else if (currentNaki === 'mkan') {
        handleMkan(tileCode, tileSrc);
    } else if (currentNaki === 'akan') {
        handleAkan(tileCode, tileSrc);
    }

    currentNaki = null;
    return true;
};
    
    // ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    // ★★★ 全ての鳴き処理を、ご要望のロジックに統一・修正しました ★★★
    // ★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

    // --- 共通のスロット削除関数 ---
    function removeSlotsFromHand(count) {
    // どんな環境でも動作するよう、より安全な方法に書き換えました。
    // 1. まず手牌エリア（#hand）の子要素を全て取得します。
    const children = Array.from(handContainer.children);

    // 2. その中から、手牌のスロット（.tile-slot）だけを抽出します。
    const handSlots = children.filter(child => child.classList.contains('tile-slot'));

    // 3. 抽出した手牌スロットの後ろから、指定された数だけ削除します。
    let removeCount = count;
    for (let i = handSlots.length - 1; i >= 0 && removeCount > 0; i--) {
        const slotToRemove = handSlots[i];
        slotToRemove.parentNode.removeChild(slotToRemove);
        removeCount--;
    }

    // 4. グローバル変数も、残った手牌スロットだけで更新します。
    const remainingChildren = Array.from(handContainer.children);
    window.tileSlots = remainingChildren.filter(child => child.classList.contains('tile-slot'));
}

    // --- ポン処理 ---
    function handlePon(tileCode, tileSrc) {
        // 1. 手牌からスロットを3つ削除
        removeSlotsFromHand(3);

        // 2. 副露データを作成
        const newMeld = { type: 'pon', tiles: [tileCode, tileCode, tileCode] };
        window.meldedSets.push(newMeld);
        
        // 3. 副露エリアに新しい牌を3つ生成
        renderSingleMeld(newMeld);
        
        // 4. 残った手牌をソート
        window.refillAndSort();
    }
    
    // --- チー処理 ---
    function handleChi(tileCode, tileSrc) {
        const suit = tileCode.slice(-1);
        const num = parseInt(tileCode[0], 10);
        if (suit === 'z' || num >= 8) {
            alert('その牌からはチーできません。');
            return;
        }

        // 1. 手牌からスロットを3つ削除
        removeSlotsFromHand(3);
        
        // 2. 副露データを作成
        const meldData = [tileCode, getNextTileCode(tileCode, 1), getNextTileCode(tileCode, 2)];
        const newMeld = { type: 'chi', tiles: meldData };
        window.meldedSets.push(newMeld);

        // 3. 副露エリアに新しい牌を3つ生成
        renderSingleMeld(newMeld);

        // 4. 残った手牌をソート
        window.refillAndSort();
    }

    // --- 明槓処理 ---
    function handleMkan(tileCode, tileSrc) {
        // 1. 手牌からスロットを4つ削除
        removeSlotsFromHand(3);

        // 2. 副露データを作成
        const newMeld = { type: 'mkan', tiles: [tileCode, tileCode, tileCode, tileCode] };
        window.meldedSets.push(newMeld);

        // 3. 副露エリアに新しい牌を4つ生成
        renderSingleMeld(newMeld);
        
        // 4. 残った手牌をソート
        window.refillAndSort();
    }

    // --- 暗槓処理 ---
    function handleAkan(tileCode, tileSrc) {
        // 1. 手牌からスロットを4つ削除
        removeSlotsFromHand(3);
        
        // 2. 副露データを作成
        const newMeld = { type: 'akan', tiles: [tileCode, tileCode, tileCode, tileCode] };
        window.meldedSets.push(newMeld);
        
        // 3. 副露エリアに新しい牌を4つ生成
        renderSingleMeld(newMeld);

        // 4. 残った手牌をソート
        window.refillAndSort();
    }

    // --- ヘルパー関数 ---
    function getNextTileCode(tileCode, offset = 1) {
        const suit = tileCode.slice(-1);
        const num = parseInt(tileCode[0], 10);
        if (isNaN(num) || num + offset > 9) return null;
        return (num + offset) + suit;
    }

    // --- 1つの副露グループを描画する共通関数 ---
    function renderSingleMeld(meld) {
    // 毎回fixed-tilesコンテナを取得しなおすことで、リセット後も正しく動作させる
    const fixedTilesContainer = document.getElementById('fixed-tiles');
    if (!fixedTilesContainer) return;

    const meldGroup = document.createElement('div');
    meldGroup.classList.add('meld-group');
        meld.tiles.forEach((tileCode, index) => {
            const tileDiv = document.createElement('div');
            tileDiv.classList.add('tile-slot');
            tileDiv.dataset.tile = tileCode;

            const imgElement = Array.from(tileImagesForNaki).find(img => img.dataset.tile === tileCode);
            if (imgElement) {
                tileDiv.style.backgroundImage = `url(${imgElement.src})`;
            }

            if ((meld.type === 'chi' && index === 0) || 
                (meld.type === 'pon' && index === 1) || 
                (meld.type === 'mkan' && index === 3)) {
                tileDiv.classList.add('naki-claimed-tile');
            } else if (meld.type === 'akan' && (index === 0 || index === 3)) {
                tileDiv.classList.add('naki-closed-tile');
            }

            meldGroup.appendChild(tileDiv);
        });
        fixedTilesContainer.appendChild(meldGroup);
    }
    
    // --- リセット処理 ---
    window.resetNakiState = function() {
    window.meldedSets = [];
    currentNaki = null;
    // DOM操作（innerHTML = ''）の行を削除
    };
});