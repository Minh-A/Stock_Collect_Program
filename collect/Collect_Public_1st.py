# Collect Public 1st Ver

# Import Library
from PyQt5.QtTest import *
from datetime import datetime  # import today
import csv  # Read & Write CSV

# Function Variable
f = open('cfiles/Collect_210222.csv','w', newline='')
date = datetime.today().strftime("%Y%m%d")


########################
# KOSPI Request
def kospi(self):
    print("\n <코스피 요청> \n")
    self.dynamicCall("SetInputValue(QString, QString)", "업종코드", "001")
    self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)
    self.dynamicCall("CommRqData(QString, QString, int, QString)", "업종일봉조회", "opt20006", "0",
                     self.screen_calculation_stock)
    self.kospi_loop.exec_()

# KOSDAQ Request
def kosdaq(self):
    print("\n <코스닥 요청> \n")
    self.dynamicCall("SetInputValue(QString, QString)", "업종코드", "101")
    self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)
    self.dynamicCall("CommRqData(QString, QString, int, QString)", "업종일봉조회", "opt20006", "0", self.screen_calculation_stock)
    self.kosdaq_loop.exec_()


# Item DB
def day_kiwoom_db(self, code=None, date=None, sPrevNext='0'):
    QTest.qWait(600)

    self.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
    self.dynamicCall("SetInputValue(QString, QString)", "수정주가구분", "1")

    # Day Data
    self.dynamicCall("SetInputValue(QString, QString)", "기준일자", date)
    self.dynamicCall("CommRqData(QString, QString, int, QString)", "주식일봉차트조회", "opt10081", sPrevNext,
                     self.screen_calculation_stock)

    self.calculator_event_loop.exec_()


########################
# Collect Main DB
def trdata_slot(self, sCrNo, sRQName, sTrCode, sRecordName, sPrevNext):

    ################################ KOSPI, KOSDAQ
    if sRQName == "업종일봉조회":

        self.kospi_loop.exit()
        self.kosdaq_loop.exit()

    ################################ Item Code
    if sRQName == "주식일봉차트조회":
        self.calcul_data = []

        code = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, "종목코드")
        code = code.strip()

        cnt = self.dynamicCall("GetRepeatCnt(QString,QString)", sTrCode, sRQName)  # Count Day

        if cnt <= 500:
            print("데이터 부족 \n")
            self.calculator_event_loop.exit()
        else:
            # 데이터 생성
            for i in range(500):
                data = []

                current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                 "현재가")  # 종가 = 현재가
                value = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "거래량")
                trading_value = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i,
                                                 "거래대금")
                date = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "일자")
                start_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "시가")
                high_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "고가")
                low_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, "저가")
                code_nm = self.dynamicCall("GetMasterCodeName(QString)", code)

                data.append(code)
                data.append(code_nm)
                data.append(date.strip())
                data.append(abs(int(current_price.strip())))
                data.append(abs(int(start_price.strip())))
                data.append(abs(int(high_price.strip())))
                data.append(abs(int(low_price.strip())))
                data.append(value.strip())
                data.append(trading_value.strip())

                self.calcul_data.append(data)

            print("종목 이름: %s \n" % self.calcul_data[0][1])

            # Write CSV
            wr = csv.writer(f)
            wr.writerows(self.calcul_data)
            self.calculator_event_loop.exit()
