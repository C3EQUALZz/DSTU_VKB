# Общие сведения

«**repair-service-app**» представляет собой пример реализации `backend` компьютерной мастерской.

## Принцип реализации

Здесь данный проект использует стандартную `Java Spring` архитектуру, которая представлена на фото ниже:

![изображение](https://github.com/user-attachments/assets/52af3dc1-9aa6-4d39-ad0c-6b6ddf59ea13)

Схема базы данных представлена на фото ниже:

![repair_service](https://github.com/user-attachments/assets/973001dc-0900-45be-a281-27fc4ce5b57d)

## Зависимости

- [`Java 23`](https://www.oracle.com/java/technologies/downloads/)
- [`Spring boot`](https://spring.io/projects/spring-boot)
- [`Spring Security`](https://spring.io/projects/spring-security)
- [`Spring Data JPA`](https://spring.io/projects/spring-data-jpa)
- [`Spring Validation`](https://spring.io/guides/gs/validating-form-input)
- [`Spring WebMVC`](https://docs.spring.io/spring-framework/reference/web/webmvc.html)
- [`logback`](https://docs.spring.io/spring-boot/docs/2.1.8.RELEASE/reference/html/howto-logging.html)
- [`springdoc`](https://springdoc.org/)
- [`hypersistence`](https://github.com/vladmihalcea/hypersistence-utils)
- [`jjwt`](https://github.com/jwtk/jjwt)

Более подробно смотрите зависимости [здесь](build.gradle.kts)

## Как установить и использовать данный проект? 

> [!NOTE]
> - Предполагается, что у вас установлена [система контроля версий `Git`](https://git-scm.com/book/ru/v2/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%9E-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B5-%D0%BA%D0%BE%D0%BD%D1%82%D1%80%D0%BE%D0%BB%D1%8F-%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B9)
> - Предполагается, что у вас установлена [система сборки проекта `Gradle`](https://gradle.org/)
> - Предполагается, что у вас установлен [`Docker`](https://www.docker.com/)

### Настройка вручную через консоль

Скачиваем репозиторий, используя систему контроля версий `Git`: 

```bash
git clone https://github.com/morrs1/repair-service-app.git
```

Скачиваем зависимости `gradle`:

```bash
./gradlew build
```

Теперь вам нужно создать файл `.env`, который будет повторять содержимое данного [файла](.env.example). 

Запускаем все зависимости, находясь в корне проекта, используя команду, которая представлена ниже:

```bash
docker compose -f docker/docker-compose.yaml --env-file=.env up
```

Теперь запускаем, используя команду ниже:

```bash
./gradlew run
```

### Настройка через `IDEA`:

Скачиваем репозиторий, используя систему контроля версий `Git`: 

```bash
git clone https://github.com/morrs1/repair-service-app.git
```

Теперь у вас появистя уведомление по сборке проекта. После удачной установки вам нужно создать файл `.env`, который будет повторять содержимое данного [файла](.env.example). 

Запускаем все зависимости, находясь в корне проекта, используя команду, которая представлена ниже:

```bash
docker compose -f docker/docker-compose.yaml --env-file=.env up
```

Теперь запускаем через кнопочку, которая есть в `IDEA`. 

> [!NOTE]
> Работа с `Gradle` в `IDEA` [тык](https://www.jetbrains.com/help/idea/gradle.html)

### Настройка и запуск проекта через терминал + `Docker` (вариант для деплоя)

Скачиваем репозиторий, используя систему контроля версий `Git`: 

```bash
git clone https://github.com/morrs1/repair-service-app.git
```

Теперь вам нужно создать файл `.env`, который будет повторять содержимое данного [файла](.env.example). 

Зайдите [сюда](src/main/resources/application.yml), закоментируйте строки, которые представлены ниже:

```bash
config:
  import: "file:.env[.properties]"
```

> [!IMPORTANT]
> Если все-таки желаете запускать `Spring` приложение из-под `IDEA`, то уберите комментарии. 

Находясь теперь в корне проекта, вбейте в терминал команду, которая представлена ниже:

```bash
docker compose -f docker/docker-compose-override.yaml --env-file=.env up
```

## Поддержка проекта

...

## Документация `Swagger`

Чтобы перейти в `Swagger` используйте url: `http://localhost:<port>/swagger-ui/index.html#/`, где `port` вы определили в `.env`.
Если вы запускаете из-под `IDEA`, то переходите по порту `8080`.

![изображение](https://github.com/user-attachments/assets/9afd0b1c-813e-4b8f-b0bb-8162e513ba7d)


## Полезные ссылки

- [Как настраивать `Swagger`?](https://struchkov.dev/blog/ru/api-swagger/)
- [Как настраивать `Swagger` c `Spring Security`](https://www.javainuse.com/boot3/sec/8)
- [Почему функции некоторые были написаны без комментариев с `changeSet`](https://stackoverflow.com/questions/34712347/create-function-from-sql-script-by-liquibase)
