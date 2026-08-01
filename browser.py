import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QLineEdit,
    QTabWidget, QWidget, QVBoxLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BrowserTab(QWidget):
    """Har naye tab ke liye layout aur web engine controller"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Web View Engine
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com'))
        self.layout.addWidget(self.browser)

class MultiTabBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Custom Python Browser - Level 1")
        self.setGeometry(100, 100, 1200, 800)

        # Tab Widget Setup
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        self.setCentralWidget(self.tabs)

        # FIX: Pehle Navigation Bar (url_bar) banao, phir initial tab add karo
        self.create_navbar()

        # Initial Tab Add Karein
        self.add_new_tab(QUrl('https://www.google.com'), 'New Tab')

    def create_navbar(self):
        navbar = QToolBar("Navigation Bar")
        self.addToolBar(navbar)

        # Back Button
        back_btn = QAction('◀ Back', self)
        back_btn.triggered.connect(lambda: self.current_browser().back() if self.current_browser() else None)
        navbar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction('▶ Forward', self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward() if self.current_browser() else None)
        navbar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction('🔄 Reload', self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload() if self.current_browser() else None)
        navbar.addAction(reload_btn)

        # Home Button
        home_btn = QAction('🏠 Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # Add Tab Button
        add_tab_btn = QAction('➕ New Tab', self)
        add_tab_btn.triggered.connect(lambda: self.add_new_tab())
        navbar.addAction(add_tab_btn)

        # Address Bar (URL Input)
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl('https://www.google.com')

        tab = BrowserTab()
        index = self.tabs.addTab(tab, label)
        self.tabs.setCurrentIndex(index)

        # URL Change aur Title Update Event Handlers
        tab.browser.urlChanged.connect(lambda q: self.update_urlbar(q, tab.browser))
        tab.browser.loadFinished.connect(lambda _, i=index, b=tab.browser: self.tabs.setTabText(i, b.page().title()[:15]))

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def tab_changed(self, i):
        current_b = self.current_browser()
        if current_b:
            self.update_urlbar(current_b.url(), current_b)

    def current_browser(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            return current_tab.browser
        return None

    def navigate_home(self):
        b = self.current_browser()
        if b:
            b.setUrl(QUrl('https://www.google.com'))

    def navigate_to_url(self):
        text = self.url_bar.text()
        if not text.startswith('http://') and not text.startswith('https://'):
            url = 'https://www.google.com/search?q=' + text
        else:
            url = text
        
        b = self.current_browser()
        if b:
            b.setUrl(QUrl(url))

    def update_urlbar(self, q, browser=None):
        if browser != self.current_browser():
            return
        if hasattr(self, 'url_bar'):
            self.url_bar.setText(q.toString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Python Browser")
    window = MultiTabBrowser()
    window.show()
    sys.exit(app.exec_())