const pptxgen = require("pptxgenjs");
const p = new pptxgen(); p.layout = "LAYOUT_16x9";
p.author = "Дюсембаев Дамир"; p.title = "Система учета заявок на общежитие";
const NAVY="1F3A5F", ACC="2E86AB", SOFT="EAF2F8", TXT="222222", GREY="6B7785", F="Calibri";
let n = 0;
function base(title, notes){
  n++; const s = p.addSlide(); s.background={color:"FFFFFF"};
  s.addShape(p.ShapeType.rect,{x:0,y:0,w:10,h:0.9,fill:{color:NAVY}});
  s.addText(title,{x:0.5,y:0.1,w:9,h:0.7,fontFace:F,fontSize:26,bold:true,color:"FFFFFF",valign:"middle",isTextBox:true,margin:0});
  s.addText("Дюсембаев Дамир · ИС 25-22",{x:0.5,y:5.25,w:5,h:0.3,fontFace:F,fontSize:10,color:GREY,isTextBox:true,margin:0});
  s.addText(String(n),{x:9,y:5.25,w:0.5,h:0.3,fontFace:F,fontSize:10,color:GREY,align:"right",isTextBox:true,margin:0});
  if(notes) s.addNotes(notes);
  return s;
}
function bullets(s, items, o={}){
  s.addText(items.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<items.length-1,paraSpaceAfter:9}})),
    Object.assign({x:0.6,y:1.2,w:8.8,h:3.8,fontFace:F,fontSize:19,color:TXT,valign:"top",isTextBox:true},o));
}
// 1 Титул
n++; let s = p.addSlide(); s.background={color:NAVY};
s.addText("Система учета заявок на общежитие",{x:0.7,y:1.3,w:8.6,h:1.3,fontFace:F,fontSize:38,bold:true,color:"FFFFFF",isTextBox:true});
s.addText("СРО · Языки и технология программирования · Тема 20",{x:0.7,y:2.8,w:8.6,h:0.5,fontFace:F,fontSize:18,color:"CFE3F0",isTextBox:true});
s.addShape(p.ShapeType.rect,{x:0.7,y:3.6,w:1.2,h:0.06,fill:{color:ACC}});
s.addText("Автор: Дюсембаев Дамир\nГруппа: ИС 25-22",{x:0.7,y:3.8,w:8.6,h:0.9,fontFace:F,fontSize:20,color:"FFFFFF",isTextBox:true});
s.addNotes("Представиться, назвать тему и цель: автоматизировать приём и обработку заявок на общежитие.");

// 2 Проблема
s = base("Проблема и актуальность","Иногородних студентов больше половины, заявок много. Ручной учёт даёт потери и дубли.");
[["364,5 тыс.","иногородних студентов из 678 тыс. по стране"],["54%","доля иногородних среди всех студентов"],["3 риска","потери заявок, ошибки данных, дубли"]].forEach((c,i)=>{
  const x=0.6+i*3.05;
  s.addShape(p.ShapeType.roundRect,{x,y:1.25,w:2.85,h:1.9,fill:{color:SOFT},line:{color:SOFT},rectRadius:0.1});
  s.addText(c[0],{x,y:1.4,w:2.85,h:0.8,fontFace:F,fontSize:32,bold:true,color:ACC,align:"center",isTextBox:true});
  s.addText(c[1],{x:x+0.15,y:2.2,w:2.55,h:0.85,fontFace:F,fontSize:14,color:TXT,align:"center",valign:"top",isTextBox:true});
});
s.addText("Цель: лёгкий инструмент приёма заявок с проверкой данных, статусами, поиском и историей.",{x:0.6,y:3.5,w:8.8,h:1.0,fontFace:F,fontSize:20,color:TXT,isTextBox:true});
s.addText("Источник цифр: BES.media (заседание фракции Respublica)",{x:0.6,y:4.75,w:8.8,h:0.3,fontFace:F,fontSize:11,color:GREY,isTextBox:true,margin:0});

// 3 Аналоги
s = base("Анализ аналогов","eGov.kz, UniDorm 2.0, Platonus — крупные решения; вузу нужен простой внутренний учёт.");
const hd={bold:true,color:"FFFFFF",fill:{color:NAVY},fontFace:F,fontSize:14};
const cell=(t,o={})=>({text:t,options:Object.assign({fontFace:F,fontSize:13,color:TXT,valign:"middle"},o)});
s.addTable([
 [{text:"Аналог",options:hd},{text:"Что делает",options:hd},{text:"Ограничение",options:hd}],
 [cell("eGov.kz",{bold:true}),cell("Онлайн-заявка, отслеживание статуса"),cell("Госсервис, нет внутреннего учёта вуза")],
 [cell("UniDorm 2.0",{bold:true}),cell("Выбор комнат, очередь"),cell("Масштабная платформа")],
 [cell("Platonus",{bold:true}),cell("Кабинеты студентов и сотрудников"),cell("Универсальная система")],
 [cell("Ручной учёт",{bold:true}),cell("Приём по очередности и конкурсу"),cell("Нет проверки, поиска, истории")],
],{x:0.6,y:1.2,w:8.8,colW:[1.9,3.5,3.4],rowH:0.6,border:{type:"solid",color:"C9D3DC",pt:1}});
s.addText("Вывод: нужен лёгкий инструмент с проверкой ввода и контролем статусов.",{x:0.6,y:4.3,w:8.8,h:0.6,fontFace:F,fontSize:18,bold:true,color:NAVY,isTextBox:true});

