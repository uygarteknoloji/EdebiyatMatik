import sys
import os
import win32print
import win32ui
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QPushButton, QGridLayout, QVBoxLayout,
    QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PIL import ImageWin
from PIL import Image, ImageDraw, ImageFont
import textwrap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "files")


# ---------------- ANA EKRAN ----------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edebi Eserler")
        self.setFixedSize(400, 450)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Edebi Eserler")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:24px; font-weight:bold;")

        subtitle = QLabel("Lütfen bir kategori seçin")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")

        grid = QGridLayout()
        grid.setSpacing(15)

        self.categories = [
            "Şiir", "Roman",
            "Hikaye", "Masal",
            "Fıkra", "Biyografi"
        ]

        positions = [(i, j) for i in range(3) for j in range(2)]

        for pos, category in zip(positions, self.categories):
            btn = QPushButton(category)
            btn.setFixedHeight(60)
            btn.setStyleSheet("""
                QPushButton {
                    font-size:16px;
                    border-radius:10px;
                    background:#2d89ef;
                    color:white;
                }
                QPushButton:hover {
                    background:#1b5fbd;
                }
            """)
            btn.clicked.connect(
                lambda checked, c=category: self.open_category(c)
            )
            grid.addWidget(btn, *pos)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addLayout(grid)
        layout.addStretch()

        self.setLayout(layout)

    def open_category(self, category):
        self.list_window = TextListWindow(category)
        self.list_window.show()
        self.close()


def text_to_image_80mm(file_path, output_path="print_temp.png"):
    WIDTH = 560  # 80mm güvenli alan
    MARGIN_X = 20
    MARGIN_Y = 20

    TITLE_FONT_SIZE = 34
    BODY_FONT_SIZE = 24
    LINE_SPACING = 10

    title_font = ImageFont.truetype(
        "C:/Windows/Fonts/arialbd.ttf", TITLE_FONT_SIZE
    )
    body_font = ImageFont.truetype(
        "C:/Windows/Fonts/arial.ttf", BODY_FONT_SIZE
    )

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    title = lines[0]
    body = lines[1:]

    wrapped_body = []
    for line in body:
        wrapped_body.extend(textwrap.wrap(
            line, width=50, replace_whitespace=False
        ) or [""])

    title_height = title_font.getbbox("Ay")[3]
    body_height = body_font.getbbox("Ay")[3]

    total_height = (
        MARGIN_Y +
        title_height + 20 +
        len(wrapped_body) * (body_height + LINE_SPACING) +
        40
    )

    img = Image.new("L", (WIDTH, total_height), 255)
    draw = ImageDraw.Draw(img)

    # 🔹 Başlık (ortalanmış)
    title_width = draw.textlength(title, font=title_font)
    draw.text(((WIDTH - title_width) // 2, MARGIN_Y),
        title,
        font=title_font,
        fill=0
    )

    y = MARGIN_Y + title_height + 20

    # 🔹 Gövde
    for line in wrapped_body:
        draw.text(
            (MARGIN_X, y),
            line,
            font=body_font,
            fill=0
        )
        y += body_height + LINE_SPACING

    # 🔹 Otomatik ayraç
    draw.line(
        (MARGIN_X, y + 10, WIDTH - MARGIN_X, y + 10),
        fill=0,
        width=2
    )

    img.save(output_path)

def print_image(image_path):
    printer_name = win32print.GetDefaultPrinter()

    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)

    hDC.StartDoc("Siir Yazdirma")
    hDC.StartPage()

    bmp = Image.open(image_path)
    dib = ImageWin.Dib(bmp)

    dib.draw(
        hDC.GetHandleOutput(),
        (0, 0, bmp.size[0], bmp.size[1])
    )

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()   

def print_txt_as_image(file_path):
    img = "print_temp.png"
    text_to_image_80mm(file_path, img)
    print_image(img)   


# ---------------- LİSTE EKRANI ----------------
class TextListWindow(QWidget):
    def __init__(self, category):
        super().__init__()
        self.category = category
        self.setWindowTitle(category)
        self.setFixedSize(500, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel(self.category)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold;")

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("font-size:30px;")
        self.list_widget.itemClicked.connect(self.print_and_return)

        self.load_texts()

        back_btn = QPushButton("← Geri")
        back_btn.clicked.connect(self.go_back)

        layout.addWidget(title)
        layout.addWidget(self.list_widget)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def load_texts(self):
        category_path = os.path.join(FILES_DIR, self.category)

        if not os.path.exists(category_path):
            return

        for file in os.listdir(category_path):
            if file.endswith(".txt"):
                file_path = os.path.join(category_path, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        first_line = f.readline().strip()

                    if first_line:
                        item = QListWidgetItem(first_line)
                        item.setData(Qt.UserRole, file_path)
                        self.list_widget.addItem(item)

                except Exception as e:
                    print(f"Hata: {file} → {e}")

    def go_back(self):
        self.main = MainWindow()
        self.main.show()
        self.close()



    def print_and_return(self, item):
        file_path = item.data(Qt.UserRole)
        print_txt_as_image(file_path)
        self.main = MainWindow()
        self.main.show




# ---------------- ÇALIŞTIR ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())