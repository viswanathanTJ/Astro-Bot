from dataclasses import dataclass

@dataclass()
class User:
    gender: str = ""
    date: int = 0
    month: int = 0
    year: int = 0
    hours: int = 0
    minutes: int = 0
    ampm: str = ""
    place: str = ""

    def __init__(self):
        pass

    def __init__(self, data):
        self.gender = data[0]
        self.date = data[1]
        self.month = data[2]
        self.year = data[3]
        self.hours = data[4]
        self.minutes = data[5]
        self.ampm = data[6]
        self.place = ' '.join(data[7:])


    def get_user(self):
        gender = 'பெண்' if 'f' in self.gender.lower() or self.gender == "பெண்" else 'ஆண்'
        ampm = 'காலை' if 'a' in self.gender.lower() or self.gender == "காலை" else 'மாலை'
        return f"""பாலினம்: {gender}
தேதி: {self.date}/{self.month}/{self.year}
நேரம்: {self.hours}:{self.minutes} {ampm}
இடம்: {self.place}
******************
தயாராகிறது"""