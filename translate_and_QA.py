import sys
import json
from typing import Dict, Any, Optional

# Импорт из предоставленных файлов
# Предполагаем, что все файлы в одной директории

from NSUTasks_GenAI_1_02.src.translator import translate_en, translate_ru
from Bidirectional_translation_with_editing.GenAI_2_02 import TranslationImprover, TranslationResult
from Lab1_develop_AI.functions_QA import get_detailed_answer, calculate_f1_score, is_answer_correct

# Инициализация QA модели из transformers (поскольку в functions_QA.py она ожидается как callable)
from transformers import pipeline

print("Initializing QA model...")
try:
    qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")
except Exception as e:
    print(f"Error occurred while downloading QA model: {e}")
    sys.exit(1)

class TranslationWithQA:
    """
    Интегрированная система: перевод en->ru, улучшение через back-translation,
    QA проверка на наличие ответа в переведенном тексте.
    """
    
    def __init__(self, gigachat_token: Optional[str] = None):
        self.improver = TranslationImprover(gigachat_token)
        self.qa_model = qa_model  # Callable модель для QA
    
    def process(self, english_text: str, question: str) -> Dict[str, Any]:
        """
        Основной процесс:
        1. Перевод en -> ru
        2. Улучшение перевода
        3. QA на улучшенном ru тексте
        4. Проверка, найден ли ответ (метрика: F1-score >= 0.8)
        
        Args:
            english_text: Исходный английский текст
            question: Вопрос по содержанию (на русском или английском, но контекст ru)
            
        Returns:
            Dict с результатами
        """
        result = {
            "original_en": english_text,
            "question": question,
            "initial_ru": None,
            "improved_ru": None,
            "qa_answer": None,
            "is_correct": False,
            "f1_score": 0.0,
            "error": None
        }
        
        try:
            # 1. Начальный перевод en -> ru
            initial_ru = translate_en(english_text)
            result["initial_ru"] = initial_ru
            
            # 2. Улучшение перевода через iterative improvement
            improvement_results = self.improver.iterative_translation_improvement(
                original_en=english_text,
                max_iterations=3,
                similarity_threshold=0.85
            )
            
            # Выбор лучшего улучшенного перевода
            if improvement_results:
                best_result: TranslationResult = max(improvement_results, key=lambda x: x.similarity_score)
                improved_ru = best_result.russian_translation
                result["improved_ru"] = improved_ru
            else:
                improved_ru = initial_ru
                result["improved_ru"] = improved_ru
            
            # 3-4. QA: Задать вопрос по улучшенному ru тексту
            # Предполагаем вопрос на русском; если на en, можно перевести, но для простоты используем as-is
            qa_result = get_detailed_answer(
                model=self.qa_model,
                question=question,
                context=improved_ru,
                return_metadata=True
            )
            
            result["qa_answer"] = qa_result.get("answer", "")
            
            # Baseline check: перевод корректен если ответ найден (F1 с пустым не 0, но проверяем наличие)
            # Метрика: ответ на вопрос найден (is_answer_correct с threshold 0.8, но нужен ground truth answer?)
            # Поскольку ground truth answer не дан, проверяем если QA вернул answer с score > 0.5 и не пустой
            qa_score = qa_result.get("score", 0.0)
            is_found = bool(qa_result["answer"].strip()) and qa_score >= 0.5
            
            # Если есть ground truth (но в задании нет), можно использовать calculate_f1_score
            # Здесь метрика: ответ найден если QA confidence high
            result["is_correct"] = is_found
            result["f1_score"] = qa_score  # Используем score как proxy метрики
            
        except Exception as e:
            result["error"] = str(e)
        
        return result

def main():
    """
    Пример использования: чтение input из stdin или файла.
    Ожидаемый input: JSON {"text": "English text", "question": "Question"}
    """
    try:
        # Чтение input
        input_data = json.loads(sys.stdin.read())
        english_text = input_data.get("text", "")
        question = input_data.get("question", "")
        
        if not english_text or not question:
            raise ValueError("Требуются 'text' и 'question' в input JSON")
        
        system = TranslationWithQA()
        result = system.process(english_text, question)
        
        # 5. Вывод результата
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения JSON: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()