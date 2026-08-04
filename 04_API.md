# HighSpeedVPN — Backend API Specification

**Версия документа:** 1.0
**Дата создания:** 04.08.2026
**Статус:** В разработке

---

# 1. Назначение документа

Документ описывает REST API Backend-сервиса HighSpeedVPN.

Backend API является единой точкой входа для Telegram-бота, панели администратора и внутренних сервисов системы.

---

# 2. Общая информация

## Базовый URL

```text
https://api.highspeedvpn.example/api/v1
```

> Адрес приведен в качестве примера и будет изменен при развертывании.

---

## Формат обмена

* Все запросы и ответы используют JSON.
* Все даты передаются в формате ISO 8601 (UTC).
* Кодировка — UTF-8.

---

## HTTP-коды

| Код | Описание            |
| --- | ------------------- |
| 200 | Успешно             |
| 201 | Создано             |
| 204 | Нет содержимого     |
| 400 | Некорректный запрос |
| 401 | Не авторизован      |
| 403 | Недостаточно прав   |
| 404 | Не найдено          |
| 409 | Конфликт данных     |
| 500 | Внутренняя ошибка   |

---

# 3. Структура API

API разделяется на две части:

```text
/api/v1

├── public
│     ├── users
│     ├── subscriptions
│     ├── tariffs
│     ├── vpn
│     ├── payments
│     └── profile
│
└── admin
      ├── users
      ├── tariffs
      ├── servers
      ├── statistics
      ├── logs
      └── settings
```

---

# 4. Public API

## Пользователи

| Метод | Endpoint                            | Назначение               |
| ----- | ----------------------------------- | ------------------------ |
| POST  | /public/users                       | Регистрация пользователя |
| GET   | /public/users/{id}                  | Получение информации     |
| GET   | /public/users/telegram/{telegramId} | Поиск по Telegram ID     |

---

## Профиль

| Метод | Endpoint        |
| ----- | --------------- |
| GET   | /public/profile |
| PUT   | /public/profile |

---

## Тарифы

| Метод | Endpoint             |
| ----- | -------------------- |
| GET   | /public/tariffs      |
| GET   | /public/tariffs/{id} |

---

## Подписки

| Метод | Endpoint                         |
| ----- | -------------------------------- |
| GET   | /public/subscriptions            |
| GET   | /public/subscriptions/{id}       |
| POST  | /public/subscriptions            |
| PUT   | /public/subscriptions/{id}/renew |

---

## VPN

| Метод | Endpoint               |
| ----- | ---------------------- |
| GET   | /public/vpn/config     |
| POST  | /public/vpn/regenerate |
| GET   | /public/vpn/status     |

---

## Платежи

| Метод | Endpoint                 |
| ----- | ------------------------ |
| POST  | /public/payments/create  |
| POST  | /public/payments/webhook |
| GET   | /public/payments/history |

---

# 5. Admin API

## Пользователи

| Метод  | Endpoint          |
| ------ | ----------------- |
| GET    | /admin/users      |
| GET    | /admin/users/{id} |
| PUT    | /admin/users/{id} |
| DELETE | /admin/users/{id} |

---

## Тарифы

| Метод  | Endpoint            |
| ------ | ------------------- |
| POST   | /admin/tariffs      |
| PUT    | /admin/tariffs/{id} |
| DELETE | /admin/tariffs/{id} |

---

## VPN-серверы

| Метод  | Endpoint            |
| ------ | ------------------- |
| GET    | /admin/servers      |
| POST   | /admin/servers      |
| PUT    | /admin/servers/{id} |
| DELETE | /admin/servers/{id} |

---

## Подписки

| Метод  | Endpoint                  |
| ------ | ------------------------- |
| GET    | /admin/subscriptions      |
| PUT    | /admin/subscriptions/{id} |
| DELETE | /admin/subscriptions/{id} |

---

## Статистика

| Метод | Endpoint                   |
| ----- | -------------------------- |
| GET   | /admin/statistics          |
| GET   | /admin/statistics/users    |
| GET   | /admin/statistics/payments |
| GET   | /admin/statistics/servers  |

---

## Журнал событий

| Метод | Endpoint    |
| ----- | ----------- |
| GET   | /admin/logs |

---

## Настройки

| Метод | Endpoint        |
| ----- | --------------- |
| GET   | /admin/settings |
| PUT   | /admin/settings |

---

# 6. Ответы API

Все ответы имеют единую структуру.

## Успешный ответ

```json
{
  "success": true,
  "data": {}
}
```

---

## Ответ с ошибкой

```json
{
  "success": false,
  "error": {
    "code": "SUBSCRIPTION_EXPIRED",
    "message": "Subscription has expired"
  }
}
```

---

# 7. Авторизация

## Telegram Bot

Backend идентифицирует пользователя по Telegram ID.

---

## Администратор

Используется JWT-токен.

Все административные запросы требуют авторизации.

---

# 8. Версионирование

Все версии API имеют префикс:

```text
/api/v1
```

При несовместимых изменениях создается новая версия (`/api/v2`).

---

# 9. Основные принципы

При разработке API необходимо придерживаться следующих правил:

* единый стиль именования;
* REST-подход;
* JSON для обмена данными;
* единая структура ответов;
* понятные коды ошибок;
* отсутствие бизнес-логики в Telegram-боте;
* вся логика сосредоточена в Backend.

---

# 10. Итог

Backend API является центральным компонентом HighSpeedVPN и обеспечивает взаимодействие между Telegram-ботом, административной панелью, базой данных и сервисом управления WireGuard. Архитектура API рассчитана на расширение функциональности без нарушения обратной совместимости.
