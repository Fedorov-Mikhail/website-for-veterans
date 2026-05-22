# Деплой проекта в продакшен через Docker (шаги 1-7)

## 1. Подготовить сервер
Нужен Linux-сервер (обычно Ubuntu 22.04+) с открытыми портами `80` и `443`, установленными Docker и Docker Compose plugin.

## 2. Склонировать проект и перейти в папку
```bash
git clone https://github.com/Fedorov-Mikhail/website-for-veterans.git
cd website-for-veterans
```

## 3. Подготовить переменные окружения
Скопируйте шаблон и заполните значения:
```bash
cp .env.example .env
```
Обязательно заполните:
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD` (app password Gmail)

## 4. Настроить DNS домена
У домена/поддомена создайте `A`-запись на IP сервера.  
Для Cloudflare включайте proxy (`orange cloud`) после проверки, что сайт открывается по HTTP.

## 5. Собрать и запустить контейнеры
```bash
docker compose up -d --build
```
После старта проверить:
```bash
docker compose ps
docker compose logs -f web
docker compose logs -f nginx
```

## 6. Подключить SSL (рекомендуемый вариант для этого проекта)
Для одностраничного сайта проще всего:
- использовать Cloudflare (режим `Full (strict)`),
- на сервере оставить Nginx как reverse-proxy (уже настроен в `deploy/nginx/default.conf`).

Если нужен SSL прямо на сервере без Cloudflare, добавьте certbot/Traefik, но это отдельный шаг.

## 7. Финальная проверка продакшена
Проверьте:
1. Главная открывается с домена.
2. Картинки и стили загружаются.
3. Форма "Сообщить о неточности" отправляет письмо.
4. Rate limit формы срабатывает после превышения лимита.
5. Перезапуск после ребута работает (`restart: unless-stopped` уже включен).

