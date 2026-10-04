import ast
import itertools
import json
import unittest
from types import SimpleNamespace
from urllib.parse import urlparse
from html import escape
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).parent
DATA_PATH = ROOT / 'data' / 'knowledge_graph.json'
if not DATA_PATH.exists():
    DATA_PATH = ROOT / 'knowledge_graph.json'


class SearchFlowTests(unittest.TestCase):
    def test_landing_search_and_clear(self):
        app = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(app.text_input[0].value, '')
        self.assertEqual(len(app.checkbox), 0)
        self.assertEqual(len(app.tabs), 0)
        self.assertEqual(len(app.metric), 0)
        self.assertEqual(len(app.sidebar), 0)
        app.text_input[0].set_value('STXBP1').run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.checkbox), 3)
        self.assertEqual(len(app.tabs), 5)
        app.text_input[0].set_value('   ').run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.tabs), 0)
        self.assertEqual(len(app.checkbox), 0)

    def test_view_combinations_and_empty_state(self):
        app = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=30)
        app.text_input[0].set_value('STXBP1').run(timeout=30)
        for selection in itertools.product([False, True], repeat=3):
            for checkbox, enabled in zip(app.checkbox, selection):
                checkbox.set_value(enabled)
            app.run(timeout=30)
            self.assertFalse(app.exception, selection)
            if not any(selection):
                self.assertTrue(any('No graph view selected' in info.value for info in app.info))

    def test_actions_and_persona_removal(self):
        app = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=30)
        for query, contact in [('STXBP1', 'University of Alberta'), ('Dravet', 'Necker-Enfants Malades'), ('CDKL5', "Children's Hospital Colorado")]:
            app.text_input[0].set_value(query).run(timeout=30)
            self.assertFalse(app.exception)
            self.assertEqual(app.tabs[0].label, 'Suggested Action')
            self.assertEqual(app.radio[0].options, ['Family', 'Researcher'])
            text = '\n'.join(item.value for item in app.markdown) + '\n'.join(item.value for item in app.caption)
            self.assertIn(contact, text)
            for unwanted in ['Maria', 'Dr. Osei', 'Independent hackathon prototype']:
                self.assertNotIn(unwanted, text)
        data = json.loads(DATA_PATH.read_text())
        self.assertNotIn('Maria', json.dumps(data))

    def test_search_citations_and_uncited_rejection(self):
        tree = ast.parse((ROOT / 'app.py').read_text())
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'safe_source_url', 'contact_search_payload'}]
        namespace = {'urlparse': urlparse, 'escape': escape}
        exec(compile(ast.Module(body=functions, type_ignores=[]), 'contacts', 'exec'), namespace)
        content = SimpleNamespace(type='output_text', text='<script>Contact [source]', annotations=[
            SimpleNamespace(type='url_citation', url='https://hospital.example/profile', title='Official profile', start_index=16, end_index=24),
        ])
        response = SimpleNamespace(output=[SimpleNamespace(type='message', content=[content])])
        result = namespace['contact_search_payload'](response)
        self.assertIn('&lt;script&gt;', result['html'])
        self.assertIn('https://hospital.example/profile', result['html'])
        content.annotations = []
        self.assertIn('error', namespace['contact_search_payload'](response))
        self.assertFalse(namespace['safe_source_url']('javascript:alert(1)'))

    def test_search_changes_primary_researcher(self):
        app = AppTest.from_file(str(ROOT / 'app.py')).run(timeout=30)
        for query, researcher in [('STXBP1', 'Saadet Mercimek-Andrews'), ('Dravet', 'Rima Nabbout'), ('CDKL5', 'Scott Demarest')]:
            app.text_input[0].set_value(query).run(timeout=30)
            self.assertFalse(app.exception)
            researcher_names = [item.value for item in app.markdown if item.value.startswith('**') and item.value.endswith('**')]
            self.assertEqual(researcher_names[0], f'**{researcher}**')
        app.text_input[0].set_value('<unknown>').run(timeout=30)
        self.assertFalse(app.exception)
        html = '\n'.join(item.value for item in app.markdown)
        self.assertIn('No supported route yet', html)
        self.assertIn('&lt;unknown&gt;', html)

    def test_ranking_counts_unique_authored_papers(self):
        tree = ast.parse((ROOT / 'app.py').read_text())
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'node_lookup', 'researcher_ranking'}]
        namespace = {}
        exec(compile(ast.Module(body=functions, type_ignores=[]), 'ranking', 'exec'), namespace)
        data = json.loads(DATA_PATH.read_text())
        rank = namespace['researcher_ranking'](data, {'dis_2'})
        self.assertEqual(rank[0]['researcher']['id'], 'researcher_2')
        self.assertEqual(rank[0]['direct'], 1)
        authored = next(e for e in data['edges'] if e['source'] == 'researcher_2' and e['relationship'] == 'AUTHORED')
        data['edges'].append(dict(authored))
        self.assertEqual(namespace['researcher_ranking'](data, {'dis_2'})[0]['direct'], 1)


if __name__ == '__main__':
    unittest.main()
