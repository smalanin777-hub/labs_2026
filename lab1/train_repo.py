import json
import xml.etree.ElementTree as ET
from exception import TransportException

class TrainRepository:
    def __init__(self):
        self._trains = []

    def add(self, name: str, capacity: int, fare: float, carriages_count: int):
        if type(name) is not str or not name.strip():
            raise TransportException("Имя поезда должно быть непустой строкой.")
        if type(capacity) is not int or capacity <= 0:
            raise TransportException("Вместимость поезда должна быть целым числом больше нуля.")
        if type(fare) is not float and type(fare) is not int or type(fare) is bool or fare < 0:
            raise TransportException("Стоимость проезда не может быть отрицательной.")
        if type(carriages_count) is not int or carriages_count <= 0:
            raise TransportException("Количество вагонов должно быть целым числом больше нуля.")
            
        train = {
            "name": name.strip(),
            "capacity": capacity,
            "fare": float(fare),
            "carriages_count": carriages_count
        }
        self._trains.append(train)

    def get_all(self) -> list:
        return self._trains

    def save_json(self, filename: str):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self._trains, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise TransportException(f"Ошибка записи JSON: {e}")

    def load_json(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if type(data) is not list:
                raise TransportException("Неверный формат данных JSON.")
            for item in data:
                self.add(item["name"], item["capacity"], item["fare"], item["carriages_count"])
        except (IOError, json.JSONDecodeError, KeyError, ValueError) as e:
            raise TransportException(f"Ошибка чтения JSON: {e}")

    def save_xml(self, filename: str):
        try:
            root = ET.Element("trains")
            for train in self._trains:
                t_elem = ET.SubElement(root, "train")
                for key, val in train.items():
                    ET.SubElement(t_elem, key).text = str(val)
            ET.ElementTree(root).write(filename, encoding='utf-8', xml_declaration=True)
        except IOError as e:
            raise TransportException(f"Ошибка записи XML: {e}")

    def load_xml(self, filename: str):
        try:
            tree = ET.parse(filename)
            for t_elem in tree.getroot().findall("train"):
                name = t_elem.find("name").text
                capacity = int(t_elem.find("capacity").text)
                fare = float(t_elem.find("fare").text)
                carriages_count = int(t_elem.find("carriages_count").text)
                self.add(name, capacity, fare, carriages_count)
        except (IOError, ET.ParseError, AttributeError, ValueError) as e:
            raise TransportException(f"Ошибка чтения XML: {e}")

