# WarThunder Discord Rich Presence (RPC)
 Integration of Discord rich presence for the War Thunder

## About

This is a application which adds War Thunder as a Discord Rich Presence.

This application pulls in-game information from War Thunder through Port 8111. 
This application modifies in no way whatsoever any data from the game, it is completely safe and will not get you banned.

## Debugging requirements

1. Golang 1.23
2. Discord
3. War Thunder

## Features

1. Shows if you are in the hangar, in a match, or loading in game.
2. Show what vehicle you are using.(Ground or air).
3. Displays an image of the vehicle you are using.
4. Сonverts the system name of the technique to a readable format (if the name of the technique is not saved in the list) or converts them to a readable format if the name is saved in the list (according to the name of the technique in the game).
5. Show simple vehicle stats(Speed | Crew total/Crew current for ground vehicle, Speed TAS | Altitude for air vehicle).
6. Show the game logo in the specified color (from the available list).

## Images

**White main logo**

![plot](/git/static/main_white.png)

**Red main logo**

![plot](/git/static/main_red.png)

**Ground vehicle**

![plot](/git/static/ground.png)

**Air vehicle**

![plot](/git/static/air.png)

**Vehicle with an unsaved name**
![plot](/git/static/unknow.png)

## How to Install

1. Go to "Releases" tab and download the latest version's .EXE file.
2. **(If you haven't downloaded settings.json)** Create file "settings.json" with this keys:
```json
{
  "refresh_time": 7, // It is responsible for the time between status updates and cannot be less than 5
  "main_logo_theme": "main_red"  // Game logo in the specified color, color list: main_red, main_white
}
```
3. Launch the app at any time.

## Know issue
1. Speed/altitude information can be set late (you can experiment with "refresh_time" in the settings)

## Что это?

Интеграция Discord rich presence для игры War Thunder.

Информация получаемая для установки статуса в Discord берется с API игра расположенной по адресу - http://127.0.0.1:8111/

За использование **нельзя** получить бан так-как приложение никак не взаимодействует напрямую с игрой.

## Зависимости необходимые для деббагинга

1. Golang 1.23
2. Discord
3. War Thunder

## Возможности

1. Отображает статус игры: в ангаре, загрузка, в бою.
2. Отображает какую технику вы используете(Наземную или авиацию).
3. Отображает изображение техники которую вы используете.
4. Конвертирует в удобочитаемый формат название техники(так-как с API приходит техническое название техники), либо берет название из игры со всем форматированием(если есть в списке)
5. Отображает некоторые данные о технике: скорость + общее количество экипажа/текущее количество экипажа для наземной техники или TAS скорость + высота для авиации.
6. Отображает лого игры в выбранном цвете(красном или белом) при установке параметра в настройках(по умолчанию белый).

## Изображения

**Белое лого игры**

![plot](/git/static/main_white.png)

**Красное лого игры**

![plot](/git/static/main_red.png)

**Наземная техника**

![plot](/git/static/ground.png)

**Авиация**

![plot](/git/static/air.png)

**Техника с названием которого нет в списке с форматированием**
![plot](/git/static/unknow.png)

## Как использовать

1. Перейдите в вкладку "Releases" и скачайте exe и settings.json(не обязательно) с последнего релиза.
2. **(Если не скачали settings.json)** Создайте рядом с exe файл "settings.json" с ключами:
```json
{
  "refresh_time": 7, // Задержка между обновлениями статуса Discord в секундах, не может быть меньше 5 секунд.
  "main_logo_theme": "main_red"  // Вариант лога игры, доступные: "main_red" - красное лого, "main_white" - белое лого.
}
```
3. Запустите приложение в любое время.

## Известные ошибки
1. Высота и скорость может устанавливать с задержкой(иногда очень большой), можете поэкспериментировать с параметром "refresh_time" в настройках.

## Что планируется добавить
1. Дополнительную технику в список форматирования(лучше выглядит и работает быстрее чем резать название).
2. Русскую локализацию для текста в статусах.