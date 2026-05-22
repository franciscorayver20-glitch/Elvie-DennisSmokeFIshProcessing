// ========================
// GLOBAL VARIABLE SAFETY
// ========================
window.currentAction = window.currentAction || "/add-product";
window.activeProductSheetId = window.activeProductSheetId || null;

// ========================
// NAVIGATION & UI LOGIC
// ========================
function showSection(sectionId) {
    console.log("Switching to Section: " + sectionId);
    document.querySelectorAll('.section-content').forEach(section => {
        if (section) section.style.display = 'none';
    });
    const target = document.getElementById(sectionId);
    if (target) {
        target.style.display = 'block';
        localStorage.setItem("activeSection", sectionId);
        if (sectionId === 'inventory') checkAndPromptInventory();
    } else {
        const home = document.getElementById('home-section');
        if (home) home.style.display = 'block';
    }
    if (window.innerWidth < 992) {
        const sidebar = $('#mainSidebar');
        if (sidebar.length) sidebar.collapse('hide');
    }
}

function checkAndPromptInventory() {
    const invSection = document.getElementById('inventory');
    if (!invSection || invSection.style.display === 'none') return;
    const productRows = document.querySelectorAll('#inventory table tbody tr');
    const isEmpty = productRows.length === 0 || (productRows.length === 1 && productRows[0].innerText.includes("No products"));
    if (isEmpty) {
        console.log("Inventory is empty. Prompting user to add a product.");
        setTimeout(() => prepareAddModal(), 300);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const isAuthPage = window.location.pathname.includes('login') || window.location.pathname.includes('sign-up') ||
                       window.location.pathname.includes('forgot-password') || window.location.pathname.includes('reset-password');
    if (!isAuthPage) {
        const hash = window.location.hash;
        if (hash === '#transactions') showSection('transactions');
        else if (hash === '#inventory') showSection('inventory');
        else if (hash === '#personnel') showSection('personnel');
        else {
            const lastSection = localStorage.getItem("activeSection") || "home-section";
            showSection(lastSection);
        }
    } else {
        localStorage.removeItem("activeSection");
    }
});

function prepareAddModal() {
    window.currentAction = "/add-product";
    const title = document.getElementById('modalTitle');
    if (title) title.innerText = "Add New Product";
    const form = document.getElementById('productForm');
    if (form) {
        form.reset();
        const cat = document.getElementById('prodCategory');
        const unit = document.getElementById('prodUnit');
        if (cat) cat.value = "Smoked";
        if (unit) unit.value = "kg";
    }
    const modal = $('#productModal');
    if (modal.length) modal.modal('show');
}

function editProduct(id, name, price, stock, category, unit) {
    if (!window.activeProductSheetId) {
        console.error("activeProductSheetId not set");
        return;
    }
    window.currentAction = `/update-product/${id}/sheet/${window.activeProductSheetId}`;
    const title = document.getElementById('modalTitle');
    if (title) title.innerText = "Edit " + name;
    const nameField = document.getElementById('prodName');
    if (nameField) {
        nameField.value = name;
        const priceField = document.getElementById('prodPrice');
        const stockField = document.getElementById('prodStock');
        const catField = document.getElementById('prodCategory');
        const unitField = document.getElementById('prodUnit');
        if (priceField) priceField.value = price;
        if (stockField) stockField.value = stock;
        if (catField) catField.value = category;
        if (unitField) unitField.value = unit;
        const modal = $('#productModal');
        if (modal.length) modal.modal('show');
    }
}

function deleteProduct(id, name) {
    if (!confirm(`Delete "${name}" from inventory?\nThis will also remove it from all product sheets.`)) return;
    fetch(`/delete-product/${id}`, { method: 'DELETE' })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                const row = document.getElementById(`row-${id}`);
                if (row) row.remove();
                checkAndPromptInventory();
            } else {
                alert(data.message || 'Deletion failed.');
            }
        })
        .catch(err => {
            console.error('Delete product error:', err);
            alert('Network error. Could not delete product.');
        });
}

