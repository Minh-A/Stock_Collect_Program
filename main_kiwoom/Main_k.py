# Main Module
# Public Version Making by 2021-02-22
# first Public Version

# Essential Library
import random  # Up to 1,000 in an hour
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from datetime import datetime  # import today

# Module CHAIN
from main_kiwoom.ErrorCode import *  # Error Module
from collect.Collect_Public_1st import *  # Condition Module

# Base Date
date = datetime.today().strftime("%Y%m%d")


##########################
# Main Code
class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("Main Module Run")

        ##########EVENT loop
        self.login_event_loop = QEventLoop()
        self.calculator_event_loop = QEventLoop()

        self.kospi_loop = QEventLoop()  # KOSPI
        self.kosdaq_loop = QEventLoop()  # KOSDAQ

        ##########Screen Number
        self.screen_my_info = "1000"
        self.screen_calculation_stock = "2000"

        ##########함수 실행
        self.get_ocx_instance()  # API 1st RUN
        self.event_slots()  # API 2ed RUN
        self.sinal_login_commconnect()  # login

        self.kospi()  # KOSPI
        self.calculator_fnc_kospi()  # KOSPI Item

        self.kosdaq()  # KOSDAQ
        self.calculator_fnc_kosdaq()  # KOSDAQ Item

    #############################################
    # Function
    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")  # API

    def event_slots(self):
        self.OnEventConnect.connect(self.login_slot)  # login
        self.OnReceiveTrData.connect(self.trdata_slot)  # Tr

    # login
    def sinal_login_commconnect(self):  # login run
        self.dynamicCall("CommConnect()")

        self.login_event_loop.exec_()

    def login_slot(self, errCode):
        print(errors(errCode))

        self.login_event_loop.exit()

    #############################################
    # Item DB Function

    # Market Code To Number of items
    def get_code_list_by_market(self, market_code):  # Get Market Code
        code_list = self.dynamicCall("GetCodeListByMarket(QString", market_code)
        code_list = code_list.split(";")[:-1]

        return code_list

    # Item DB (KOSPI)
    def calculator_fnc_kospi(self):
        code0_list = self.get_code_list_by_market("0")  # 0 = KOSPI
        code0_list = random.sample(code0_list, 499)

        print("코스피 개수 : %s개" % len(code0_list))
        for idx, code in enumerate(code0_list):
            self.dynamicCall("DisconnectRealData(QString)", self.screen_calculation_stock)
            print("%s / %s : KOSPI Stock Code : %s" % (idx + 1, len(code0_list), code))
            self.day_kiwoom_db(code=code, date= date)

    # Item DB (KOSDAQ)
    def calculator_fnc_kosdaq(self):
        code10_list = self.get_code_list_by_market("10")  # 10 = KOSDAQ
        code10_list = random.sample(code10_list, 499)

        print("코스닥 개수 : %s개" % len(code10_list))
        for idx, code in enumerate(code10_list):
            self.dynamicCall("DisconnectRealData(QString)", self.screen_calculation_stock)
            print("%s / %s : KOSDAQ Stock Code : %s" % (idx + 1, len(code10_list), code))
            self.day_kiwoom_db(code=code, date= date)


    #############################################
    # Condition Module
    day_kiwoom_db = day_kiwoom_db
    kospi = kospi
    kosdaq = kosdaq
    trdata_slot = trdata_slot














