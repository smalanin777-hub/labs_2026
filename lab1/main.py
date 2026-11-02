import sys
from bus_repo import BusRepository
from train_repo import TrainRepository
from passenger_repo import PassengerRepository
from exception import TransportException

def print_help():
    print("\nИспользование: COMMAND [OPTION]")
    print("\nКОМАНДЫ:")
    print("  help (h)                Показать это справочное окно")
    print("  quit (q)                Завершить работу программы")
    print("  ls (l) OPTION           Вывести таблицу объектов:")
    print("                            -t, --transport     весь транспорт")
    print("                            -p, --passengers    все пассажиры")
    print("  add (a) OPTION          Запустить пошаговое добавление:")
    print("                            -t, --transport     новый автобус или поезд")
    print("                            -p, --passengers    новый пассажир")
    print("  rm (r) OPTION           Удалить объект по номеру из таблицы:")
    print("                            -t, --transport     удалить транспорт")
    print("                            -p, --passengers    удалить пассажира")
    print("  edit (e) OPTION         Изменить объект по номеру из таблицы:")
    print("                            -t, --transport     изменить транспорт")
    print("                            -p, --passengers    изменить пассажира")

def read_input(prompt: str) -> str:
    try:
        val = input(prompt)
        return val.strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВвод прерван.")
        return ""

def read_int(prompt: str) -> int:
    while True:
        val = read_input(prompt)
        if not val:
            raise TransportException("Ввод отменен.")
        try:
            return int(val)
        except ValueError:
            print("Ошибка: Введите целое число.")

def read_float(prompt: str) -> float:
    while True:
        val = read_input(prompt)
        if not val:
            raise TransportException("Ввод отменен.")
        try:
            return float(val)
        except ValueError:
            print("Ошибка: Введите число с плавающей точкой.")

def auto_save(bus_repo, train_repo, pass_repo):
    bus_repo.save_json("buses.json")
    bus_repo.save_xml("buses.xml")
    train_repo.save_json("trains.json")
    train_repo.save_xml("trains.xml")
    pass_repo.save_json("passengers.json")
    pass_repo.save_xml("passengers.xml")

def display_transport_table(bus_repo, train_repo):
    buses = bus_repo.get_all()
    trains = train_repo.get_all()
    print("\n=== ТАБЛИЦА ТРАНСПОРТА ===")
    print(f"{'№':<4} | {'Тип':<8} | {'Название':<20} | {'Вместимость':<12} | {'Тариф':<8} | {'Спецификация':<15}")
    print("-" * 78)
    idx = 1
    for b in buses:
        print(f"{idx:<4} | {'Автобус':<8} | {b['name']:<20} | {b['capacity']:<12} | {b['fare']:<8.2f} | Маршрут: {b['route_number']}")
        idx += 1
    for t in trains:
        print(f"{idx:<4} | {'Поезд':<8} | {t['name']:<20} | {t['capacity']:<12} | {t['fare']:<8.2f} | Вагонов: {t['carriages_count']}")
        idx += 1
    return idx - 1

def display_passenger_table(pass_repo):
    passengers = pass_repo.get_all()
    print("\n=== ТАБЛИЦА ПАССАЖИРОВ ===")
    print(f"{'№':<4} | {'Паспорт':<15} | {'ФИО':<30} | {'Возраст':<7}")
    print("-" * 62)
    idx = 1
    for p in passengers:
        print(f"{idx:<4} | {p['passport_id']:<15} | {p['full_name']:<30} | {p['age']:<7}")
        idx += 1
    return idx - 1

