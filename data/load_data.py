class Data:
    path = 'gravitational_systems/data/bodies_data.txt'

    def bodies_data(self, body_nr, parameter_nr):
        with open(self.path, 'r') as file:
            base = file.readlines()
            data = base[body_nr].split(" ")
        return data[parameter_nr]
