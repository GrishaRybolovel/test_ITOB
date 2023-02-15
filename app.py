from flask import Flask, request, render_template
import time
import datetime
from config import BOILING_TIME, AMOUNT_OF_WATER, MAX_TEMP
from database.db import connect_sql, add_message

app = Flask(__name__)

# Просто функция для проверки на то, что строка является float
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# Сам класс чайника, в котором прописаны все методы взаимодествия с ним
class ElectricKettle:
    def __init__(self):
        self.switched_on = False
        self.water_level = 0
        self.water_temperature = 'Нет воды'

    # Включение
    def switch_on(self):
        self.switched_on = True
        return "Kettle switched on."

    # Выключение
    def switch_off(self):
        self.switched_on = False
        return "Kettle switched off."

    # Опустошение чайника
    def water_off(self):
        self.water_level = 0
        self.water_temperature = 'Нет воды'

    # Заполнение чайника водой
    def fill_kettle(self, amount):
        if 0 <= self.water_level + amount <= AMOUNT_OF_WATER:
            self.water_temperature = 30
            self.water_level += amount
        else:
            return False
        return f"{amount} ml of water added. Current water level: {self.water_level} ml."

    # Функция для получения текущей температуры чайника
    def get_temperature(self):
        return str(self.water_temperature)

    # Функция для кипячения чайника
    def boil(self):
        if self.switched_on and self.water_level > 0:
            for i in range(BOILING_TIME):
                self.water_temperature += (MAX_TEMP - 30) / BOILING_TIME
                time.sleep(1)
            ###
            with open('log.txt', 'a+') as f:
                f.write(f'Чайник закончил кипятиться  {datetime.datetime.now()}\n')
            conn = connect_sql()
            add_message(conn, 'Чайник закончил кипятиться')
            conn.close()
            ###
        elif not self.switched_on:
            return -1
        elif self.water_level == 0:
            return -2
        return 1

# Объявление экземпляра класса чайника
kettle = ElectricKettle()


# Функция, которая возвращает генератор значений температуры чайника,
# чтобы каждую секунду отображать текущую температуру на страничке
def start_boiling():
    while True:
        yield kettle.get_temperature()

# Объявляем генератор
gen_total = start_boiling()

# Функция для отображения текущей температуры
@app.get("/update")
def update():
    global gen_total  # get the global iterator

    # return the next value in iterator
    return str(next(gen_total))

# Главная страничка приложения
@app.route('/', methods=['POST', 'GET'])
def main_page():
    if request.method == 'GET':
        error = ''
        return render_template('index.html', status=kettle.switched_on, water_level=kettle.water_level, error=error, boiling=False, w=AMOUNT_OF_WATER)
    else:
        error = ''
        boiling = False
        if 'on' in request.form.keys() and request.form['on'] == 'Включить':
            ###
            with open('log.txt', 'a+') as f:
                f.write(f'Чайник включился  {datetime.datetime.now()}\n')
            conn = connect_sql()
            add_message(conn, 'Чайник включился')
            conn.close()
            ###
            kettle.switch_on()
        if 'off' in request.form.keys() and request.form['off'] == 'Выключить':
            ###
            with open('log.txt', 'a+') as f:
                f.write(f'Чайник выключился  {datetime.datetime.now()}\n')
            conn = connect_sql()
            add_message(conn, 'Чайник выключился')
            conn.close()
            ###
            kettle.switch_off()
        if 'fill' in request.form.keys() and request.form['fill']:
            water = request.form['fill']
            if isfloat(water) and 0 <= float(water) <= AMOUNT_OF_WATER:
                check = kettle.fill_kettle(float(water))
                if not check:
                    error = 'Чайник переполнен'
                    ###
                    with open('log.txt', 'a+') as f:
                        f.write(f'Чайник переполнен  {datetime.datetime.now()}\n')
                    conn = connect_sql()
                    add_message(conn, 'Чайник переполнен')
                    conn.close()
                    ###
                else:
                    ###
                    with open('log.txt', 'a+') as f:
                        f.write(f'Чайник пополнился на {water}  {datetime.datetime.now()}\n')
                    conn = connect_sql()
                    add_message(conn, f'Чайник пополнился на {water}')
                    ###
                    conn.close()
            else:
                error=f'Введите значение от 0 до {AMOUNT_OF_WATER}'
                ###
                with open('log.txt', 'a+') as f:
                    f.write(f'Введено неверное значение кол-ва воды  {datetime.datetime.now()}\n')
                conn = connect_sql()
                add_message(conn, 'Введено неверное значение кол-ва воды')
                conn.close()
                ###
        if 'water_off' in request.form.keys() and request.form['water_off'] == 'Вылить':
            ###
            with open('log.txt', 'a+') as f:
                f.write('Чайник опустошен\n')
            conn = connect_sql()
            add_message(conn, 'Чайник опустошен')
            conn.close()
            ###

            kettle.water_off()
        if 'boil' in request.form.keys() and request.form['boil'] == 'Вскипятить':
            res = kettle.boil()
            if res == -1:
                ###
                with open('log.txt', 'a+') as f:
                    f.write(f'Ошибка при кипячении(чайник выключен)  {datetime.datetime.now()}\n')
                conn = connect_sql()
                add_message(conn, 'Ошибка при кипячении(чайник выключен)')
                conn.close()
                ###

                error = 'Включите чайник'
            elif res == -2:
                ###
                with open('log.txt', 'a+') as f:
                    f.write(f'Ошибка при кипячении(нет воды)  {datetime.datetime.now()}\n')
                conn = connect_sql()
                add_message(conn, 'Ошибка при кипячении(нет воды)')
                conn.close()
                ###

                error = 'Налейте воду'
            else:
                ###
                with open('log.txt', 'a+') as f:
                    f.write(f'Чайник начал кипятиться  {datetime.datetime.now()}\n')
                conn = connect_sql()
                add_message(conn, 'Чайник начал кипятиться')
                conn.close()
                ###
        return render_template('index.html', status=kettle.switched_on, water_level=kettle.water_level, error=error, w=AMOUNT_OF_WATER)

if __name__ == '__main__':
    app.run(debug=True)
