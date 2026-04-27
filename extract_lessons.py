import sys
import os
import json
import re
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document

# Mapping: LESSONS array order -> DOCX file paths
# Module 0: Основы знаний (22 lessons)
# Module 1: Ручные техники (10 lessons)
# Module 2: Аппаратные методики (19 lessons)
# Module 3: Косметология (19 lessons)
# Module 4: Маски и обёртывания (5 lessons)

base = r"C:\Users\Madiyar\Desktop\клод проекты\Атырау\уроки"

lesson_files = [
    # Module 0: Основы знаний (22)
    os.path.join(base, "Основы знаний", "Целлюлит.docx"),
    os.path.join(base, "Основы знаний", "Жировая ткань.docx"),
    os.path.join(base, "Основы знаний", "Лимфатическая система.docx"),
    os.path.join(base, "Основы знаний", "Составление протоколов.docx"),
    os.path.join(base, "Основы знаний", "Класификация методик.docx"),
    os.path.join(base, "Основы знаний", "Этика и психология.docx"),
    os.path.join(base, "Основы знаний", "Дряблая кожа.docx"),
    os.path.join(base, "Основы знаний", "Синяки.docx"),
    os.path.join(base, "Основы знаний", "ЛИпидема.docx"),
    os.path.join(base, "Основы знаний", "Клиенты после липосакции.docx"),
    os.path.join(base, "Основы знаний", "Липолитические методики.docx"),
    os.path.join(base, "Основы знаний", "Массаж при диабете.docx"),
    os.path.join(base, "Основы знаний", "Работа с гипертониками.docx"),
    os.path.join(base, "Основы знаний", "Работа с гипотериозом.docx"),
    os.path.join(base, "Основы знаний", "Работа с инсулинорезистентностьь.docx"),
    os.path.join(base, "Основы знаний", "Работа при миоме.docx"),
    os.path.join(base, "Основы знаний", "Работа при наличии камней.docx"),
    os.path.join(base, "Основы знаний", "Работа при узлах в щитовкидке.docx"),
    os.path.join(base, "Основы знаний", "Работа с мужчинами.docx"),
    os.path.join(base, "Основы знаний", "Работа с фитнес-бикини.docx"),
    os.path.join(base, "Основы знаний", "Запоры.docx"),
    os.path.join(base, "Основы знаний", "Отслеживание динамики снижения веса.docx"),
    # Module 1: Ручные техники (10) — order matches LESSONS array
    os.path.join(base, "Ручные техники", "Антицеллюлитный ручной массаж.docx"),
    os.path.join(base, "Ручные техники", "Моделирующий массаж.docx"),
    os.path.join(base, "Ручные техники", "МЕДОВЫЙ МАССАЖ.docx"),
    os.path.join(base, "Ручные техники", "сАМУРАЙСКИЙ МАССАЖ.docx"),
    os.path.join(base, "Ручные техники", "Бразильская выкатка.docx"),
    os.path.join(base, "Ручные техники", "ИММТ.docx"),
    os.path.join(base, "Ручные техники", "Блэйд.docx"),
    os.path.join(base, "Ручные техники", "Золотое Сечение.docx"),
    os.path.join(base, "Ручные техники", "Хлопковы массаж.docx"),
    os.path.join(base, "Ручные техники", "Скрабирвание.docx"),
    # Module 2: Аппаратные методики (19)
    os.path.join(base, "Аппаратка", "LPG массаж.docx"),
    os.path.join(base, "Аппаратка", "Вакуумный массаж.docx"),
    os.path.join(base, "Аппаратка", "Вакуумная Кавитация.docx"),
    os.path.join(base, "Аппаратка", "Прессотерапия.docx"),
    os.path.join(base, "Аппаратка", "Миостимуляция.docx"),
    os.path.join(base, "Аппаратка", "Криолиполиз.docx"),
    os.path.join(base, "Аппаратка", "Индиба.docx"),
    os.path.join(base, "Аппаратка", "Биофотон.docx"),
    os.path.join(base, "Аппаратка", "Квантовый Массаж БЭМ.docx"),
    os.path.join(base, "Аппаратка", "Магнэтик Про.docx"),
    os.path.join(base, "Аппаратка", "Impuls.docx"),
    os.path.join(base, "Аппаратка", "3D моделирование.docx"),
    os.path.join(base, "Аппаратка", "Ролл Шейпер.docx"),
    os.path.join(base, "Аппаратка", "Турбо массаж.docx"),
    os.path.join(base, "Аппаратка", "Биботинг.docx"),
    os.path.join(base, "Аппаратка", "Кедровая бочка.docx"),
    os.path.join(base, "Аппаратка", "Сауна.docx"),
    os.path.join(base, "Аппаратка", "Термо-одеяло.docx"),
    os.path.join(base, "Аппаратка", "Трон Кегеля.docx"),
    # Module 3: Косметология (19)
    os.path.join(base, "Косметология", "Ручная пластика лица.docx"),
    os.path.join(base, "Косметология", "Вакуумный массаж лица.docx"),
    os.path.join(base, "Косметология", "Медовый массаж лица.docx"),
    os.path.join(base, "Косметология", "БМС.docx"),
    os.path.join(base, "Косметология", "ЛПджи лицо.docx"),
    os.path.join(base, "Косметология", "Бэм лицо.docx"),
    os.path.join(base, "Косметология", "Индиба лицо.docx"),
    os.path.join(base, "Косметология", "Миостимуляция лицо.docx"),
    os.path.join(base, "Косметология", "2Д моделирование.docx"),
    os.path.join(base, "Косметология", "Гидропилинг.docx"),
    os.path.join(base, "Косметология", "Карбоновый пилинг.docx"),
    os.path.join(base, "Косметология", "Пилинги.docx"),
    os.path.join(base, "Косметология", "Микроигольчатый.docx"),
    os.path.join(base, "Косметология", "Озон.docx"),
    os.path.join(base, "Косметология", "Оксиженео.docx"),
    os.path.join(base, "Косметология", "Холодная плазма", "Холодная Плазма.docx"),
    os.path.join(base, "Косметология", "Тэрмаж.docx"),
    os.path.join(base, "Косметология", "Лазерная Эпиляция.docx"),
    os.path.join(base, "Косметология", "Удаление татуажа.docx"),
    # Module 4: Маски и обёртывания (5)
    os.path.join(base, "Маски и обертывания", "Общая информация по маскам.docx"),
    os.path.join(base, "Маски и обертывания", "БАНДАЖНОЕ ОБЕРТОВАНИЕ.docx"),
    os.path.join(base, "Маски и обертывания", "Водорослевое обертование.docx"),
    os.path.join(base, "Маски и обертывания", "Гипсомоделирование.docx"),
    os.path.join(base, "Маски и обертывания", "Грязевые маски.docx"),
]