def handle_add_transport(bus_repo, train_repo, pass_repo):
    print("Выберите тип транспорта:\n  1. Автобус\n  2. Поезд")
    t_type = read_input(">/# ")
    if t_type not in ("1", "2"):
        print("Неверный выбор типа транспорта.")
        return
    name = read_input("Введите название >/# ")
    if not name:
        print("Имя не может быть пустым.")
        return
    try:
        capacity = read_int("Введите вместимость >/# ")
        fare = read_float("Введите стоимость проезда >/# ")
    except TransportException as e:
        print(e)
        return
    if t_type == "1":
        route_number = read_input("Введите номер маршрута >/# ")
        if not route_number:
            print("Номер маршрута не может быть пустым.")
            return
        bus_repo.add(name, capacity, fare, route_number)
    elif t_type == "2":
        try:
            carriages_count = read_int("Введите количество вагонов >/# ")
        except TransportException as e:
            print(e)
            return
        train_repo.add(name, capacity, fare, carriages_count)
    auto_save(bus_repo, train_repo, pass_repo)
    print("Транспорт успешно добавлен и сохранен.")

def handle_add_passenger(bus_repo, train_repo, pass_repo):
    passport_id = read_input("Введите серию/номер паспорта >/# ")
    if not passport_id:
        print("Паспортные данные не могут быть пустыми.")
        return
    full_name = read_input("Введите ФИО >/# ")
    if not full_name:
        print("ФИО не может быть пустым.")
        return
    try:
        age = read_int("Введите возраст >/# ")
    except TransportException as e:
        print(e)
        return
    pass_repo.add(passport_id, full_name, age)
    auto_save(bus_repo, train_repo, pass_repo)
    print("Пассажир успешно добавлен и сохранен.")

def handle_remove_transport(bus_repo, train_repo, pass_repo):
    total = display_transport_table(bus_repo, train_repo)
    if total == 0:
        print("Таблица пуста.")
        return
    try:
        num = read_int("Введите номер строки для удаления >/# ")
    except TransportException as e:
        print(e)
        return
    if num < 1 or num > total:
        print("Неверный номер строки.")
        return
    buses_count = len(bus_repo.get_all())
    if num <= buses_count:
        bus_repo.remove_at(num - 1)
    else:
        train_repo.remove_at(num - 1 - buses_count)
    auto_save(bus_repo, train_repo, pass_repo)
    print("Объект успешно удален и файлы обновлены.")

def handle_remove_passenger(bus_repo, train_repo, pass_repo):
    total = display_passenger_table(pass_repo)
    if total == 0:
        print("Таблица пуста.")
        return
    try:
        num = read_int("Введите номер строки для удаления >/# ")
    except TransportException as e:
        print(e)
        return
    if num < 1 or num > total:
        print("Неверный номер строки.")
        return
    pass_repo.remove_at(num - 1)
    auto_save(bus_repo, train_repo, pass_repo)
    print("Пассажир успешно удален и файлы обновлены.")

def handle_edit_transport(bus_repo, train_repo, pass_repo):
    total = display_transport_table(bus_repo, train_repo)
    if total == 0:
        print("Таблица пуста.")
        return
    try:
        num = read_int("Введите номер строки для изменения >/# ")
    except TransportException as e:
        print(e)
        return
    if num < 1 or num > total:
        print("Неверный номер строки.")
        return
    buses_count = len(bus_repo.get_all())
    name = read_input("Новое название (оставьте пустым для пропуска) >/# ")
    try:
        capacity_str = read_input("Новая вместимость (оставьте пустым для пропуска) >/# ")
        capacity = int(capacity_str) if capacity_str else None
        fare_str = read_input("Новый тариф (оставьте пустым для пропуска) >/# ")
        fare = float(fare_str) if fare_str else None
    except ValueError:
        print("Ошибка ввода числовых значений. Изменение отменено.")
        return
    if num <= buses_count:
        route_number = read_input("Новый номер маршрута (оставьте пустым для пропуска) >/# ")
        bus_repo.edit_at(num - 1, name=name, capacity=capacity, fare=fare, route_number=route_number)
    else:
        try:
            carriages_str = read_input("Новое кол-во вагонов (оставьте пустым для пропуска) >/# ")
            carriages_count = int(carriages_str) if carriages_str else None
        except ValueError:
            print("Ошибка ввода. Изменение отменено.")
            return
        train_repo.edit_at(num - 1 - buses_count, name=name, capacity=capacity, fare=fare, carriages_count=carriages_count)
    auto_save(bus_repo, train_repo, pass_repo)
    print("Данные объекта изменены и сохранены.")

