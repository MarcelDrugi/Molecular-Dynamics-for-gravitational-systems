from numpy import sqrt, dtype, float64, zeros, shape


class Positions:
	PAR_NUMBER = 7

	def __init__(self):
		self.G = 6.674083131 * 10 ** (-11)  # Gravitational constant [m/kg/s]

	def algorithm(self, parameters, dt, variant):
		'''
		Calls the requested algorithm.
		:param parameters:
		:param dt:
		:param variant:
		'''
		bodies_number = int((parameters.shape[0]) / self.PAR_NUMBER)

		if variant == 'velocity':
			return self.velocity_verlet(parameters, dt, bodies_number)
		elif variant == 'leapfrog':
			return self.leapfrog_verlet(parameters, dt, bodies_number)
		elif variant == 'euler_cromer':
			return self.euler_cromer(parameters, dt, bodies_number)
		elif variant == 'rk4':
			return self.rk4(parameters, dt, bodies_number)
		else:
			raise ValueError('Unknown algorithm')

	def velocity_verlet(self, parameters, dt, bodies_number):
		'''
		Verlet algorithm - velocity variant
		:param parameters:
		:param dt:
		:param bodies_number:
		:return new_values:
		'''
		new_values = zeros(self.PAR_NUMBER * bodies_number, dtype=float64)
		# positions and masses
		for j in range(bodies_number):
			new_values[0 + j*self.PAR_NUMBER] = \
				parameters[0 + j*self.PAR_NUMBER] + \
				parameters[2 + j*self.PAR_NUMBER] * dt + \
				0.5*parameters[4 + j*self.PAR_NUMBER] * dt * dt
			new_values[1 + j*self.PAR_NUMBER] = \
				parameters[1 + j*self.PAR_NUMBER] + \
				parameters[3 + j*self.PAR_NUMBER] * dt + \
				0.5*parameters[5 + j*self.PAR_NUMBER] * dt * dt
			new_values[6 + j*self.PAR_NUMBER] = \
				parameters[6 + j*self.PAR_NUMBER]

		# accelerations
		accelerations = self.accelerations_calculation(
			new_values,
			bodies_number,
		)
		for j in range(bodies_number):
			new_values[4 + j*self.PAR_NUMBER] = accelerations[0][j]
			new_values[5 + j*self.PAR_NUMBER] = accelerations[1][j]

		# velocities
		for j in range(bodies_number):
			new_values[2 + j*self.PAR_NUMBER] = \
				parameters[2 + j*self.PAR_NUMBER] + \
				0.5 * (parameters[4 + j*self.PAR_NUMBER] +
					new_values[4 + j*self.PAR_NUMBER]) * dt
			new_values[3 + j*self.PAR_NUMBER] = \
				parameters[3 + j*self.PAR_NUMBER] + \
				0.5*(parameters[5 + j*self.PAR_NUMBER] +
					new_values[5 + j*self.PAR_NUMBER]) * dt
			new_values[6 + j*self.PAR_NUMBER] = \
				parameters[6 + j*self.PAR_NUMBER]

		return new_values

	def leapfrog_verlet(self, parameters, dt, bodies_number):
		'''
		Verlet algorithm - leapfrog variant.
		:param parameters:
		:param dt:
		:param bodies_number:
		:return new_values:
		'''
		new_values = zeros(self.PAR_NUMBER * bodies_number, dtype=float64)

		# half velocities calculation and masses writing
		vxp = [0] * bodies_number
		vyp = [0] * bodies_number
		for j in range(bodies_number):
			vxp[j] = parameters[2 + j*self.PAR_NUMBER] + \
					parameters[4 + j*self.PAR_NUMBER] * dt * 0.5
			vyp[j] = parameters[3 + j*self.PAR_NUMBER] + \
					parameters[5 + j*self.PAR_NUMBER] * dt * 0.5
			new_values[6 + j*self.PAR_NUMBER] = \
				parameters[6 + j*self.PAR_NUMBER]

		# positions
		for j in range(bodies_number):
			new_values[0 + j*self.PAR_NUMBER] = \
				parameters[0 + j*self.PAR_NUMBER] + vxp[j] * dt
			new_values[1 + j*self.PAR_NUMBER] = \
				parameters[1 + j*self.PAR_NUMBER] + vyp[j] * dt

		# accelerations
		accelerations = self.accelerations_calculation(
			new_values,
			bodies_number,
		)
		for j in range(bodies_number):
			new_values[4 + j*self.PAR_NUMBER] = accelerations[0][j]
			new_values[5 + j*self.PAR_NUMBER] = accelerations[1][j]

		# velocities
		for j in range(bodies_number):
			new_values[2 + j*self.PAR_NUMBER] = \
				vxp[j] + new_values[4 + j * self.PAR_NUMBER] * 0.5 * dt
			new_values[3 + j*self.PAR_NUMBER] = \
				vyp[j] + new_values[5 + j*self.PAR_NUMBER] * 0.5 * dt

		return new_values

	def euler_cromer(self, parameters, dt, bodies_number):
		'''
		Simple Euler algorithm.
		:param parameters:
		:param dt:
		:param bodies_number:
		:return new_values:
		'''
		new_values = zeros(self.PAR_NUMBER * bodies_number, dtype=float64)

		for j in range(bodies_number):
			# velocities
			new_values[2 + j*self.PAR_NUMBER] = \
				parameters[2 + j*self.PAR_NUMBER] + \
				parameters[4 + j*self.PAR_NUMBER] * dt
			new_values[3 + j*self.PAR_NUMBER] = \
				parameters[3 + j*self.PAR_NUMBER] + \
				parameters[5 + j*self.PAR_NUMBER] * dt

			# positions
			new_values[0 + j*self.PAR_NUMBER] = \
				parameters[0 + j*self.PAR_NUMBER] + \
				new_values[2 + j*self.PAR_NUMBER] * dt
			new_values[1 + j*self.PAR_NUMBER] = \
				parameters[1 + j*self.PAR_NUMBER] + \
				new_values[3 + j*self.PAR_NUMBER] * dt

			# masses
			new_values[6 + j*self.PAR_NUMBER] = \
				parameters[6 + j*self.PAR_NUMBER]

		# accelerations
		accelerations = self.accelerations_calculation(
			new_values,
			bodies_number,
		)
		for j in range(bodies_number):
			new_values[4 + j*self.PAR_NUMBER] = accelerations[0][j]
			new_values[5 + j*self.PAR_NUMBER] = accelerations[1][j]

		return new_values

	def rk4(self, parameters, dt, bodies_number):
		'''
		Runge-Kutta fourth-order algorithm
		:param parameters:
		:param dt:
		:param bodies_number:
		:return new_values:
		'''
		new_values = zeros(self.PAR_NUMBER * bodies_number, dtype=float64)

		# Runge-Kutta algorithm indirect factors
		k1rx = zeros(bodies_number, dtype=float64)
		k1ry = zeros(bodies_number, dtype=float64)
		k1vx = zeros(bodies_number, dtype=float64)
		k1vy = zeros(bodies_number, dtype=float64)
		k2rx = zeros(bodies_number, dtype=float64)
		k2ry = zeros(bodies_number, dtype=float64)
		k2vx = zeros(bodies_number, dtype=float64)
		k2vy = zeros(bodies_number, dtype=float64)
		k3rx = zeros(bodies_number, dtype=float64)
		k3ry = zeros(bodies_number, dtype=float64)
		k3vx = zeros(bodies_number, dtype=float64)
		k3vy = zeros(bodies_number, dtype=float64)
		k4rx = zeros(bodies_number, dtype=float64)
		k4ry = zeros(bodies_number, dtype=float64)
		k4vx = zeros(bodies_number, dtype=float64)
		k4vy = zeros(bodies_number, dtype=float64)

		for j in range(bodies_number):
			# K1 coefficient for all quantities
			k1rx[j] = parameters[2 + j*self.PAR_NUMBER] * dt
			k1ry[j] = parameters[3 + j*self.PAR_NUMBER] * dt
			k1vx[j] = parameters[4 + j*self.PAR_NUMBER] * dt
			k1vy[j] = parameters[5 + j*self.PAR_NUMBER] * dt

		# mid step accelerations
		accelerations = self.accelerations_calculation(
			parameters,
			bodies_number,
			k1rx,
			k1ry
		)

		# K2 coefficient for all quantities
		for j in range(bodies_number):
			k2rx[j] = (parameters[2 + j*self.PAR_NUMBER] + k1vx[j]/2) * dt
			k2ry[j] = (parameters[3 + j*self.PAR_NUMBER] + k1vy[j]/2) * dt
			k2vx[j] = accelerations[0][j] * dt
			k2vy[j] = accelerations[1][j] * dt

		# mid step accelerations (overwrite acceleration array)
		accelerations = self.accelerations_calculation(
			parameters,
			bodies_number,
			k2rx,
			k2ry
		)

		# K3 coefficient for all quantities
		for j in range(bodies_number):
			k3rx[j] = (parameters[2 + j*self.PAR_NUMBER] + k2vx[j]/2) * dt
			k3ry[j] = (parameters[3 + j*self.PAR_NUMBER] + k2vy[j]/2) * dt
			k3vx[j] = accelerations[0][j] * dt
			k3vy[j] = accelerations[1][j] * dt

		# mid step accelerations (overwrite acceleration array)
		accelerations = self.accelerations_calculation(
			parameters,
			bodies_number,
			2 * k3rx,
			2 * k3ry
		)

		# K4 coefficient for all quantities
		for j in range(bodies_number):
			k4rx[j] = (parameters[2 + j*self.PAR_NUMBER] + k3vx[j]) * dt
			k4ry[j] = (parameters[3 + j*self.PAR_NUMBER] + k3vy[j]) * dt
			k4vx[j] = accelerations[0][j] * dt
			k4vy[j] = accelerations[1][j] * dt

		# write new parameters
		for j in range(bodies_number):
			# positions
			new_values[0 + j*self.PAR_NUMBER] = \
				parameters[0 + j*self.PAR_NUMBER] + \
				(k1rx[j] + 2*k2rx[j] + 2*k3rx[j] + k4rx[j]) / 6
			new_values[1 + j*self.PAR_NUMBER] = \
				parameters[1 + j*self.PAR_NUMBER] + \
				(k1ry[j] + 2*k2ry[j] + 2*k3ry[j] + k4ry[j]) / 6
			# velocities
			new_values[2+j*self.PAR_NUMBER] = \
				parameters[2+j*self.PAR_NUMBER] + \
				(k1vx[j] + 2*k2vx[j] + 2*k3vx[j] + k4vx[j]) / 6
			new_values[3+j*self.PAR_NUMBER] = \
				parameters[3+j*self.PAR_NUMBER] + \
				(k1vy[j] + 2*k2vy[j] + 2*k3vy[j] + k4vy[j]) / 6
			# masses
			new_values[6 + j*self.PAR_NUMBER] = \
				parameters[6 + j*self.PAR_NUMBER]

		# full step accelerations (overwrite acceleration array)
		accelerations = self.accelerations_calculation(
			new_values,
			bodies_number,
		)
		for j in range(bodies_number):
			new_values[4 + j * self.PAR_NUMBER] = accelerations[0][j]
			new_values[5 + j * self.PAR_NUMBER] = accelerations[1][j]

		return new_values

	def accelerations_calculation(self, parameters, bodies_number, krx=None,
								  kry=None):
		'''
		Compute accelerations for all used algorithms.
		:param parameters:
		:param bodies_number:
		:param krx:
		:param kry:
		:return ax, ay:
		'''
		if krx is None:
			krx = zeros(bodies_number, dtype=float64)
		if kry is None:
			kry = zeros(bodies_number, dtype=float64)
		ax = zeros(bodies_number, dtype=float64)
		ay = zeros(bodies_number, dtype=float64)
		for j in range(bodies_number):
			for i in range(bodies_number):
				if i != j:
					dx = parameters[0 + i * self.PAR_NUMBER] + krx[i] / 2 - \
						(parameters[0 + j * self.PAR_NUMBER] + krx[j] / 2)
					dy = parameters[1 + i * self.PAR_NUMBER] + kry[i] / 2 - \
						(parameters[1 + j * self.PAR_NUMBER] + kry[j] / 2)

					r = sqrt((dx * dx) + (dy * dy))
					f = self.G * (
							(
									parameters[6 + j * self.PAR_NUMBER] *
									parameters[6 + i * self.PAR_NUMBER]
							) / (r * r)
					)
					ax[j] += (f / parameters[6 + j * self.PAR_NUMBER]) * (dx/r)
					ay[j] += (f / parameters[6 + j * self.PAR_NUMBER]) * (dy/r)

		return ax, ay
