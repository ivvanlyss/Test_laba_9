"""
Упрощенные автотесты для лабораторной работы по GitHub Actions
"""

import unittest
import os
import sys
from datetime import datetime

class TestCalculator(unittest.TestCase):
    """Тесты простого калькулятора"""
    
    def test_addition(self):
        """Тест сложения"""
        self.assertEqual(2 + 2, 4)
        self.assertEqual(0 + 5, 5)
        self.assertEqual(-3 + 3, 0)
    
    def test_subtraction(self):
        """Тест вычитания"""
        self.assertEqual(5 - 3, 2)
        self.assertEqual(10 - 10, 0)
        self.assertEqual(-5 - 5, -10)
    
    def test_multiplication(self):
        """Тест умножения"""
        self.assertEqual(3 * 4, 12)
        self.assertEqual(0 * 100, 0)
        self.assertEqual(-2 * 3, -6)
    
    def test_division(self):
        """Тест деления"""
        self.assertEqual(10 / 2, 5)
        self.assertEqual(0 / 5, 0)
        with self.assertRaises(ZeroDivisionError):
            _ = 5 / 0
    
    def test_environment(self):
        """Тест окружения"""
        # Проверяем, что Python работает
        self.assertTrue(isinstance(sys.version, str))
        
        # Проверяем рабочую директорию
        self.assertTrue(os.path.exists("."))
        
        # Проверяем текущую дату
        current_year = datetime.now().year
        self.assertGreater(current_year, 2020)
        self.assertLess(current_year, 2030)

class TestStringOperations(unittest.TestCase):
    """Тесты строковых операций"""
    
    def test_string_concatenation(self):
        """Тест конкатенации строк"""
        self.assertEqual("Hello" + " " + "World", "Hello World")
        self.assertEqual("Test" * 3, "TestTestTest")
    
    def test_string_methods(self):
        """Тест строковых методов"""
        text = "Hello World"
        self.assertEqual(text.upper(), "HELLO WORLD")
        self.assertEqual(text.lower(), "hello world")
        self.assertEqual(len(text), 11)
        self.assertTrue(text.startswith("Hello"))
        self.assertTrue(text.endswith("World"))
    
    def test_string_formatting(self):
        """Тест форматирования строк"""
        name = "Alice"
        age = 30
        formatted = f"{name} is {age} years old"
        self.assertEqual(formatted, "Alice is 30 years old")
        
        formatted2 = "{} is {} years old".format(name, age)
        self.assertEqual(formatted2, "Alice is 30 years old")

class TestFileOperations(unittest.TestCase):
    """Тесты файловых операций"""
    
    def setUp(self):
        """Подготовка теста"""
        self.test_filename = "test_file.txt"
        self.test_content = "This is test content\nFor testing purposes"
    
    def tearDown(self):
        """Очистка после теста"""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    def test_file_creation(self):
        """Тест создания файла"""
        # Создаем файл
        with open(self.test_filename, 'w') as f:
            f.write(self.test_content)
        
        # Проверяем, что файл создан
        self.assertTrue(os.path.exists(self.test_filename))
        
        # Проверяем содержимое
        with open(self.test_filename, 'r') as f:
            content = f.read()
        self.assertEqual(content, self.test_content)
    
    def test_file_appending(self):
        """Тест добавления в файл"""
        # Создаем файл
        with open(self.test_filename, 'w') as f:
            f.write("Initial content")
        
        # Добавляем текст
        with open(self.test_filename, 'a') as f:
            f.write("\nAppended content")
        
        # Проверяем результат
        with open(self.test_filename, 'r') as f:
            content = f.read()
        expected = "Initial content\nAppended content"
        self.assertEqual(content, expected)

def run_tests():
    """Запуск всех тестов"""
    print("=" * 60)
    print("Запуск автотестов для лабораторной работы")
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Создаем test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем тесты
    suite.addTests(loader.loadTestsFromTestCase(TestCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestStringOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим статистику
    print("\n" + "=" * 60)
    print("СТАТИСТИКА ТЕСТОВ:")
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        return 0
    else:
        print("\n❌ НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ!")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())