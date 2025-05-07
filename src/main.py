from src.gui.mainwindow import MainWindow
from src.logic.LibraryManager import LibraryManager
libMan = LibraryManager()
app = MainWindow(libMan)
app.mainloop()