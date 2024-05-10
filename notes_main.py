from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout
import os
import json

if not os.path.exists('db.json'):
    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump({
            'Добро пожаловать': {
                'текст': 'Это самое лучшее приложение для заметок в мире',
                'теги': ['welcome', 'инструкция']
            }
        }, f, ensure_ascii=False, indent=4)

app = QApplication([])
mw = QWidget()
mw.setWindowTitle('SmartNotes')

# ! column 1
field_text = QTextEdit()
# ! column 2
list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')
button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')

list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')
field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег...')
button_tag_add = QPushButton('Добавить тег')
button_tag_del = QPushButton('Удалить тег')
button_tag_search = QPushButton('Искать по тегу')

status_bar = QLabel('status_bar')

col1 = QVBoxLayout()
col1.addWidget(field_text)
col1.addWidget(status_bar)
col2 = QVBoxLayout()
col2.addWidget(list_notes_label)
col2.addWidget(list_notes)
row1 = QHBoxLayout()
row1.addWidget(button_note_create)
row1.addWidget(button_note_del)
col2.addLayout(row1)
col2.addWidget(button_note_save)

col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(field_tag)
row2 = QHBoxLayout()
row2.addWidget(button_tag_add)
row2.addWidget(button_tag_del)
col2.addLayout(row2)
col2.addWidget(button_tag_search)

layout_notes = QHBoxLayout()
layout_notes.addLayout(col1, 60)
layout_notes.addLayout(col2, 40)

def add_note():
    notes_name, ok = QInputDialog.getText(mw, 'Добавить заметку', 'Название:')
    if ok and notes_name != '':
        notes[notes_name] = {
            'текст': '',
            'теги': []
        }
    list_notes.addItem(notes_name)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open('db.json', 'w', encoding='utf-8') as f:
            json.dump(notes, f, indent=4, ensure_ascii=False)
        status_bar.setText('Заметка сохранена')
    else:
        status_bar.setText('Заметка не выбрана')

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        field_tag.clear()
        field_text.clear()
        list_notes.clear()
        list_notes.addItems(notes)
        with open('db.json', 'w', encoding='utf-8') as f:
            json.dump(notes, f, ensure_ascii=False, indent=4)
        status_bar.setText('Заметка успешно удалена')

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag != '':
            if not tag in notes[key]["теги"]:
                notes[key]["теги"].append(tag)
                list_tags.addItem(tag)
                field_tag.clear()
            with open('db.json', 'w', encoding='utf-8') as f:
                json.dump(notes, f, ensure_ascii=False, indent=4)
            status_bar.setText('Заметка добавлена')
    else:
        status_bar.setText('Заметка не выбрана')

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open('db.json', 'w', encoding='utf-8') as f:
            json.dump(notes, f, ensure_ascii=False, indent=4)
        status_bar.setText('Заметка удалена')
    else:
        status_bar.setText('Заметка не выполнена')

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Искать по тегу" and tag:
        notes_filtered = {} #заметки с выделеным текстом
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note]=notes[note]
        button_tag_search.setText("Сбросить поиск")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Сбросить поиск":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Искать заметки по тегу")
    else:
        pass
        


button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)
list_notes.itemClicked.connect(show_note)


with open('db.json', 'r', encoding='utf-8') as f:
    notes = json.load(f)
list_notes.addItems(notes)

mw.setLayout(layout_notes)
mw.resize(800, 600)
mw.show()
app.exec_()