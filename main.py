from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QComboBox, QTextEdit, QGroupBox
from PyQt5.QtCore import Qt
from googletrans import Translator
from gtts import gTTS
from languages import list_key, list_value
import os
import sys

#Translations class
class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.design()
        self.event_button()
    
    def settings(self): #setting size, starting point, title
        self.setGeometry(300, 150, 860, 500)
        self.setWindowTitle('Translator')
    
    def design(self):
        #making objects
        self.dropbox_1 = QComboBox()
        self.dropbox_1.setFixedWidth(170)
        self.dropbox_2 = QComboBox()
        self.dropbox_2.setFixedWidth(170)
        self.dropbox_1.addItems(list_value)
        self.dropbox_2.addItems(list_value)
        self.dropbox_1.setCurrentIndex(21)
        self.dropbox_2.setCurrentIndex(26)

        self.translate_button = QPushButton('Translate')
        self.translate_button.setObjectName("button1")
        self.speak_button = QPushButton('Speak')
        self.speak_button.setObjectName("button2")
        self.clear_button = QPushButton('Clear')
        self.clear_button.setObjectName("button3")
        self.reverse_button = QPushButton('Reverse')
        self.reverse_button.setObjectName("button4")
        self.groupbox = QGroupBox('App actions')

        self.input_box = QTextEdit()
        self.output_box = QTextEdit()
        self.input_box.setPlaceholderText('Type something here...')
        self.output_box.setPlaceholderText('Translation...')

        #finale layout
        self.master = QHBoxLayout()
        self.column_1 = QVBoxLayout()
        self.column_2 = QVBoxLayout()

        #layout for buttons
        self.buttonhold = QVBoxLayout()
        self.row_1 = QHBoxLayout()
        self.row_2 = QHBoxLayout()
        self.row_1.addWidget(self.translate_button, alignment = Qt.AlignLeft)
        self.row_1.addWidget(self.speak_button, alignment = Qt.AlignRight)
        self.row_2.addWidget(self.reverse_button, alignment = Qt.AlignLeft)
        self.row_2.addWidget(self.clear_button, alignment = Qt.AlignRight)
        self.buttonhold.addLayout(self.row_1)
        self.buttonhold.addLayout(self.row_2)
        
        #fill the buttons in a group box
        self.groupbox.setLayout(self.buttonhold) 
        self.empty_row = QHBoxLayout()
        self.column_1.addLayout(self.empty_row, 60)
        self.column_1.addWidget(self.groupbox, 40)

        self.rightrow_1 = QHBoxLayout()
        self.rightrow_2 = QHBoxLayout()
        self.rightrow_1.addWidget(QLabel('Input:'))
        self.rightrow_1.addWidget(self.dropbox_1)
        self.rightrow_2.addWidget(QLabel('Output:'))
        self.rightrow_2.addWidget(self.dropbox_2)

        self.column_2.addLayout(self.rightrow_1)
        self.column_2.addWidget(self.input_box)
        self.column_2.addLayout(self.rightrow_2)
        self.column_2.addWidget(self.output_box)

        self.master.addLayout(self.column_1, 30)
        self.master.addLayout(self.column_2, 70)
        self.setLayout(self.master)

        self.setStyleSheet("""
        #button1 { padding: 5px 20px;
                        }
        #button2 { padding: 5px 28px;
                        }
        #button3 { padding: 5px 31px;
                        }
        #button4 { padding: 5px 23px;
                        }
                           
        QPushButton{
                           background-color: grey;
                           border-radius:5px;
                           
                           }
        QPushButton:hover{
                           background-color: #031d39;                           
                           }
        
                        """)

    def event_button(self): #triggers the buttons
        self.translate_button.clicked.connect(self.apply_translation)
        self.reverse_button.clicked.connect(self.reverse_language)
        self.clear_button.clicked.connect(self.clear_method)
        self.speak_button.clicked.connect(self.speak_method)

    def apply_translation(self): #applying the translation
        text = self.input_box.toPlainText()
        source_position = self.dropbox_1.currentIndex()
        source_language = list_key[source_position]

        dest_position = self.dropbox_2.currentIndex()
        dest_language = list_key[dest_position]

        self.gg_Translate(text, dest_language, source_language)

    def gg_Translate(self, text, dest_language, source_language): #implement the google translation module
        translation = Translator()
        translate = translation.translate(text, dest = dest_language, src = source_language)
        self.output_box.setText(translate.text)

    def reverse_language(self): #reverse the index position between two dropboxes
        source_position = self.dropbox_1.currentIndex()
        dest_position = self.dropbox_2.currentIndex()
        self.dropbox_1.setCurrentIndex(dest_position)
        self.dropbox_2.setCurrentIndex(source_position)
        switch_text_1 = self.input_box.toPlainText()
        switch_text_2 = self.output_box.toPlainText()
        self.input_box.setText(switch_text_2)
        self.output_box.setText(switch_text_1)

    def clear_method(self): #clearing the text
        self.input_box.clear()
        self.output_box.clear()
    
    def speak_method(self):
        text = self.output_box.toPlainText()
        try:
            tts = gTTS(text, lang = 'en')
            if getattr(sys, 'frozen', False):
                app_dir = os.path.dirname(sys.executable)
            else:
                app_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(app_dir,"output.mp3")
            tts.save(output_file)
            os.system(f'afplay output.mp3')
            os.remove("output.mp3")
        except Exception as e:
            print("Error:", e)

# Boilerplate
if __name__ == "__main__":
    app = QApplication([])
    window = TranslatorApp()
    window.show()
    app.exec()