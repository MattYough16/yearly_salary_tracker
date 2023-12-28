from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
import os
from salary_calculator import salary_calculator

def enter_amount():
    adder = salary_calculator()

    status = adder.enter_amount(sAmount.text(), Income_check.isChecked(), makeup_check.isChecked(), es_check.isChecked(), Bar_check.isChecked())
    sAmountShow.setText(status)

def show_current_salary():
    calculator = salary_calculator()

    salary = calculator.calc_salary(Net_check.isChecked(), Gross_check.isChecked(), sYear.text())
    sOut.setText(salary)

###### GUI ######

app = QApplication([])

w = QWidget() 
w.setGeometry(200,200,425,240) 
#############################################################################################################

# Makeup
sMakeup_Label = QLabel(w)
sMakeup_Label.move(2,2)
sMakeup_Label.setText("Makeup:")

makeup_check = QCheckBox(w) 
makeup_check.move(55,2)

# Esthetician
sEs_label = QLabel(w)
sEs_label.move(90,2)
sEs_label.setText("Esthetician:")

es_check = QCheckBox(w) 
es_check.move(160,2)

# Bartending
sBar_label = QLabel(w)
sBar_label.move(195,2)
sBar_label.setText("Bartending:")

Bar_check = QCheckBox(w) 
Bar_check.move(265,2)

# Income
bIncome_label = QLabel(w)
bIncome_label.move(335,2)
bIncome_label.setText("Income:")

Income_check = QCheckBox(w) 
Income_check.move(385,2)

# Expense
bExpense_label = QLabel(w)
bExpense_label.move(335,27)
bExpense_label.setText("Expense:")

Expense_check = QCheckBox(w) 
Expense_check.move(390,27)

#############################################################################################################

# Adding a Label for Dollar Amount
sDollar_label = QLabel(w)
sDollar_label.move(10,27)
sDollar_label.setText("Dollar Amount")

# Adding a Label for $
sDollar = QLabel(w)
sDollar.move(2,52)
sDollar.setText("$")

# Adding a Text Entry Box for Dollar Amount
sAmount = QLineEdit(w)
sAmount.setGeometry(15, 48, 75, 30) 

#############################################################################################################
# Adding Label for Status
sDollar_label = QLabel(w)
sDollar_label.move(260,27)
sDollar_label.setText("Status")

# Adding a Text Entry Box for Status
sAmountShow = QLineEdit(w)
sAmountShow.setGeometry(230, 48, 110, 30) 

#############################################################################################################

# Adding a Label for Year
sYear_label = QLabel(w)
sYear_label.move(20,120)
sYear_label.setText("Year")

# Adding a Text Entry Box for Year
sYear = QLineEdit(w)
sYear.setGeometry(2, 140, 75, 30) 

#############################################################################################################

# Adding Button to Enter Dollar Amount
Enter_btn = QPushButton(w)
Enter_btn.setGeometry(110, 30, 120, 50)
Enter_btn.setText("Enter Amount")
Enter_btn.clicked.connect(enter_amount)

#############################################################################################################
# Addint a Button to Display Salary
Display_btn = QPushButton(w)
Display_btn.setGeometry(80, 120, 120, 50)
Display_btn.setText("Display Salary")
Display_btn.clicked.connect(show_current_salary)

# Adding a Text Entry Box for Displaying Salary
sOut = QLineEdit(w)
sOut.setGeometry(2, 175, 195, 50) 

# Net
bNet_label = QLabel(w)
bNet_label.move(215,120)
bNet_label.setText("Net:")

Net_check = QCheckBox(w) 
Net_check.move(245,120)

# Gross
bGross_label = QLabel(w)
bGross_label.move(215,145)
bGross_label.setText("Gross:")

Gross_check = QCheckBox(w) 
Gross_check.move(255,145)

#############################################################################################################

# Execute GUI
w.show()
app.exec()