function filterbyDate(tabElement, timePeriod) {
    const tabs = document.querySelectorAll('.excel-tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    if (tabElement) tabElement.classList.add('active');
    const rows = document.querySelectorAll('#transactionBody tr');
    rows.forEach(row => {
        const dateCell = row.querySelector('td:last-child');
        if (!dateCell) return;
        if (dateCell.innerText.includes(timePeriod) || row.colSpan > 1) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

function addDailySheet(todayDate) {
    fetch('/add-daily-sheet', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ date: todayDate }) })
        .then(response => response.json())
        .then(data => { if (data.success) location.reload(); else alert(data.message); });
}

function openAddBoxModal() {
    const boxNameSpan = document.getElementById('modalBoxName');
    const boxNameInput = document.getElementById('modalBoxNameInput');
    const boxIdInput = document.getElementById('modalBoxId');
    const productList = document.getElementById('boxProductList');
    const totalSpan = document.getElementById('modalTotalPrice');
    if (boxNameSpan) boxNameSpan.innerText = "New Box Instance";
    if (boxNameInput) boxNameInput.value = "";
    if (boxIdInput) boxIdInput.value = "";
    if (productList) productList.innerHTML = "";
    if (totalSpan) totalSpan.innerText = "Php 0.00";
    if (typeof addNewProductRow === 'function') addNewProductRow();
    const modal = $('#boxModal');
    if (modal.length) modal.modal('show');
}

function updateModalTotal() {
    let total = 0;
    document.querySelectorAll('#boxProductList tr').forEach(row => {
        const dropdown = row.querySelector('.product-dropdown');
        const qtyInput = row.querySelector('.qty-input');
        if (!dropdown || !qtyInput) return;
        const selectedOption = dropdown.options[dropdown.selectedIndex];
        if (selectedOption && selectedOption.dataset.price) {
            total += parseFloat(selectedOption.dataset.price) * (parseInt(qtyInput.value) || 0);
        }
    });
    const totalSpan = document.getElementById('modalTotalPrice');
    if (totalSpan) totalSpan.innerText = `Php ${total.toLocaleString(undefined, { minimumFractionDigits: 2 })}`;
}

function viewBoxDetails(boxId, boxName) {
    const boxNameSpan = document.getElementById('modalBoxName');
    const boxNameInput = document.getElementById('modalBoxNameInput');
    const boxIdInput = document.getElementById('modalBoxId');
    const productList = document.getElementById('boxProductList');
    if (boxNameSpan) boxNameSpan.innerText = boxName;
    if (boxNameInput) boxNameInput.value = boxName;
    if (boxIdInput) boxIdInput.value = boxId;
    if (productList) productList.innerHTML = '<tr><td colspan="3" class="text-center text-muted">Loading...</td></tr>';
    const modal = $('#boxModal');
    if (modal.length) modal.modal('show');
    if (typeof fetchProductsForCurrentSheet === 'function') {
        fetchProductsForCurrentSheet().then(() => {
            fetch(`/get-box-details/${boxId}`)
                .then(res => res.json())
                .then(data => {
                    if (productList) productList.innerHTML = '';
                    if (data.products && data.products.length > 0) {
                        data.products.forEach(item => { if (typeof addNewProductRow === 'function') addNewProductRow(item.id, item.quantity); });
                    } else {
                        if (typeof addNewProductRow === 'function') addNewProductRow();
                    }
                    updateModalTotal();
                })
                .catch(() => { if (productList) productList.innerHTML = '<td><td colspan="3" class="text-danger text-center">Failed to load.小说网'; });
        });
    } else {
        console.warn("fetchProductsForCurrentSheet not defined");
    }
}

function updateBoxStatus(id, status) {
    fetch('/update-box-status', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: id, status: status }) })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success' && data.last_modified) {
                const cell = document.getElementById(`modified-${id}`);
                if (cell) {
                    const d = new Date(data.last_modified);
                    cell.innerText = d.toLocaleString('en-PH', { month:'2-digit', day:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit', hour12:true });
                }
            } else if (data.status !== 'success') {
                alert("Failed to update status.");
            }
        });
}

document.addEventListener('DOMContentLoaded', function () {
    const boxModal = document.getElementById('boxModal');
    if (boxModal) {
        boxModal.addEventListener('hidden.bs.modal', function () {
            const productList = document.getElementById('boxProductList');
            const totalSpan = document.getElementById('modalTotalPrice');
            const boxNameSpan = document.getElementById('modalBoxName');
            const boxNameInput = document.getElementById('modalBoxNameInput');
            const boxIdInput = document.getElementById('modalBoxId');
            if (productList) productList.innerHTML = "";
            if (totalSpan) totalSpan.innerText = "Php 0.00";
            if (boxNameSpan) boxNameSpan.innerText = "New Box";
            if (boxNameInput) boxNameInput.value = "";
            if (boxIdInput) boxIdInput.value = "";
        });
    }
});

