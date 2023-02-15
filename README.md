# test_ITOB

Тестовое задание выполнил Рыболовлев Григорий Александрович

Данный проект являетсся Flask приложением, которое реализует функционал чайника

Внешний вид:
![Image alt](https://github.com/GrishaRybolovel/test_ITOB/blob/main/Screenshot%202023-02-16%20at%2002.35.39.png)
![Image alt](https://github.com/GrishaRybolovel/test_ITOB/blob/main/Screenshot%202023-02-16%20at%2002.35.57.png)

После того, как мы запустили проект, нужно перейти на http://localhost:5000/
Далее мы видим все данные о чайнике. Для того, чтобы использовать его, для начала нужно его включить, нажав на кнопку включения
После того, как мы включили чайник, мы можем налить туда воду. Изначально температура воды 30 градусов
После того, как мы включили чайник и налили туда воду, можно начать ее кипятить, нажав соответствующую кнопку. Каждую секунду
информация о температуре чайника обновляется, соответственно при закипании, температура воды увеличивается до установленной отметки.
Затем мы можем вылить воду и заново начать цикл.

Примечания:
1) Если пользователь сделал что-то неверно, то чайник выведет соответствующую ошибку(к примеру о том, что нужно налить воды)
2) Ведется логирование всех действий с чайником в файл log.txt
3) Логирование также ведется в базу данных в формате 'сообщение' 'дата сообщения'
4) Такие параметры, как максимальная температура, время кипения и максимальное количество воды можно менять в файле config.py
