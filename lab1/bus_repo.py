import json
import xml.etree.ElementTree as ET
from exception import TransportException

class BusRepository:
    def __init__(self):
        self._buses = []

    def add(self, name: str, capacity: int, fare: float, route_number: str):
        if type(name) is not str or not name.strip():
            raise TransportException("Имя автобуса должно быть непустой строкой.")
        if type(capacity) is not int or capacity <= 0:
            raise TransportException("Вместимость автобуса должна быть целым числом больше нуля.")
        if type(fare) is not float and type(fare) is not int or type(fare) is bool or fare < 0:
            raise TransportException("Стоимость проезда не может быть отрицательной.")
        if type(route_number) is not str or not route_number.strip():
            raise TransportException("Номер маршрута должен быть непустой строкой.")
            
        bus = {
            "name": name.strip(),
            "capacity": capacity,
            "fare": float(fare),
            "route_number": route_number.strip()
        }
        self._buses.append(bus)

    def get_all(self) -> list:
        return self._buses

    def save_json(self, filename: str):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self._buses, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise TransportException(f"Ошибка записи JSON: {e}")

    def load_json(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if type(data) is not list:
                raise TransportException("Неверный формат данных JSON.")
            for item in data:
                self.add(item["name"], item["capacity"], item["fare"], item["route_number"])
        except (IOError, json.JSONDecodeError, KeyError, ValueError) as e:
            raise TransportException(f"Ошибка чтения JSON: {e}")

    def save_xml(self, filename: str):
        try:
            root = ET.Element("buses")
            for bus in self._buses:
                b_elem = ET.SubElement(root, "bus")
                for key, val in bus.items():
                    ET.SubElement(b_elem, key).text = str(val)
            ET.ElementTree(root).write(filename, encoding='utf-8', xml_declaration=True)
        except IOError as e:
            raise TransportException(f"Ошибка записи XML: {e}")

    def load_xml(self, filename: str):
        try:
            tree = ET.parse(filename)
            for b_elem in tree.getroot().findall("bus"):
                name = b_elem.find("name").text
                capacity = int(b_elem.find("capacity").text)
                fare = float(b_elem.find("fare").text)
                route_number = b_elem.find("route_number").text
                self.add(name, capacity, fare, route_number)
        except (IOError, ET.ParseError, AttributeError, ValueError) as e:
            raise TransportException(f"Ошибка чтения XML: {e}")