def handle_edit_passenger(bus_repo, train_repo, pass_repo):
    total = display_passenger_table(pass_repo)
    if total == 0:
        print("Таблица пуста.")
        return
    try:
        num = read_int("Введите номер строки для изменения >/# ")
    except TransportException as e:
        print(e)
        return
    if num < 1 or num > total:
        print("Неверный номер строки.")
        return
    passport_id = read_input("Новый паспорт (оставьте пустым для пропуска) >/# ")
    full_name = read_input("Новое ФИО (оставьте пустым для пропуска) >/# ")
    try:
        age_str = read_input("Новый возраст (оставьте пустым для пропуска) >/# ")
        age = int(age_str) if age_str else None
    except ValueError:
        print("Ошибка ввода возраста. Изменение отменено.")
        return
    pass_repo.edit_at(num - 1, passport_id=passport_id, full_name=full_name, age=age)
    auto_save(bus_repo, train_repo, pass_repo)
    print("Данные пассажира изменены и сохранены.")

def auto_load(bus_repo, train_repo, pass_repo):
    import os
    try:
        if os.path.exists("buses.json"):
            bus_repo.load_json("buses.json")
        if os.path.exists("trains.json"):
            train_repo.load_json("trains.json")
        if os.path.exists("passengers.json"):
            pass_repo.load_json("passengers.json")
    except Exception:
        pass

def execute_with_flag(cmd_name, args, t_func, p_func):
    if not args:
        print(f"Ошибка: Команда {cmd_name} требует флаг (-t, --transport, -p, --passengers)")
        return
    flag = args[0].lower()
    if flag in ("-t", "--transport"):
        t_func()
    elif flag in ("-p", "--passengers"):
        p_func()
    else:
        print(f"Неизвестный флаг для {cmd_name}: {flag}")

def main():
    bus_repo = BusRepository()
    train_repo = TrainRepository()
    pass_repo = PassengerRepository()
    
    auto_load(bus_repo, train_repo, pass_repo)
    
    print("Добро пожаловать в систему управления транспортом!")
    print_help()
    
    while True:
        try:
            cmd_line = read_input("> ")
            if not cmd_line:
                continue
            parts = cmd_line.split()
            cmd = parts[0].lower()
            args = parts[1:]
            
            if cmd in ("quit", "q"):
                print("Завершение работы.")
                break
            elif cmd in ("help", "h"):
                print_help()
            elif cmd in ("ls", "l"):
                execute_with_flag("ls", args, lambda: display_transport_table(bus_repo, train_repo), lambda: display_passenger_table(pass_repo))
            elif cmd in ("add", "a"):
                execute_with_flag("add", args, lambda: handle_add_transport(bus_repo, train_repo, pass_repo), lambda: handle_add_passenger(bus_repo, train_repo, pass_repo))
            elif cmd in ("rm", "r"):
                execute_with_flag("rm", args, lambda: handle_remove_transport(bus_repo, train_repo, pass_repo), lambda: handle_remove_passenger(bus_repo, train_repo, pass_repo))
            elif cmd in ("edit", "e"):
                execute_with_flag("edit", args, lambda: handle_edit_transport(bus_repo, train_repo, pass_repo), lambda: handle_edit_passenger(bus_repo, train_repo, pass_repo))
            else:
                print("Неизвестная команда. Введите 'help' для просмотра списка доступных команд.")
        except TransportException as e:
            print(f"Ошибка бизнес-логики: {e}")
        except Exception as e:
            print(f"Системная ошибка: {e}")

if __name__ == "__main__":
    main()

