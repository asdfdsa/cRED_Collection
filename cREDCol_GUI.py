from PyQt4 import QtGui
import cRED_Main
import sys
import os
import threading

class cREDCol(QtGui.QWidget):
    def __init__(self):
        #threading.Thread.__init__(self)
        super(cREDCol,self).__init__()
        self.initUI()
        
    def initUI(self):
        self.stopEvent=threading.Event()
        
        self.lbl1=QtGui.QLabel('Please input the desired saving path here:',self)
        self.lbl1.move(20,20)
        
        self.lbl2=QtGui.QLabel('log file created.',self)
        self.lbl2.move(20,100)
        self.lbl2.hide()
        
        self.lbl3=QtGui.QLabel('Please rotate the particle to desired starting angle (i.e. -45 degree).',self)
        self.lbl3.move(20,120)
        self.lbl3.hide()
        
        self.lbl4=QtGui.QLabel('Please adjust z height. Press "Collect" to collect data if done the preparation.',self)
        self.lbl4.move(20,140)
        self.lbl4.hide()
        
        self.lbl5=QtGui.QLabel('Path invalid. Please enter a valid path.',self)
        self.lbl5.move(20,120)
        self.lbl5.hide()
        
        self.lbl6=QtGui.QLabel('Data Collection Done! Images saved to path. Close window to quit.',self)
        self.lbl6.move(20,240)
        self.lbl6.hide()
                
        self.le1=QtGui.QLineEdit(self)
        self.le1.move(20,40)
        self.le1.setFixedWidth(500)
        
        self.btn1=QtGui.QPushButton('Confirm',self)
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.move(550,38)
        self.btn1.clicked.connect(self.ReadDir)

        self.btn2=QtGui.QPushButton('Collect',self)
        self.btn2.resize(self.btn2.sizeHint())
        self.btn2.move(500,120)
        self.btn2.clicked.connect(self.DataCollection)
        
        self.btn3=QtGui.QPushButton('Stop',self)
        self.btn3.resize(self.btn3.sizeHint())
        self.btn3.move(580,120)
        self.btn3.clicked.connect(self.stop)
        
        self.setGeometry(200,200,700,200)
        self.setWindowTitle('cRED Data Collection GUI')
        self.show()
        
    def ReadDir(self):
        path=self.le1.text()
        path=r"{}".format(path)
        
        if os.path.exists(path):
            self.lbl2.show()
            self.lbl3.show()
            self.lbl4.show()
            self.lbl5.hide()
            return path
        else:
            self.lbl2.hide()
            self.lbl3.hide()
            self.lbl4.hide()
            self.lbl5.show()
            return 0
    
    def DataCollection(self):
        path=self.ReadDir()
        cRED_Main.main(path,self.stopEvent)
        self.lbl6.show()

    def closeEvent(self,event):
        reply=QtGui.QMessageBox.question(self,'Message',"Are you sure to quit?",QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            
    def stop(self):
        self.stopEvent.set()
                    
def main():
    app=QtGui.QApplication(sys.argv)
    ex=cREDCol()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()