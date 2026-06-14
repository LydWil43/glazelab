// ─── INGREDIENT ROWS ─────────────────────────────────────────────────────────

let ingCount = document.querySelectorAll('.ingredient-row').length;

function addIngredient() {
  const list = document.getElementById('ingredients-list');
  const row = document.createElement('div');
  row.className = 'ingredient-row';
  row.innerHTML = `
    <input type="text" name="material[]" placeholder="Material name" class="ing-material">
    <input type="number" name="amount[]" placeholder="Amount" step="0.01" class="ing-amount">
    <label class="ing-additive-label">
      <input type="checkbox" name="is_additive[]" value="${ingCount}"> Additive
    </label>
    <button type="button" class="btn-remove-ing" onclick="removeIngredient(this)">×</button>
  `;
  list.appendChild(row);
  ingCount++;
  row.querySelector('input').focus();
}

function removeIngredient(btn) {
  const row = btn.closest('.ingredient-row');
  const list = document.getElementById('ingredients-list');
  if (list.querySelectorAll('.ingredient-row').length > 1) {
    row.remove();
  }
}

// ─── FLASH AUTO-DISMISS ───────────────────────────────────────────────────────

document.querySelectorAll('.flash').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity 0.4s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 400);
  }, 3000);
});