function validateBoxEntry() {
    const rows = document.querySelectorAll('#boxProductList tr');
    let products = [];
    const date = new Date().toISOString().split('T')[0];
    rows.forEach(row => {
        const select = row.querySelector('.product-dropdown');
        const qtyInput = row.querySelector('.qty-input');
        if (select && select.value) {
            products.push({ productId: select.value, qty: qtyInput ? qtyInput.value : 1 });
        }
    });
    if (products.length === 0) { alert("Please add at least one product."); return; }
    fetch('/save-box-transaction', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ products: products, date: date }) })
        .then(response => response.json())
        .then(data => { if (data.status === 'success') location.reload(); else alert("Failed to save transaction: " + data.message); });
}

// ========================
// PRODUCT SUBMIT (ADD/EDIT) - FIXED (always refresh the table)
// ========================
function submitProduct() {
    const nameInput = document.getElementById('prodName').value.trim();
    if (nameInput === "") {
        alert("Product name cannot be empty.");
        return;
    }
    if (!/^[a-zA-Z\s]+$/.test(nameInput)) {
        alert("Product name can only contain letters and spaces.");
        return;
    }

    const priceInput = document.getElementById('prodPrice').value;
    const stockInput = document.getElementById('prodStock').value;

    if (priceInput === "" || isNaN(parseFloat(priceInput))) {
        alert("Please enter a valid price.");
        return;
    }
    if (stockInput === "" || isNaN(parseInt(stockInput))) {
        alert("Please enter a valid stock quantity.");
        return;
    }

    const formData = new FormData(document.getElementById('productForm'));
    formData.append('sheet_id', window.activeProductSheetId);

    console.log("Submitting product to:", window.currentAction);
    console.log("Form data:", {
        name: nameInput,
        price: parseFloat(priceInput),
        stock: parseInt(stockInput),
        category: document.getElementById('prodCategory').value,
        unit: document.getElementById('prodUnit').value,
        sheet_id: window.activeProductSheetId
    });

    fetch(window.currentAction, { method: 'POST', body: formData })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
                $('#productModal').modal('hide');
                // Always refresh the current product sheet table
                fetch(`/get-product-sheet/${window.activeProductSheetId}`)
                    .then(res => res.json())
                    .then(sheetData => {
                        // Call the render function from inventory.html (it must be global)
                        if (typeof renderInventoryTable === 'function') {
                            renderInventoryTable(sheetData.products);
                        } else {
                            console.warn("renderInventoryTable not found, reloading page");
                            location.reload();
                        }
                        // Restore search filter if needed
                        const searchInput = document.getElementById('inventorySearch');
                        if (searchInput && searchInput.value) {
                            searchInventory(searchInput.value);
                        }
                    })
                    .catch(err => console.error("Failed to refresh table:", err));
            } else {
                alert("Error: " + data.message);
            }
        })
        .catch(err => {
            console.error("Fetch error:", err);
            alert("Network error: " + err.message);
        });
}

// Helper to format date for product table (used in updates)
function formatProductDateTime(dtStr) {
    if (!dtStr) return '-';
    const d = new Date(dtStr);
    return d.toLocaleString('en-PH', {
        month: '2-digit', day: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit', hour12: true
    });
}

// Helper for search inventory (if not already defined)
function searchInventory(query) {
    const q = query.toLowerCase().trim();
    const rows = document.querySelectorAll('#inventoryBody tr[id^="row-"]');
    let anyVisible = false;
    rows.forEach(row => {
        // Ensure row is a real element (not the dummy from override)
        if (!row.cells) return;
        const name = (row.cells[1] ? row.cells[1].innerText : '').toLowerCase();
        const category = (row.cells[2] ? row.cells[2].innerText : '').toLowerCase();
        const match = name.includes(q) || category.includes(q);
        row.style.display = match ? '' : 'none';
        if (match) anyVisible = true;
    });
    const emptyRow = document.getElementById('inventoryEmptyRow');
    if (emptyRow) emptyRow.style.display = anyVisible ? 'none' : '';
}

// Helper to escape HTML (used by other functions)
function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}