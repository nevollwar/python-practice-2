import json
import os
from typing import List, Dict, Any


class Contact:
    """
    Класс, представляющий элемент записной книжки.

    Атрибуты:
        full_name (str): Фамилия, имя и отчество контакта.
        phone_number (str): Контактный номер телефона.
        email (str): Адрес электронной почты.
        birth_date (str): Дата рождения контакта.
    """

    def __init__(self, full_name: str, phone_number: str, email: str, birth_date: str) -> None:
        self.full_name: str = full_name
        self.phone_number: str = phone_number
        self.email: str = email
        self.birth_date: str = birth_date

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование объекта контакта в словарь для JSON."""
        return {
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "birth_date": self.birth_date
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Contact":
        """Фабричный метод создания экземпляра контакта из словаря."""
        return cls(
            full_name=data["full_name"],
            phone_number=data["phone_number"],
            email=data["email"],
            birth_date=data["birth_date"]
        )

    def __str__(self) -> str:
        return (f"ФИО: {self.full_name} | "
                f"Тел: {self.phone_number} | "
                f"E-mail: {self.email} | "
                f"Дата рождения: {self.birth_date}")


class Notebook:
    """
    Класс записной книжки с поддержкой сохранения и загрузки в JSON.
    """

    def __init__(self) -> None:
        self.contacts: List[Contact] = []

    def add_contact(self, full_name: str, phone_number: str, email: str, birth_date: str) -> Contact:
        """Добавить новый контакт в книжку."""
        contact = Contact(full_name, phone_number, email, birth_date)
        self.contacts.append(contact)
        print(f"Запись '{full_name}' успешно добавлена в записную книжку.")
        return contact

    def remove_contact(self, full_name: str) -> bool:
        """Удалить запись по ФИО."""
        for contact in self.contacts:
            if contact.full_name.lower() == full_name.lower():
                self.contacts.remove(contact)
                print(f"Запись '{full_name}' успешно удалена.")
                return True
        print(f"Запись с ФИО '{full_name}' не найдена.")
        return False

    def display_all(self) -> None:
        """Вывести все записи на экран."""
        if not self.contacts:
            print("Записная книжка пуста.")
            return

        print("\n" + "=" * 35 + " СОДЕРЖИМОЕ ЗАПИСНОЙ КНИЖКИ " + "=" * 35)
        for idx, contact in enumerate(self.contacts, 1):
            print(f"{idx:2d}. {contact}")
        print("=" * 98 + "\n")

    def save_to_json(self, filepath: str) -> None:
        """Сохранение записной книжки на диск в формате JSON."""
        data = [contact.to_dict() for contact in self.contacts]
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Данные записной книжки успешно сохранены в файл: {filepath}")

    def load_from_json(self, filepath: str) -> None:
        """Загрузка данных из JSON-файла в текущий экземпляр записной книжки."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл по пути '{filepath}' не найден на диске.")

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.contacts = [Contact.from_dict(item) for item in data]
        print(f"Данные успешно загружены из файла '{filepath}'. Всего записей: {len(self.contacts)}.")