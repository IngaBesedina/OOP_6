#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Вариант 1.
Использовать словарь, содержащий следующие ключи:
фамилия и инициалы; номер группы; успеваемость (список из пяти элементов).
Написать программу, выполняющую следующие действия:
ввод с клавиатуры данных в список, состоящий из словарей заданной структуры;
записи должны быть упорядочены по возрастанию номера группы;
вывод на дисплей фамилий и номеров групп для всех студентов,
если средний балл студента больше 4.0;
если таких студентов нет, вывести соответствующее сообщение.
"""


import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List


class UnknownCommandError(Exception):

    def __init__(self, command, message="Unknown command"):
        self.command = command
        self.message = message
        super(UnknownCommandError, self).__init__(message)

    def __str__(self):
        return f"{self.command} -> {self.message}"


@dataclass(frozen=True)
class Student:
    surname: str
    group_number: int
    grades: list[int]


@dataclass
class Students:
    students: List[Student] = field(default_factory=lambda: [])

    def add_student(
        self, surname: str, group_number: int, grades: list[int]
    ) -> None:
        self.students.append(
            Student(surname=surname, group_number=group_number, grades=grades)
        )

        self.students.sort(key=lambda student: student.group_number)

    def __str__(self) -> str:
        table = []
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 14
        )

        table.append(line)

        table.append(
            "| {:^4} | {:^30} | {:^20} | {:^14} |".format(
                "№", "Ф.И.О.", "Группа", "Оценки"
            )
        )
        table.append(line)

        # Вывести данные о всех студентах.
        for idx, student in enumerate(self.students, 1):
            table.append(
                "| {:>4} | {:<30} | {:<20} | {:>14} |".format(
                    idx,
                    student.surname,
                    student.group_number,
                    ", ".join(str(el) for el in student.grades),
                )
            )

        table.append(line)

        return "\n".join(table)

    def select_students(self) -> List[Student]:
        # Сформировать список студентов, средний балл которых больше 4.0
        result: List[Student] = []
        for student in self.students:
            if sum(student.grades) / len(student.grades) > 4:
                result.append(student)

        return result

    def load_students(self, file_name: str) -> None:
        with open(file_name, "r", encoding="utf-8") as fin:
            xml = fin.read()

        parser = ET.XMLParser(encoding="utf8")
        tree = ET.fromstring(xml, parser=parser)

        self.students = []
        for student_element in tree:
            surname, group_number, grades = None, None, None

            for element in student_element:
                if element.tag == "surname":
                    surname = element.text
                elif element.tag == "group_number":
                    group_number = int(element.text)
                elif element.tag == "grades":
                    grades = [int(el) for el in element.text]

                if (
                    surname is not None
                    and group_number is not None
                    and grades is not None
                ):
                    self.students.append(
                        Student(
                            surname=surname,
                            group_number=group_number,
                            grades=grades,
                        )
                    )

    def save_students(self, file_name: str) -> None:
        root = ET.Element("students")
        for student in self.students:
            student_element = ET.Element("student")

            surname_element = ET.SubElement(student_element, "surname")
            surname_element.text = student.surname

            group_number_element = ET.SubElement(
                student_element, "group_number"
            )
            group_number_element.text = str(student.group_number)

            grades_element = ET.SubElement(student_element, "grades")
            grades_element.text = "".join(str(el) for el in student.grades)

            root.append(student_element)

        tree = ET.ElementTree(root)
        with open(file_name, "wb") as fout:
            tree.write(fout, encoding="utf8", xml_declaration=True)


if __name__ == "__main__":
    students = Students()

    while True:
        try:
            command = input(">>> ").lower()

            if command == "exit":
                break

            if command == "add":
                surname = input("Фамилия и инициалы: ")
                group_number = int(input("Номер группы: "))
                input_grades = input("Успеваемость: ")
                grades = list(map(int, input_grades.split(" ")))

                students.add_student(surname, group_number, grades)

            elif command == "list":
                print(students)

            elif command == "select":
                selected = students.select_students()

                if selected:
                    for idx, student in enumerate(selected, 1):
                        print(
                            "{:>4}: {}, группа: {}".format(
                                idx, student.surname, student.group_number
                            )
                        )
                else:
                    print(
                        "Cтуденты, средний балл которых больше 4.0, не найдены"
                    )

            elif command.startswith("load "):
                parts = command.split(maxsplit=1)
                students.load_students(parts[1])

            elif command.startswith("save "):
                parts = command.split(maxsplit=1)

                students.save_students(parts[1])

            elif command == "help":
                print("Список команд:\n")
                print("add - добавить работника;")
                print("list - вывести список работников;")
                print("select - студенты, средний балл которых больше 4.0")
                print("load <имя_файла> - загрузить данные из файла;")
                print("save <имя_файла> - сохранить данные в файл;")
                print("help - отобразить справку;")
                print("exit - завершить работу с программой.")

            else:
                raise UnknownCommandError(command)

        except Exception as exc:
            print(exc, file=sys.stderr)
