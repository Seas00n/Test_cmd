from PyQt5 import QtCore, QtGui, QtWidgets
import numpy
import sys
from PyQt5.Qt import *

import Calculate_cmd
import Search_Cmd
from GUI.app import *
import time
from Calculate_cmd import *
from Search_Cmd import *
import unicodedata


class TestCMD(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(TestCMD, self).__init__(parent=parent)
        self.setupUi(self)
        self.set_Limit_Value()
        self.btn_state_init()
        self.servor_or_MIT = None
        self.working_mode = None
        self.combox_init()
        self.line_edit_init()
        self.Pos = 0.0
        self.I = 0.0
        self.Vel = 0.0
        self.Accel = 0.0
        self.deviceID = 2
        self.IDLineEdit.setText(self.deviceID.__str__())
        can_id = calculate_ID(self.deviceID, CAN_SET_ORIGIN)
        self.SetOriginTextBrowser.setText(can_id + "00")

    def set_Limit_Value(self):
        self.pos_max = Calculate_cmd.pos_max
        self.MaxPosLabel.setText('<' + self.pos_max.__str__()+'rad/s')
        self.vel_max = Calculate_cmd.vel_max
        self.MaxVelLabel.setText('<' + self.vel_max.__str__()[0:3]+'rad/s')
        self.I_max = Calculate_cmd.current_max
        self.MaxCurLabel.setText('<' + self.I_max.__str__()+"A")
        self.A_max = Calculate_cmd.accel_max
        self.MaxAccelLabel.setText('<' + self.A_max.__str__()+"erpm/s")
        self.Kp_max = Calculate_cmd.Kp_max
        self.MaxKpLabel.setText('<' + self.Kp_max.__str__())
        self.Kd_max = Calculate_cmd.Kd_max
        self.MaxKdLabel.setText('<' + self.Kd_max.__str__())

    def combox_init(self):
        self.Servor_Or_MIT_Combobox.clear()
        self.Servor_Or_MIT_Combobox.addItem("Servor")
        self.Servor_Or_MIT_Combobox.addItem("MIT")
        self.ModeCombobox.clear()
        print('combox init')

    def btn_state_init(self):
        self.CalculatePushButton.setEnabled(False)
        self.SearchPushButton.setEnabled(True)
        self.ServorOrMITModeUpdateBtn.setEnabled(True)
        self.ModeUpdateBtn.setEnabled(False)
        self.CalculatePushButton.clicked.connect(self.CalculateButtonPushCallback)
        self.ServorOrMITModeUpdateBtn.clicked.connect(self.ServorOrMITModeUpdateButtonPushCallback)
        self.SearchPushButton.clicked.connect(self.SearchButtonPushCallback)
        self.ModeUpdateBtn.clicked.connect(self.ModeUpdateButtonPushCallback)
        print('button init')

    def line_edit_init(self):
        self.CurrentLineEdit.setText('0.0')
        self.PositionLineEdit.setText('0.0')
        self.VelocityLineEdit.setText('0.0')

    def CalculateButtonPushCallback(self):
        print("Calculate CMD in {}-{} Mode".format(self.servor_or_MIT, self.working_mode))
        self.CalculatorBrowser.clear()
        if str.isdigit(self.IDLineEdit.text()):
            self.deviceID = int(self.IDLineEdit.text())
        else:
            print('ID not Digit')
            return

        if self.working_mode == 'Current Mode':
            self.PositionLineEdit.setText('0.0')
            self.VelocityLineEdit.setText('0.0')
            if isfloat(self.CurrentLineEdit.text()):
                self.I = float(self.CurrentLineEdit.text())
                cmd = calculate_current_cmd(self.I)
                can_id = calculate_ID(self.deviceID, CAN_SET_CURRENT)
                self.CalculatorBrowser.setText(can_id + cmd)
            else:
                print('Please Enter a Number Current')
        elif self.working_mode == 'Position Mode':
            self.CurrentLineEdit.setText('0.0')
            self.VelocityLineEdit.setText('0.0')
            if isfloat(self.PositionLineEdit.text()):
                self.Pos = float(self.PositionLineEdit.text())
                cmd = calculate_position_cmd(self.Pos)
                can_id = calculate_ID(self.deviceID, CAN_SET_POSITION)
                self.CalculatorBrowser.setText(can_id + cmd)
            else:
                print('Please Enter a Number Position')
        elif self.working_mode == 'Velocity Mode':
            self.CurrentLineEdit.setText('0.0')
            self.PositionLineEdit.setText('0.0')
            if isfloat(self.VelocityLineEdit.text()):
                self.Vel = float(self.VelocityLineEdit.text())
                cmd = calculate_velocity_cmd(self.Vel)
                can_id = calculate_ID(self.deviceID, CAN_SET_VELOCITY)
                self.CalculatorBrowser.setText(can_id + cmd)
            else:
                print('Please Enter a Number Velocity')
        elif self.working_mode == 'P&S Mode':
            self.CurrentLineEdit.setText('0.0')
            if isfloat(self.PositionLineEdit.text()) and \
                    isfloat(self.VelocityLineEdit.text()) and \
                    isfloat(self.AccelLineEdit.text()):
                self.Pos = float(self.PositionLineEdit.text())
                self.Vel = float(self.VelocityLineEdit.text())
                self.Accel = float(self.AccelLineEdit.text())
                can_id = calculate_ID(self.deviceID, CAN_SET_POS_SPD)
                cmd = calculate_p_and_s_cmd(self.Pos, self.Vel, self.Accel)
                self.CalculatorBrowser.setText(can_id + cmd)
            else:
                print("Please Enter Numbers")
        elif self.working_mode == 'MIT Mode':
            if isfloat(self.PositionLineEdit.text()) and \
                    isfloat(self.VelocityLineEdit.text()) and \
                    isfloat(self.TorqueLineEdit.text()) and \
                    isfloat(self.KpLineEdit.text()) and \
                    isfloat(self.KdLineEdit.text()):
                self.Pos = float(self.PositionLineEdit.text())
                self.Vel = float(self.VelocityLineEdit.text())
                self.Torque = float(self.TorqueLineEdit.text())
                self.Kp = float(self.KpLineEdit.text())
                self.Kd = float(self.KdLineEdit.text())
                can_id = calculate_ID(self.deviceID, CAN_MIT)
                cmd = calculate_mit_cmd(self.Pos, self.Vel, self.Torque, self.Kp, self.Kd)
                self.CalculatorBrowser.setText(can_id + cmd)
            else:
                print("Please Enter Numbers")
        else:
            print('Wrong Mode')

    def SearchButtonPushCallback(self):
        cmd = self.SearchLineEdit.text()
        print("search cmd: {}".format(cmd))
        info = Search_Cmd.unpack_cmd(cmd)
        self.SearchTextBrowser.setText(info)

    def ServorOrMITModeUpdateButtonPushCallback(self):
        if self.servor_or_MIT != self.Servor_Or_MIT_Combobox.currentText():
            self.ModeUpdateBtn.setEnabled(False)
            self.CalculatePushButton.setEnabled(False)
            self.working_mode = None
        if self.Servor_Or_MIT_Combobox.currentText() == "Servor":
            self.servor_or_MIT = "Servor"
            self.ModeUpdateBtn.setEnabled(True)
            self.ModeCombobox.clear()
            self.ModeCombobox.addItem("Current Mode")
            self.ModeCombobox.addItem("Position Mode")
            self.ModeCombobox.addItem("Velocity Mode")
            self.ModeCombobox.addItem("P&S Mode")
            print("Choose Servor Mode")
        elif self.Servor_Or_MIT_Combobox.currentText() == "MIT":
            self.servor_or_MIT = "MIT"
            self.ModeUpdateBtn.setEnabled(True)
            self.ModeCombobox.clear()
            self.ModeCombobox.addItem("MIT Mode")
            print("Choose MIT Mode")
        else:
            print("Choose Servor or MIT")

    def ModeUpdateButtonPushCallback(self):
        if self.ModeCombobox.currentText() is not None:
            self.working_mode = self.ModeCombobox.currentText()
            self.CalculatePushButton.setEnabled(True)
            print("Choose Mode {}".format(self.working_mode))


def isfloat(str):
    try:
        float(str)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(str)
        return True
    except (TypeError, ValueError):
        pass
        return False


if __name__ == '__main__':
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    w = TestCMD()
    w.show()
    sys.exit(app.exec())
