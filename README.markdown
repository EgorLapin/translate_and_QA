# Проект "translate_and_QA"

Этот проект объединяет функциональность перевода текста с английского на русский, улучшения перевода через обратный перевод и ответа на вопросы с использованием моделей искусственного интеллекта. Он зависит от трех форков репозиториев: `NSUTasks_GenAI_1_02`, `Bidirectional_translation_with_editing` и `Lab1_develop_AI`.

## Установка

Для запуска проекта выполните следующие шаги:

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/EgorLapin/translate_and_QA.git
   cd translate_and_QA
   ```

2. **Создайте виртуальное окружение** (рекомендуется):
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: .\venv\Scripts\Activate.ps1
   ```

3. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```
   Это установит все необходимые пакеты, включая форки репозиториев, `transformers`, `torch`, `sentencepiece`, `numpy` и `sacremoses`.

## Использование

Скрипт `translate_and_QA.py` принимает входные данные в формате JSON через стандартный ввод и возвращает результаты в формате JSON через стандартный вывод.

1. **Создайте файл `input.json`**:
   Пример `input.json`:
   ```json
   {
       "text": "Hello, world!",
       "question": "Что такое искусственный интеллект?"
   }
   ```

2. **(Опционально) Укажите GigaChat токен**:
   Для улучшения перевода требуется токен GigaChat. Получите его на [https://developers.sber.ru/portal/products/gigachat](https://developers.sber.ru/portal/products/gigachat) и укажите в `translate_and_QA.py`:
   ```python
   system = TranslationWithQA(gigachat_token="YOUR_TOKEN_HERE")
   ```
   Без токена перевод не улучшается, используется начальный перевод.

3. **Запустите скрипт**:
   Используйте `input.json` для передачи данных:
   ```bash
   type input.json | python translate_and_QA.py > output.json  # На Windows
   cat input.json | python translate_and_QA.py > output.json  # На Unix
   ```
   Или запустите интерактивно:
   ```bash
   python translate_and_QA.py
   ```
   Затем вставьте JSON в консоль и нажмите `Ctrl+Z` (Windows) или `Ctrl+D` (Unix) для завершения ввода:
   ```json
   {
       "text": "Hello, world!",
       "question": "Что такое искусственный интеллект?"
   }
   ```

4. **Проверьте результаты**:
   Результаты сохраняются в `output.json` (при использовании перенаправления) или выводятся в консоль. Пример `output.json`:
   ```json
   {
       "original_en": "Hello, world!",
       "question": "Что такое искусственный интеллект?",
       "initial_ru": "Привет, мир!",
       "improved_ru": "Здравствуйте, мир!",
       "qa_answer": "Искусственный интеллект — это область компьютерных наук, которая занимается созданием систем, способных выполнять задачи, требующие человеческого интеллекта, такие как обучение, принятие решений и обработка естественного языка.",
       "is_correct": true,
       "f1_score": 0.85,
       "error": null
   }
   ```

## Зависимости

Проект использует следующие репозитории:
- `NSUTasks_GenAI_1_02`
- `Bidirectional_translation_with_editing`
- `Lab1_develop_AI`
А также библиотеки, которые указаны в requirements.txt вместе с вышеуказанными репозиториями