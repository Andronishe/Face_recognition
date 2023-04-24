
import sqlite3
import os


class Select:
    @staticmethod
    def write_to_file(data, filename):
        # Преобразование двоичных данных в нужный формат
        with open(filename, 'wb') as file:
            file.write(data)
        print("Данный из blob сохранены в: ", filename, "\n")

    @staticmethod
    def convert_to_binary_data(filename):
        # Преобразование данных в двоичный формат
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data

    @staticmethod
    def read_blob_data():
        try:
            sqlite_connection = sqlite3.connect('photos.sqlite3')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            result = []
            sql_fetch_blob_query = """SELECT * from Persons """
            cursor.execute(sql_fetch_blob_query)
            record = cursor.fetchall()
            for row in record:
                result.append(row)
                print("Id = ", row[0], "Name = ", row[1])
                name = row[1]
                photo = row[2]

                print("Сохранение изображения сотрудника и резюме на диске \n")
                photo_path = os.path.join("images/", name + ".jpg")
                Select.write_to_file(photo, photo_path)
            cursor.close()
            return result

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    @staticmethod
    def insert_blob( name, photo):
        try:
            sqlite_connection = sqlite3.connect('photos.sqlite3')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")

            sqlite_insert_blob_query = """INSERT INTO Persons
                                      (name, photo) VALUES ( ?, ?)"""

            emp_photo = Select.convert_to_binary_data(photo)
            # Преобразование данных в формат кортежа
            data_tuple = ( name, emp_photo)
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            sqlite_connection.commit()
            print("Изображение и файл успешно вставлены как BLOB в таблиу")
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

#Лучше делать выборку фото по айди для того, чтобы циклом передавать айди и сравнивать
if __name__ == "__main__":
    Select().insert_blob(name="Anton Velentey", photo='Anton.jpg')
    # Select().read_blob_data()
