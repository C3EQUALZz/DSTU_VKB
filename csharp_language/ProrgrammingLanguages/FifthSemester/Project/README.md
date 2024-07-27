# Общие сведения

<b>«Shield»</b> представляет из себя пример реализации итогового проекта по курсу .NET 10-й предметной области <b>«Отдел вневедомственной охраны»</b> (далее ОВО).

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

# Структура проекта

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



[Исходный код Shield.Web](Shield.Web)

## Shield.App

[Исходный код Shield.App](Shield.App)

## Shield.App.Core

[Исходный код Shield.App.Core](Shield.App.Core)
