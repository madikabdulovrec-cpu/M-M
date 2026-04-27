"""
Script to add 2 new modules (11 lessons) to M&M Academy platform.
- Module 0: Стандарты и сервис M&M (6 lessons)
- Module 1: Карьерный путь M&M (5 lessons)
- Existing modules shift from 0-4 to 2-6
"""
import sys, os, json, re
sys.stdout.reconfigure(encoding='utf-8')
from docx import Document

base = r"C:\Users\Madiyar\Desktop\клод проекты\Атырау\новый файлы"

# New files in order matching new lessons
new_files = [
    # Module 0: Стандарты и сервис (6 lessons)
    os.path.join(base, "ДНК массажиста.docx"),
    os.path.join(base, "Культура общения.docx"),
    os.path.join(base, "Правильное общение с клиентами .docx"),
    os.path.join(base, "Регламент внешнего вида мастера.docx"),
    os.path.join(base, "Регламент и правила сервиса.docx"),
    os.path.join(base, "Скрипт встреча клиента.docx"),
    # Module 1: Карьерный путь (5 lessons)
    os.path.join(base, "1 категория.docx"),
    os.path.join(base, "2 категория.docx"),
    os.path.join(base, "3 категория.docx"),
    os.path.join(base, "4 категория.docx"),
    os.path.join(base, "5 категория.docx"),
]

def docx_to_html(filepath):
    try:
        doc = Document(filepath)
    except Exception as e:
        return f"<p>Ошибка загрузки: {e}</p>"
    html_parts = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        style = para.style.name.lower() if para.style else ''
        if 'heading 1' in style or 'title' in style:
            html_parts.append(f'<h3>{text}</h3>')
        elif 'heading 2' in style:
            html_parts.append(f'<h4>{text}</h4>')
        elif 'heading 3' in style or 'heading 4' in style:
            html_parts.append(f'<h5>{text}</h5>')
        elif 'list' in style or text.startswith(('•', '-', '–', '—', '·')):
            clean = re.sub(r'^[•\-–—·]\s*', '', text)
            html_parts.append(f'<li>{clean}</li>')
        else:
            if len(text) < 80 and text == text.upper() and len(text) > 3:
                html_parts.append(f'<h4>{text}</h4>')
            else:
                all_bold = all(run.bold for run in para.runs if run.text.strip()) if para.runs else False
                if all_bold and len(text) < 100:
                    html_parts.append(f'<h5>{text}</h5>')
                else:
                    formatted = ''
                    for run in para.runs:
                        t = run.text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        if not t: continue
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

# Extract HTML content from all 11 new files
new_contents = []
for i, fpath in enumerate(new_files):
    html = docx_to_html(fpath)
    new_contents.append(html)
    print(f"[{i+1}/11] OK: {os.path.basename(fpath)} ({len(html)} chars)")

# Save new contents
with open(r"C:\Users\Madiyar\Desktop\клод проекты\Атырау\new_lesson_contents.json", 'w', encoding='utf-8') as f:
    json.dump(new_contents, f, ensure_ascii=False, indent=2)

print(f"\nExtracted {len(new_contents)} new lessons, total {sum(len(c) for c in new_contents)} chars")

# Now modify the HTML file
html_path = r"C:\Users\Madiyar\Desktop\клод проекты\Атырау\index.html.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace MODULES array
old_modules = """const MODULES = [
  { id:'basics', title:'Основы знаний', icon:'&#128218;', color:'var(--blue)', desc:'Теоретический фундамент: анатомия, физиология, работа с клиентами' },
  { id:'manual', title:'Ручные техники', icon:'&#9995;', color:'var(--pink)', desc:'Мануальные методики коррекции фигуры' },
  { id:'apparatus', title:'Аппаратные методики', icon:'&#9881;', color:'var(--green)', desc:'Современные аппаратные технологии' },
  { id:'cosmetology', title:'Косметология', icon:'&#10024;', color:'#9c27b0', desc:'Процедуры для лица и эстетика' },
  { id:'wraps', title:'Маски и обёртывания', icon:'&#127807;', color:'#ff9800', desc:'Обёртывания, маски, уход за кожей тела' }
];"""

