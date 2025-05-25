Software Design | BHW 2

Автор: Лившиц Леонид Игоревич, БПИ 235

“Text Scanner”

Проект на Python FastAPI для анализа текстовых файлов:

* подсчёт количества параграфов, слов и символов;
* генерация Word Cloud через QuickChart Word Cloud API.

---

## Архитектура

Система состоит из трёх микросервисов, каждый с собственным Dockerfile, объединённых `docker-compose.yml`:

1. **API Gateway**

   – единственная точка входа для клиента;

   – верификация JWT;

   – маршрутизация запросов к остальным сервисам.

2. **File Storing Service**

   – приём и хранение загруженных файлов;

   – выдача файла по `id`.

3. **File Analysis Service**

   – скачивание текста у File Storing Service;

   – подсчёт статистики (параграфы, слова, символы);

   – генерация URL облака слов;

   – сохранение результатов в БД;
   
   – выдача результатов и скачивание готового PNG с облаком слов. (может не работать из-за соединения или корса)

---

## Базы данных

Используется PostgreSQL (self-hosted в Docker):

### File Service

* Таблица `FileMeta`:

  * `id` - идентификатор;
  * `filename`, `content_type`, `size`;
  * `upload_time`.
* Файлы лежат в локальном `volume`.

### File Analysis Service

* Таблица `analysis_results`:

  * `id`, `file_id` - связь с файлом;
  * `paragraphs`, `words`, `characters`;
  * `wordcloud_url` - ссылка на QuickChart;
  * `created_at`.
* Само изображение облака слов не сохраняется в БД, оно доступно по URL или через скачивание.

---

## Тестирование

* API документировано Swagger/OpenAPI, доступно на каждом сервисе:

  * Gateway:  `http://localhost:8000/docs`
  * File Service:  `http://localhost:8001/docs`
  * Analysis Service:  `http://localhost:8002/docs`

> **Дисклеймер:** некоторые запросы могут вернуть ошибку `502` или  `500`, но это точно не внутренняя ошибка, правда-правда.

---

## Запуск проекта

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/leonidlivshits/Software-Design-big-hw-2.git
   cd Software-Design-big-hw-2
   ```

2. Скопируйте пример `.env.sample` в корне и заполните свои настройки:

   ```bash
   cp .env.sample .env
   ```

3. Сгенерируйте JWT для тестов Gateway:

   ```bash
   python generate_token.py
   ```

   Скопируйте выданный `Bearer <token>` и вставьте его в Swagger UI или в заголовок `Authorization`.

4. Активиуйте ввиртульное окружение, запустите все сервисы через Docker Compose:

   ```bash
   venv/scripts/activate
   docker-compose up --build
   ```

---

## Примеры curl-запросов

### API Gateway (порт 8000)

```bash
# Загрузка файла
curl -X POST http://localhost:8000/api/files/ \
  -H "Authorization: Bearer <token>" \
  -F "file=@example.txt"

# Скачивание файла по ID
curl http://localhost:8000/api/files/2 \
  -H "Authorization: Bearer <token>" --output downloaded.txt

# Запуск анализа
curl -X POST http://localhost:8000/api/analyze/2 \
  -H "Authorization: Bearer <token>"

# Получение результатов анализа
curl http://localhost:8000/api/analyze/2 \
  -H "Authorization: Bearer <token>"

# Скачивание картинки облака слов
curl http://localhost:8000/api/analyze/2/wordcloud \
  -H "Authorization: Bearer <token>" --output cloud.png
```

### File Storing Service (порт 8001)

```bash
curl -X POST http://localhost:8001/files/ \
  -F "file=@example.txt"

curl http://localhost:8001/files/2 --output downloaded.txt
```

### File Analysis Service (порт 8002)

```bash
curl -X POST http://localhost:8002/analyze/2
curl    http://localhost:8002/analyze/2
curl    http://localhost:8002/analyze/2/wordcloud --output cloud.png
```

---

Внимание: Если что-то упало, попробуйте повторить операцию позже, возможно дело в соединении (это касается API Wordcloud). Если, что, есть демонстрационное фото с файлом file_service\storage\5_SE BHW 2.txt
