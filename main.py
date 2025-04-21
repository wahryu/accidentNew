import locale
import os
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QThread
from datetime import datetime
import worker

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainMenu(QMainWindow):
    # localeモジュールで時間のロケールを'ja_JP.UTF-8'に変更する
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
    def __init__(self, parent=None, *args, **kwargs):
        super(MainMenu, self).__init__(parent, *args, **kwargs)
        loadUi(resource_path('main.ui'), self)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowTitle("無災害記録表")
        f = open(resource_path("start_date.txt"), "r")
        self.startDate = datetime.strptime(f.read(), '%Y-%m-%d').date()
        ft = open(resource_path("target.txt"), "r")
        self.targetLcd.display(int(ft.read()))
        # self.refreshAction.triggered.connect(self.refresh)
        self.workerRF = worker.WorkerFileRefresh()
        self.worker_threadRF = QThread()
        self.workerRF.moveToThread(self.worker_threadRF)
        self.workerRF.progress.connect(self.refresh)
        self.worker_threadRF.started.connect(self.workerRF.do_work)
        self.worker_threadRF.start()
                
        self.refresh()
        
        self.ResetBtn.clicked.connect(self.ResetConfirm)
        self.TargetBtn.clicked.connect(self.TargetSetting)

        
    def refresh(self):
        self.dateNow = datetime.now().date()
        self.dateLabel.setText(self.dateNow.strftime("%m月%d日"))
        countNow = self.dateNow - self.startDate
        self.countLcd.display(countNow.days + 1)
    
    def ResetConfirm(self):
        msg = "カウントをリセットしますか?"
        reply = QMessageBox.question(self, '確認', msg, QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # self.Reset()
            text, ok = QInputDialog.getText(self, 'パスワード入力', 'パスワードを入力してください:')
            if ok:
                if text == "Aokibuild225567":
                    self.Reset()
                    QMessageBox.information(self, '完了', "リセットしました", QMessageBox.StandardButton.Ok)
                else:
                    msg = "パスワードが違います"
                    QMessageBox.warning(self, '警告', msg, QMessageBox.StandardButton.Ok)
                    # 何もしない
                    pass
            else:
                pass
        else:
            pass
        
    def Reset(self):
        self.worker_threadRF.quit()
        # self.worker_threadRF.wait()
        self.dateNow = datetime.now().date()
        self.startDate = self.dateNow
        
        f = open(resource_path("start_date.txt"), "w")
        f.write(self.dateNow.strftime('%Y-%m-%d'))
        f.close()
        
        self.refresh()
        self.worker_threadRF.start()
        
    def TargetSetting(self):
        text, ok = QInputDialog.getText(self, '目標日数', '新しい目標日数を入力してください！！:')
        if ok:
            if text.isdigit():
                self.targetLcd.display(int(text))
                f = open(resource_path("target.txt"), "w")
                f.write(text)
                f.close()
                msg = "目標日数を設定しました"
                QMessageBox.information(self, '完了', msg, QMessageBox.StandardButton.Ok)
            else:
                msg = "数字を入力してください"
                QMessageBox.warning(self, '警告', msg, QMessageBox.StandardButton.Ok)

        else:
            msg = "パスワードが違います"
            QMessageBox.warning(self, '警告', msg, QMessageBox.StandardButton.Ok)
            # 何もしない
            pass
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainMenu()
    win.show()
    sys.exit(app.exec())