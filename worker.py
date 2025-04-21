from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot
import datetime
import time

def sleepUntil(hour, minute):
    t = datetime.datetime.today()
    future = datetime.datetime(t.year, t.month, t.day, hour, minute)
    if t.timestamp() > future.timestamp():
        future += datetime.timedelta(days=1)
    time.sleep((future-t).total_seconds())

class WorkerFileRefresh(QObject):
    progress = Signal(int)
    completed = Signal(int)
    error = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_killed = False

    @Slot()
    def do_work(self):
        try:
            for i in range(0,365):
                sleepUntil(2, 0)  # Sleep until 2:00 AM
                self.progress.emit(i+1)
                
                if self.is_killed:
                    break
                
            self.completed.emit(1)
            
        except Exception as e:
            self.error.emit(e)
            
    def kill(self):
        self.is_killed = True