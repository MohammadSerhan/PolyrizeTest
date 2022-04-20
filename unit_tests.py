import unittest
import DB_operations

class TestDB(unittest.TestCase):
    def test_insert_material(self):
        result = DB_operations.insert_material('test1', 5)
        testvalue = DB_operations.get_material('test1')
        self.assertEqual(result, True)
        self.assertEqual(testvalue[0], 'test1')
        self.assertEqual(testvalue[1], 5)
        #cleanup DB
        DB_operations.remove_material('test1')

    def test_edit_material(self):
        result = DB_operations.insert_material('test1', 5)
        testvalue = DB_operations.get_material('test1')
        self.assertEqual(result, True)
        self.assertEqual(testvalue[0], 'test1')
        self.assertEqual(testvalue[1], 5)
        result = DB_operations.insert_material('test1', 10)
        testvalue = DB_operations.get_material('test1')
        self.assertEqual(result, True)
        self.assertEqual(testvalue[0], 'test1')
        self.assertEqual(testvalue[1], 10)

        #cleanup
        DB_operations.remove_material('test1')

    def test_remove_material(self):
        DB_operations.insert_material('test1', 5)
        DB_operations.remove_material('test1')
        testvalue = DB_operations.get_material('test1')
        self.assertEqual(testvalue, None)

    def test_insert_product(self):
        DB_operations.insert_material('test1', 4)
        DB_operations.insert_material('test2', 3)
        DB_operations.insert_material('test3', 5)
        
        result = DB_operations.insert_product("test_prod", ['<test1, 8>', '<test2, 3>', '<test3, 6>'])
        testvalue = DB_operations.get_product("test_prod")
        self.assertEqual(result, True)
        #8*4 + 3*3 + 6*5 = 71
        self.assertEqual(testvalue[1], 71)

        DB_operations.insert_material('test1', 6)
        testvalue = DB_operations.get_product("test_prod")
        #8*6 + 3*3 + 6*5 = 87
        self.assertEqual(testvalue[1], 87)

        #cleanup 
        DB_operations.remove_material('test1')
        DB_operations.remove_material('test2')
        DB_operations.remove_material('test3')
        DB_operations.remove_product('test_prod')
        
    def test_edit_product(self):
        DB_operations.insert_material('test1', 4)
        DB_operations.insert_material('test2', 3)
        DB_operations.insert_material('test3', 5)
        
        result = DB_operations.insert_product("test_prod", ['<test1, 8>', '<test2, 3>', '<test3, 6>'])
        testvalue = DB_operations.get_product("test_prod")
        self.assertEqual(result, True)
        #8*4 + 3*3 + 6*5 = 71
        self.assertEqual(testvalue[1], 71)

        DB_operations.insert_product("test_prod", ['<test1, 1>', '<test2, 3>', '<test3, 6>'])
        testvalue = DB_operations.get_product("test_prod")
        #1*4 + 3*3 + 6*5 = 43
        self.assertEqual(testvalue[1], 43)

        DB_operations.insert_product("test_prod", ['<test2, 5>', '<test3, 6>'])
        testvalue = DB_operations.get_product("test_prod")
        #5*3 + 6*5 = 45
        self.assertEqual(testvalue[1], 45)

        #cleanup 
        DB_operations.remove_material('test1')
        DB_operations.remove_material('test2')
        DB_operations.remove_material('test3')
        DB_operations.remove_product('test_prod')
    
    def test_remove_product(self):
        DB_operations.insert_material('test1', 4)
        DB_operations.insert_material('test2', 3)
        
        result = DB_operations.insert_product("test_prod", ['<test1, 8>', '<test2, 3>'])
        
        self.assertEqual(result, True)
        DB_operations.remove_product('test_prod')
        testvalue = DB_operations.get_product("test_prod")

        self.assertEqual(testvalue, None)
        #cleanup 
        DB_operations.remove_material('test1')
        DB_operations.remove_material('test2')
        DB_operations.remove_product('test_prod')

if __name__ == '__main__':
    unittest.main()