new_modules = """const MODULES = [
  { id:'standards', title:'Стандарты и сервис M&M', icon:'&#128142;', color:'var(--pink)', desc:'Корпоративная культура, сервис, общение с клиентами и коллегами' },
  { id:'career', title:'Карьерный путь M&M', icon:'&#128200;', color:'var(--yellow)', desc:'Система категорий: от новичка до ведущего технолога' },
  { id:'basics', title:'Основы знаний', icon:'&#128218;', color:'var(--blue)', desc:'Теоретический фундамент: анатомия, физиология, работа с клиентами' },
  { id:'manual', title:'Ручные техники', icon:'&#9995;', color:'#e91e63', desc:'Мануальные методики коррекции фигуры' },
  { id:'apparatus', title:'Аппаратные методики', icon:'&#9881;', color:'var(--green)', desc:'Современные аппаратные технологии' },
  { id:'cosmetology', title:'Косметология', icon:'&#10024;', color:'#9c27b0', desc:'Процедуры для лица и эстетика' },
  { id:'wraps', title:'Маски и обёртывания', icon:'&#127807;', color:'#ff9800', desc:'Обёртывания, маски, уход за кожей тела' }
];"""

html = html.replace(old_modules, new_modules)
print("Replaced MODULES array")

# 2. Add new lessons at beginning of LESSONS array and shift module indices
new_lessons_js = """  // === Module 0: Стандарты и сервис M&M (6 lessons) ===
  { module:0, title:'ДНК массажиста', desc:'Философия профессии: любовь к делу, эмпатия, интуиция и саморазвитие', task:'Опишите 5 ключевых качеств идеального специалиста по коррекции фигуры и объясните, почему каждое из них важно.' },
  { module:0, title:'Культура общения в компании', desc:'Правила внутренней коммуникации: WhatsApp, критика, обратная связь', task:'Напишите пример ЗРС-сообщения руководителю о возникшей проблеме с оборудованием.' },
  { module:0, title:'Правильное общение с клиентами', desc:'Золотое правило тишины, запрещённые темы, 3 обязательных вопроса', task:'Перечислите 3 обязательных вопроса клиенту перед процедурой и объясните, почему каждый из них критически важен.' },
  { module:0, title:'Регламент внешнего вида', desc:'Стандарты формы, макияжа, маникюра и гигиены мастера', task:'Составьте чек-лист из 10 пунктов для проверки внешнего вида перед сменой.' },
  { module:0, title:'Регламент и правила сервиса', desc:'Золотые правила сервиса M&M: приветствие, забота, субординация', task:'Опишите идеальный путь клиента от входа до выхода из центра с точки зрения сервиса.' },
  { module:0, title:'Скрипт встречи клиента', desc:'Пошаговый сценарий первой встречи: замеры, фото, экскурсия', task:'Напишите свой скрипт приветствия и проведения экскурсии для нового клиента.' },

  // === Module 1: Карьерный путь M&M (5 lessons) ===
  { module:1, title:'Категория 1 — Новичок', desc:'Стажировка, адаптация, базовые аппаратные процедуры (200 000 ₸)', task:'Опишите, что должен сделать стажёр в первый день и какие процедуры входят в 1 категорию.' },
  { module:1, title:'Категория 2 — Вакуумный специалист', desc:'LPG, вакуумный массаж, Золотое Сечение (300 000 ₸)', task:'Какие условия нужно выполнить для перехода из 1 во 2 категорию? Опишите подробно.' },
  { module:1, title:'Категория 3 — Эксперт интенсивных методик', desc:'Турбо, Торнадо, Биофотон — работа с телом в глубину (350 000 ₸)', task:'Почему для 3 категории требуется минимум 100 положительных отзывов? Какие методики открываются?' },
  { module:1, title:'Категория 4 — Специалист ручных методик', desc:'Ручная пластика, лимфо/липокоррекция, самурайский массаж (400 000 ₸)', task:'Чем отличается путь внешнего кандидата в 4 категорию от внутреннего повышения?' },
  { module:1, title:'Категория 5 — Ведущий технолог', desc:'Вершина карьеры: наставничество, стандарты, лидерство (450 000 ₸)', task:'Опишите все обязанности ведущего технолога и почему эта роль — «сердце компании».' },

"""

