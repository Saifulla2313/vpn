# Развёртывание VPN Bot на сервере

## Требования

- Docker и Docker Compose
- Домен с настроенным DNS (A-запись на IP сервера)
- SSL сертификат (Let's Encrypt)

## Шаги развёртывания

### 1. Клонирование проекта

```bash
git clone <your-repo-url> vpn-bot
cd vpn-bot
```

### 2. Настройка переменных окружения

```bash
cp .env.example .env
nano .env
```

Обязательно заполните:
- `BOT_TOKEN` - токен бота от @BotFather
- `ADMIN_IDS` - ваш Telegram ID
- `DATABASE_URL` - оставьте для Docker: `postgresql+asyncpg://vpnbot:vpnbot_password@postgres:5432/vpnbot`
- `REDIS_URL` - для Docker: `redis://redis:6379/0`
- `REMNAWAVE_URL`, `REMNAWAVE_API_KEY` - данные RemnaWave панели
- `YOOKASSA_SHOP_ID`, `YOOKASSA_SECRET_KEY` - данные ЮКассы

Также добавьте в `.env`:
```
POSTGRES_USER=vpnbot
POSTGRES_PASSWORD=vpnbot_password
POSTGRES_DB=vpnbot
```

### 3. Настройка nginx

Отредактируйте `nginx/nginx.conf`:
- Замените `your-domain.com` на ваш домен

### 4. Получение SSL сертификата

```bash
mkdir -p nginx/ssl

sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com

sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/
```

### 5. Запуск

```bash
docker-compose up -d
```

### 6. Проверка статуса

```bash
docker-compose ps
docker-compose logs -f vpn-bot
```

## Команды управления

```bash
docker-compose up -d      # Запуск
docker-compose down       # Остановка
docker-compose restart    # Перезапуск
docker-compose logs -f    # Логи

docker-compose exec vpn-bot python -c "from app.database.session import init_db; import asyncio; asyncio.run(init_db())"  # Инициализация БД
```

## Обновление

```bash
git pull
docker-compose build
docker-compose up -d
```

## Настройка автообновления SSL

Добавьте в cron:
```bash
crontab -e
```

```
0 0 1 * * certbot renew --quiet && cp /etc/letsencrypt/live/your-domain.com/fullchain.pem /path/to/vpn-bot/nginx/ssl/ && cp /etc/letsencrypt/live/your-domain.com/privkey.pem /path/to/vpn-bot/nginx/ssl/ && docker-compose -f /path/to/vpn-bot/docker-compose.yml restart nginx
```

## Структура

```
vpn-bot/
├── app/                 # Код приложения
├── static/              # Статические файлы (miniapp)
├── nginx/
│   ├── nginx.conf       # Конфиг nginx
│   └── ssl/             # SSL сертификаты
├── data/                # Данные и бэкапы
├── Dockerfile
├── docker-compose.yml
├── .env                 # Переменные окружения
└── requirements.txt
```

## Troubleshooting

### Бот не запускается
```bash
docker-compose logs vpn-bot
```

### Проблемы с БД
```bash
docker-compose exec postgres psql -U vpnbot -d vpnbot
```

### Миниапп не открывается
1. Проверьте что домен доступен по HTTPS
2. Проверьте nginx логи: `docker-compose logs nginx`
3. Убедитесь что SSL сертификаты на месте

### Webhooks не работают
Добавьте ваш домен в настройки бота через @BotFather:
1. /mybots -> Ваш бот -> Bot Settings -> Domain
2. Укажите ваш домен: `https://your-domain.com`
