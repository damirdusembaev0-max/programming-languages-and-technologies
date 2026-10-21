# Лабораторная работа №8
**Дисциплина:** «Языки и технология программирования» / «Технология программирования»  
**Тема:** Работа с JSON и локальным хранилищем (LocalStorage, SessionStorage): сохранение и загрузка пользовательских данных  
**Студент:** Дюсембаев Дамир  
**Группа:** ИС-25  
**Вариант:** 5 (Список избранных книг)[cite: 2]  

---

## 📌 Цель работы
Освоить сериализацию и десериализацию объектов JavaScript в JSON, хранение данных в `localStorage`, восстановление пользовательского интерфейса после обновления страницы, а также обработку ошибок и удаление записей[cite: 1].

---

## 🛠 Структура проекта
Проект состоит из одного комплексного файла `index.html`, содержащего разметку, стили и логику на JavaScript[cite: 1, 3, 5].

### Исходный код (`index.html`)

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Задание 5 — Избранные книги</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f6f8;
      margin: 20px;
    }
    .container {
      max-width: 500px;
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      margin: auto;
    }
    h2 {
      text-align: center;
      color: #333;
    }
    .form-group {
      display: flex;
      gap: 8px;
      margin-bottom: 15px;
    }
    input {
      flex: 1;
      padding: 8px;
      border: 1px solid #ccc;
      border-radius: 4px;
      outline: none;
    }
    input:focus {
      border-color: #28a745;
    }
    button {
      padding: 8px 12px;
      background-color: #28a745;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    button:hover {
      background-color: #218838;
    }
    ul {
      list-style-type: none;
      padding: 0;
    }
    li {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px;
      border-bottom: 1px solid #eee;
    }
    .delete-btn {
      background-color: #dc3545;
    }
    .delete-btn:hover {
      background-color: #c82333;
    }
    .empty {
      text-align: center;
      color: #777;
      font-style: italic;
      margin-top: 15px;
    }
  </style>
</head>
<body>

  <div class="container">
    <h2>📚 Список избранных книг</h2>
    
    <div class="form-group">
      <input type="text" id="titleInput" placeholder="Название книги">
      <input type="text" id="authorInput" placeholder="Автор">
      <button id="addBtn">Добавить</button>
    </div>

    <ul id="bookList"></ul>
  </div>

  <script>
    const STORAGE_KEY = 'lab8_favorite_books';

    const titleInput = document.getElementById('titleInput');
    const authorInput = document.getElementById('authorInput');
    const addBtn = document.getElementById('addBtn');
    const bookList = document.getElementById('bookList');

    let books = [];

    // Загрузка и десериализация данных из localStorage с защитой от ошибок
    function loadBooks() {
      try {
        const rawData = localStorage.getItem(STORAGE_KEY);
        books = rawData ? JSON.parse(rawData) : [];
        if (!Array.isArray(books)) books = [];
      } catch (e) {
        console.error('Ошибка загрузки данных из localStorage:', e);
        books = [];
      }
    }

    // Сохранение и сериализация данных в localStorage
    function saveBooks() {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(books));
      render();
    }

    // Отрисовка интерфейса
    function render() {
      bookList.replaceChildren();

      if (books.length === 0) {
        const emptyLi = document.createElement('div');
        emptyLi.className = 'empty';
        emptyLi.textContent = 'Список пока пуст. Добавьте первую книгу!';
        bookList.append(emptyLi);
        return;
      }

      books.forEach((book, index) => {
        const li = document.createElement('li');
        
        const span = document.createElement('span');
        span.textContent = `«${book.title}» — ${book.author}`;

        const delBtn = document.createElement('button');
        delBtn.textContent = 'Удалить';
        delBtn.className = 'delete-btn';
        delBtn.addEventListener('click', () => {
          books.splice(index, 1);
          saveBooks();
        });

        li.append(span, delBtn);
        bookList.append(li);
      });
    }

    // Обработчик добавления книги
    addBtn.addEventListener('click', () => {
      const title = titleInput.value.trim();
      const author = authorInput.value.trim();

      if (!title || !author) {
        alert('Пожалуйста, заполните оба поля!');
        return;
      }

      books.push({ title, author });
      titleInput.value = '';
      authorInput.value = '';
      saveBooks();
    });

    // Инициализация при старте приложения
    loadBooks();
    render();
  </script>

</body>
</html>
