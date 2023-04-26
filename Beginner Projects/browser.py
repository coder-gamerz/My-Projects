from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
 
        self.tabs = QTabWidget()
 
        self.tabs.setDocumentMode(True)
 
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
 
        self.tabs.currentChanged.connect(self.current_tab_changed)
 
        self.tabs.setTabsClosable(True)
 
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
 
        self.setCentralWidget(self.tabs)
 
        self.status = QStatusBar()
 
        self.setStatusBar(self.status)
 
        navtb = QToolBar("Navigation")
 
        self.addToolBar(navtb)
 
        back_btn = QAction("⮘", self)
 
        back_btn.setStatusTip("Back to previous page")
 
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
 
        navtb.addAction(back_btn)
 
        next_btn = QAction("⮚", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)
 
        reload_btn = QAction("⟳", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
 
        home_btn = QAction("⌂", self)
        home_btn.setStatusTip("Go home")
 
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
 
        navtb.addSeparator()
 
        self.urlbar = QLineEdit()
 
        self.urlbar.returnPressed.connect(self.navigate_to_url)
 
        navtb.addWidget(self.urlbar)
 
        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
 
        self.add_new_tab(QUrl('https://www.startpage.com'), 'Homepage')
 
        self.show()
 
        self.setWindowTitle("Browser")
 
    def add_new_tab(self, qurl = None, label ="Blank"):
 
        if qurl is None:
            qurl = QUrl('https://www.startpage.com')
 
        browser = QWebEngineView()
 
        browser.setUrl(qurl)
 
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
 
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                   self.update_urlbar(qurl, browser))
 
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                     self.tabs.setTabText(i, browser.page().title()))
 
    def tab_open_doubleclick(self, i):
 
        if i == -1:
            self.add_new_tab()
 
    def current_tab_changed(self, i):
 
        qurl = self.tabs.currentWidget().url()
 
        self.update_urlbar(qurl, self.tabs.currentWidget())
 
        self.update_title(self.tabs.currentWidget())
 
    def close_current_tab(self, i):
 
        if self.tabs.count() < 2:
            return
 
        self.tabs.removeTab(i)
 
    def update_title(self, browser):
 
        if browser != self.tabs.currentWidget():
            return
 
        title = self.tabs.currentWidget().page().title()
 
        self.setWindowTitle("% s - Browser" % title)
 
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.startpage.com"))
 
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
 
        if q.scheme() == "":
            q.setScheme("https")
 
        self.tabs.currentWidget().setUrl(q)
 
    def update_urlbar(self, q, browser = None):
 
        if browser != self.tabs.currentWidget():
 
            return
 
        self.urlbar.setText(q.toString())
 
        self.urlbar.setCursorPosition(0)
 
app = QApplication(sys.argv)
 
app.setApplicationName("Jungle")

window = MainWindow()

app.exec_()

# A cool browser with tabs and its own GUI


