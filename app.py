#начни тут создавать приложение с умными заметкамиэ
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout, QInputDialog, QMessageBox
import json

app = QApplication([])
#параметры окна приложения
notes_win = QWidget()
notes_win.setWindowIcon(QtGui.QIcon('main.png'))
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900, 600)
notes_win.setStyleSheet("background-color: lightyellow; color: rgb(181, 135, 230);")

#виджеты окна приложения
list_notes = QListWidget()
list_notes.setStyleSheet("background-color: rgb(255,255,255);")
list_notes_label = QLabel('Список заметок')
button_note_create = QPushButton(icon=QtGui.QIcon('plus.png'),text='Создать заметку')

button_note_create.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightgreen;"
                             "}")
button_note_del = QPushButton(icon=QtGui.QIcon('del.png'), text='Удалить заметку')
button_note_del.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : red;"
                             "}")
button_note_save = QPushButton(icon=QtGui.QIcon('save.png'), text='Сохранить заметку')
button_note_save.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : blue;"
                             "}")
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
button_tag_add = QPushButton(icon=QtGui.QIcon('plus.png'), text='Добавить к заметке')

button_tag_add.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightgreen;"
                             "}")
button_tag_del = QPushButton(icon=QtGui.QIcon('del.png'), text='Открепить от заметки')

button_tag_del.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : red;"
                             "}")
button_tag_search = QPushButton(icon=QtGui.QIcon('search.png'), text='Искать заметки по тегу')

button_tag_search.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : blue;"
                             "}")
list_tags = QListWidget()
list_tags.setStyleSheet("background-color: rgb(255,255,255);")
list_tags_label = QLabel('Список тегов')
field_text = QTextEdit()
field_text.setStyleSheet("background-color: rgb(255,255,255);")


#лейауты
main_layout = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
row1 = QHBoxLayout()
row2 = QHBoxLayout()
col1.addWidget(field_text)
col2.addWidget(list_notes_label)
col2.addWidget(list_notes)
row1.addWidget(button_note_create)
row1.addWidget(button_note_del)
col2.addLayout(row1)
col2.addWidget(button_note_save)
col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(field_tag)
row2.addWidget(button_tag_add)
row2.addWidget(button_tag_del)
col2.addLayout(row2)
col2.addWidget(button_tag_search)
main_layout.addLayout(col1)
main_layout.addLayout(col2)
notes_win.setLayout(main_layout)

#основной код
notes = {}

'''функционал приложения!'''

#загрузка в файл
def dump():
    global notes
    with open('notes_data.json', 'w', encoding="utf-8") as file:
        json.dump(notes, file)
#загрузка из файла
def load():
    global notes
    with open('notes_data.json', 'r', encoding="utf-8") as file:
        notes = json.load(file)

def show_message(title, text, icon=None):
    msg = QMessageBox(notes_win)
    msg.setStyleSheet("background-color: rgb(255,255,255);")
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.exec_()

load() #первый раз загружаем из файла
for key in notes:
    list_notes.addItem(key)

#показать заметку
def show_note():
    #получаем текст из заметки с выделенным названием и отображаем его в поле редактирования вместе с тегами
    key = list_notes.selectedItems()[0].text() #здесь я получаю название выделенной заметки
    field_text.setText(notes[key]['text']) #у поля редактирования текста устанавилваем текст выбранной заметки
    list_tags.clear() #чисти список тегов
    list_tags.addItems(notes[key]['tags'])

#создать заметку
def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Добавить заметку", "Название заметки: ") #создаем вспомоагтельное окно для ввода названия заметки
    if ok and note_name != "": #
        notes[note_name] = {"text" : "", "tags" : []}
        list_notes.clear()
        list_notes.addItems(notes)
        dump()

def del_note():
    if len(list_notes.selectedItems()) != 0:
        key = list_notes.selectedItems()[0].text() #здесь я получаю название выделенной заметки
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        dump()
    else:
        show_message('Предупреждение!', 'Не выбрана заметка для удаления')

def save_note():
    if len(list_notes.selectedItems()) != 0:
        key = list_notes.selectedItems()[0].text() #здесь я получаю название выделенной заметки
        notes[key]['text'] = field_text.toPlainText()
        dump()
        show_message('Уведомление', 'Заметка успешно сохранена')
    else:
        show_message('Предупреждение!', 'Не выбрана заметка для сохранения')
     
def add_tag():
    if len(list_notes.selectedItems()) != 0:
        if field_tag.text() != '':
            key = list_notes.selectedItems()[0].text() #здесь я получаю название выделенной заметки
            if field_tag.text() in notes[key]['tags']:
                show_message('Уведомление', 'Такой тег у заметки уже есть')
            else:
                notes[key]['tags'].append(field_tag.text())
                list_tags.addItem(field_tag.text())
                field_tag.clear()
                dump()
        else:
            show_message('Предупреждение!', 'Тег пустой! Заполните поле тега')
    else:
        show_message('Предупреждение!', 'Не выбрана заметка для добавления тега')

def del_tag():
    if len(list_notes.selectedItems()) != 0:
        if len(list_tags.selectedItems()) != 0:
            key = list_notes.selectedItems()[0].text() #здесь я получаю название выделенной заметки
            tag = list_tags.selectedItems()[0].text() #здесь я получаю название тега по которому я кликнул
            notes[key]['tags'].remove(tag) #удаляем тег из списка в словаре
            list_tags.clear() #чистим виджет тегов
            list_tags.addItems(notes[key]['tags']) #заполнить виджет обновленным списком тегов
            dump()
        else:
            show_message('Предупреждение!', 'Тег не выбран!')
    else:
        show_message('Предупреждение!', 'Не выбрана заметка')

def search_tag():
    if field_tag.text() != '':
        found_notes = []
        for key in notes:
            if field_tag.text() in notes[key]['tags']:
                found_notes.append(key)
        if len(found_notes) != 0:
            list_notes.clear()
            list_notes.addItems(found_notes)
        else:
            show_message('Предупреждение!', 'Заметок с таким тегом не найдено!')
    else:
        list_notes.clear()
        list_notes.addItems(notes)
        show_message('Предупреждение!', 'Сначала введите тег для поиска')

button_tag_search.clicked.connect(search_tag)           
button_tag_del.clicked.connect(del_tag)
button_tag_add.clicked.connect(add_tag)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)

notes_win.show()
app.exec_()

