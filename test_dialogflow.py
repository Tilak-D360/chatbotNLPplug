import unittest
from dialogflowUtils import *
from main import *
class dialogflowTest(unittest.TestCase):
    def test1_colorRangeExtraction(self):
        tests = [
            {
                'range' : 'c-j',
                'colors' : [],
                'out' : ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            },
            {
                'range' : 'a-d',
                'colors' : ['f', 'm'],
                'out' : ['A', 'B', 'C', 'D', 'F', 'M']
            },
            {
                'range' : 'color a-d',
                'colors' : ['f', 'm'],
                'out' : ['A', 'B', 'C', 'D', 'F', 'M']
            },
            {
                'range' : 'color',
                'colors' : ['f', 'm'],
                'out' : ['F', 'M']
            },{
                'range' : 'color TO',
                'colors' : ['f', 'm'],
                'out' : ['F', 'M']
            }

        ]

        for test in tests:
            out = color_range_extraction(test['range'], test['colors'])
            self.assertEqual(test['out'], out)

    def test2_calcFunc(self):
        tests = [
            {
                'input': 'around mes1 5',
                'output' : [4.85, 5.15]
            },
            {
                'input': 'around mes1 ',
                'output' : []
            },
            {
                'input': ' 3 4 5 6 ct',
                'output' : [3.0, 4.0, 5.0, 6.0]
            },
            {
                'input': '2 to 3 ct',
                'output' : [2.0, 3.0]
            },
            {
                'input': '2-3 ',
                'output' : [2.0, 3.0]
            },
            {
                'input': 'around 2 to 3 ',
                'output' : [1.85, 3.15]
            }
        ]
        for test in tests:
            out = func(test['input'])
            self.assertEqual(test['output'], out)

    def test3_worker(self):
        
        tests = [
            {
                'name' : ['sym_value', 'mes1_value', 'carat_weight'],
                'value' : [['G', 'VG'], ['around 2'], ['2 to 3']],
                'out' : {
                    'name' : ['sym', 'mes1', 'size'],
                    'val' : [['G', 'VG'], [[1.85, 2.15]], [[2.0, 3.0]]]
                }
            },
            {
                'name' : ['sym_value', 'mes1_value', 'carat_weight'],
                'value' : [['G', 'VG'], ['around 2 to 4'], ['2 - 9.10']],
                'out' : {
                    'name' : ['sym', 'mes1', 'size'],
                    'val' : [['G', 'VG'], [[1.85, 4.15]], [[2.0, 9.10]]]
                }
            },
            {
                'name' : ['color_value_range', 'color_value'],
                'value' : [['color i-j'], ['a', 'd']],
                'out' : {
                    'name' : ['color'],
                    'val' : [['A', 'D', 'I', 'J']]
                }
            },
        ]
        for test in tests:
            test_object = {
                'queryResult' : {
                    "queryText": "color i-j",
                    'parameters' : {}
                }
            }
            for x, y in zip(test['name'], test['value']):
                test_object['queryResult']['parameters'][x] = y
            out = workerFun(test_object)
            self.assertEqual(test['out']['name'], out['entityName'])
            self.assertEqual(test['out']['val'], out['entityValue'])
    def test4_queryTester(self):
        tests = [
            # {
            #     'query' : 'symmetry good, very good, mes1  1.85-2.15  weight  2 to 3',
            #     'out' : {
            #         'name' : ['sym', 'mes1', 'size'],
            #         'val' : [['G', 'VG'], [[1.85, 2.15]], [[2.0, 3.0]]]
            #     }
            # },
            {
                'query' : 'symmetry good and very good',
                'out' : {
                    'name' : ['sym'],
                    'val' : [['G', 'VG']]
                }
            },
            {
                'query' : 'symmetry good and very good, mes1  around 2 to 4, weight  2 to 9.10',
                'out' : {
                    'name' : ['sym', 'mes1', 'size'],
                    'val' : [['G', 'VG'], [[1.85, 4.15]], [[2.0, 9.10]]]
                }
            },
            {
                'query' : 'color a, d and color range i to l',
                'out' : {
                    'name' : ['color'],
                    'val' : [['A', 'D', 'I', 'J', 'K', 'L']]
                }
            },
        ]
        for test in tests:
            out = query(test['query'])
            self.assertEqual(test['out']['name'], out['entityName'])
            self.assertEqual(test['out']['val'], out['entityValue'])
if __name__ == "__main__":
    unittest.main()