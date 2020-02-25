from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QSlider, QComboBox, \
	QLineEdit, QMessageBox, QCheckBox
from PyQt5.QtGui import QFont, QColor, QPen
from collections import OrderedDict
from operator import itemgetter
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QPainterPath
from positions import Positions
from data.load_data import Data
from math import fabs


class MainWindow(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.moving = None
		self.options = None
		self.start = None
		self.stop = None
		self.parameters_board = None
		
	def show_window(self):
		# widgets options
		self.setGeometry(180, 60, 400, 240)
		self.setWindowTitle('Grawitacja')

		self.start = QPushButton("START", self)
		self.start.move(10, 10)
		self.start.resize(100, 50)
		self.start.clicked.connect(lambda: self.start_moving_area())
		self.start.setEnabled(False)

		self.stop = QPushButton("STOP", self)
		self.stop.move(10, 70)
		self.stop.resize(100, 50)
		self.stop.clicked.connect(lambda: self.stop_moving_area())
		self.stop.setEnabled(False)

		self.parameters_board = QPushButton("DODAJ OBIEKTY", self)
		self.parameters_board.move(120, 10)
		self.parameters_board.resize(270, 30)
		self.parameters_board.clicked.connect(lambda: self.parameters_area())
		
		end = QPushButton("KONIEC", self)
		end.move(10, 130)
		end.resize(100, 50)
		end.clicked.connect(lambda: self.close_main())
		
		self.show()

	def start_moving_area(self):
		if ParameterSettings.parameters:
			self.moving = Gravitation(None, ParameterSettings.parameters)
			self.options = SimulationOptions()
			self.stop.setEnabled(True)
			self.parameters_board.setEnabled(False)
			try:
				Gravitation.dt = SimulationOptions.init_dt
			except AttributeError:
				pass

	def parameters_area(self):
		ParameterSettings()
		self.start.setEnabled(True)

	def stop_moving_area(self):
		self.moving.close()
		self.options.close()
		self.stop.setEnabled(False)
		ParameterSettings.parameters = []
		self.parameters_board.setEnabled(True)

	def close_main(self):
		self.close()
		try:
			self.moving.close()
			self.options.close()
		except AttributeError:
			pass
		try:
			self.par.close()
		except AttributeError:
			pass
	

class ParameterSettings(MainWindow, Data):
	parameters = []
	active_bodies_number = 0
	PARAMETERS_NUMBER = 7

	def __init__(self, parent=None):
		super(ParameterSettings, self).__init__()
		self.bodies_number = QComboBox(self)
		self.system = QComboBox(self)
		self.done = QPushButton("GOTOWE", self)
		self.cancel = QPushButton("ANULUJ", self)
		self.bodies = []
		self.parameters_values = []

		self.position_x = None
		self.position_y = None
		self.velocity_x = None
		self.velocity_y = None
		self.acceleration_x = None
		self.acceleration_y = None
		self.mass = None

		# fonts setting
		# major
		self.font_1 = QFont("Monospace", 11, QFont.Bold)
		# parameters types
		self.font_2 = QFont("Monospace", 9, QFont.Bold)
		# parameters values
		self.font_3 = QFont("UltraCondensed", 8)

		self.show_window()
		
	def show_window(self):
		self.setGeometry(200, 130, 650, 160)
		self.setWindowTitle('Parametry obiektow')

		major_label = QLabel(
			"Wprowadz liczbe obiektow, ktorych ruch zamierzasz modelowac:",
			self
		)
		major_label.move(10, 10)
		major_label.setFont(self.font_1)

		self.bodies_number.move(560, 5)
		self.bodies_number.resize(80, 30)
		self.bodies_number.addItems([None, '2', '3', '4', '5', '6', '7', '8'])
		self.bodies_number.currentIndexChanged.connect(self.my_parameters)
		self.bodies_number.activated.connect(self.reset_system)
		
		ready_system_label = QLabel("Lub wybierz gotowy uklad:", self)
		ready_system_label.move(10, 50)
		ready_system_label.setFont(self.font_1)

		self.system.move(245, 45)
		self.system.resize(200, 30)
		self.system.addItems(
			[
				None,
				'Slonce - Ziemia',
				'Ziemia - Ksiezyc',
				'Gwiazda Podwójna HD 59686',
				'Jowisz z 4 największymi księżycami',
				'Gwiazda Podwójna HD 12329 z planetą'
			]
		)
		self.system.currentIndexChanged.connect(self.prepared_system)

		self.done.move(50, 100)
		self.done.resize(100, 50)
		self.done.setEnabled(False)
		self.done.clicked.connect(lambda: self.data_verify())

		self.cancel.move(500, 100)
		self.cancel.resize(100, 50)
		self.cancel.clicked.connect(lambda: self.start_cancel())
		
		self.show()
	
	def reset_system(self):
		self.system.setCurrentIndex(0)
		self.my_parameters()
		
	def my_parameters(self):
		try:
			self.active_bodies_number = int(self.bodies_number.currentText())
		except ValueError:
			if self.bodies_number.currentText() == '':
				self.active_bodies_number = 0
		self.resize(980, 160 + self.active_bodies_number * 100)
		self.cancel.move(600, 100 + self.active_bodies_number * 100)
		self.done.move(280, 100 + self.active_bodies_number * 100)

		if self.active_bodies_number > 0:
			self.done.setEnabled(True)
			if self.position_x is None:
				self.create_data_fields()
			if self.system.currentText() == '':
				self.del_data_fields()
				self.create_values()
		else:
			self.done.setEnabled(False)
			self.create_data_fields()
			self.del_data_fields()
		self.show()

	def create_data_fields(self):
		self.position_x = QLabel("polozenie \npoczatkowe X:", self)
		self.position_x.move(60, 90)
		self.position_x.setFont(self.font_2)
		self.position_x.resize(130, 40)
		self.position_x.setAlignment(Qt.AlignCenter)
		self.position_x.show()

		self.position_y = QLabel("polozenie \npoczatkowe Y:", self)
		self.position_y.move(190, 90)
		self.position_y.setFont(self.font_2)
		self.position_y.resize(130, 40)
		self.position_y.setAlignment(Qt.AlignCenter)
		self.position_y.show()

		self.velocity_x = QLabel("predkosc \npoczatkowa X:", self)
		self.velocity_x.move(320, 90)
		self.velocity_x.setFont(self.font_2)
		self.velocity_x.resize(130, 40)
		self.velocity_x.setAlignment(Qt.AlignCenter)
		self.velocity_x.show()

		self.velocity_y = QLabel("predkosc \npoczatkowa Y:", self)
		self.velocity_y.move(450, 90)
		self.velocity_y.setFont(self.font_2)
		self.velocity_y.resize(130, 40)
		self.velocity_y.setAlignment(Qt.AlignCenter)
		self.velocity_y.show()

		self.acceleration_x = QLabel("przyspieszenie \npoczatkowe X:", self)
		self.acceleration_x.move(580, 90)
		self.acceleration_x.setFont(self.font_2)
		self.acceleration_x.resize(130, 40)
		self.acceleration_x.setAlignment(Qt.AlignCenter)
		self.acceleration_x.show()

		self.acceleration_y = QLabel("przyspieszenie \npoczatkowe Y:", self)
		self.acceleration_y.move(710, 90)
		self.acceleration_y.setFont(self.font_2)
		self.acceleration_y.resize(130, 40)
		self.acceleration_y.setAlignment(Qt.AlignCenter)
		self.acceleration_y.show()

		self.mass = QLabel("masa \nobiektu:", self)
		self.mass.move(840, 90)
		self.mass.setFont(self.font_2)
		self.mass.resize(130, 40)
		self.mass.setAlignment(Qt.AlignCenter)
		self.mass.show()

		self.create_values()

	def create_values(self):
		self.parameters_values = []
		try:
			self.active_bodies_number = int(self.bodies_number.currentText())
		except ValueError:
			self.active_bodies_number = 0
		for i in range(self.active_bodies_number):
			self.parameters_values.append([])
			for j in range(self.PARAMETERS_NUMBER):
				self.parameters_values[i].append(QLineEdit(self))
				self.parameters_values[i][j].move(60 + 130 * j, 145 + i * 100)
				self.parameters_values[i][j].resize(130, 30)
				self.parameters_values[i][j].setFont(self.font_3)
				self.parameters_values[i][j].show()
		if self.active_bodies_number > 0:
			self.parameters_values[0][0].setPlaceholderText('format:  1.0e22')

		self.bodies = []
		for i in range(self.active_bodies_number):
			self.bodies.append(QLabel(str(i + 1) + " :", self))
			self.bodies[i].move(10, 150 + i * 100)
			self.bodies[i].setFont(self.font_2)
			self.bodies[i].resize(60, 20)
			self.bodies[i].setAlignment(Qt.AlignCenter)
			self.bodies[i].show()

	def del_data_fields(self):
		try:
			for values_set in self.parameters_values:
				for value in values_set:
					value.deleteLater()
		except AttributeError:
			pass
		try:
			for body in self.bodies:
				body.deleteLater()
		except AttributeError:
			pass

		self.active_bodies_number = 0
			
	def prepared_system(self):
		if self.system.currentText() == '':
			self.reset_system()
		if self.system.currentText() == 'Slonce - Ziemia':
			self.del_data_fields()
			self.bodies_number.setCurrentIndex(1)
			self.create_values()
			SimulationOptions.init_dt = 4000
			SimulationOptions.max_dt = 800000
			# ascribe bodies
			for i in range(self.PARAMETERS_NUMBER):
				self.parameters_values[0][i].setText(self.bodies_data(1, i))
				self.parameters_values[1][i].setText(self.bodies_data(2, i))
		if self.system.currentText() == 'Ziemia - Ksiezyc':
			self.del_data_fields()
			self.bodies_number.setCurrentIndex(1)
			self.create_values()
			SimulationOptions.init_dt = 2000
			SimulationOptions.max_dt = 200000
			# ascribe bodies
			for i in range(self.PARAMETERS_NUMBER):
				self.parameters_values[0][i].setText(self.bodies_data(4, i))
				self.parameters_values[1][i].setText(self.bodies_data(5, i))
		if self.system.currentText() == 'Gwiazda Podwójna HD 59686':
			self.del_data_fields()
			self.bodies_number.setCurrentIndex(1)
			self.create_values()
			SimulationOptions.init_dt = 8000
			SimulationOptions.max_dt = 600000
			# ascribe bodies
			for i in range(self.PARAMETERS_NUMBER):
				self.parameters_values[0][i].setText(self.bodies_data(7, i))
				self.parameters_values[1][i].setText(self.bodies_data(8, i))
		if self.system.currentText() == 'Jowisz z 4 największymi księżycami':
			self.del_data_fields()
			self.bodies_number.setCurrentIndex(4)
			self.create_values()
			SimulationOptions.init_dt = 120
			SimulationOptions.max_dt = 120000
			# ascribe bodies
			for i in range(self.PARAMETERS_NUMBER):
				self.parameters_values[0][i].setText(self.bodies_data(10, i))
				self.parameters_values[1][i].setText(self.bodies_data(11, i))
				self.parameters_values[2][i].setText(self.bodies_data(12, i))
				self.parameters_values[3][i].setText(self.bodies_data(13, i))
				self.parameters_values[4][i].setText(self.bodies_data(14, i))
		if self.system.currentText() == 'Gwiazda Podwójna HD 12329 z planetą':
			self.del_data_fields()
			self.bodies_number.setCurrentIndex(2)
			self.create_values()
			SimulationOptions.init_dt = 2000
			SimulationOptions.max_dt = 80000
			# ascribe bodies
			for i in range(self.PARAMETERS_NUMBER):
				self.parameters_values[0][i].setText(self.bodies_data(16, i))
				self.parameters_values[1][i].setText(self.bodies_data(17, i))
				self.parameters_values[2][i].setText(self.bodies_data(18, i))

				
	def data_verify(self):
		'''Check if all fields are filled correct.'''
		for i in range(self.active_bodies_number):
			for j in range(self.PARAMETERS_NUMBER):
				try:
					float(self.parameters_values[i][j].text())
				except ValueError:
					QMessageBox.critical(self, "Błąd",
										"Co najmniej jedna z wartosci "
										"wpisana zostala niepoprawnie")
					return None
		for i in range(self.active_bodies_number):
			for j in range(Positions.PAR_NUMBER):
				self.parameters.append(
					float(self.parameters_values[i][j].text())
				)
		self.close()
		
	def start_cancel(self):
		self.close()


class SimulationOptions(MainWindow):

	init_dt = 4000
	max_dt = 400000

	def __init__(self, parent=None):
		super().__init__(parent)
		self.step_slider = None
		self.trajectory_chb = None
		self.algorithm_box = None
		self.show_window()

	def simulation_settings(self):
		self.step_slider = QSlider(Qt.Horizontal, self)
		self.step_slider.setMinimum(1)
		self.step_slider.setMaximum(self.max_dt)
		self.step_slider.setValue(self.init_dt)
		self.step_slider.move(100, 40)
		self.step_slider.resize(450, 40)
		self.step_slider.setTickPosition(QSlider.TicksBelow)
		self.step_slider.setTickInterval(int((self.max_dt-self.init_dt)/100))
		self.step_slider.valueChanged.connect(lambda: self.step())

		self.trajectory_chb = QCheckBox("RYSUJ TRAJEKTORIE", self)
		self.trajectory_chb.move(30, 145)
		self.trajectory_chb.setChecked(True)
		self.trajectory_chb.toggle()
		self.trajectory_chb.stateChanged.connect(lambda: self.draw_trajectory())
		self.trajectory_chb.setStyleSheet("font: bold 13px; color:blue")

		self.algorithm_box = QComboBox(self)
		self.algorithm_box.move(175, 205)
		self.algorithm_box.resize(300, 30)
		self.algorithm_box.addItems(
			[
				'velocity (prędkościowy)',
				'leapfrog (skokowy)'
			]
		)
		self.algorithm_box.currentIndexChanged.connect(self.change_algorithm)

		dt_font = QFont("Monospace", 12, QFont.Bold)
		dt_label = QLabel(
			"Wybierz krok czasowy (wpływa na tempo wizualizacji): ", self)
		dt_label.move(120, 10)
		dt_label.setFont(dt_font)

		wr_font = QFont("Monospace", 10)
		mistake_label = QLabel(
			"Pamięta! Zwiększenie kroku czasowego przyspiesza symulację, ale"
			" zwiększa błąd. Dla układów o krótkim \nokresie obiegu "
			"(np księżyce Jowisza) można zaobserwować jak stopniowe zwiększanie"
			" kroku sprawi, że \ntrajektorie rozjadą się, a planeta zgubi"
			"wewnętrzne księżyce. Algorytm Verleta jest jednak stabilny i "
			"niewielkie\n                                                     "
			"                                                           "
			"błędy nie będą się nawarstwiać!",
			self
		)
		mistake_label.move(10, 90)
		mistake_label.setStyleSheet('color: red')
		mistake_label.setFont(wr_font)

		al_font = QFont("Monospace", 10, QFont.Bold)
		algorithm_label = QLabel(
			"Wybierz wariant Algorytmu Verleta: ", self)
		algorithm_label.move(190, 175)
		algorithm_label.setFont(al_font)

	def step(self):
		Gravitation.dt = self.step_slider.value()

	def draw_trajectory(self):
		if self.trajectory_chb.isChecked():
			Gravitation.trajectory = True
		else:
			Gravitation.trajectory = False

	def change_algorithm(self):
		if self.algorithm_box.currentText() == 'leapfrog':
			Gravitation.algorithm_kind = 'velocity'
		if self.algorithm_box.currentText() == 'velocity':
			Gravitation.algorithm_kind = 'leapfrog'

	def show_window(self):
		self.setGeometry(600, 30, 650, 250)
		self.setWindowTitle('Ustawienia symulacji')
		self.simulation_settings()
		print(self.init_dt)
		self.show()


class Gravitation(SimulationOptions, Positions):

	parameters_num = Positions.PAR_NUMBER
	algorithm_kind = 'velocity'
	dt = 1000
	
	# size limits of painting bodies
	max = 30
	min = 5
	delta = max - min

	refresh = 1
	total_time = 0
	days = 0
	hours = 0
	trajectory = False

	def __init__(self, parent=None, parameters=[]):
		super().__init__(parent=parent)
		self.window_size_x = 1000
		self.window_size_y = 600
		self.path = QPainterPath()
		self.parameters = parameters
		self.bodies_x = []
		self.bodies_y = []
		self.bodies_num = int(len(self.parameters)/self.parameters_num)
		self.scale = self.calibration(self.bodies_num)
		self.timer = QTimer(self)

		for i in range(self.bodies_num):
			self.bodies_x.append(
				self.parameters[0 + i * self.parameters_num] / self.scale[2])
			self.bodies_y.append(
				self.parameters[1 + i * self.parameters_num] / self.scale[2])
			
		self.diameters = self.add_diameters(self.parameters, self.bodies_num)
		self.norm_x = [self.window_size_x] * self.bodies_num
		self.norm_y = [self.window_size_y] * self.bodies_num
		
		self.show_window()
		self.moves()

	def moves(self):
		self.timer.start(self.refresh)
		self.timer.timeout.connect(self.update_positions)
			
	def update_positions(self):

		# list of calculated new positions and velocities
		update = self.algorithm(self.parameters, self.dt, self.algorithm_kind)
		for i in range(self.bodies_num):
			self.bodies_x[i] = update[0+i*self.parameters_num] / self.scale[2]
			self.bodies_y[i] = update[1+i*self.parameters_num] / self.scale[2]
			
			if self.bodies_x[i] > self.window_size_x or self.bodies_x[i] < 0:
				while update[0+i*self.parameters_num] / self.scale[2] > \
					self.norm_x[i] + self.window_size_x:
					self.norm_x[i] += self.window_size_x
					while update[0+i*self.parameters_num] / self.scale[2] \
						< self.norm_x[i]:
						self.norm_x[i] -= self.window_size_x
				self.bodies_x[i] = update[0+i*self.parameters_num] / \
					self.scale[2] - self.norm_x[i]
			
			if self.bodies_y[i] > self.window_size_y or self.bodies_y[i] < 0:
				while update[1+i*self.parameters_num] / self.scale[2] > \
					self.norm_y[i] + self.window_size_y:
					self.norm_y[i] += self.window_size_y
					while update[1+i*self.parameters_num] / \
						self.scale[2] < self.norm_y[i]:
						self.norm_y[i] -= self.window_size_y
				self.bodies_y[i] = update[1+i*self.parameters_num] / \
					self.scale[2] - self.norm_y[i]

		# updated values become new parameters
		self.parameters = update
		# increasing total time
		self.total_time += self.dt
		self.days = int(self.total_time / 86400.)
		self.hours = int(self.total_time / 3600.)
		# update window
		self.update()

	def show_window(self):
		self.setGeometry(140, 340, 1000, 600)
		self.setWindowTitle('Wizualizacja ruchu')

		self.show()

	def paintEvent(self, event):
		for i in range(self.bodies_num):
			painter = QPainter()
			try:
				painter.begin(self)
				painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
				painter.drawEllipse(
					QtCore.QPoint(self.bodies_x[i], self.bodies_y[i]),
					self.diameters[i], self.diameters[i])
				painter.end()
			except AttributeError:
				pass
		painter_t = QPainter(self)
		self.draw_text(event, painter_t)
		painter_t.setPen(QColor(38, 4, 113))
		if self.trajectory is True:
			for i in range(self.bodies_num):
				self.path.moveTo(self.bodies_x[i], self.bodies_y[i])
				self.path.addEllipse(self.bodies_x[i], self.bodies_y[i], 3,
									 3)
				painter_t.drawPath(self.path)

	def draw_text(self, event, qp):
		qp.setPen(QColor(168, 84, 13))
		qp.setFont(QFont('Decorative', 12))
		text = 'upływ czasu,     godziny: ' + str(self.hours) + \
			'    dni: ' + str(self.days)
		qp.drawText(event.rect(), Qt.AlignTop, text)

	def add_diameters(self, parameters, bodies_num):
		'''Calculate bodies diameters and determines their location'''
		diameters = [None] * bodies_num
		masses = {}
		for i in range(bodies_num):
			masses.update({i: parameters[6+i*self.parameters_num]})
		masses = list(
			OrderedDict(
				sorted(masses.items(), key=itemgetter(1), reverse=True)
			).items()
		)
		
		iterator = 0
		recalculated_diameter = self.delta / (bodies_num - 1)

		for i in range(len(masses)):
			if i > 0 and masses[i-1][1] / masses[i][1] > 4.5:
				iterator += 1
				diameters[
					masses[i][0]] = self.max - recalculated_diameter * iterator
			else:
				diameters[
					masses[i][0]
				] = self.max - recalculated_diameter * iterator
		
		return diameters
	
	def calibration(self, bodies_num):
		position_x = []
		position_y = []
		masses = {}
		
		for i in range(bodies_num):
			masses.update({i: self.parameters[6+i*self.parameters_num]})
			position_x.append(self.parameters[0+i*self.parameters_num])
			position_y.append(self.parameters[0+i*self.parameters_num])

		masses = list(
			OrderedDict(
				sorted(masses.items(), key=itemgetter(1), reverse=True)
			).items()
		)
		iterator = 0
		center_x = 0
		center_y = 0
		total_system_weight = 0
		for element in masses:
			center_x += self.parameters[0+element[0]*self.parameters_num] * \
				self.parameters[6+element[0]*self.parameters_num]
			center_y += self.parameters[1+element[0]*self.parameters_num] * \
				self.parameters[6+element[0]*self.parameters_num]
			total_system_weight += \
				self.parameters[6+element[0]*self.parameters_num]
			iterator += 1
				
		center_x /= total_system_weight
		center_y /= total_system_weight
		power = 1
		limit = 0
		for i in range(bodies_num):
			if fabs(self.parameters[0+i*self.parameters_num]-center_x) > limit:
				limit = self.parameters[0+i*self.parameters_num] - center_x
			if fabs(self.parameters[1+i*self.parameters_num]-center_y) > limit:
				limit = fabs(self.parameters[1+i*self.parameters_num]-center_y)

		if self.window_size_y <= self.window_size_x:
			criterion = self.window_size_y * 0.38
		else:
			criterion = self.window_size_y * 0.38
		while limit > criterion:
			limit /= 1.1
			power += 1

		power = 1.1**power
		
		# giving bodies positions
		for i in range(bodies_num):
			x = center_x - ((self.window_size_y*power)/2)  # correction for x
			self.parameters[0+i*self.parameters_num] -= x
			self.bodies_x.append(self.parameters[0+i*self.parameters_num]/power)
			y = center_y - ((self.window_size_y*power)/2)  # correction for y
			self.parameters[1+i*self.parameters_num] -= y
			self.bodies_y.append(self.parameters[1+i*self.parameters_num]/power)
			
		return center_x, center_y, power
