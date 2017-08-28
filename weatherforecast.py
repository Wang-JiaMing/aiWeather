class weatherforecast:
    f_index = []
    f_time = []
    situation = []
    temperature = []
    wind_direction = []

    def __init__(self, f_index, f_time, situation, temperature, wind_direction):
        self.f_index = f_index
        self.f_time = f_time
        self.situation = situation
        self.temperature = temperature
        self.wind_direction = wind_direction
