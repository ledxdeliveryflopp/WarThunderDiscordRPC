# WarThunder Discord Rich Presence (RPC)
 Integration of Discord rich presence for the War Thunder

[EN](#About) | [RU](#что-это)

## About

This is a application which adds War Thunder as a Discord Rich Presence.

This application pulls in-game information from War Thunder through Port 8111. 
This application modifies in no way whatsoever any data from the game, it is completely safe and will not get you banned.

## Debugging requirements

1. Python 3.13.9
2. Discord
3. War Thunder

## Features

1. Shows if you are in the hangar, in a match, or loading in game.
2. Show what vehicle you are using.(Ground or air).
3. Displays an image of the vehicle you are using.
4. Сonverts the system name of the vehicle to a readable format (if the name of the vehicle is not saved in the list) or converts them to a readable format if the name is saved in the list (according to the name of the vehicle in the game).
5. Show simple vehicle stats(Speed | Crew total/Crew current for ground vehicle, Speed TAS | Altitude for air vehicle).
6. Show the game logo in the specified color (from the available list).
7. Notifications about the release of a new version of the application.
8. Auto-start.
9. Update without manual download from GitHub.

## Images


**Red main logo**

![plot](/git_static/en/main_red.png)


**Air vehicle (basic)**

![plot](/git_static/en/mig_21_lazur.png)


## Custom images

![plot](/git_static/custom_en/F_A18.png)

![plot](/git_static/custom_en/rah_66.png)

## How to Install

1. Go to "Releases" tab and download the latest version's .EXE file.
2. Launch the app at any time.
3. Execute autostart_service.exe with admin right, if you don't start main file everytime.

## How activate windows notification about app new version
1) Set the "show_notification" setting to True
2) In Windows Settings -> System -> Notifications, disable the "Do not disturb" option

![plot](/git_static/notify_settings.png)

![](/git_static/update.gif)

## Что это?

Интеграция Discord rich presence для игры War Thunder.

Информация получаемая для установки статуса в Discord берется с API игра расположенной по адресу - http://127.0.0.1:8111/

За использование **нельзя** получить бан так-как приложение никак не взаимодействует напрямую с игрой.

## Зависимости необходимые для деббагинга

1. Python 3.13.9
2. Discord
3. War Thunder

## Возможности

1. Отображает статус игры: в ангаре, загрузка, в бою.
2. Отображает какую технику вы используете(Наземную или авиацию).
3. Отображает изображение техники которую вы используете.
4. Конвертирует в удобочитаемый формат название техники
5. Отображает некоторые данные о технике: скорость + общее количество экипажа/текущее количество экипажа для наземной техники или TAS/IAS скорость + абсолютная высота/радиовысота для авиации.
6. Отображает лого игры в выбранном цвете(красном или белом) при установке параметра в настройках(по умолчанию белый).
7. Уведомления о выходе новой версии приложения.
8. Автозапуск.
9. Обновление без ручного скачивания с GitHub.

## Изображения

**Белое лого игры**

![plot](/git_static/ru/main_white.png)

**Красное лого игры**

![plot](/git_static/ru/red_logo.png)

**Наземная техника (c индикаторами)**

![plot](/git_static/ru/ground_with_indicators.png)

**Наземная техника (Без индикаторов)**

![plot](/git_static/ru/ground_without_indicators.png)

**Авиация (C Индикаторами IAS + Радиовысота)**

![plot](/git_static/ru/air_ias_radio.png)

**Авиация (C Индикаторами TAS + Абсолютная высота)**

![plot](/git_static/ru/air_tas_absolute.png)

**Авиация (Без индикаторов)**

![plot](/git_static/ru/air_without_indicators.png)


## Кастомные изображения

![plot](/git_static/custom/mig23ml.png)

![plot](/git_static/custom/mig25.png)

![plot](/git_static/custom/wolfpack.png)


## Как использовать

1. Перейдите в вкладку "Releases" и скачайте архив.
2. Распакуйте архив
3. По желанию настройке settings.yaml.
4. Запустите exe
5. Можете запустить autostart_service.exe с админ правами, что-бы добавить приложение в автозапуск


## Как включить нотификации об обновлениях
1) Поставьте настройку "show_notification" на True
2) В настройках Windows -> Система -> Уведомления, отключите параметр "Не беспокоить"

![plot](/git_static/notify_settings.png)

![plot](/git_static/ru/notify.png)

## Что планируется добавить
1. ~~Дополнительную технику в список форматирования(лучше выглядит и работает быстрее чем резать название).~~
2. ~~Русскую локализацию для текста в статусах.~~
3. ~~Автоматический парсинг названий техники с вики~~
4. ~~Перевод приложения на Python~~
5. ~~Автозапуск~~

## Примечания
1. Если у самолета нет радиовысотомера, то принудительно будет выводиться высота относительно моря


## Список кастомных изображений техники / custom vehicle image list

![plot](/git_static/custom_list.png)