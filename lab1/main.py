import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

class TransportException(Exception):
    pass

class PassengerTransport(ABC):
    def __init__(self, name: str, capacity: int, fare: float):
        if capacity <= 0:
            raise TransportException("Вместимость должна быть больше нуля.")
        if fare < 0:
            raise TransportException("Стоимость проезда не может быть отрицательной.")
        
        self.name = name
        self.capacity = capacity
        self.fare = fare

    @abstractmethod
    def move(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "capacity": self.capacity,
            "fare": self.fare
        }

    @staticmethod
    def from_dict(data: dict):
        t_type = data.get("type")
        if t_type == "Bus":
            return Bus(data["name"], int(data["capacity"]), float(data["fare"]), data["route_number"])
        elif t_type == "Train":
            return Train(data["name"], int(data["capacity"]), float(data["fare"]), int(data["carriages_count"]))
        raise TransportException(f"Неизвестный тип: {t_type}")

class Bus(PassengerTransport):
    def __init__(self, name: str, capacity: int, fare: float, route_number: str):
        super().__init__(name, capacity, fare)
        self.route_number = route_number

    def move(self) -> str:
        return f"Автобус {self.name} (Маршрут {self.route_number}) едет по выделенной полосе."

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["route_number"] = self.route_number
        return d

class Train(PassengerTransport):
    def __init__(self, name: str, capacity: int, fare: float, carriages_count: int):
        super().__init__(name, capacity, fare)
        if carriages_count <= 0:
            raise TransportException("Количество вагонов должно быть больше нуля.")
        self.carriages_count = carriages_count

    def move(self) -> str:
        return f"Поезд {self.name} ({self.carriages_count} вагонов) следует по рельсам."

    def to_dict(self) -> dict:
        d = super().to_dict()
        d["carriages_count"] = self.carriages_count
        return d

class TransportManager:
    def __init__(self):
        self.fleet = []

    def save_to_json(self, filename: str):
        data = [t.to_dict() for t in self.fleet]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_json(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.fleet = [PassengerTransport.from_dict(item) for item in data]

    def save_to_xml(self, filename: str):
        root = ET.Element("fleet")
        for t in self.fleet:
            t_dict = t.to_dict()
            t_elem = ET.SubElement(root, "transport", type=t_dict.pop("type"))
            for key, val in t_dict.items():
                ET.SubElement(t_elem, key).text = str(val)
        ET.ElementTree(root).write(filename, encoding='utf-8', xml_declaration=True)

    def load_from_xml(self, filename: str):
        tree = ET.parse(filename)
        new_fleet = []
        for t_elem in tree.getroot().findall("transport"):
            data = {"type": t_elem.get("type")}
            for child in t_elem:
                data[child.tag] = child.text
            new_fleet.append(PassengerTransport.from_dict(data))
        self.fleet = new_fleet

if __name__ == "__main__":
    manager = TransportManager()
    manager.fleet.append(Bus("ЛиАЗ-5292", 105, 55.0, "М3"))
    manager.fleet.append(Train("Ласточка", 400, 350.0, 5))

    print("--- Исходный парк ---")
    for t in manager.fleet:
        print(t.move())

    manager.save_to_json("transport.json")
    manager.save_to_xml("transport.xml")

    manager.load_from_json("transport.json")
    print("\n--- Загружено обратно ---")
    for t in manager.fleet:
        print(f"{t.name}: мест {t.capacity}, билет {t.fare}руб.")

