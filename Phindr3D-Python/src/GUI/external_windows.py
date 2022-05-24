from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyqtgraph as pg


class external_windows():
    def buildExtractWindow(self):
        largetext = QFont("Arial", 12, 1)
        win = QDialog()
        win.setWindowTitle("Extract Metadata")
        directory = "Image Root Directory"
        samplefilename = "Sample File Name"
        layout = QGridLayout()
        imagerootbox = QTextEdit()
        imagerootbox.setReadOnly(True)
        imagerootbox.setText(directory)
        imagerootbox.setFixedSize(300,60)
        imagerootbox.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        imagerootbox.setFont(largetext)

        selectimage = QPushButton("Select Image Directory")
        selectimage.setFixedSize(selectimage.minimumSizeHint())
        selectimage.setFixedHeight(40)

        samplefilebox = QTextEdit()
        samplefilebox.setReadOnly(True)
        samplefilebox.setText(samplefilename)
        samplefilebox.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        samplefilebox.setFont(largetext)
        samplefilebox.setFixedSize(450, 30)

        expressionbox = QLineEdit()
        expressionbox.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        expressionbox.setFont(largetext)
        expressionbox.setFixedSize(450, 30)
        expressionbox.setPlaceholderText("Type Regular Expression Here")

        evaluateexpression = QPushButton("Evaluate Regular Expression")
        evaluateexpression.setFixedSize(evaluateexpression.minimumSizeHint())
        evaluateexpression.setFixedHeight(30)

        outputfilebox = QLineEdit()
        outputfilebox.setAlignment(Qt.AlignCenter)
        outputfilebox.setFont(largetext)
        outputfilebox.setPlaceholderText("Output Metadata File Name")
        outputfilebox.setFixedSize(200, 30)

        createfile = QPushButton("Create File")
        createfile.setFixedSize(createfile.minimumSizeHint())
        createfile.setFixedHeight(30)

        cancel = QPushButton("Cancel")
        cancel.setFixedSize(cancel.minimumSizeHint())
        cancel.setFixedHeight(30)

        # button functions

        cancel.clicked.connect(win.close)


        layout.addWidget(imagerootbox, 0, 0, 1, 2)
        layout.addWidget(selectimage, 0, 2, 1, 1)
        layout.addWidget(samplefilebox, 1, 0, 1, 3)
        layout.addWidget(expressionbox, 2, 0, 1, 3)
        layout.addWidget(evaluateexpression, 3, 0, 1, 1)
        layout.addWidget(outputfilebox, 4, 0, 1, 1)
        layout.addWidget(createfile, 4, 1, 1, 1)
        layout.addWidget(cancel, 4, 2, 1, 1)
        layout.setSpacing(10)
        win.setLayout(layout)
        win.setFixedSize(win.minimumSizeHint())

        return win

    def buildResultsWindow(self):
        win = QDialog()
        win.setWindowTitle("Results")
        menubar = QMenuBar()
        file = menubar.addMenu("File")
        inputfile = file.addAction("Input Feature File")
        data = menubar.addMenu("Data Analysis")
        classification = data.addMenu("Classification")
        selectclasses = classification.addAction("Select Classes")
        clustering = data.addMenu("Clustering")
        estimate = clustering.addAction("Estimate Clusters")
        setnumber = clustering.addAction("Set Number of Clusters")
        piemaps = clustering.addAction("Pie Maps")
        export = clustering.addAction("Export Cluster Results")
        plotproperties = menubar.addMenu("Plot Properties")
        rotation = plotproperties.addAction("3D Rotation")
        resetview = plotproperties.addAction("Reset Plot View")

        # menu features go here

        # defining widgets
        box = QGroupBox()
        boxlayout = QGridLayout()
        selectfile = QPushButton("Select Feature File")
        typedropdown = QComboBox()
        typedropdown.addItem("PCA")
        typedropdown.addItem("t-SNE")
        typedropdown.addItem("Sammon")
        twod = QCheckBox("2D")
        threed = QCheckBox("3D")
        dimensionbox = QGroupBox()
        dimensionboxlayout = QHBoxLayout()
        dimensionboxlayout.addWidget(twod)
        dimensionboxlayout.addWidget(threed)
        dimensionbox.setLayout(dimensionboxlayout)
        colordropdown = QComboBox()
        boxlayout.addWidget(selectfile, 0, 0, 3, 1)
        boxlayout.addWidget(QLabel("Plot Type"), 0, 1, 1, 1)
        boxlayout.addWidget(typedropdown, 1, 1, 1, 1)
        boxlayout.addWidget(dimensionbox, 2, 1, 1, 1)
        boxlayout.addWidget(QLabel("Color By"), 0, 2, 1, 1)
        boxlayout.addWidget(colordropdown, 1, 2, 1, 1)
        box.setLayout(boxlayout)

        # button features go here

        # building layout
        layout = QGridLayout()
        plotwindow = pg.plot()
        scatter = pg.ScatterPlotItem(size=10)
        plotwindow.addItem(scatter)
        layout.addWidget(plotwindow, 0, 0, 1, 1)
        layout.addWidget(box, 1, 0, 1, 1)
        plotwindow.setBackground('w')
        layout.setMenuBar(menubar)
        win.setLayout(layout)
        minsize = win.minimumSizeHint()
        minsize.setHeight(win.minimumSizeHint().height() + 200)
        minsize.setWidth(win.minimumSizeHint().width() + 100)
        win.setFixedSize(minsize)
        return win

    def aboutAlert(self):
        alert = QMessageBox()
        alert.setText("talk about the program")
        alert.setWindowTitle("About")
        alert.exec()

    def buildParamWindow(self):
        win = QDialog()
        win.setWindowTitle("Set Parameters")
        winlayout = QGridLayout()

        # super voxel box
        superbox = QGroupBox()
        superbox.setLayout(QGridLayout())
        supersizebox = QGroupBox()
        supersizebox.setLayout(QGridLayout())
        superxin = QLineEdit()
        superyin = QLineEdit()
        superzin = QLineEdit()
        superxin.setFixedWidth(30)
        superyin.setFixedWidth(30)
        superzin.setFixedWidth(30)
        supersizebox.layout().addWidget(superxin, 0, 1, 1, 1)
        supersizebox.layout().addWidget(superyin, 1, 1, 1, 1)
        supersizebox.layout().addWidget(superzin, 2, 1, 1, 1)
        supersizebox.layout().addWidget(QLabel("X"), 0, 0, 1, 1)
        supersizebox.layout().addWidget(QLabel("Y"), 1, 0, 1, 1)
        supersizebox.layout().addWidget(QLabel("Z"), 2, 0, 1, 1)
        supersizebox.setTitle("Size")
        supersizebox.layout().setContentsMargins(20, 10, 20, 20)
        superbox.setTitle("Super Voxel")
        svnum = QLineEdit()
        svnum.setFixedWidth(30)
        superbox.layout().addWidget(svnum, 1, 1, 1, 1)
        superbox.layout().addWidget(QLabel("#SV\n Categories"), 1, 0, 1, 1)
        superbox.layout().addWidget(supersizebox, 0, 0, 1, 2)
        superbox.setFixedWidth(superbox.minimumSizeHint().width() + 20)
        superbox.setFixedHeight(superbox.minimumSizeHint().height() + 20)

        # mega voxel box
        megabox = QGroupBox()
        megabox.setLayout(QGridLayout())
        megasizebox = QGroupBox()
        megasizebox.setLayout(QGridLayout())
        megaxin = QLineEdit()
        megayin = QLineEdit()
        megazin = QLineEdit()
        megaxin.setFixedWidth(30)
        megayin.setFixedWidth(30)
        megazin.setFixedWidth(30)
        megasizebox.layout().addWidget(megaxin, 0, 1, 1, 1)
        megasizebox.layout().addWidget(megayin, 1, 1, 1, 1)
        megasizebox.layout().addWidget(megazin, 2, 1, 1, 1)
        megasizebox.layout().addWidget(QLabel("X"), 0, 0, 1, 1)
        megasizebox.layout().addWidget(QLabel("Y"), 1, 0, 1, 1)
        megasizebox.layout().addWidget(QLabel("Z"), 2, 0, 1, 1)
        megasizebox.setTitle("Size")
        megasizebox.layout().setContentsMargins(20, 10, 20, 20)
        megabox.setTitle("Mega Voxel")
        mvnum = QLineEdit()
        mvnum.setFixedWidth(30)
        megabox.layout().addWidget(mvnum, 1, 1, 1, 1)
        megabox.layout().addWidget(QLabel("#MV\n Categories"), 1, 0, 1, 1)
        megabox.layout().addWidget(megasizebox, 0, 0, 1, 2)
        megabox.setFixedSize(superbox.size())

        # main box
        mainbox = QGroupBox()
        mainbox.setLayout(QGridLayout())
        voxelcategories = QLineEdit()
        voxelcategories.setFixedWidth(30)
        trainingimages = QLineEdit()
        trainingimages.setFixedWidth(30)
        usebackground = QCheckBox("Use Background Voxels for comparing") # text is cutoff, don't know actual line?
        normalise = QCheckBox("Normalise Intesity\n Per Condition")
        trainbycondition = QCheckBox("Train by condition")
        leftdropdown = QComboBox()
        leftdropdown.setEnabled(False)
        rightdropdown = QComboBox()
        rightdropdown.setEnabled(False)
        normalise.clicked.connect(lambda: leftdropdown.setEnabled(not leftdropdown.isEnabled()))
        trainbycondition.clicked.connect(lambda: rightdropdown.setEnabled(not rightdropdown.isEnabled()))

        mainbox.layout().addWidget(QLabel("#Voxel\nCategories"), 0, 0, 1, 1)
        mainbox.layout().addWidget(voxelcategories, 0, 1, 1, 1)
        mainbox.layout().addWidget(QLabel("#Training\nImages"), 0, 3, 1, 1)
        mainbox.layout().addWidget(trainingimages, 0, 4, 1, 1)
        mainbox.layout().addWidget(usebackground, 1, 0, 1, 6)
        mainbox.layout().addWidget(normalise, 2, 0, 1, 3)
        mainbox.layout().addWidget(trainbycondition, 2, 3, 1, 3)
        mainbox.layout().addWidget(leftdropdown, 3, 0, 1, 3)
        mainbox.layout().addWidget(rightdropdown, 3, 3, 1, 3)
        mainbox.setFixedWidth(mainbox.minimumSizeHint().width() + 50)
        mainbox.setFixedHeight(mainbox.minimumSizeHint().height() + 20)

        # reset and done buttons
        reset = QPushButton("Reset")
        done = QPushButton("Done")

        # button behaviours
        def donePressed():
            # When done is pressed, all the inputted values are returned, stored in their place
            # and the window closes
            # Theoretically stored where overall parameters are stored (externally)
            superx = superxin.text()
            supery = superyin.text()
            superz = superzin.text()
            svcategories = svnum.text()
            megax = megaxin.text()
            megay = megayin.text()
            megaz = megazin.text()
            mvcategories = mvnum.text()
            voxelnum = voxelcategories.text()
            trainingnum = trainingimages.text()
            bg = usebackground.isChecked() # For checkboxes, return boolean for if checked or not
            norm = normalise.isChecked()
            conditiontrain = trainbycondition.isChecked()
            # dropdown behaviour goes here <--
            print(superx, supery, superz, svcategories, megax, megay, megaz,
                  mvcategories, voxelnum, trainingnum)
            if bg:
                print("bg")
            if norm:
                print("norm")
            if conditiontrain:
                print("conditiontrain")

            win.close()

        done.clicked.connect(donePressed)
        winlayout.addWidget(superbox, 0, 0, 1, 1)
        winlayout.addWidget(megabox, 0, 1, 1, 1)
        winlayout.addWidget(mainbox, 1, 0, 1, 2)
        winlayout.addWidget(reset, 2, 0, 1, 1)
        winlayout.addWidget(done, 2, 1, 1, 1)
        winlayout.setAlignment(Qt.AlignLeft)
        win.setLayout(winlayout)
        return win