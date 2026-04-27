# M&M Fabrica — экосистема для бьюти-бизнеса

Репозиторий с продуктами M&M Fabrica: мобильное приложение, презентации для клиник и платформа обучения стажёров **M&M Academy**.

> Брендинг единый: жёлтый `#FFE600` + розовый `#FF2D7B`, шрифты Unbounded (заголовки) и Inter / Space Grotesk (текст).

---

## Структура репозитория

| Артефакт | Что это |
|---|---|
| [`upload_academy/index.html`](upload_academy/index.html) | **M&M Academy** — single-page платформа обучения стажёров (Firestore + localStorage). Активная разработка. Боевой URL: [academy.mmfabrica.com](https://academy.mmfabrica.com) |
| [`index.html`](index.html), [`mmfabrica-app.html`](mmfabrica-app.html) | Мобильное PWA-приложение M&M Fabrica (1113 строк, splash → home → catalogue) |
| [`presentation.html`](presentation.html) | Общая презентация M&M Fabrica |
| [`aspersio-presentation.html`](aspersio-presentation.html) | Презентация **Aspersio × Нейрон** для клиники в Актау |
| [`уроки/`](уроки/) | Исходные `.docx` уроков по 6 разделам: Аппаратка, Косметология, Маски и обертывания, Основы знаний, Противопоказания, Ручные техники |
| [`новый файлы/`](новый%20файлы/) | Регламенты, идеология, скрипты, 5 категорий мастеров |
| [`biblia-mastera.pdf`](biblia-mastera.pdf) | «Библия Мастера по коррекции фигуры» — раздаточный PDF |
| [`screenshots_mmfabrica/`](screenshots_mmfabrica/) | Скриншоты для маркетинга |

### Python-утилиты пайплайна контента

- [`extract_lessons.py`](extract_lessons.py) — парсит `.docx` из `уроки/` → `lesson_contents.json`
- [`read_new_files.py`](read_new_files.py) — парсит `.docx` из `новый файлы/` → `new_lesson_contents.json`
- [`embed_content.py`](embed_content.py) — встраивает JSON-контент в `LESSON_CONTENTS` массив внутри `upload_academy/index.html`
- [`add_new_modules.py`](add_new_modules.py) — добавление новых модулей в структуру

---

## M&M Academy — техническое описание

Главный рабочий артефакт сейчас — `upload_academy/index.html` (~13 200 строк, ~1.5 МБ).

### Стек

- Один HTML, без сборки.
- Firebase Firestore (compat 10.7.1) — облачная синхронизация прогресса между устройствами.
- `localStorage` (`mmAcademyInterns_v1`) — мгновенный кеш, работает офлайн.

### Контент-модель

| Размерность | Значение |
|---|---|
| Уроки | 86 |
| Модули | 7 |
| Категории мастеров | 5 |

Распределение уроков по модулям: `6 / 5 / 22 / 10 / 19 / 19 / 5 = 86`.

| # | Модуль | Уроков |
|---|---|---|
| 0 | Стандарты и сервис M&M | 6 |
| 1 | Карьерный путь M&M | 5 |
| 2 | Основы знаний | 22 |
| 3 | Ручные техники | 10 |
| 4 | Аппаратные методики | 19 |
| 5 | Косметология | 19 |
| 6 | Маски и обёртывания | 5 |

### Экраны

`loginScreen` → `dashScreen` → `lessonScreen` / `profileScreen` / `ratingScreen` / `adminScreen`.

### Роли

- **Стажёр** — вход по имени + фамилии + коду доступа (выдаёт админ).
- **Админ** — логин `admin`, пароль `mmfabrica2025`. Управляет стажёрами, доступом к категориям, оценками.

### Архитектура синхронизации

```
[ UI ]
  ↓
[ INTERNS массив (in-memory) ]
  ↓ persist()
[ localStorage mmAcademyInterns_v1 ] ←→ [ Firestore /mmAcademy/interns ]
        ↑                                       ↑
   loadPersisted()                        cloudLoad() / onSnapshot
```

При каждой мутации (`addNewIntern`, `deleteIntern`, `setCategoryAccess`, `submitAssignment`, `saveGrades`, `retakeAssignment`, `confirmRedeem`, `doLogout`) вызывается `persist()`, которая синхронно пишет в `localStorage` и асинхронно дублирует в Firestore.

Защита от гонок:
- `cloudInitialLoadDone` — пока облако не загрузилось, `cloudPush` не пишет (иначе можно затереть облако пустым массивом).
- В `cloudLoad`/`cloudSubscribe` пустой `data.list` от облака **не затирает** локальные данные, если они есть — наоборот, локальное пушится в облако.
- `cloudLastPushedHash` — дедуп: если payload не изменился, запись пропускается (экономит квоту Spark Free tier — 20 K writes/день).
- `purgeDemoInterns` запускается одноразово, через флаг `mmAcademyPurgedDemo_v1`, чтобы случайно не удалить реального стажёра, чьё имя/код совпали с демо.

---

## Firebase

| Параметр | Значение |
|---|---|
| Project ID | `mmacademy-eb213` |
| Project number | `860820609983` |
| Web App | `MMAcademy Web` (App ID `1:860820609983:web:5503353278fbc1365bdf0a`) |
| Database location | `europe-central2` |
| Тариф | Spark Free (no-cost) |

### Security Rules

В Firestore Console → Rules:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /mmAcademy/interns {
      allow read, write: if true;
    }
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

Открыт **только** документ `mmAcademy/interns`, всё остальное закрыто.

### Защита API-ключа

В Google Cloud Console → APIs & Services → Credentials → Browser key (auto created by Firebase) → **Application restrictions** → **Websites**: добавлен `academy.mmfabrica.com`. С других доменов ключ не работает.

---

## Хостинг (Plesk)

| Домен | Что лежит |
|---|---|
| `mmfabrica.com` | Корневой сайт |
| `academy.mmfabrica.com` | M&M Academy (docroot `httpdocs/`, файл `index.html` копируется из `upload_academy/index.html`) |

Заливка обновлений Academy:
1. Открыть Plesk → **academy.mmfabrica.com** → **Files** → `httpdocs/`.
2. Удалить старый `index.html`.
3. Загрузить свежий `upload_academy/index.html` (~1.5 МБ).
4. Открыть `https://academy.mmfabrica.com` в инкогнито, F12 → Console — должны появиться логи `[cloud] Firebase инициализирован` и зелёный бейдж «✅ Облако подключено».

---

## Workflow добавления новых уроков

1. Положить новый `.docx` в соответствующий подкаталог `уроки/<раздел>/` (или в `новый файлы/`).
2. Запустить парсер:
   ```bash
   python extract_lessons.py        # для уроки/
   python read_new_files.py         # для новый файлы/
   ```
3. Запустить встройку:
   ```bash
   python embed_content.py
   ```
4. Открыть `upload_academy/index.html` и убедиться, что массив `LESSON_CONTENTS` обновился. Проверить, что `LESSONS` и `CATEGORY_MAP` (длина 86) синхронны с числом уроков.
5. Залить обновлённый HTML в Plesk.

Не редактировать `LESSON_CONTENTS` в HTML вручную — всегда через JSON + `embed_content.py`.

---

## Git и деплой

Два remote:
- `origin` → [github.com/madikabdulovrec-cpu/Aktau](https://github.com/madikabdulovrec-cpu/Aktau)
- `mm` → [github.com/madikabdulovrec-cpu/M-M](https://github.com/madikabdulovrec-cpu/M-M) (с GitHub Pages workflow)

После значимых изменений — пушить в **оба**:
```bash
git push origin main
git push mm main
```

---

## Известные ограничения / TODO

- [ ] UX: блокировать кнопки «Войти» и «Добавить стажёра» пока `cloudInitialLoadDone === false` (сейчас можно нажать раньше, чем облако подгрузится → видишь пустой список).
- [ ] Перенести `LESSON_CONTENTS` из inline-массива в отдельный JSON-файл — HTML слишком большой для редактирования.
- [ ] Реализовать `QUIZZES` (массив сейчас пустой).
- [ ] Авто-деплой в Plesk через GitHub Actions (сейчас руками через файловый менеджер).
