import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document

base = r"C:\Users\Madiyar\Desktop\клод проекты\Атырау\новый файлы"

files = [
    "1 категория.docx",
    "2 категория.docx",
    "3 категория.docx",
    "4 категория.docx",
    "5 категория.docx",
    "ДНК массажиста.docx",
    "Идеология компании \"M&M\".docx",
    "Культура общения.docx",
    "Правильное общение с клиентами .docx",
    "Регламент внешнего вида мастера.docx",
    "Регламент и правила сервиса.docx",
    "Скрипт встреча клиента.docx",
]

for fname in files:
    fpath = os.path.join(base, fname)
    print(f"\n{'='*80}")
    print(f"FILE: {fname}")
    print(f"{'='*80}")
    try:
        doc = Document(fpath)
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                print(text)
    except Exception as e:
        print(f"ERROR: {e}")
