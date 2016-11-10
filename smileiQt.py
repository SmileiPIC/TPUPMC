#!/usr/bin/env python 
"""
Plot fields of smilei simulaition
"""
import sys, os, random

import logging as log

log.basicConfig(level=log.INFO,
    format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-4d: %(message)s',
    datefmt='%m-%d %H:%M',
    )
    
from pprint import pprint

from matplotlib.figure import Figure
from matplotlib.colors import LogNorm
# from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


# from matplotlib.backends import qt_compat
# 
# if qt_compat.QT_API == qt_compat.QT_API_PYSIDE:
#     from PySide.QtCore import *
#     from PySide.QtGui import *
#     from PyQt4 import uic
# else:
#     from PyQt4.QtCore import *
#     from PyQt4.QtGui import *
#     from PyQt4 import uic

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from Smilei import *
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
        
        
class smileiQtPlot(QWidget):
    scalarDict=dict()
    fieldDict=dict()
    phaseDict=dict()
    nplots=0
    ax={}
    dirName='.'
    someCheckBoxChanged=True
    pauseSignal=pyqtSignal()
    shiftPressed=False
    title=''
    
    def __init__(self,parent,dirName):
        super(smileiQtPlot, self).__init__()   
        self.setParent(parent)
        uiFile=os.path.dirname(os.path.realpath(__file__))+'/smileiQtPlot.ui'
        self.ui=uic.loadUi(uiFile,self)
        
        self.dirName=dirName
        self.smilei=Smilei(self.dirName)
        
        self.parent=parent

        self.parent.timer.timeout.connect(self.next)
        self.parent.ui.next.released.connect(self.next)
        self.parent.ui.previous.released.connect(self.previous)
        self.parent.ui.first.released.connect(self.first)
        self.parent.ui.last.released.connect(self.last)
        
        self.pauseSignal.connect(self.parent.pause)

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(dirName)

        self.step=0
        
        self.ui.savePoints.setIcon(self.ui.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.ui.savePoints.released.connect(self.doSavePoints)
                
        self.ui.tabWidget.currentChanged.connect(self.changeTab)
        self.ui.autoScale.stateChanged.connect(self.doPlots)
        
        self.fig = Figure()
        
        self.ui.reload.setIcon(self.ui.style().standardIcon(QStyle.SP_BrowserReload))
        self.ui.reload.released.connect(self.reloadAll)

        
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()
        self.canvas.mpl_connect('motion_notify_event', self.on_movement)
        self.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.canvas.mpl_connect('key_release_event', self.on_key_release)
        self.canvas.mpl_connect('button_press_event', self.on_button_press)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setFixedHeight(18)
        self.canvas.setCursor(Qt.CrossCursor)

        self.ui.plotLayout.addWidget(self.canvas)
        self.ui.plotLayout.addWidget(self.toolbar)

#retrieve stuff from namelist
        self.cell_length=self.smilei.namelist.Main.cell_length[0]
        self.timestep=self.smilei.namelist.Main.timestep
        self.sim_length=self.smilei.namelist.Main.sim_length

#scalars
        scalarSteps=[]
        for scalar in self.smilei.Scalar().getScalars():
            if len(scalarSteps) ==0:
                scalarSteps=self.smilei.Scalar(scalar).getAvailableTimesteps()
            else:
                if not np.array_equal(scalarSteps,self.smilei.Scalar(scalar).getAvailableTimesteps()):
                    log.error("Problem reading scalarSteps %s"%scalar)
            my_button= QCheckBox(scalar)
            my_button.stateChanged.connect(self.checkBoxChanged)
            self.ui.layoutScalars.addWidget(my_button)
            
        self.ui.layoutScalars.addStretch()

#fields
        self.fieldSteps=self.smilei.Field().getAvailableTimesteps()
        if not np.array_equal(scalarSteps,self.fieldSteps): 
            newfieldSteps=[]
            for i in range(0,min(len(scalarSteps),len(self.fieldSteps))):
                if scalarSteps[i] == self.fieldSteps[i]:
                    newfieldSteps.append(scalarSteps[i])
                else:
                    break
            self.fieldSteps=newfieldSteps
            log.warning("Problem reading fieldSteps")
        for field in self.smilei.Field().getFields():
            my_button= QCheckBox(field)
            my_button.stateChanged.connect(self.checkBoxChanged)
            self.ui.layoutFields.addWidget(my_button)

        self.ui.layoutFields.addStretch()

        self.ui.slider.setRange(0,len(self.fieldSteps))
        self.ui.spinStep.setSuffix("/"+str(len(self.fieldSteps)))
        self.ui.spinStep.setMaximum(len(self.fieldSteps))


#phase spaces
        i=0
        # self.smilei.ParticleDiagnostic(0)._type ...
        for phase in self.smilei.namelist.DiagParticles:
            if not np.array_equal(self.fieldSteps,self.smilei.ParticleDiagnostic(i).getAvailableTimesteps()): 
                log.warning("Problem reading phaseSteps")

            name=str(i)+' '
            for ax in phase.axes:
                name+=ax[0] 
            my_button= QCheckBox(name)
            my_button.stateChanged.connect(self.checkBoxChanged)
            self.ui.layoutPhase.addWidget(my_button)
            i=i+1
        self.ui.layoutPhase.addStretch()

        self.load_settings()

        if sys.platform == "darwin":
            self.raise_()
        self.show()
        
        
    def reloadAll(self):
        self.smilei=Smilei(self.dirName)
        self.fieldSteps=self.smilei.Field().getAvailableTimesteps()
        self.ui.slider.setRange(0,len(self.fieldSteps))
        self.ui.spinStep.setSuffix("/"+str(len(self.fieldSteps)))
        self.ui.spinStep.setMaximum(len(self.fieldSteps))
        self.preparePlots()
        
    def doSavePoints(self):
        fname=QFileDialog.getSaveFileName(self, 'Save Point logger', self.dirName, selectedFilter='*.txt')
        if fname:
            f = open(fname, 'w')
            f.write(self.ui.logger.toPlainText())
            f.close()


    def checkBoxChanged(self):
        self.someCheckBoxChanged=True
      
    def load_settings(self):
        settings=QSettings(QFileInfo(__file__).fileName(),"")
        settings.beginGroup(QDir(self.dirName).dirName())
        log.info("settings file: %s"%settings.fileName())
        frames=[self.ui.scalars, self.ui.fields, self.ui.phase]
        for frame in [self.ui.scalars, self.ui.fields, self.ui.phase] :
            settings.beginGroup(frame.objectName())            
            for chkbox in frame.findChildren(QCheckBox):
                chkbox.setChecked(settings.value(chkbox.text())=='true')
            settings.endGroup()
        settings.endGroup()
        self.ui.tabWidget.setCurrentIndex(0)

    def save_settings(self):
        settings=QSettings(QFileInfo(__file__).fileName(),"")
        settings.beginGroup(QDir(self.dirName).dirName())
        frames=[self.ui.scalars, self.ui.fields, self.ui.phase]
        for frame in [self.ui.scalars, self.ui.fields, self.ui.phase] :
            settings.beginGroup(frame.objectName())            
            for chkbox in frame.findChildren(QCheckBox):
                settings.setValue(chkbox.text(),chkbox.isChecked())
            settings.endGroup()
        settings.endGroup()

    def next(self):
        self.ui.slider.setValue(self.step+1)
    
    def previous(self):
        self.ui.slider.setValue(self.step-1)
    
    def first(self):
        self.ui.slider.setValue(0)
    
    def last(self):
        self.ui.slider.setValue(len(self.fieldSteps)-1)
               
    def on_slider_valueChanged(self,step):
        self.step=step
        self.doPlots()
    
    @pyqtSignature("int")
    def on_spinStep_valueChanged(self,my_step):
        self.ui.slider.setValue(my_step)

    @pyqtSignature("int")
    def changeTab(self, tabNum):
        if self.ui.tabWidget.currentIndex()==0:
            self.doPlots()
        else:
            self.pauseSignal.emit()

    def preparePlots(self):
        self.someCheckBoxChanged=False
        
        self.scalarDict=dict()
        self.fieldDict=dict()
        self.phaseDict=dict()

        self.nplots=0
        frames=[self.ui.scalars, self.ui.fields, self.ui.phase]
        for frame in [self.ui.scalars, self.ui.fields, self.ui.phase] :
            for chkbox in frame.findChildren(QCheckBox):
                if chkbox.isChecked() :
                    self.nplots+=1

        self.fig.clear()
        if self.nplots > 0:
            self.title=self.fig.suptitle('')       
            

            self.ax={}
              
            plot=0
            col=0
            log.info("preparing scalars")
            for i in self.ui.scalars.findChildren(QCheckBox):
                col+=1
                if i.isChecked() :
                    name=str(i.text())
                    
                    x=self.smilei.Scalar(name).getAvailableTimesteps()*self.timestep
                    y=self.smilei.Scalar(name).getData()
                    self.scalarDict[name]=(x,y)
                    ax=self.fig.add_subplot(self.nplots,1,plot+1)
                    ax.xaxis.grid(True)
                    ax.yaxis.grid(True)
                    print len(x), len(y)
                    ax.plot(x,y)
                    ax.set_xlim(x.min(),x.max())
                    
                    ax.set_ylabel(name)
                    ax.axvline(x=0,c="red",linewidth=2,zorder=0, clip_on=False)
                    self.ax[name]=ax

                    plot+=1
                

            log.info("preparing fields")
            for i in self.ui.fields.findChildren(QCheckBox):
                if i.isChecked() :
                    log.info(i.text())
                    ax=self.fig.add_subplot(self.nplots,1,plot+1)
                    ax.xaxis.grid(True)
                    ax.yaxis.grid(True)

                    data=[]
                    name=str(i.text())
                    log.info("\tField %s"%name)
                    data=self.smilei.Field(name).getData()
                                        
                    self.fieldDict[name]=data
                    
                    if len(self.sim_length) == 1 :
                        ax.set_xlim(0,self.sim_length[0])
                        ax.set_ylabel(name)
                        x=np.array(range(len(data[0])))*self.cell_length
                        y=data[0]
                        ax.plot(x,y)
                        self.ax[name]=ax
                    elif len(self.sim_length) == 2 :
                        divider = make_axes_locatable(ax)
                        cax = divider.new_horizontal(size="2%", pad=0.05)
                        self.fig.add_axes(cax)
                        ax.set_ylabel(name)

                        im=ax.imshow([[0]],extent=(0,self.sim_length[0],0,self.sim_length[1]), aspect='auto',origin='lower')
                        im.set_interpolation('nearest')
                        cb=self.fig.colorbar(im, cax=cax, ax=ax)
                        self.ax[name]=ax

                    plot+=1

            log.info("preparing phase")
            for i in self.ui.phase.findChildren(QCheckBox):
                if i.isChecked() :
                    name=str(i.text())
                    number=int(name.split(' ')[0])
                    phase=self.smilei.ParticleDiagnostic(number)
                    self.phaseDict[name]=phase.getData()
                   
                    if phase._naxes is not 2:
                        log.error("phasespace len is not 2 : %s"%name)
                        
                        
                    my_extent=[phase._axes[0]['min'],phase._axes[0]['max'],phase._axes[1]['min'],phase._axes[1]['max']]
                    
                    ax=self.fig.add_subplot(self.nplots,1,plot+1)
                    ax.xaxis.grid(True)
                    ax.yaxis.grid(True)
                    ax.set_ylabel(name)
                    divider = make_axes_locatable(ax)
                    cax = divider.new_horizontal(size="2%", pad=0.05)
                    self.fig.add_axes(cax)
                    
                    im=ax.imshow([[0]],extent=my_extent,aspect='auto',origin='lower')
                    im.set_interpolation('nearest')
                    cb=self.fig.colorbar(im, cax=cax, ax=ax)

                    self.ax[name]=ax
                    plot+=1
                
            log.info("done")    
            self.doPlots()
    
    def on_movement(self, event):
        if not event.inaxes: return
        msg = "%G %G" % (event.xdata, event.ydata)
        self.ui.pos.setText(msg)

    def on_key_press(self,event):
        if not event.inaxes: return
        if event.key == 'a':
            for line in event.inaxes.lines :
                if line.get_xdata().size > 1:
                    data=line.get_ydata()
                    nonzero=data[np.nonzero(data)]
                    if len(nonzero) :
                        mini=np.min(nonzero)
                        maxi=np.max(nonzero)
                        if mini != maxi :
                            event.inaxes.set_ylim(mini,maxi)
            for image in event.inaxes.images :
                data=np.array(image.get_array()) 
                nonzero=data[np.nonzero(data)]
                if len(nonzero) :
                    mini=np.min(nonzero)
                    maxi=np.max(nonzero)
                    if mini != maxi :
                        image.set_clim(mini,maxi)
            self.canvas.draw()

        elif event.key == 'l':
            if event.inaxes.lines :
                scale='log' if event.inaxes.get_yaxis().get_scale()== 'linear' else 'linear'
                try:
                    event.inaxes.set_yscale(scale)
                    self.canvas.draw()
                except ValueError:
                    scale='log' if scale == 'linear' else 'linear'
                    event.inaxes.set_yscale(scale)
                    self.canvas.draw()
            elif event.inaxes.images :
                for image in event.inaxes.images :
                    mini = np.array(image.get_array()).clip(0).min()
                    if mini >0:
                        maxi = np.array(image.get_array()).clip(0).max()
                        pprint (vars(event.inaxes.images[0].norm))
                        try:
                            event.inaxes.images[0].set_norm(LogNorm(mini,maxi))
                            self.canvas.draw()
                        except ValueError:
                            self.canvas.draw()
        elif event.key == 'x':
            range, ok = QInputDialog.getText(self, 'Ranges', 'Give '+event.key+' range:')        
            if ok:
                ranges=range.split(' ')
                event.inaxes.set_xlim(float(ranges[0]),float(ranges[1]))

            self.canvas.draw()
        elif event.key == 'y':
            range, ok = QInputDialog.getText(self, 'Ranges', 'Give '+event.key+' range:')        
            if ok:
                ranges=range.split(' ')
                event.inaxes.set_ylim(float(ranges[0]),float(ranges[1]))

            self.canvas.draw()
        elif event.key == 'c':
            range, ok = QInputDialog.getText(self, 'Ranges', 'Give '+event.key+' range:')        
            if ok:
                ranges=range.split(' ')
                event.inaxes.images[0].set_clim(float(ranges[0]),float(ranges[1]))

            self.canvas.draw()
        elif event.key == 'shift':
            self.shiftPressed=True

    def on_key_release(self,event):
        if not event.inaxes: return
        if event.key == 'shift':
            self.shiftPressed=False
            

    def on_button_press(self,event):
        if not event.inaxes: return
        if self.shiftPressed == True :
            self.ui.logger.moveCursor (QTextCursor.End);
            for i in range(len(self.fig.axes)) :
                if self.fig.axes[i] == event.inaxes:                    
                    # JDT txt = "%d %G %G %G\n" % (i, self.step/self.timestep*self.fieldEvery, event.xdata, event.ydata)
                    txt = "%d %G %G\n" % (i, event.xdata, event.ydata)
                    QApplication.clipboard().setText(txt)
                    self.ui.logger.insertPlainText(txt);
                    self.ui.logger.moveCursor (QTextCursor.End);
            
        
    def doPlots(self):
    
        if len(self.fieldSteps) == 0 : return

        if self.someCheckBoxChanged==True:
            self.preparePlots()
        
        self.step %= len(self.fieldSteps)
        self.slider.setValue(self.step)
        
        self.ui.spinStep.setValue(self.step)
        # JDT time=float(self.step)/self.timestep*self.fieldEvery
        time=self.fieldSteps[self.step]*self.timestep
        
        self.fig.suptitle("Time: %g"%time)
        
        for name in self.scalarDict:
            self.ax[name].lines[-1].set_xdata(time)
           
        for name in self.fieldDict:
            data=self.fieldDict[name][self.step]
            if len(self.sim_length) == 1 :
                self.ax[name].lines[-1].set_ydata(data)
                if self.ui.autoScale.isChecked():
                    self.ax[name].set_ylim(min(data),max(data))
            elif len(self.sim_length) == 2 :
                im=self.ax[name].images[-1]
                npData=np.array(data)
                im.set_data(npData.T)
                if self.ui.autoScale.isChecked():
                    im.set_clim(npData.min(),npData.max())

                    
        for name in self.phaseDict:
            data=self.phaseDict[name][self.step].T
            im=self.ax[name].images[-1]
            im.set_data(data)
            if self.ui.autoScale.isChecked():
                im.set_clim(data.min(),data.max())
                                
        self.canvas.draw()
        if self.ui.saveImages.isChecked():
            fname=self.dirName+'/frame-%06d.png' % self.step
            self.fig.savefig(fname)

    def closeEvent(self,event):
        self.save_settings()
        self.parent.plots.remove(self)
        QApplication.processEvents()
        self.deleteLater()


class smileiQt(QMainWindow):
    def __init__(self, args):
        super(smileiQt, self).__init__()
                
        self.setWindowFlags(self.windowFlags() | Qt.Tool | Qt.Dialog)

        uiFile=os.path.dirname(os.path.realpath(__file__))+'/smileiQt.ui'
        self.ui=uic.loadUi(uiFile,self)

        self.ui.dir.setIcon(self.ui.style().standardIcon(QStyle.SP_DirOpenIcon))
        
        self.ui.playStop.setIcon(self.ui.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.previous.setIcon(self.ui.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.ui.next.setIcon(self.ui.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.ui.first.setIcon(self.ui.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.ui.last.setIcon(self.ui.style().standardIcon(QStyle.SP_MediaSkipForward))        
        
        self.timer=QTimer()
        self.plots=[]
        for i in args : 
            self.addDir(i)

        self.timer.timeout.connect(self.timeout)

        if sys.platform == "darwin":
            self.raise_()
        self.show()
        
    def timeout(self):
        if len(self.plots) == 0:
            self.ui.playStop.setChecked(False)
            
    def addDir(self,name):
        self.plots.append(smileiQtPlot(self,name))
             
    def on_playStop_toggled(self):
        if self.playStop.isChecked() :
            self.ui.playStop.setIcon(self.ui.style().standardIcon(QStyle.SP_MediaStop))
            self.timer.start(100)
        else:
            self.ui.playStop.setIcon(self.ui.style().standardIcon(QStyle.SP_MediaPlay))
            self.timer.stop()
    
    def pause(self):
        self.playStop.setChecked(False)
        
    def on_dir_released(self):
        dirName=QFileDialog.getExistingDirectory(self,options=QFileDialog.ShowDirsOnly)
        if not dirName.isEmpty():
            self.addDir(str(dirName))
    
    def closeEvent(self,event):
        if len(self.plots)>0:
            result = QMessageBox.question(self,"Confirm Exit...","Are you sure you want to exit ?", QMessageBox.Yes| QMessageBox.No)
            if result == QMessageBox.No:
                event.ignore()
                return
            for plot in self.plots:
                plot.deleteLater()
        event.accept()
        QApplication.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    args = ["."] if len(sys.argv) == 1 else sys.argv[1:]
    app.self.setWindowIcon(QIcon(os.path.dirname(os.path.realpath(__file__))+'/smileiIcon.ico'))

    smileiQt(args)
    sys.exit(app.exec_())
    
