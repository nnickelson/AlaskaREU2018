# RK Estimator method for CO2 emissions and costs
# Estimator based on method by Dr. Vladimir Alexeev
# GUI by Nathan Nickelson

# Class Window GUI File 

import sys
import pyqtgraph as pg
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyqtgraph.Qt import *
from pyqtgraph import *
import ClimateGameRK724 as rk
import random as rn


class Ui_MainWindow(object):

    ########################################################################################################!!!!!
    ### GUI Initialization and setup                           #############################################!!!!!
    ### After this section is the event handlers               #############################################!!!!!
    ### The last section is the RK estimator algorithm         #############################################!!!!!
    ########################################################################################################!!!!!

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 950)

        self.numSC = 5                                  #Number of scenarios
        self.xArr = []
        self.costArr = []
        self.minPlayers = 2
        self.maxPlayers = 4

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #### Graph Area ###################################################
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setYRange(0.0, 3.0)
        self.graphicsView.setGeometry(QtCore.QRect(20, 20, 1100, 600))
        self.graphicsView.plotItem.showGrid(y=True, x=True, alpha=0.65)

        #### Scenario Checkboxes ##########################################
        self.scenarios = QtWidgets.QGroupBox(self.centralwidget)                          
        self.scenarios.setGeometry(QtCore.QRect(20, 650, 200, 200)) 
        self.scenarios.setStyleSheet("QGroupBox#scenarios { border: 1px solid black;}")                      
        self.scenarios.setObjectName("scenarios")   
        
        self.rkm = []
        self.scenarioRadioButtons = []
        self.scenarioShowGraphCheckboxes = []
        self.scenarioPlayers = []
        self.scenarioButtonGroup = QtWidgets.QButtonGroup()

        self.nsp = QtWidgets.QLabel(self.scenarios)
        self.nsp.setText("Show  Edit             # of players")
        self.nsp.move(5, 10)
        for i in range(self.numSC):

            self.rkm.append(rk.RKMethod())
            self.xArr.append(None)
            self.costArr.append(None)

            self.scenarioShowGraphCheckboxes.append(QtWidgets.QCheckBox(self.scenarios))
            self.scenarioShowGraphCheckboxes[i].move(10, 52 + i * 25)
            self.scenarioShowGraphCheckboxes[i].setChecked(True)
            self.scenarioShowGraphCheckboxes[i].stateChanged.connect(self.scenarioCheckbox_clicked)

            self.scenarioRadioButtons.append(QtWidgets.QRadioButton(self.scenarios))
            self.scenarioButtonGroup.addButton(self.scenarioRadioButtons[i], i)
            self.scenarioRadioButtons[i].setText("Scenario-{}".format(i+1))
            self.scenarioRadioButtons[i].move(45, 50 + i * 25)

            self.scenarioPlayers.append(QtWidgets.QLineEdit(self.scenarios))
            self.scenarioPlayers[i].setGeometry(145, 50 + i * 25, 30, 20 )
            self.scenarioPlayers[i].setValidator(QtGui.QIntValidator())
            self.scenarioPlayers[i].setMaxLength(2)
            self.scenarioPlayers[i].editingFinished.connect(self.playersChanged)

        self.scenarioButtonGroup.buttonClicked.connect(self.scenarioRadioButton_clicked)
        self.scenarioRadioButtons[0].toggle()
        self.currentScenario = 0
        #############################################################################################

        #### Stacked Slider Widget Pages ###################################################################
        self.betaSlider = []
        self.betaLabel = []
        self.lambdaSlider = []
        self.lambdaLabel = []
        self.stackedSliderWidgetPage = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedSliderWidgetPage.setGeometry(1150, 20, 200, 200)
        self.stackedSliderWidgetPage.setObjectName("stackedSliderWidgetPage")
        self.stackedSliderWidgetPage.setStyleSheet("#stackedSliderWidgetPage { border: 1px solid black;}")
        self.sliderPage = []                      
        for i in range(self.numSC):
            self.sliderPage.append(QtWidgets.QWidget())
            sliderPageLabel = QtWidgets.QLabel(self.sliderPage[i])
            sliderPageLabel.setText("Slider Page {}".format(i + 1))
            sliderPageLabel.setGeometry(10, 10, 80, 20)
            self.stackedSliderWidgetPage.addWidget(self.sliderPage[i])
            self.betaSlider.append(None)
            self.betaLabel.append(None)
            self.lambdaSlider.append(None)
            self.lambdaLabel.append(None)
        #############################################################################################

        #### Stacked Variables Widget Pages #########################################################
        self.xCheckbox = []
        self.xLabel = []
        self.costCheckbox = []
        self.costLabel = []
        self.stackedVariablesWidgetPage = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedVariablesWidgetPage.setGeometry(1150, 240, 200, 380)
        self.stackedVariablesWidgetPage.setObjectName("stackedVariablesWidgetPage")
        self.stackedVariablesWidgetPage.setStyleSheet("#stackedVariablesWidgetPage { border: 1px solid black;}")
        self.variablesPage = []
        for i in range(self.numSC):
            self.variablesPage.append(QtWidgets.QWidget())
            variablesPageLabel = QtWidgets.QLabel(self.variablesPage[i])
            variablesPageLabel.setText("Variables Page {}".format(i + 1))
            variablesPageLabel.setGeometry(10, 10, 120, 20)
            self.stackedVariablesWidgetPage.addWidget(self.variablesPage[i])
            self.xCheckbox.append(None)
            self.xLabel.append(None)
            self.costCheckbox.append(None)
            self.costLabel.append(None)
        #############################################################################################

        #### Stacked Cost Widget Pages ##############################################################
        self.costLabelbox = []
        self.stackedCostsWidgetPage = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedCostsWidgetPage.setGeometry(250, 650, 200, 200)
        self.stackedCostsWidgetPage.setObjectName("stackedCostsWidgetPage")
        self.stackedCostsWidgetPage.setStyleSheet("#stackedCostsWidgetPage { border: 1px solid black;}")
        self.costsPage = []
        for i in range(self.numSC):
            self.costsPage.append(QtWidgets.QWidget())
            costsPageLabel = QtWidgets.QLabel(self.costsPage[i])
            costsPageLabel.setText("Total Costs Page {}".format(i + 1))
            costsPageLabel.setGeometry(5, 10, 120, 20)
            self.stackedCostsWidgetPage.addWidget(self.costsPage[i])
            self.costLabelbox.append(None)
        #############################################################################################

        ### Stacked Payoff Matrix Widget Pages ######################################################
        self.payoffBox = []
        self.stackedPayoffWidgetPage = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedPayoffWidgetPage.setGeometry(475, 650, 400, 200)
        self.stackedPayoffWidgetPage.setObjectName("stackedPayoffWidgetPage")
        self.stackedPayoffWidgetPage.setStyleSheet("#stackedPayoffWidgetPage { border: 1px solid black;}")
        self.payoffPage = []
        for i in range(self.numSC):
            self.payoffPage.append(QtWidgets.QWidget())
            payoffPageLabel = QtWidgets.QLabel(self.payoffPage[i])
            payoffPageLabel.setText("Payoff Matrix Page {}".format(i + 1))
            payoffPageLabel.setGeometry(10, 10, 120, 20)
            self.stackedPayoffWidgetPage.addWidget(self.payoffPage[i])
            self.payoffBox.append(None)
        #############################################################################################

        #### Select Strategy Page ###################################################################
        self.strategyBox = []
        self.stackedStrategyWidgetPage = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedStrategyWidgetPage.setGeometry(900, 650, 450, 200)
        self.stackedStrategyWidgetPage.setObjectName("stackedStrategyWidgetPage")
        self.stackedStrategyWidgetPage.setStyleSheet("#stackedStrategyWidgetPage { border: 1px solid black;}")
        self.strategyPage = []
        for i in range(self.numSC):
            self.strategyPage.append(QtWidgets.QWidget())
            strategyPageLabel = QtWidgets.QLabel(self.strategyPage[i])
            strategyPageLabel.setText("Strategy Page {}".format(i + 1))
            strategyPageLabel.setGeometry(10, 10, 120, 20)
            self.stackedStrategyWidgetPage.addWidget(self.strategyPage[i])
            self.strategyBox.append(None)
        #############################################################################################

        #############################################################################################
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #############################################################################################



    ### Scenario Radio edit Buttons #################################################################
    ### depending on the radio button selected, the variables and sliders 
    ### of that scenario are visible and can be edited 

    def scenarioRadioButton_clicked(self):
        index = self.scenarioButtonGroup.checkedId() 
        self.stackedSliderWidgetPage.setCurrentIndex(index)
        self.stackedVariablesWidgetPage.setCurrentIndex(index)
        self.stackedCostsWidgetPage.setCurrentIndex(index)
        self.stackedPayoffWidgetPage.setCurrentIndex(index)
        self.stackedStrategyWidgetPage.setCurrentIndex(index)

    ### Scenario CheckBox Clicked ###################################################################
    ### clears and plots all of the plots of a scenario that have their checkbox checked
    
    def scenarioCheckbox_clicked(self):
        index = -1
        sender = self.graphicsView.sender()
        for button in self.scenarioShowGraphCheckboxes:
            if sender == button:
                index = self.scenarioShowGraphCheckboxes.index(button)
                print("Scenario {} ----".format(index))
                if self.xCheckbox[index] != None:
                    for box in self.xCheckbox[index]:
                        if button.isChecked():
                            self.xPlots(index, self.xCheckbox[index].index(box), True)
                            self.costPlots(index, self.xCheckbox[index].index(box), True)
                        else: 
                            #print("len of costCheckbox = {}". format(len(self.costCheckbox[index])))
                            self.xPlots(index, self.xCheckbox[index].index(box), False)
                            #print("xplots cleared")
                            self.costPlots(index, self.xCheckbox[index].index(box), False)
                            #print("cost plots cleared")

    #### Set Sliders on The Page ####################################################################
    #### the sliders are on a stacked widget page. If the number of players  
    #### is set or altered for a particular page, this also sets the number  
    #### of sliders equal to the number of players on the page and then      
    #### sets the current widget page to whichever scenario was changed 

    def setSlidersOnPage(self):
        p = self.stackedSliderWidgetPage.currentIndex()
        #print("current stackedsliderwidget page = {}".format(p)) 
        self.stackedSliderWidgetPage.removeWidget(self.sliderPage[p])
        self.sliderPage[p] = QtWidgets.QWidget()
        
        tempSlider = []
        tempLabel = []

        for j in range(int(self.scenarioPlayers[p].text())):
            tempSlider.append(QtWidgets.QSlider(self.sliderPage[p]))
            tempSlider[j].setGeometry(QtCore.QRect(30, 60 + j*30, 75, 15))
            tempSlider[j].setOrientation(QtCore.Qt.Horizontal)
            tempSlider[j].setObjectName("LS{}{}".format(p,j))
            tempSlider[j].setMinimum(0)
            tempSlider[j].setMaximum(1000)
            tempSlider[j].setValue(rn.randint(0,1000))
            self.rkm[p].alam[j] = tempSlider[j].value()/100.0
            tempSlider[j].valueChanged.connect(self.lambdaChanged)
            tempSlider[j].sliderReleased.connect(self.lambdaReleased)
            
            tempLabel.append(QtWidgets.QLabel(self.sliderPage[p]))
            tempLabel[j].setGeometry(QtCore.QRect(110, 60 + j*30, 75, 15))
            tempLabel[j].setText("   L{} = {}".format(j+1, tempSlider[j].value()/100.0))
            tempLabel[j].setObjectName("LL{}{}".format(p,j))
        
        self.betaSlider[p] = QtWidgets.QSlider(self.sliderPage[p])
        self.betaSlider[p].setGeometry(QtCore.QRect(30, 35, 75, 15))
        self.betaSlider[p].setOrientation(QtCore.Qt.Horizontal)
        self.betaSlider[p].setObjectName("betaSlider{}".format(p))
        self.betaSlider[p].setMinimum(10)
        self.betaSlider[p].setMaximum(1000)
        self.betaSlider[p].setValue(100)
        self.betaSlider[p].valueChanged.connect(self.betaChanged)
        self.betaSlider[p].sliderReleased.connect(self.betaReleased)

        self.betaLabel[p] = QtWidgets.QLabel(self.sliderPage[p])
        self.betaLabel[p].setGeometry(QtCore.QRect(110, 35, 75, 15))
        self.betaLabel[p].setText("Beta = {}".format(self.betaSlider[p].value()/100))
        self.betaLabel[p].setObjectName("betaLabel")
        
        sliderPageLabel = QtWidgets.QLabel(self.sliderPage[p])
        sliderPageLabel.setText("Slider Page {}".format(p + 1))
        sliderPageLabel.setGeometry(10, 10, 80, 20)

        self.lambdaSlider[p] = tempSlider
        self.lambdaLabel[p] = tempLabel
        self.stackedSliderWidgetPage.insertWidget(p, self.sliderPage[p])
        self.stackedSliderWidgetPage.setCurrentIndex(p)
        
    #### Set Variables on the Page ##################################################################
    #### sets the checkboxes for making visible and clearing the x plots and cost 
    #### plots of each page. If the number of players is either set or changed,   
    #### this page will change the number of x and cost checkboxes to match       

    def setVariablesOnPage(self, p):
        self.stackedVariablesWidgetPage.removeWidget(self.variablesPage[p])
        self.variablesPage[p] = QtWidgets.QWidget()

        tempX = []
        tempXLabel = []
        tempCost = []
        tempCostLabel = []

        for j in range(int(self.scenarioPlayers[p].text())):
            tempX.append(QtWidgets.QCheckBox(self.variablesPage[p]))
            tempXLabel.append(QtWidgets.QLabel(self.variablesPage[p]))
            tempCost.append(QtWidgets.QCheckBox(self.variablesPage[p]))
            tempCostLabel.append(QtWidgets.QLabel(self.variablesPage[p]))

            tempX[j].move(40, 100 + j*50)
            tempX[j].stateChanged.connect(self.xCheck)
            tempXLabel[j].setGeometry(QtCore.QRect(80, 100 + j*50, 125, 15))
            tempXLabel[j].setText("X{}".format(j+1))
            tempCost[j].move(40, 125 + j*50)
            tempCost[j].stateChanged.connect(self.costCheck)
            tempCostLabel[j].setGeometry(QtCore.QRect(80, 125 + j*50, 125, 15))
            tempCostLabel[j].setText("Cost{}".format(j+1))

            self.rkm[p].plotX.append(None)
            self.rkm[p].plotCost.append(None)
        
        allX = QtWidgets.QCheckBox(self.variablesPage[p])
        allX.move(40, 35)
        allXLabel = QtWidgets.QLabel(self.variablesPage[p])
        allXLabel.setGeometry(65, 30, 75, 25)
        allXLabel.setText("ALL X's")
        allX.stateChanged.connect(self.checkAllXs)
        allCost = QtWidgets.QCheckBox(self.variablesPage[p])
        allCost.move(40, 55)
        allCostLabel = QtWidgets.QLabel(self.variablesPage[p])
        allCostLabel.setGeometry(65, 50, 75, 25)
        allCostLabel.setText("ALL Costs")
        allCost.stateChanged.connect(self.checkAllCosts)

        variablesPageLabel = QtWidgets.QLabel(self.variablesPage[p])
        variablesPageLabel.setText("Variables Page {}".format(p + 1))
        variablesPageLabel.setGeometry(10, 10, 120, 20)
        
        self.xCheckbox[p] = tempX
        self.xLabel[p] = tempXLabel
        self.costCheckbox[p] = tempCost
        self.costLabel[p] = tempCostLabel
        self.stackedVariablesWidgetPage.insertWidget(p, self.variablesPage[p])
        self.stackedVariablesWidgetPage.setCurrentIndex(p)
        
    #### Set Costs on the Page ######################################################################
    #### this function updates the cost values of the page whenever 
    #### the number of players is set or altered or any of the sliders
    #### have been adjusted

    def setCostsOnPage(self, p):
        self.stackedCostsWidgetPage.removeWidget(self.costsPage[p])
        self.costsPage[p] = QtWidgets.QWidget()
        
        tempCostLabel = []

        for j in range(int(self.scenarioPlayers[p].text())):
            tempCostLabel.append(QtWidgets.QLabel(self.costsPage[p]))
            tempCostLabel[j].setGeometry(QtCore.QRect(10, 45 + j*25, 225, 15))
            tempCostLabel[j].setText("Cost {} Totals = {:0.3f}".format((j+1), self.rkm[p].costTotals[j]))
        
        costsPageLabel = QtWidgets.QLabel(self.costsPage[p])
        costsPageLabel.setText("Costs Page {}".format(p + 1))
        costsPageLabel.setGeometry(10, 10, 120, 20)

        self.costLabelbox[p] = tempCostLabel
        self.stackedCostsWidgetPage.insertWidget(p, self.costsPage[p])
        self.stackedCostsWidgetPage.setCurrentIndex(p)

    #### Set Payoff Matrix ##########################################################################
    #### this function sets up the payoff matrix for each scenario
    #### it allows for any of the line edit boxes to be changed
    #### this will call a function to edit the graphs and costs for that scenario

    def setPayoffOnPage(self, p):
        self.stackedPayoffWidgetPage.removeWidget(self.payoffPage[p])
        self.payoffPage[p] = QtWidgets.QWidget()

        tempPayoffBox = []
        tempPayoffLabel = []

        for j in range(2*int(self.scenarioPlayers[p].text())):
            tempPayoffBox.append(QtWidgets.QLineEdit(self.payoffPage[p]))
            #print ("j%2 = {} .... j/2 = {}".format(j%2 , int(j/2) ))
            tempPayoffBox[j].setGeometry(QtCore.QRect(160 + (j%2)*100, 50 + int(j/2)*35, 100, 35))
            font = tempPayoffBox[j].font()
            font.setPointSize(16)
            tempPayoffBox[j].setFont(font)
            tempPayoffBox[j].setAlignment(QtCore.Qt.AlignCenter)
            tempPayoffBox[j].setValidator(QtGui.QIntValidator())
            tempPayoffBox[j].editingFinished.connect(self.payoffChanged)
            tempPayoffBox[j].setText("68")
            if (j%2 == 0):
                tempPayoffLabel.append(QtWidgets.QLabel(self.payoffPage[p]))
                tempPayoffLabel[int(j/2)].setGeometry(QtCore.QRect(10, 50 + int(j/2)*35, 100, 35))
                tempPayoffLabel[int(j/2)].setText("Player {} Utility: ".format(int(j/2)+1))


        payoffPageLabel = QtWidgets.QLabel(self.payoffPage[p])
        payoffPageLabel.setText("Payoff Matrix Page {}".format(p + 1))
        payoffPageLabel.setGeometry(10, 10, 120, 20)
        payoffCoopLabel = QtWidgets.QLabel(self.payoffPage[p])
        payoffCoopLabel.setText("Coop Strategy")
        payoffCoopLabel.setGeometry(160, 20, 120, 20)
        payoffDefLabel = QtWidgets.QLabel(self.payoffPage[p])
        payoffDefLabel.setText("Defect Strategy")
        payoffDefLabel.setGeometry(260, 20, 120, 20)


        self.payoffBox[p] = tempPayoffBox
        self.stackedPayoffWidgetPage.insertWidget(p, self.payoffPage[p])
        self.stackedPayoffWidgetPage.setCurrentIndex(p)

    #### Set Strategies Page ########################################################################
    #### allows for each player to have an individual 'c'ooperate or 'd'efect strategy
    #### for each turn. Allows for a sequence of strategies which will be executed in 
    #### order and then repeated until the end turns is reached

    def setStrategiesOnPage(self, p):
        self.stackedStrategyWidgetPage.removeWidget(self.strategyPage[p])
        self.strategyPage[p] = QtWidgets.QWidget()

        tempStrategyBox = []
        tempStrategyLabel = []

        for j in range(int(self.scenarioPlayers[p].text())):
            tempStrategyBox.append(QtWidgets.QLineEdit(self.strategyPage[p]))
            tempStrategyBox[j].setGeometry(QtCore.QRect(120, 40 + j*40, 225, 35))
            font = tempStrategyBox[j].font()
            font.setPointSize(14)
            tempStrategyBox[j].setFont(font)
            tempStrategyBox[j].setAlignment(QtCore.Qt.AlignCenter)
            tempStrategyBox[j].setText("C")
            tempStrategyBox[j].editingFinished.connect(self.strategyChanged)
            
            tempStrategyLabel.append(QtWidgets.QLabel(self.strategyPage[p]))
            tempStrategyLabel[j].setGeometry(QtCore.QRect(10, 40 + j*40, 100, 35))
            tempStrategyLabel[j].setText("Player {} Strategy: ".format(j+1))

        
        strategiesPageLabel = QtWidgets.QLabel(self.strategyPage[p])
        strategiesPageLabel.setText("Strategy Page {}".format(p + 1))
        strategiesPageLabel.setGeometry(10, 10, 120, 20)

        self.strategyBox[p] = tempStrategyBox
        self.stackedStrategyWidgetPage.insertWidget(p, self.strategyPage[p])
        self.stackedStrategyWidgetPage.setCurrentIndex(p)
        

    #### Players Changed ############################################################################
    #### resets a scenario to the changed number of players from the line edit box. It then calls 
    #### a reset of the other widget boxes of the same current page to reset them, too
      
    def playersChanged(self):
        self.graphicsView.plotItem.plot(clear=True)
        sender = self.graphicsView.sender()
        for button in self.scenarioPlayers:
            if sender == button:
                index = self.scenarioPlayers.index(button)
        if int(self.scenarioPlayers[index].text()) < self.minPlayers:
            self.scenarioPlayers[index].setText("2")
        if int(self.scenarioPlayers[index].text()) > self.maxPlayers:
            self.scenarioPlayers[index].setText("4")
        numPlay = int(self.scenarioPlayers[index].text())
        self.rkm[index].changeNumPlayers(numPlay)
        self.scenarioRadioButtons[index].setChecked(True)
        self.stackedSliderWidgetPage.setCurrentIndex(index)
        self.setSlidersOnPage()
        self.setVariablesOnPage(index)
        self.setCostsOnPage(index)
        self.setPayoffOnPage(index)
        self.setStrategiesOnPage(index)
        self.graphicsUpdate()

    
    def lambdaChanged(self):
        p = self.stackedSliderWidgetPage.currentIndex()
        sender = self.graphicsView.sender()
        for slider in self.lambdaSlider[p]:
            if slider == sender:
                index = self.lambdaSlider[p].index(slider)
                val = self.lambdaSlider[p][index].value()/100.0
                self.lambdaLabel[p][index].setText("   L{} = {}".format(index+1, val))


    def lambdaReleased(self):
        print("released L")
        p = self.stackedSliderWidgetPage.currentIndex()
        val = -1
        sender = self.graphicsView.sender()
        for slider in self.lambdaSlider[p]:
            if slider == sender:
                index = self.lambdaSlider[p].index(slider)
                val = self.lambdaSlider[p][index].value()/100.0
        print("lambda totals = {}".format(self.rkm[p].alam))
        if val != -1:
            self.rkm[p].alam[index] = val
        print("Graphics update")
        self.graphicsUpdate()


    def betaChanged(self):
        p = self.stackedSliderWidgetPage.currentIndex()
        val = self.betaSlider[p].value()/100.0
        self.betaLabel[p].setText("Beta = {}".format(val))


    def betaReleased(self):
        p = self.stackedSliderWidgetPage.currentIndex()
        val = self.betaSlider[p].value()/100.0
        print(val)
        self.rkm[p].beta = val
        self.graphicsUpdate()


    def payoffChanged(self):
        p = self.stackedPayoffWidgetPage.currentIndex()
        sender = self.graphicsView.sender()
        for box in self.payoffBox[p]:
            if box == sender:
                index = self.payoffBox[p].index(box)
        i =  int(index/2)
        j = index%2
        #print("i = {} -- j = {}".format(i, j))
        #print("payoff text = {}".format(self.payoffBox[p][index].text()))
        if self.payoffBox[p][index].text() == "":
            #print("setting text")
            self.payoffBox[p][index].setText("60")
        if self.payoffBox[p][index].text() != "":
            if int(self.payoffBox[p][index].text())/10.0 == self.rkm[p].payoff[i][j]:
                return
            if int(self.payoffBox[p][index].text()) < 0:
                self.payoffBox[p][index].setText("0")
            if int(self.payoffBox[p][index].text()) >1000:
                self.payoffBox[p][index].setText("1000")
            self.rkm[p].payoff[i][j] = int(self.payoffBox[p][index].text())/100.0
        #print("payoff = {}".format(self.rkm[p].payoff))
        #print("index = {}, p = {}".format(index, p))
        #print("size rkm = {}, size strategybox = {}, size strat[p] = {}".format(len(self.rkm), len(self.strategyBox),len(self.strategyBox[p])))
        self.rkm[p].setStrategy(i, self.strategyBox[p][i].text())
        self.graphicsUpdate()

    
    def strategyChanged(self):
        p = self.stackedStrategyWidgetPage.currentIndex()
        sender = self.graphicsView.sender()
        for box in self.strategyBox[p]:
            if box == sender:
                index = self.strategyBox[p].index(box)
        if self.strategyBox[p][index].text() == "":
            self.strategyBox[p][index].setText("C")
        if self.strategyBox[p][index].text() == self.rkm[p].lastStrategy[index]:
            return
        else:
            self.rkm[p].lastStrategy[index] = self.strategyBox[p][index].text()
        self.rkm[p].setStrategy(index, self.strategyBox[p][index].text())
        print("strategy = {}".format(self.rkm[p].strategy))
        self.graphicsUpdate()


    def xCheck(self):
        p = self.stackedSliderWidgetPage.currentIndex()
        sender = self.graphicsView.sender()
        for box in self.xCheckbox[p]:
            index = self.xCheckbox[p].index(box)
            if box == sender:
                if box.isChecked():
                    print("xCheck index {}".format(index))
                    self.xPlots(p, index, True)
                else:
                    print("xCheck index {}".format(index))
                    self.xPlots(p, index, False)
                break

    
    def costCheck(self):
        p = self.stackedSliderWidgetPage.currentIndex()
        sender = self.graphicsView.sender()
        for box in self.costCheckbox[p]:
            index = self.costCheckbox[p].index(box)
            if box == sender:
                if box.isChecked():
                    print("costCheck index {}".format(index))
                    self.costPlots(p, index, True)
                else:
                    print("costCheck index {}".format(index))
                    self.costPlots(p, index, False)
                break


    def graphicsUpdate(self):
        self.numPlots()
        self.checkAllBoxStates()
        self.setCostsOnPage(self.stackedSliderWidgetPage.currentIndex())


    def checkAllBoxStates(self):
        self.graphicsView.plotItem.plot(clear=True)
        for sCheck in self.scenarioShowGraphCheckboxes:
            i = self.scenarioShowGraphCheckboxes.index(sCheck)
            if sCheck.isChecked():
                print("no. of players for scenario {} is {}".format(i, self.rkm[i].NP))
                for j in range(self.rkm[i].NP):
                    if self.xCheckbox[i][j].isChecked():
                        #print("{} {} true".format(i, j))
                        self.xPlots(i, j, True)
                    else:
                        #print("{} {} false".format(i, j))
                        self.xPlots(i, j, False)
                    if self.costCheckbox[i][j].isChecked():
                        self.costPlots(i, j, True)
                    else:
                        self.costPlots(i, j, False)

    def checkAllXs(self, state):
        p = self.stackedSliderWidgetPage.currentIndex()
        for box in self.xCheckbox[p]:
            box.setChecked(state)

    def checkAllCosts(self, state):
        p = self.stackedSliderWidgetPage.currentIndex()
        for box in self.costCheckbox[p]:
            box.setChecked(state)

            
    def xPlots(self, p, index, plt):
        if plt is True and self.scenarioShowGraphCheckboxes[p].isChecked() and self.xCheckbox[p][index].isChecked():
            self.rkm[p].plotX[index] = self.graphicsView.plotItem.plot(self.xArr[p][index,:], pen=pg.mkPen((255-50*index, 75+30*index, 0), width=2.5))
        elif (self.rkm[p].plotX[index]) != None: 
            self.rkm[p].plotX[index].clear()

    
    def costPlots(self, p, index, plt):
        if plt is True and self.scenarioShowGraphCheckboxes[p].isChecked() and self.costCheckbox[p][index].isChecked():
            print("drawing costs")
            self.rkm[p].plotCost[index] = self.graphicsView.plotItem.plot(self.costArr[p][index,:], pen=pg.mkPen((0, 255, 0), width=2.5))
        elif (self.rkm[p].plotCost[index]) != None: 
            print("clearing costs")
            self.rkm[p].plotCost[index].clear()

            
        
    # This function calls the RKPlots() function and stores the return values (for plotting the graph)
    # into individual arrays
    def numPlots(self):
        p = self.stackedCostsWidgetPage.currentIndex()
        self.xArr[p], self.costArr[p] = self.rkm[p].RKPlots()