// 4 Требования
s = base("Требования","6 функциональных и 4 нефункциональных требования; критерии приёмки зафиксированы в docs/.");
s.addText("Функциональные",{x:0.6,y:1.1,w:4.2,h:0.4,fontFace:F,fontSize:20,bold:true,color:ACC,isTextBox:true,margin:0});
bullets(s,["Подача заявки с проверкой полей","Список и сортировка","Поиск и фильтры","Статусы по правилам","История, статистика","Запрет дубля активной заявки"],{x:0.6,y:1.55,w:4.2,h:3.5,fontSize:16});
s.addText("Нефункциональные",{x:5.2,y:1.1,w:4.2,h:0.4,fontFace:F,fontSize:20,bold:true,color:ACC,isTextBox:true,margin:0});
bullets(s,["Python 3.8+, без зависимостей","Сохранность данных (JSON)","Понятные сообщения об ошибках","Устойчивость к пустому вводу"],{x:5.2,y:1.55,w:4.2,h:3.5,fontSize:16});

// 5 ЖЦ и архитектура
s = base("Модель ЖЦ и архитектура","Выбрана инкрементная модель: проект небольшой, каждый инкремент проверяется тестами.");
const steps=["Модель и\nвалидация","Добавление,\nпоиск, сортировка","Статусы,\nистория","JSON и\nменю","Тесты и\nдефекты"];
steps.forEach((t,i)=>{const x=0.5+i*1.85;
 s.addShape(p.ShapeType.roundRect,{x,y:1.2,w:1.65,h:1.0,fill:{color:i%2?ACC:NAVY},line:{color:i%2?ACC:NAVY},rectRadius:0.08});
 s.addText(t,{x,y:1.2,w:1.65,h:1.0,fontFace:F,fontSize:13,bold:true,color:"FFFFFF",align:"center",valign:"middle",isTextBox:true});});
s.addText("Инкрементная модель: 5 инкрементов",{x:0.5,y:2.3,w:9,h:0.35,fontFace:F,fontSize:13,color:GREY,isTextBox:true,margin:0});
s.addText("Архитектура",{x:0.6,y:2.9,w:8.8,h:0.4,fontFace:F,fontSize:20,bold:true,color:ACC,isTextBox:true,margin:0});
s.addText("Валидаторы → Application / Status → DormRegistry → JSON → консольное меню",{x:0.6,y:3.35,w:8.8,h:0.5,fontFace:F,fontSize:18,color:TXT,isTextBox:true,margin:0});
s.addText("Статусы: Новая → На рассмотрении → Одобрена / Отклонена",{x:0.6,y:4.0,w:8.8,h:0.5,fontFace:F,fontSize:18,color:TXT,isTextBox:true,margin:0});

// 6 Алгоритмы
s = base("Алгоритмы и структуры данных","Связь с лекциями: циклы, функции, коллекции, строки, структуры и перечисления.");
bullets(s,["dataclass Application, Enum Status (лекция 8)","Словарь допустимых переходов TRANSITIONS","Регулярные выражения для ФИО и телефона (лекция 7)","Цикл повторного ввода и главное меню (лекция 4)","Сортировка по ключу, поиск и фильтр по списку (лекции 5–6)"]);

// 7 Интерфейс
s = base("Интерфейс и демонстрация","Показать живой запуск: подача заявки с ошибкой, смена статуса, недопустимый переход, поиск.");
s.addImage({path:"../screenshots/01_podacha_zayavki.png",x:0.5,y:1.1,w:4.9,h:3.78});
s.addImage({path:"../screenshots/03_status_poisk.png",x:5.7,y:1.1,w:3.12,h:3.78});
s.addText("Подача заявки с повторным вводом и смена статусов (консоль)",{x:0.5,y:4.9,w:9,h:0.3,fontFace:F,fontSize:11,color:GREY,isTextBox:true,margin:0});

// 8 Тесты
s = base("Результаты тестирования","16 автотестов: основные, ошибочный ввод, граничные, регрессионные. Найдено и исправлено 4 дефекта.");
[["16","тестов"],["16","PASS"],["4","дефекта исправлено"]].forEach((c,i)=>{const x=0.6+i*3.05;
 s.addShape(p.ShapeType.roundRect,{x,y:1.2,w:2.85,h:1.5,fill:{color:SOFT},line:{color:SOFT},rectRadius:0.1});
 s.addText(c[0],{x,y:1.25,w:2.85,h:0.9,fontFace:F,fontSize:44,bold:true,color:ACC,align:"center",isTextBox:true});
 s.addText(c[1],{x,y:2.1,w:2.85,h:0.5,fontFace:F,fontSize:16,color:TXT,align:"center",isTextBox:true});});
bullets(s,["5 основных, 4 ошибочного ввода, 3 граничных, 4 регрессионных","D1: ФИО из дефисов · D2: нелатинские цифры · D3: курс True · D4: падение при Ctrl+D","Протокол: tests/protocol.md; запуск: python tests/run_protocol.py"],{y:3.0,h:2.1,fontSize:16});

// 9 GitHub
s = base("GitHub, README и вклад автора","Проект выполнен индивидуально: анализ, код, тесты, документация, презентация.");
bullets(s,["README: анализ, аналоги и источники, запуск, скриншоты, протокол тестов","Структура: src/, tests/, docs/, screenshots/, presentation/","История коммитов по инкрементам","Вклад автора: 100% (индивидуальный проект)"]);

// 10 Выводы
s = base("Выводы и перспективы","Итог: рабочее приложение с проверкой данных, жизненным циклом заявки и протоколом тестов.");
bullets(s,["Реализовано приложение приёма и обработки заявок на общежитие","Применены циклы, функции, коллекции, строки, dataclass и Enum","Проверено 16 тестами, найденные дефекты исправлены","Развитие: веб-интерфейс, роли пользователей, база данных, учёт комнат"]);
p.writeFile({fileName:"presentation.pptx"}).then(()=>console.log("ok"));
