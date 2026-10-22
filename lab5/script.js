// Получение элементов из DOM
const taskInput = document.querySelector("#new-task-input");
const searchInput = document.querySelector("#search-task-input");
const addBtn = document.querySelector("#btn-add-task");
const todoList = document.querySelector("#todo-list");
const errorMsg = document.querySelector("#error-message");

const countCompleted = document.querySelector("#stat-completed");
const countPending = document.querySelector("#stat-pending");

// Массив для хранения задач
let todoData = [];

// Функция создания объекта задачи и добавления в массив
function handleAddTask() {
    const textValue = taskInput.value.trim();

    if (!textValue) {
        errorMsg.textContent = "Поле не может быть пустым!";
        return;
    }

    errorMsg.textContent = "";

    const newTask = {
        id: Date.now(),
        title: textValue,
        done: false
    };

    todoData.push(newTask);
    taskInput.value = "";
    
    renderTodoList();
}

// Перебор массива и отрисовка задач
function renderTodoList() {
    todoList.innerHTML = "";
    const filterQuery = searchInput.value.toLowerCase();

    // Фильтрация и цикл
    todoData.forEach((task) => {
        if (!task.title.toLowerCase().includes(filterQuery)) {
            return;
        }

        const taskHTML = `
            <li class="task-item ${task.done ? 'is-done' : ''}" data-id="${task.id}">
                <div class="task-content">
                    <input type="checkbox" class="task-checkbox" ${task.done ? 'checked' : ''}>
                    <span class="task-title">${escapeHtml(task.title)}</span>
                </div>
                <button class="btn-remove" title="Удалить">&times;</button>
            </li>
        `;

        todoList.insertAdjacentHTML("beforeend", taskHTML);
    });

    updateStatistics();
}

// Функция подсчета статистики
function updateStatistics() {
    let completed = 0;
    let pending = 0;

    for (let i = 0; i < todoData.length; i++) {
        if (todoData[i].done) {
            completed++;
        } else {
            pending++;
        }
    }

    countCompleted.textContent = completed;
    countPending.textContent = pending;
}

// Защита от XSS при выводе текста
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// Делегирование событий на списке (клик по чекбоксу и кнопке удаления)
todoList.addEventListener("click", (event) => {
    const target = event.target;
    const parentLi = target.closest(".task-item");

    if (!parentLi) return;

    const taskId = Number(parentLi.dataset.id);

    // Изменение статуса выполненности
    if (target.classList.contains("task-checkbox")) {
        const currentTask = todoData.find((item) => item.id === taskId);
        if (currentTask) {
            currentTask.done = target.checked;
            renderTodoList();
        }
    }

    // Удаление задачи
    if (target.classList.contains("btn-remove")) {
        todoData = todoData.filter((item) => item.id !== taskId);
        renderTodoList();
    }
});

// Обработчики событий ввода и нажатий
addBtn.addEventListener("click", handleAddTask);

taskInput.addEventListener("keyup", (event) => {
    if (event.key === "Enter") {
        handleAddTask();
    }
});

searchInput.addEventListener("input", renderTodoList);

// Первоначальный вызов
renderTodoList();