# Find "const LESSONS = [" and insert new lessons after it
old_lessons_start = "const LESSONS = [\n  // === Module 0: Основы знаний"
new_lessons_start = "const LESSONS = [\n" + new_lessons_js + "  // === Module 2: Основы знаний"
html = html.replace(old_lessons_start, new_lessons_start)
print("Added 11 new lessons to LESSONS array")

# 3. Shift existing module indices: 0->2, 1->3, 2->4, 3->5, 4->6
# In the LESSONS array comments and module: values
html = html.replace("// === Module 0: Основы знаний", "// === Module 2: Основы знаний")
html = html.replace("// === Module 1: Ручные техники", "// === Module 3: Ручные техники")
html = html.replace("// === Module 2: Аппаратные методики", "// === Module 4: Аппаратные методики")
html = html.replace("// === Module 3: Косметология", "// === Module 5: Косметология")
html = html.replace("// === Module 4: Маски", "// === Module 6: Маски")

# Now shift all module:N values in existing lessons
# We need to be careful to only change within the LESSONS array
# Find the region of existing lessons and replace module values
import re as regex

# Replace module:0 through module:4 with module:2 through module:6
# But only for the OLD lessons (after our new ones)
# Strategy: find our marker comments and replace within those sections
for old_m, new_m in [(0, 2), (1, 3), (2, 4), (3, 5), (4, 6)]:
    # Match "module:N," where N is old value, but only in lesson objects (not in our new module:0 and module:1)
    # We'll use the section comments as anchors
    old_comment = f"// === Module {new_m}:"  # already renamed
    if old_m == 0:
        section_marker = "Module 2: Основы"
    elif old_m == 1:
        section_marker = "Module 3: Ручные"
    elif old_m == 2:
        section_marker = "Module 4: Аппаратные"
    elif old_m == 3:
        section_marker = "Module 5: Косметология"
    elif old_m == 4:
        section_marker = "Module 6: Маски"

    # Find the section and replace module:old with module:new within it
    # Simple approach: replace "{ module:OLD," with "{ module:NEW," globally
    # This works because our new lessons already have correct module values
    pass

# Actually simpler: since we already inserted new lessons with module:0 and module:1,
# and old lessons still have module:0 through module:4,
# we need to shift OLD module values. Do it in reverse order to avoid double-shifting.
for old_m in [4, 3, 2, 1, 0]:
    new_m = old_m + 2
    # Count occurrences first
    old_pattern = f"{{ module:{old_m}, title:'"
    new_pattern = f"{{ module:{new_m}, title:'"
    count = html.count(old_pattern)
    html = html.replace(old_pattern, new_pattern)
    print(f"  module:{old_m} -> module:{new_m} ({count} replacements)")

# But we just broke our NEW module:0 and module:1 lessons! Fix them back.
# Our new module:0 titles: ДНК массажиста, Культура общения, etc.
# They got shifted to module:2. Fix:
for title in ['ДНК массажиста', 'Культура общения в компании', 'Правильное общение с клиентами',
              'Регламент внешнего вида', 'Регламент и правила сервиса', 'Скрипт встречи клиента']:
    html = html.replace(f"{{ module:2, title:'{title}'", f"{{ module:0, title:'{title}'")

for title in ['Категория 1 — Новичок', 'Категория 2 — Вакуумный специалист',
              'Категория 3 — Эксперт интенсивных методик', 'Категория 4 — Специалист ручных методик',
              'Категория 5 — Ведущий технолог']:
    html = html.replace(f"{{ module:3, title:'{title}'", f"{{ module:1, title:'{title}'")

print("Fixed module indices for new lessons")

# 4. Prepend new content to LESSON_CONTENTS array
old_lc_start = "const LESSON_CONTENTS = [\n"
new_lc_items = ""
for content in new_contents:
    escaped = content.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    new_lc_items += f"  `{escaped}`,\n"
new_lc_start = "const LESSON_CONTENTS = [\n" + new_lc_items
html = html.replace(old_lc_start, new_lc_start)
print(f"Prepended {len(new_contents)} items to LESSON_CONTENTS")

# 5. Update welcome modal text
html = html.replace("5 модулей, 75 уроков", "7 модулей, 86 уроков")
html = html.replace("75 уроков", "86 уроков")
# Update stat default values
html = html.replace('0/75', '0/86')

print("Updated welcome text and stats")

# Write back
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! File size: {len(html)} chars")
print("New structure: 7 modules, 86 lessons")
