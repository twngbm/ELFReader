import pyqt_gui

if __name__ == "__main__":

    app=pyqt_gui.QtWidgets.QApplication([])
    sr=app.desktop().screenGeometry()
    main_windows=pyqt_gui.main_windows(sr.width(),sr.height())
    main_windows.showMaximized()
    pyqt_gui.sys.exit(app.exec_())
