import psutil, time
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import numpy as np
import platform

# bg/fore
pg.setConfigOption('background','k')
pg.setConfigOption('foreground','w')

# app configs
app = QtWidgets.QApplication([])
window = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout()
window.setLayout(layout)
layout.setContentsMargins(10,10,10,10)
layout.setSpacing(8)
window.setWindowTitle("Monitor de Disco SSD")


# se for windows usa o disco C, ou outro disco que o usuario preferir, basta substituir
if platform.system() == "Windows":
    disk = "C:\\"
else: 
    disk = "/" #Mac/Linux

#coleta de dados atuais do disco
du = psutil.disk_usage(disk)
total_mb_capacity = du.total/(1024*1024)
total_mb_used = du.used/(1024*1024)
total_mb_free = du.free/(1024*1024)



# lbl actual usage
uso_total = f"Espaço Total em Disco: {total_mb_capacity:.2f}MB\nUso Atual do Disco: {total_mb_used:.2f}MB\nEspaço Livre em Disco: {total_mb_free:.2f}MB\nPercentual de Uso do Disco: {du.percent}%"
labelUsage = QtWidgets.QLabel(f"{uso_total}")
labelUsage.setStyleSheet("color: white; font-size: 14px")
layout.addWidget(labelUsage)

# plot graphRead
plotRead = pg.PlotWidget(title="Leitura do SSD (MB/s)")
plotRead.showGrid(x=True,y=True,alpha=0.3)
plotRead.setLabel('bottom','Samples')
plotRead.setLabel('left','MB/s')
curveRead = plotRead.plot(pen=pg.mkPen(color='#8ce88b',width=2),name="Read")
layout.addWidget(plotRead)

# lbl graphread
labelRead = QtWidgets.QLabel("Leitura atual: 0 MB/s")
labelRead.setStyleSheet("color: white; font-size: 14px")
layout.addWidget(labelRead)

# plot graphWrite
plotWrite = pg.PlotWidget(title="Escrita do SSD (MB/s)")
plotWrite.showGrid(x=True,y=True,alpha=0.3)
plotWrite.setLabel('left','MB/s')
plotWrite.setLabel('bottom','Samples')
curveWrite = plotWrite.plot(pen=pg.mkPen(color='#fa4f00',width=2),name="Write")
layout.addWidget(plotWrite)

# lbl graphWrite
labelWrite = QtWidgets.QLabel("Escrita atual: 0 MB/s")
labelWrite.setStyleSheet("color: white; font-size: 14px")
layout.addWidget(labelWrite)

# buffers
dataRead = np.zeros(100)
dataWrite = np.zeros(100)

# initializing
prev = psutil.disk_io_counters()
prev_time = time.time()

# real time update (0.1)sec
def update():
    global prev, dataRead, dataWrite, prev_time

    curr = psutil.disk_io_counters()
    now = time.time()
    interval = now - prev_time
    prev_time = now

    read_mb  = (curr.read_bytes - prev.read_bytes)/(1024*1024*interval)
    write_mb = (curr.write_bytes - prev.write_bytes)/(1024*1024*interval)

    # update graphs
    dataRead = np.roll(dataRead, -1)
    dataRead[-1] = read_mb
    curveRead.setData(dataRead)
    labelRead.setText(f"Leitura atual: {read_mb:.1f} MB/s")

    dataWrite = np.roll(dataWrite, -1)
    dataWrite[-1] = write_mb
    curveWrite.setData(dataWrite)
    labelWrite.setText(f"Escrita atual: {write_mb:.1f} MB/s")

    prev = curr

# tmr
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(100)

window.show()
QtWidgets.QApplication.instance().exec_()
