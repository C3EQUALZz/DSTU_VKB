# Общие сведения

Проект по предмету: `Машинное обучение и искусственый интеллект`

## Задание

### Описание

Разработать телеграмм бота `"Помогатор"`, который взаимодействует с нейронными сетями, которые вы должны обучить сами и использовать.  

## Принцип реализации

В проекте используется архитектурный подход [`DDD`](https://en.wikipedia.org/wiki/Domain-driven_design) и [`EDD`](https://en.wikipedia.org/wiki/Event-driven_programming).
Проект организован по принципу микросервисом, где разделением является - доменная область, в которой применяется микросервис. 

# Зависимости

В проекте используются следующие зависимости: 
- [`poetry`](https://python-poetry.org/)
- [`mypy`](https://www.mypy-lang.org/)
- [`ruff`](https://docs.astral.sh/ruff/linter/)
- [`isort`](https://pycqa.github.io/isort/)
- [`faststream[aiokafka]`](https://faststream.airt.ai/latest/)
- [`fastapi`](https://fastapi.tiangolo.com/)
- [`prometheus-fastapi-instrumentator`](https://github.com/trallnag/prometheus-fastapi-instrumentator)
- [`concurrent-log-handler`](https://github.com/Preston-Landers/concurrent-log-handler)
- [`dishka`](https://dishka.readthedocs.io/en/stable/)
- [`taskiq`](https://taskiq-python.github.io/)
- [`taskiq-redis`](https://github.com/taskiq-python/taskiq-redis)
- [`aiogram`](https://aiogram.dev/)
- [`aiogram-i18n`](https://aiogram-i18n.readthedocs.io/en/latest/)
- [`tenserflow`](https://www.tensorflow.org/?hl=ru)
- [`taskiq-aiogram`](https://pypi.org/project/taskiq-aiogram/)
- [`sqlalchemy[asyncpg]`](https://www.sqlalchemy.org/)
- [`opencv`](https://opencv.org/)
- [`formatter-chatgpt-telegram`](https://github.com/Latand/formatter-chatgpt-telegram)
- [`pydantic`](https://docs.pydantic.dev/latest/)
  
> [!IMPORTANT]
> Все зависимости можно найти в `pyproject.toml` каждого микросервиса

# Структура проекта

Сама логика приложения находится в `app`. Внутри данной директории есть 5 модулей.

- `application`
- `domain`
- `infrastructure`
- `logic`
- `settings`

Рассмотрим каждый модуль по отдельности зачем он нужен за что отвечает. 

## Что такое `domain`? 

В основе `DDD` - Домен (Domain). Это модель предмета и его задач, под которые строится приложение. Счет, который оплачиваем, Сообщение, которое отправляем, или Пользователь, которому выставляем оценку. Домены строятся на сущностях из реального мира и ложатся в центр приложения. 

> [!NOTE]
> Например, по заданию у нас библиотека, где нужно оперировать книгами, поэтому `domain` - это книга. 
> Если добавится сервис регистрации, то появится новый `domain` - это человек.

### Что там находится внутри директории `domain`?

Там Вы найдете 2 директории, которые Вас должны заинтересовать `entities` и `values`. 

- [`entities`](https://blog.jannikwempe.com/domain-driven-design-entities-value-objects) - это и есть наши домены, про которые я говорил выше.
- [`values`](https://blog.jannikwempe.com/domain-driven-design-entities-value-objects) - здесь находятся, так называемые, `value objects`. Грубо говоря, это характеристики нашего домена, т.е поля (атрибуты) `domain`. Почему делается так? Все очень просто: для валидации данных.

> [!NOTE]
> Если Вы хотите добавить новый `domain`, то создайте `Python` файл, который описывает его. Например, `peoples.py`. Ваш класс должен наследоваться от [`BaseEntity`](app/domain/entities/base.py). Пример прилагаю ниже: 

```python
@dataclass(eq=False)
class Human:
  """
  Domain which associated with the real human
  """
  nickname: NickName
  email: Email
  is_active: bool
```

> [!NOTE]
> Если Вы хотите добавить новый `value object`, то создайте `Python` файл, который описывает его. Например, `surname.py`. Ваш класс должен наследоваться от `BaseValueObject`. Пример прилагаю ниже:

```python
@dataclass(frozen=True)
class NickName(BaseValueObject[str]):
    """
    Value object which associated with the book name
    """
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 15:
            raise ValueTooLongException(self.value)

    @override
    def as_generic_type(self) -> str:
        return self.value
```

## Что такое `application`?

Здесь обычно содержится `api` для работы с приложением. Различные [backend endpoints](https://dev.to/apidna/api-endpoints-a-beginners-guide-ief), [sockets](https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%BA%D0%B5%D1%82_(%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D1%8B%D0%B9_%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81)) и т.п. 
Каждая директория в `api` - это handlers для сущности (домен), с которой мы работаем.

> [!NOTE]
> Например, по заданию у нас библиотека, где нужно оперировать книгами, поэтому директория называется `books`. 
> Если бы нужно было добавить функционал для работы с пользователем, то в `application/api` появилась бы директория `people`.

### Что за файлы в `application/api/{domain}`?

- `dependencies.py` - здесь находится логика, к которой должны обращаться `handlers`, чтобы выполнить определенные бизнес задачи. Делается с той целью, чтобы было минимальное количество кода в handlers. Пример для книги [`dependencies.py`](app/application/api/books/dependecies.py)
- `handlers.py` - здесь находится та часть, которая выступает "мордой" нашего приложения. В данном случае здесь находятся функции, которые запрашивают данные от пользователя и запускают определенные функции из `dependencies.py`. Например, здесь могут уже находиться ручки `FastAPI`, которые в свою очередь вызывают через [`Depends`](https://fastapi.tiangolo.com/tutorial/dependencies/) определенные функции из `dependencies.py`. Пример для книги [`handlers.py`](app/application/api/books/handlers.py)
- `schemas.py` - здесь находятся схемы валидации данных или просто [`DTO`](https://ru.wikipedia.org/wiki/DTO). В реальных кейсах используются [`pydantic BaseModel`](https://docs.pydantic.dev/latest/api/base_model/) для валидации данных. Пример для книги [`schemas.py`](app/application/api/books/schemas.py)

## Что такое `infrastrucutre`?

На данном слое архитектуры реализована логика работы с данными посредством следующих паттернов:
 
- [`Unit Of Work`](https://qna.habr.com/q/574561)
- [`Repository`](https://www.cosmicpython.com/book/chapter_02_repository.html), 
- [`Service`](https://lyz-code.github.io/blue-book/architecture/service_layer_pattern/)
- [`Message Bus`](https://dev.to/billy_de_cartel/a-beginners-guide-to-understanding-message-bus-architecture-22ec)
- [`Dependecy Injection`](https://thinhdanggroup.github.io/python-dependency-injection/)

### Что там находится внутри директории `infrastrucutre`?

Здесь вы найдете директории и `Python` файлы для описания работ. Каждая директория также называется, как и паттерн, которые я указал выше. Давайте рассмотрим каждый из них по отдельности.  

#### `Repository`

Здесь реализована логика работы с базой данных на уровне объектов. Репозиторий управляет коллекцией доменов (моделей).

Как можно написать свой репозиторий? Все очень просто: Вам нужно унаследоваться от интерфейса, который описывает ваш домен.

Например, я приведу реализацию `SQLAlchemyUserRepository`, где используется библиотека [`SQLAlchemy`](https://www.sqlalchemy.org/).

```python
class SQLAlchemyUsersRepository(SQLAlchemyAbstractRepository[UserEntity], UsersRepository):

    def get(self, id: int) -> Optional[UserEntity]:
        result: Result = self._session.execute(select(UserEntity).filter_by(id=id))
        return result.scalar_one_or_none()

    def get_by_title(self, title: str) -> Optional[UserEntity]:
        result: Result = self._session.execute(select(UserEntity).filter_by(title=title))
        return result.scalar_one_or_none()

    def add(self, model: UserEntity) -> UserEntity:
        result: Result = self._session.execute(
            insert(UserEntity).values(**await model.to_dict(exclude={'oid'})).returning(UserEntity)
        )

        return result.scalar_one()
```

#### `Unit Of Work`

Название паттерна `Unit of Work` намекает на его задачу управлять атомарностью операций. 

Приведу пример того, как написать свой `Unit of Work` для книг, используя [`SQLAlchemy`](https://www.sqlalchemy.org/).

```python
class SQLAlchemyAbstractUnitOfWork(AbstractUnitOfWork):
    """
    Unit of work interface for SQLAlchemy, from which should be inherited all other units of work,
    which would be based on SQLAlchemy logics.
    """

    def __init__(self, session_factory: sessionmaker = default_session_factory) -> None:
        super().__init__()
        self._session_factory: sessionmaker = session_factory

    def __enter__(self) -> Self:
        self._session: Session = self._session_factory()
        return super().__aenter__()

    def __exit__(self, *args, **kwargs) -> None:
        super().__exit__(*args, **kwargs)
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.expunge_all()
        self._session.rollback()


class SQLAlchemyUsersUnitOfWork(SQLAlchemyAbstractUnitOfWork, UsersUnitOfWork):

    def __enter__(self) -> Self:
        uow = super().__enter__()
        self.users: UsersRepository = SQLAlchemyUsersRepository(session=self._session)
        return uow
```

### `Service`

Здесь агрегируется логика `UoW` и `Repository`. Именно из-под данного слоя идет работа с данными уже для обращения в командах.
Сервисы всегда пишутся на ванильном Python (как я вижу в примерах), так что здесь имеет смысл писать новый сервис, если добавилась новая сущность в проект.  
Пример сервиса для книг можете увидеть [здесь](app/infrastructure/services). 

Приведу пример того, как написать новый сервис, если появилась сущность (домен) `Human`

```python
class UsersService:
    """
    Service layer core according to DDD, which using a unit of work, will perform operations on the domain model.
    """

    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow = uow

    def add(self, user: UserEntity) -> UserEntity:
        with self._uow as uow:
            new_human = uow.people.add(model=user)
            uow.commit()
            return new_human

    def check_existence(self, oid: Optional[str] = None, email: Optional[str] = None) -> bool:
        if not (oid or email):
            return False

        with self._uow as uow:
            if oid and uow.people.get(oid):
                return True

            if title and uow.people.get_by_email(email):
                return True

        return False
```

## Что такое `logic`?

Здесь на данном слое собрана вся бизнес логика, где требуется реализовать наш функционал по тз. 
В `logic` у нас есть директории `commands` и `events`, `handlers`. 

События - это побочные действия, которые выполняются после определенной команды. Например, при создании пользователя отправить ему email об успешной регистрации. 

### `Commands`

Команды - это действие, которое должно выполнять наше приложение. Например, создать пользователя, создать книгу, удалить книгу. Обычно это оформляется в виде `DTO` класса. Примеры вот [здесь](app/logic/commands/books.py).
Но если команды это `DTO`, то как осуществлять бизнес логику? Здесь на помощь приходят `handlers`, которые вы можете увидеть ниже. Пока приведу пример того, как написать свою команды для регистрации условного человека в нашей библиотеке. 

```python
@dataclass(frozen=True)
class RegisterHumanCommand(AbstractCommand):
    username: str
    password: str
    email: str
```

### `CommandHandlers`

Это как раз перехватчики наши команд, которые ожидают `DTO`, написанный вами ранее. Именно здесь идет логика уже. Приведу пример того, как написать `handler` для команд. 

```python

CT = TypeVar("CT", bound=AbstractCommand)

class UsersCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: PeopleUnitOfWork) -> None:
        self._uow = uow

class RegisterHumanCommandHandler(UsersCommandHandler[RegisterHumanCommand]):

    def __call__(self, command: RegisterHumanCommand) -> Human:
        """
        Registers a new user, if user with provided credentials doesn't exist, and creates event signaling that
        operation was successfully executed.
        """

        people_service = PeopleService(uow=self._uow)
        if people_service.check_user_existence(email=command.email, username=command.username):
            raise UserAlreadyExistsError

        human = Human(**command.to_dict())
        human.password = hash_password(human.password)

        return people_service.register(human=human)
```

Но встает вопрос. Как это все связать, чтобы все заработало? Вам нужно добавить в контейнере в словарике команду и её перехватчик.
Например, чтобы добавить команду и наш хендлер, нужно в конце добавить значение `RegisterHumanCommand: RegisterHumanCommandHandler`. В результате у Вас должен получится вот такой словарик. 

```python
COMMANDS_HANDLERS_FOR_INJECTION: Dict[Type[CT], Type[AbstractCommandHandler[CT]]] = {
    CreateBookCommand: CreateBookCommandHandler,
    GetBookByIdCommand: GetBookByIdCommandHandler,
    GetBookByTitleCommand: GetBookByTitleCommandHandler,
    GetBookByTitleAndAuthorCommand: GetBookByTitleAndAuthorCommandHandler,
    GetAllBooksCommand: GetAllBooksCommandHandler,
    UpdateBookCommand: UpdateBookCommandHandler,
    DeleteBookCommand: DeleteBookCommandHandler,
    RegisterHumanCommand: RegisterHumanCommandHandler,
}
``` 

## Что такое `settings`?

Здесь находятся параметры подключения к БД обычно, настройки логгирования и т.п.
В рамках тестового задания настройка логгирования и класс Settings, в котором я указываю путь к файлу для сохранения `json`.

Приведу пример ниже, как обычно оформляют класс Settings для backend приложений с использованием `pydantic` и `pydantic-settings`. 

```python
class MongoSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MONGO_DB",
        extra="ignore"
    )

    url: MongoDsn = Field(alias="MONGO_DB_URL")
    chat_database: str = Field(default="chat", alias="MONGO_DB_CHAT_DATABASE")
    chat_collection: str = Field(default="chat", alias="MONGO_DB_CHAT_COLLECTION")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore"
    )

    database: MongoSettings = MongoSettings()
```

# Как можно улучшить проект? 

В качестве улучшений можно было бы добавить [`IoC контейнер`](https://en.wikipedia.org/wiki/Inversion_of_control), использовав [`punq`](https://github.com/bobthemighty/punq) или крутой фреймворк [`dishka`](https://github.com/reagento/dishka), чтобы настраивать зависимости в одном месте и не дублировать код, как у меня в [`dependecies.py`](app/application/api/books/dependecies.py).

# Установка проекта и запуск

Команда для запуска представлена ниже: 

> [!IMPORTANT]
> - Предполагается, что в Вашей системе уже установлены `git`, `Docker`, `Make`.
> - Для каждой директории в текущем проекте, где `README.md` создайте файл `.env`, как показано в примере `.env.example`.
> - В нужных проектах создайте нейросети, скачав их на свой ПК или же запустив их тренировку. Более подробно смотрите в каждой директории, где есть постфикс `-service`.

```bash
git clone https://github.com/C3EQUALZz/DSTU_VKB
cd machine_learning/project
make all
```

После того, как вы настроили, то можете общаться с вашим телеграмм ботом. Приятного использования! 
