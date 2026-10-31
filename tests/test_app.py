from pathlib import Path
import unittest
from streamlit.testing.v1 import AppTest


class AppTests(unittest.TestCase):
    def test_question_filter_download_and_empty_state(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.metric), 4)
        app.text_input[0].set_value('Show monthly sales trend')
        app.button(key='FormSubmitter:ask-分析問題').click().run()
        self.assertFalse(app.exception)
        self.assertIn('月份', app.success[0].value)
        app.sidebar.multiselect[0].set_value(['Laptop']).run()
        self.assertFalse(app.exception)
        app.text_input[0].set_value('預測明年產品營收')
        app.button(key='FormSubmitter:ask-分析問題').click().run()
        self.assertTrue(app.warning)
        app.sidebar.multiselect[0].set_value([]).run()
        self.assertFalse(app.exception)
        self.assertIn('沒有資料', app.warning[0].value)

    def test_example(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=30)
        app.button[3].click().run()
        self.assertFalse(app.exception)
        self.assertIn('毛利', app.success[0].value)
