import json
import xml.etree.ElementTree as ET
from exception import TransportException

class PassengerRepository:
    def __init__(self):
        self._passengers = []

    def add(self, passport_id: str, full_name: str, age: int):
        if type(passport_id) is not str or not passport_id.strip():
            raise TransportException("Серия/номер паспорта должны быть непустой строкой.")
        if type(full_name) is not str or not full_name.strip():
            raise TransportException("ФИО пассажира должно быть непустой строкой.")
        if type(age) is not int or age < 0 or age > 150:
            raise TransportException("Указан некорректный возраст пассажира.")
            
        passenger = {
            "passport_id": passport_id.strip(),
            "full_name": full_name.strip(),
            "age": age
        }
        self._passengers.append(passenger)

    def get_all(self) -> list:
        return self._passengers

    def save_json(self, filename: str):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self._passengers, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise TransportException(f"Ошибка записи JSON: {e}")

    def load_json(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if type(data) is not list:
                raise TransportException("Неверный формат данных JSON.")
            for item in data:
                self.add(item["passport_id"], item["full_name"], item["age"])
        except (IOError, json.JSONDecodeError, KeyError, ValueError) as e:
            raise TransportException(f"Ошибка чтения JSON: {e}")

    def save_xml(self, filename: str):
        try:
            root = ET.Element("passengers")
            for passenger in self._passengers:
                p_elem = ET.SubElement(root, "passenger")
                for key, val in passenger.items():
                    ET.SubElement(p_elem, key).text = str(val)
            ET.ElementTree(root).write(filename, encoding='utf-8', xml_declaration=True)
        except IOError as e:
            raise TransportException(f"Ошибка записи XML: {e}")

    def load_xml(self, filename: str):
        try:
            tree = ET.parse(filename)
            for p_elem in tree.getroot().findall("passenger"):
                passport_id = p_elem.find("passport_id").text
                full_name = p_elem.find("full_name").text
                age = int(p_elem.find("age").text)
                self.add(passport_id, full_name, age)
        except (IOError, ET.ParseError, AttributeError, ValueError) as e:
            raise TransportException(f"Ошибка чтения XML: {e}")