def docx_to_html(filepath):
    """Convert DOCX paragraphs to simple HTML"""
    try:
        doc = Document(filepath)
    except Exception as e:
        return f"<p>Ошибка загрузки: {e}</p>"

    html_parts = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Escape HTML
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        # Detect headings
        style = para.style.name.lower() if para.style else ''

        if 'heading 1' in style or 'title' in style:
            html_parts.append(f'<h3>{text}</h3>')
        elif 'heading 2' in style:
            html_parts.append(f'<h4>{text}</h4>')
        elif 'heading 3' in style or 'heading 4' in style:
            html_parts.append(f'<h5>{text}</h5>')
        elif 'list' in style or text.startswith(('•', '-', '–', '—', '·')):
            # Clean bullet prefix
            clean = re.sub(r'^[•\-–—·]\s*', '', text)
            html_parts.append(f'<li>{clean}</li>')
        else:
            # Check if text is all caps or short = likely a section header
            if len(text) < 80 and text == text.upper() and len(text) > 3:
                html_parts.append(f'<h4>{text}</h4>')
            else:
                # Check for bold runs - if entire paragraph is bold, make it a subheading
                all_bold = all(run.bold for run in para.runs if run.text.strip()) if para.runs else False
                if all_bold and len(text) < 100:
                    html_parts.append(f'<h5>{text}</h5>')
                else:
                    # Build paragraph with inline formatting
                    formatted = ''
                    for run in para.runs:
                        t = run.text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        if not t:
                            continue
                        if run.bold and run.italic:
                            formatted += f'<strong><em>{t}</em></strong>'
                        elif run.bold:
                            formatted += f'<strong>{t}</strong>'
                        elif run.italic:
                            formatted += f'<em>{t}</em>'
                        else:
                            formatted += t
                    if not formatted:
                        formatted = text
                    html_parts.append(f'<p>{formatted}</p>')

    # Wrap consecutive <li> in <ul>
    result = []
    in_list = False
    for part in html_parts:
        if part.startswith('<li>'):
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(part)
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(part)
    if in_list:
        result.append('</ul>')

    return '\n'.join(result)

# Extract all lessons
results = []
for i, fpath in enumerate(lesson_files):
    if os.path.exists(fpath):
        html = docx_to_html(fpath)
        results.append(html)
        print(f"[{i+1}/{len(lesson_files)}] OK: {os.path.basename(fpath)} ({len(html)} chars)")
    else:
        results.append(f"<p>Файл не найден: {os.path.basename(fpath)}</p>")
        print(f"[{i+1}/{len(lesson_files)}] MISSING: {fpath}")

# Save as JSON for easy loading
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lesson_contents.json")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nDone! {len(results)} lessons extracted to {output_path}")
print(f"Total size: {sum(len(r) for r in results)} chars")
