class Data:
    def __init__(self):
        self.bodies_path = 'gravitational_systems/data/bodies_data.txt'
        self.algorithm_info_path = 'gravitational_systems/data/info.txt'

    def bodies_data(self, body_nr, parameter_nr):
        with open(self.bodies_path, 'r') as file:
            base = file.readlines()
            data = base[body_nr].split(" ")
        return data[parameter_nr]

    def algorithm_info_data(self):
        with open(self.algorithm_info_path, 'r', encoding="utf-8") as file:
            text = str(file.read())
        return text
