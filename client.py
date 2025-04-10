import sys, asyncio, threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
import websockets
from datetime import datetime
import os

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat")
        self.resize(400, 600)

        self.username, ok = QInputDialog.getText(self, "username", "Please Enter Your Name：")
        if not ok or not self.username:
            self.username = "Unknown"

        self.log_file = f"chat_log_{self.username}.txt"

        self.layout = QVBoxLayout(self)
        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.input = QLineEdit()
        self.send_btn = QPushButton("Send")

        self.layout.addWidget(self.chat_box)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.send_btn)

        self.send_btn.clicked.connect(self.send_message)
        self.input.returnPressed.connect(self.send_message)

        self.ws = None
        self.loop = None

        QTimer.singleShot(100, self.start_ws_connection)

        self.load_chat_history()

    def load_chat_history(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                self.chat_box.setPlainText(f.read())
                self.scroll_to_bottom()

    def append_message(self, text):
        self.chat_box.append(text)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        self.scroll_to_bottom()

    def start_ws_connection(self):
        threading.Thread(target=self.run_event_loop, daemon=True).start()

    def send_message(self):
        msg = self.input.text().strip()
        if not self.ws:
            QMessageBox.warning(self, "Unconnect", "You have not connect to the server, can not send message.")
            return
        if msg:
            asyncio.run_coroutine_threadsafe(self.ws.send(msg), self.loop)
            timestamp = datetime.now().strftime("%H:%M:%S")
            display_msg = f"[{timestamp}] Me: {msg}"
            self.append_message(display_msg)
            self.input.clear()

    async def receive(self):
        try:
            uri = f"ws://34.214.61.91:8000/ws?username={self.username}"
            async with websockets.connect(uri) as ws:
                self.ws = ws
                while True:
                    raw_msg = await ws.recv()
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    if "::" in raw_msg:
                        sender, msg = raw_msg.split("::", 1)
                        if sender == self.username:
                            continue  
                        display_msg = f"[{timestamp}] {sender}: {msg}"
                    else:
                        display_msg = f"[{timestamp}] {raw_msg}"
                    self.append_message(display_msg)
        except Exception as e:
            self.append_message(f"[Fail to connect] {e}")

    def scroll_to_bottom(self):
        scrollbar = self.chat_box.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def run_event_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.receive())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatClient()
    window.show()
    sys.exit(app.exec_())
