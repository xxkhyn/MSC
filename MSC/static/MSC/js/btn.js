document.querySelectorAll('.btn-group').forEach(group => {
    group.addEventListener('click', e => {
      if (e.target.classList.contains('btn')) {
        // そのグループ内のボタン全てから .selected を外す
        group.querySelectorAll('.btn').forEach(btn => btn.classList.remove('selected'));
        // 押されたボタンに .selected を付ける
        e.target.classList.add('selected');
      }
    });
  });
  document.querySelectorAll('.option-group').forEach(group => {
    group.addEventListener('click', e => {
      if (e.target.classList.contains('btn')) {
        // そのグループ内のボタン全てから .selected を外す
        group.querySelectorAll('.btn').forEach(btn => btn.classList.remove('selected'));
        // 押されたボタンに .selected を付ける
        e.target.classList.add('selected');
      }
    });
  });