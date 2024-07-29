# Общие сведения

<b>«Shield»</b> представляет из себя пример реализации итогового проекта по курсу .NET 10-й предметной области <b>«Отдел вневедомственной охраны»</b> (далее ОВО).

> [!NOTE]
> Автор (т.е. я, [челик с ВПР](https://github.com/aexra)), не несет никакой ответственности за весь говнокод который можно здесь найти.<br>
> Реализация проекта далека от идеала и может иметь массу других возможных исполнений, с другими фреймворками, другим интерфейсом, архитектурой и т.д. и т.п.

## Задание

Задание варианта:
> Отдел вневедомственной охраны (ОВО) занимается охраной объектов физических и юридических лиц. ОВО является коммерческим подразделением милиции. Клиент, желающий обеспечить охрану своего имущества, обращается в ОВО и составляет договор охраны. В договоре оговариваются следующие моменты: адрес объекта; план расположения помещений; количество входов/выходов; расположение окон; список лиц, отвечающих за имущество; ответственное лицо от клиента, которое будет присутствовать в момент вскрытия помещения. После заключения договора объект подключается к сигнализации. В случае срабатывания сигнализации дежурный посылает патруль на осмотр объекта и сообщает ответственному лицу клиента о данном факте. Патруль, вместе с ответственным лицом клиента, осматривает объект, проверяет сохранность имущества и работу сигнализации (в случае ложного срабатывания). После каждого выезда составляется акт, который является основанием для возбуждения уголовного дела относительно лиц, незаконно проникшим на объект. По результатам своей деятельности ОВО предоставляет отчетность в вышестоящие органы милицейского руководства.

[Все варианты](tasks.md)

## Принцип реализации

Проект принято реализовать с использованием отдельных проектов: «клиент» - классическое приложение Windows для работы администрации ОВО с базой данных, и «сервер» - веб-приложение для манипуляций с единой базой данных всех контрактов предприятия.
Такое решение было принято для минимизации клиентской нагрузки и возможности многопользовательской работы сервиса - несколько «клиентов» могут работать с одной единственной базой данных одновременно, с возможностью авторизации администраторов, чтобы избежать доступа к функционалу сервиса неуполномоченными на то пользователями.

# Фреймворки

В проекте задействованы следующие основные фреймворки:
- [WinUI 3](https://learn.microsoft.com/en-us/windows/apps/winui/winui3/) - «клиент»
- [ASP.NET Core](https://dotnet.microsoft.com/ru-ru/apps/aspnet) - «сервер»

> [!IMPORTANT]
> В проекте также задействованы некоторые другие вспомогательные фреймворки. Их все можно найти в менеджере пакетов NuGet в VisualStudio или в ```.csproj``` каждого проекта

# Структура проекта

![Application Scheme](https://github.com/user-attachments/assets/e052ae32-2a3d-4f44-8830-7e2c0bd27731)

В настоящий момент проект представляет из себя одно решение Visual Studio [Shield.sln](#Shield.sln), содержащее 4 проекта:
- [Shield.DataAccess](#Shield.DataAccess)
- [Shield.Web](#Shield.Web)
- [Shield.App](#Shield.App)
- [Shield.App.Core](#Shield.App.Core)

## Shield.DataAccess

Проект <b>DataAccess</b> представляет из себя библиотеку классов .NET, содержащую все необходимые <i>DTO</i> (Data Transfer Object), используемые для обмена данными между ASP.NET и WinUI 3 посредством веб-запросов, а также все необходимые <i>модели</i> баз данных.

[Исходный код Shield.DataAccess](Shield.DataAccess)

## Shield.Web

Проект <b>Web</b> является небольшим веб-приложением, отвечающим за все манипуляции с контрактами ОВО

### База данных

Выбранный тип СУБД - [SQLite](https://www.sqlite.org/), ввиду «скромного» функционала приложения.
В среде [.NET](https://dotnet.microsoft.com/ru-ru/) манипуляции с базами данных принято выполнять с помощью фреймворка [Entity Framework](https://learn.microsoft.com/ru-ru/ef/)

Логгирование пользователей реализуется с использованием [Identity Framework](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity?view=aspnetcore-8.0&tabs=visual-studio) и [JWT Bearer](https://learn.microsoft.com/en-us/dotnet/api/microsoft.aspnetcore.authentication.jwtbearer?view=aspnetcore-8.0)

В приложении задействовано две базы данных:
- ```Identity.db```
- ```Data.db```

```Identity.db``` необходима для Identity Framework, содержит информацию о пользователях (слева).<br>
```Data.db``` содержит информацию о контрактах ОВО (справа).

![Identity.db relationships scheme](https://github.com/user-attachments/assets/8f442e2a-eb41-4610-b96c-6f8792cd8d7f)
![Data.db relationships scheme](https://github.com/user-attachments/assets/fe020361-41ed-43ac-a59f-c5ef96d8fbb3)

### Контексты

В Entity Framework за создание, изменение и манипуляции с содержимым баз данных отвечают «контексты баз данных» - 1 контекст к 1 базе данных.<br>
В представленном приложении таких контекстов всего два:
- [```IdentityContext.cs```](Shield.Web/Data/Contexts/IdentityContext.cs)
- [```DataContext.cs```](Shield.Web/Data/Contexts/DataContext.cs)

### Модели

Контексты баз данных содержат объекты типа ```DbSet``` - 1 сет к 1 таблице в базе данных.

```IdentityContext``` использует всего одну модель - [```User```](Shield.Web/Data/Models/User.cs) - модель пользователя приложения, наследует ```IdentityUser``` без изменений.

```DataContext``` использует 4 модели:
- [```Contract```](Shield.DataAccess/Models/Contract.cs)
- [```Plan```](Shield.DataAccess/Models/Plan.cs)
- [```Picture```](Shield.DataAccess/Models/Picture.cs)
- [```Alarm```](Shield.DataAccess/Models/Alarm.cs)

### REST API

Веб-запросы в <b>ASP.NET</b> реализуются в контроллерах архитектуры MVC. Контроллеры приложения Shield.Web:
- [```AppUserController```](Shield.Web/Controllers/AppUserController.cs)
- [```AppRoleController```](Shield.Web/Controllers/RoleController.cs)
- [```ContractController```](Shield.Web/Controllers/ContractController.cs)
- [```AlarmController```](Shield.Web/Controllers/AlarmController.cs)

Запросы в контроллерах:

![image](https://github.com/user-attachments/assets/b1a64fab-6130-460c-9a9c-dbb9951101ec)<br>
![image](https://github.com/user-attachments/assets/f7310e75-c128-4807-af2c-8feeab04a58a)

> [!TIP]
> Для запуска SwaggerUI (как на скриншотах запросов выше), необходимо [здесь](Shield.Web/Properties/launchSettings.json) убрать комментирование строк ```"launchBrowser": true```.

Инициализация приложения происходит в скрипте [Program.cs](Shield.Web/Program.cs)

[Исходный код Shield.Web](Shield.Web)

## Shield.App

Проект <b>App</b> - это приложение [WinUI 3](https://learn.microsoft.com/en-us/windows/apps/winui/winui3/), используемое в качестве «фронтенда» проекта. 

Описывать механизмы работы фреймворка слишком долго, желающие найдут всю информацию в документации по ссылке выше, здесь вкратце расскажу что я наделал «кастомного» и какие-то интересные фичи.

### Template Studio

В проекте для ускорения разработки было принято использовать [Template Studio WinUI 3](https://github.com/microsoft/TemplateStudio) ([расширение для VS](https://marketplace.visualstudio.com/items?itemName=TemplateStudio.TemplateStudioForWinUICs)).

Это небольшое приложение, позволяющее в пару кликов создать приложение WinUI 3, разместив в нем страницу навигации, которая будет открывать указанные вами в TemplateStudio страницы.<br>
Вся последующая разработка ведется вручную.

![image](https://github.com/user-attachments/assets/35ee5f64-3b4b-4880-91ec-f9035737d667)

### Страницы

Приложение имеет всего 4 [страницы](Shield.App/Views):
- Контракты ```ContractsPage.xaml + ContractsPage.xaml.cs```
- Сигнализации ```AlarmsPage.xaml + AlarmsPage.xaml.cs```
- Профиль ```ProfilePage.xaml + ProfilePage.xaml.cs```
- Настройки ```SettingsPage.xaml + SettingsPage.xaml.cs```

![image](https://github.com/user-attachments/assets/1dc48323-2678-466f-bcb1-cc39a73e6519)<br>
![image](https://github.com/user-attachments/assets/3cd8d9b1-0e7b-4a5f-a811-fa7e6476a5d4)<br>
![image](https://github.com/user-attachments/assets/ef7d6c36-e365-4754-86d8-dacec3d73e98)<br>
![image](https://github.com/user-attachments/assets/b903b0ef-cb32-4431-ba0c-19be478add46)<br>

> [!TIP]
> Вы можете добавить свои страницы в проект, для этого нужно:
> 1. Создать пустую страницу путем выбора шаблона WinUI 3 (ПКМ -> добавить -> все шаблоны -> WinUI 3 -> Пустая страница), традиционно в папке Views
> 2. Создать ее ViewModel в папке ViewModels и привязать к странице (посмотрите пример, допустим, в ContractsPage.xaml.cs)
> 3. Добавить страницу и ViewModel как Transient в Dependency Injection [тут](Shield.App/App.xaml.cs)
> 4. Слинковать ViewModel и Page в [```NavigationHelper.cs```](Shield.App/Helpers/NavigationHelper.cs)
> 5. Добавить элемент ```NavigationMenuItem``` со ссылкой на вашу страницу [тут](Shield.App/Views/ShellPage.xaml) на примере остальных страниц

### Пользовательские элементы управления

Для удобного управления были реализованы следующие [элементы управления](Sheild.App/Controls): 
- ```ContractControl.xaml``` + ```ContractControl.xaml.cs```
- ```AlarmControl.xaml``` + ```AlarmControl.xaml.cs```
- ```RemovableTextBoxControl.xaml``` + ```RemovableTextBoxControl.xaml.cs```

![image](https://github.com/user-attachments/assets/12c661ce-dad5-475b-ba4e-d04212bfbd6e)<br>
![image](https://github.com/user-attachments/assets/efc4814d-96ae-45d3-95df-076b0f6fe13e)<br>
![image](https://github.com/user-attachments/assets/a120f9a5-4d60-4742-b7dc-541a64a713f0)<br>

### Диалоговые окна

Для подтверждения действий или заполнения форм было принято использовать диалоговые окна, содержимое которых является полем ```Content``` диалогового окна и представляет из себя пользовательский элемент управления.

Содержимое [диалоговых окон](Shield.App/Dialogs):
- ```CreateContractContent.xaml``` + ```CreateContractContent.xaml.cs```
- ```RegisterContent.xaml``` + ```RegisterContent.xaml.cs```
- ```LoginContent.xaml``` + ```LoginContent.xaml.cs```

![image](https://github.com/user-attachments/assets/b9c32915-9775-4938-95b1-f1170d04f411)<br>
![image](https://github.com/user-attachments/assets/e6a21afb-6e5d-4b23-961d-495e8a9ea264)<br>
![image](https://github.com/user-attachments/assets/c33215b1-9e83-4eb9-a02f-b2a060e32ef5)<br>

### Карта

Для удобства указания адреса объекта в диалоговом окне создания контракта был добавлен элемент управления ```WebView2```, отображающий [эту](Shield.App/Misc/html/map/index.html) HTML страницу. 

> [!IMPORTANT]
> Карта будет работать только при наличии валидного токена Яндекс.Карт

Страница содержит ```div``` с Yandex Maps API, где в строке<br>
```html
<script src="https://api-maps.yandex.ru/2.1/?apikey=APIKEY&lang=ru_RU" type="text/javascript"></script>
```
слово ```APIKEY``` должно быть заменено уникальным токеном [Yandex API](https://developer.tech.yandex.ru/services) (вашим собственным или публикатора приложения)

### Экспорт в ```.docx```

Приложение позволяет экспортировать контракты в документ <b>Word</b>.<br>
Для этого используется библиотека [Spire](https://www.e-iceblue.com/Introduce/free-doc-component.html)

> [!WARNING]
> Используется <b>бесплатная</b> версия библиотеки FreeSpire, где действуют некоторые ограничения. Подбробности читайте в документации.

### План объекта

В диалоговом окне создания контракта пользователя просят выбрать из системы изображение объекта и его план ```.rvt``` формата документа [Autodesk Revit](https://www.autodesk.com/products/revit/overview?term=1-YEAR&tab=subscription)

![image](https://github.com/user-attachments/assets/17cf0929-4efe-4d75-8d80-d60386e06e12)

![image](https://github.com/user-attachments/assets/2a2e7a14-ea51-489e-8411-6fce74b3a914)

> [!WARNING]
> <b>Revit</b>, в особенности в паре с <b>AutoCad</b>, могут вызывать привыкание.<br>
> Перед применением проконсультируйтесь со строителем.

> Хочу в BIM Хочу в BIM Хочу в BIM

[Исходный код Shield.App](Shield.App)

## Shield.App.Core

Вспомогательный проект Template Studio, не требующий внесения изменений

[Исходный код Shield.App.Core](Shield.App.Core)
