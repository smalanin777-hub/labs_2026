from bus_repo import BusRepository
from train_repo import TrainRepository
from passenger_repo import PassengerRepository
from exception import TransportException

def main():
    bus_repo = BusRepository()
    train_repo = TrainRepository()
    pass_repo = PassengerRepository()

    try:
        bus_repo.add("ЛиАЗ-5292", 105, 55.0, "М3")
        train_repo.add("Ласточка", 400, 350.0, 5)
        pass_repo.add("4510-123456", "Иванов Иван Иванович", 25)
        
        bus_repo.save_json("buses.json")
        train_repo.save_json("trains.json")
        pass_repo.save_json("passengers.json")
        
        bus_repo.save_xml("buses.xml")
        train_repo.save_xml("trains.xml")
        pass_repo.save_xml("passengers.xml")
        
        print("Данные успешно сохранены во всех форматах.")
        
    except TransportException as e:
        print(f"Контролируемая ошибка бизнес-логики: {e}")
    except Exception as e:
        print(f"Критическая системная ошибка: {e}")

if __name__ == "__main__":
    main()

