from main_kiwoom.Main_k import *
import sys
from PyQt5.QtWidgets import *

class Main():
    def __init__(self):
        print("Collect Program")

        self.app = QApplication(sys.argv)

        self.kiwoom = Kiwoom()


if __name__== "__main__":
    Main()

