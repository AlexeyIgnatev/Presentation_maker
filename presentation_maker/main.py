# def main():
#     topic = input('Введите тему презентации: ')
#     lang = int(input('Выберите язык презентации (1 - русский, 2 - английский)(введите цифру): '))
#     if lang < 1 or lang > 2:
#         print('Выбран некорректный язык!')
#         exit(-1)
#     lang = 'ru' if lang == 1 else 'en'
#     wiki = Wiki()
#     wiki.set_lang(lang)
#     wiki.load_page(topic)
#     wiki.clean_page()
#     search_headers, headers = wiki.headers
#     search_headers = ','.join(search_headers)
#     docx = Docx()
#     docx.create_document(wiki.content)
#     docx.save_document()
#     response = google_images_download.googleimagesdownload()
#     absolute_image_paths = response.download({"keywords": search_headers, 'limit': 1})
#     # pptx = Pptx()
#     # pptx.create_presentation(headers, absolute_image_paths)
#
#
# if __name__ == '__main__':
#     main()
from PyQt5 import QtCore, QtGui, QtWidgets
from presentation_maker.pages.py.start_page import Ui_MainWindow as StartPage
from presentation_maker.pages.py.second_page import Ui_MainWindow as Second_page
import sys
import langdetect
from presentation_maker.wiki_api import Wiki
from presentation_maker.docx_api import Docx
from presentation_maker.pptx_api import Pptx
from google_images_download import google_images_download

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = None
        self.topic = ''
        self.start_page()

    def start_page(self):
        self.ui = StartPage()
        self.ui.setupUi(self)
        self.ui.comboBox.addItem('Автоматически')
        self.ui.comboBox.addItem('Русский')
        self.ui.comboBox.addItem('Английский')
        self.ui.NextButton.clicked.connect(self.load_wiki)

    def load_wiki(self):
        self.topic = self.ui.lineEdit.text()
        if self.topic.strip() == '':
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Тема не должна быть пустой строкой')
            return
        index = self.ui.comboBox.currentIndex()
        lang = ''
        if index == 0:
            lang = langdetect.detect(self.topic)
        elif index == 1:
            lang = 'ru'
        else:
            lang = 'en'
        wiki = Wiki()
        wiki.set_lang(lang)
        num = wiki.load_page(self.topic)
        if num == 1:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Введите корректный поисковой запрос!')
            return
        if num == 2:
            QtWidgets.QMessageBox.about(self, 'Ошибка', 'Информации по такому запросу не найдено!')
            return
        wiki.clean_page()
        headers = wiki.headers
        docx = Docx()
        docx.create_document(wiki.content)
        docx.save_document()
        docx.open_document()
        self.second_page(headers)

    def second_page(self, headers):
        self.ui = Second_page()
        self.ui.setupUi(self)
        self.ui.previousButton.clicked.connect(self.start_page)
        self.ui.nextButton.clicked.connect(self.create_presentation)
        for i in headers:
            line = self.create_line_edit()
            line.setText(i)
            self.ui.scrollAreaWidgetContents.layout().addWidget(line)

        self.ui.addButton.clicked.connect(self.add_line)
        self.ui.removeButton.clicked.connect(self.remove_line)

    def add_line(self):
        self.ui.scrollAreaWidgetContents.layout().addWidget(self.create_line_edit())

    def remove_line(self):
        count = self.ui.scrollAreaWidgetContents.layout().count()
        line = self.ui.scrollAreaWidgetContents.layout().itemAt(count - 1).widget()
        line.setParent(None)

    @staticmethod
    def create_line_edit():
        line_edit = QtWidgets.QLineEdit()
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        line_edit.setFont(font)
        line_edit.setObjectName("lineEdit")
        return line_edit

    def create_presentation(self):
        headers = []
        search_headers = []
        for i in range(self.ui.scrollAreaWidgetContents.layout().count()):
            line = self.ui.scrollAreaWidgetContents.layout().itemAt(i).widget().text()
            line = line.strip()
            if line:
                headers.append(line)
                search_headers.append('{} {}'.format(self.topic, line))
        response = google_images_download.googleimagesdownload()
        search_headers = ','.join(search_headers)
        absolute_image_paths = response.download({"keywords": search_headers, 'limit': 1})
        pptx = Pptx()
        pptx.create_presentation(self.topic, headers, absolute_image_paths)
        pptx.save_presentation()
        pptx.open_presentation()
        QtWidgets.QMessageBox.about(self, 'Всё готово!', 'Презентация успешно создана.')
        self.start_page()



app = QtWidgets.QApplication([])
application = MainWindow()
application.show()

sys.exit(app.exec())
