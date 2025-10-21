const apiUser = "/api/user/users/";
const apiBook = "/api/book/books/";
const apiBorrow = "/api/borrow/borrows/";

// === USERS ===
async function loadUsers() {
  const res = await fetch(apiUser);
  const data = await res.json();
  const list = document.getElementById("user-list");
  list.innerHTML = "";
  data.forEach(u => {
    list.innerHTML += `<li class="list-group-item d-flex justify-content-between">
      ${u.id}. ${u.username} (${u.email})
      <div>
        <button class="btn btn-sm btn-info me-2" onclick="viewUser(${u.id})">Xem</button>
        <button class="btn btn-sm btn-warning me-2" onclick="editUser(${u.id}, '${u.username}', '${u.email}')">Sửa</button>
        <button class="btn btn-sm btn-danger" onclick="deleteUser(${u.id})">Xóa</button>
      </div>
    </li>`;
  });
}

async function deleteUser(id) {
  await fetch(apiUser + id + "/", { method: "DELETE" });
  loadUsers();
}

function viewUser(id) {
  window.location.href = `/user/${id}/`;
}

async function editUser(id, username, email) {
  const newUsername = prompt("Nhập tên người dùng mới:", username);
  const newEmail = prompt("Nhập email mới:", email);
  if (newUsername && newEmail) {
    await fetch(apiUser + id + "/", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: newUsername, email: newEmail })
    });
    loadUsers();
  }
}

document.getElementById("userForm").addEventListener("submit", async e => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  await fetch(apiUser, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email })
  });
  e.target.reset();
  loadUsers();
});

// === BOOKS ===
async function loadBooks() {
  const res = await fetch(apiBook);
  const data = await res.json();
  const list = document.getElementById("book-list");
  list.innerHTML = "";
  data.forEach(b => {
    list.innerHTML += `<li class="list-group-item d-flex justify-content-between">
      ${b.id}. ${b.title} - ${b.author} (${b.available ? "✅" : "❌"})
      <div>
        <button class="btn btn-sm btn-info me-2" onclick="viewBook(${b.id})">Xem</button>
        <button class="btn btn-sm btn-warning me-2" onclick="editBook(${b.id}, '${b.title}', '${b.author}', ${b.available})">Sửa</button>
        <button class="btn btn-sm btn-danger" onclick="deleteBook(${b.id})">Xóa</button>
      </div>
    </li>`;
  });
}

async function deleteBook(id) {
  await fetch(apiBook + id + "/", { method: "DELETE" });
  loadBooks();
}

function viewBook(id) {
  window.location.href = `/book/${id}/`;
}

async function editBook(id, title, author, available) {
  const newTitle = prompt("Nhập tên sách mới:", title);
  const newAuthor = prompt("Nhập tác giả mới:", author);
  const newAvailable = confirm("Sách có sẵn chứ? (OK = Có, Cancel = Không)");
  if (newTitle && newAuthor) {
    await fetch(apiBook + id + "/", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitle, author: newAuthor, available: newAvailable })
    });
    loadBooks();
  }
}

document.getElementById("bookForm").addEventListener("submit", async e => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const author = document.getElementById("author").value;
  await fetch(apiBook, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, author, available: true })
  });
  e.target.reset();
  loadBooks();
});

// === BORROWS ===
async function loadBorrows() {
  const res = await fetch(apiBorrow);
  const data = await res.json();
  const list = document.getElementById("borrow-list");
  list.innerHTML = "";
  
  data.forEach(b => {
    const userName = b.user_name || `User ${b.user}`;
    const bookName = b.book_title || `Book ${b.book}`;
    list.innerHTML += `<li class="list-group-item">
      #${b.id}: ${userName} mượn "${bookName}", Ngày mượn: ${b.borrow_date}, Trả: ${b.return_date || "Chưa trả"}
    </li>`;
  });
}

// Load users into dropdown
async function loadUserDropdown() {
  const res = await fetch(apiUser);
  const users = await res.json();
  const select = document.getElementById("user_select");
  select.innerHTML = '<option value="">Chọn người dùng</option>';
  users.forEach(user => {
    select.innerHTML += `<option value="${user.id}">${user.username} (${user.email})</option>`;
  });
}

// Load books into dropdown
async function loadBookDropdown() {
  const res = await fetch(apiBook);
  const books = await res.json();
  const select = document.getElementById("book_select");
  select.innerHTML = '<option value="">Chọn sách</option>';
  books.forEach(book => {
    const status = book.available ? "✅" : "❌";
    select.innerHTML += `<option value="${book.id}" ${!book.available ? 'disabled' : ''}>${book.title} - ${book.author} ${status}</option>`;
  });
}

document.getElementById("borrowForm").addEventListener("submit", async e => {
  e.preventDefault();
  const userId = document.getElementById("user_select").value;
  const bookId = document.getElementById("book_select").value;
  const borrow_date = document.getElementById("borrow_date").value;
  
  if (!userId || !bookId) {
    alert("Vui lòng chọn người dùng và sách!");
    return;
  }
  
  await fetch(apiBorrow, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user: userId, book: bookId, borrow_date })
  });
  e.target.reset();
  loadBorrows();
  loadBookDropdown(); // Reload to update availability
});

loadUsers();
loadBooks();
loadBorrows();
loadUserDropdown();
loadBookDropdown();