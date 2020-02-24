from numpy import sqrt


class Positions:
	G = 6.674083131*10**(-11)  # Gravitational constant [m/kg/s]
	PAR_NUMBER = 7

	def algorithm(self, parameters, dt, variant):
		bodies_number = int(len(parameters) / self.PAR_NUMBER)

		if variant == 'velocity':
			return self.velocity_verlet(parameters, dt, bodies_number)
		elif variant == 'leapfrog':
			return self.leapfrog_verlet(parameters, dt, bodies_number)
		else:
			raise ValueError('Unknown algorithm')

	def velocity_verlet(self, parameters, dt, bodies_number):
		new_parameters = [0, 0, 0, 0, 0, 0, 0] * bodies_number
		# positions
		for j in range(bodies_number):
			new_parameters[0+j*self.PAR_NUMBER] = \
				parameters[0+j*self.PAR_NUMBER] + \
				parameters[2+j*self.PAR_NUMBER] * dt + \
				0.5*parameters[4+j*self.PAR_NUMBER] * dt**2
			new_parameters[1+j*self.PAR_NUMBER] = \
				parameters[1+j*self.PAR_NUMBER] + \
				parameters[3+j*self.PAR_NUMBER] * dt + \
				0.5*parameters[5+j*self.PAR_NUMBER] * dt**2
		# accelerations
		for j in range(bodies_number):
			for i in range(bodies_number):
				if i != j:
					dx = new_parameters[0+i*self.PAR_NUMBER] - \
						new_parameters[0+j*self.PAR_NUMBER]
					dy = new_parameters[1+i*self.PAR_NUMBER] - \
						new_parameters[1+j*self.PAR_NUMBER]
					r = sqrt((dx * dx) + (dy * dy))

					f = self.G * ((parameters[6+j*self.PAR_NUMBER] *
								parameters[6+i*self.PAR_NUMBER])/(r*r))
					new_parameters[4+j*self.PAR_NUMBER] += \
						(f/parameters[6+j*self.PAR_NUMBER]) * (dx/r)
					new_parameters[5+j*self.PAR_NUMBER] += \
						(f/parameters[6+j*self.PAR_NUMBER]) * (dy/r)
		# velocities and masses
		for j in range(bodies_number):
			new_parameters[2+j*self.PAR_NUMBER] = \
				parameters[2+j*self.PAR_NUMBER] + \
				0.5 * (parameters[4+j*self.PAR_NUMBER] +
					new_parameters[4+j*self.PAR_NUMBER]) * dt
			new_parameters[3+j*self.PAR_NUMBER] = \
				parameters[3+j*self.PAR_NUMBER] + \
				0.5*(parameters[5+j*self.PAR_NUMBER] +
					new_parameters[5+j*self.PAR_NUMBER]) * dt
			new_parameters[6+j*self.PAR_NUMBER] = \
				parameters[6+j*self.PAR_NUMBER]

		return new_parameters

	def leapfrog_verlet(self, parameters, dt, bodies_number):
		new_parameters = [0, 0, 0, 0, 0, 0, 0] * bodies_number
		# half velocities
		vxp = [0] * bodies_number
		vyp = [0] * bodies_number
		for j in range(bodies_number):
			vxp[j] = parameters[2+j*self.PAR_NUMBER] + \
					parameters[4+j*self.PAR_NUMBER] * dt * 0.5
			vyp[j] = parameters[3+j*self.PAR_NUMBER] + \
					parameters[5+j*self.PAR_NUMBER] * dt * 0.5

		# positions
		for j in range(bodies_number):
			new_parameters[0+j*self.PAR_NUMBER] = \
				parameters[0+j*self.PAR_NUMBER] + vxp[j] * dt
			new_parameters[1+j*self.PAR_NUMBER] = \
				parameters[1+j*self.PAR_NUMBER] + vyp[j] * dt

		# velocities
		for j in range(bodies_number):
			for i in range(bodies_number):
				if i != j:
					dx = new_parameters[0+i*self.PAR_NUMBER] - \
						new_parameters[0+j*self.PAR_NUMBER]
					dy = new_parameters[1+i*self.PAR_NUMBER] - \
						new_parameters[1+j*self.PAR_NUMBER]

					r = sqrt((dx * dx) + (dy * dy))

					f = self.G * ((parameters[6+j*self.PAR_NUMBER] *
								parameters[6+i*self.PAR_NUMBER])/(r*r))

					new_parameters[4+j*self.PAR_NUMBER] += \
						(f/parameters[6+j*self.PAR_NUMBER]) * (dx/r)
					new_parameters[5+j*self.PAR_NUMBER] += \
						(f/parameters[6+j*self.PAR_NUMBER]) * (dy/r)

		# velocities and masses
		for j in range(bodies_number):
			new_parameters[2+j*self.PAR_NUMBER] = \
				vxp[j] + new_parameters[4+j * self.PAR_NUMBER] * 0.5 * dt
			new_parameters[3+j*self.PAR_NUMBER] = \
				vyp[j] + new_parameters[5+j*self.PAR_NUMBER] * 0.5 * dt
			new_parameters[6+j*self.PAR_NUMBER] = \
				parameters[6+j*self.PAR_NUMBER]

		return new_parameters
