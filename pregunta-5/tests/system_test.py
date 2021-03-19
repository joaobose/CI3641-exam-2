from ..src.system import TypeSystem
import unittest


class SystemTest(unittest.TestCase):
    def test_types(self):
        s = TypeSystem()

        # --------------- parse
        to_parse = 'a -> a -> a'
        transformed = s.typ_parser.inter(to_parse)
        self.assertEqual(to_parse, str(transformed))

        # --------------- unificacion

        # ----- domain constant
        constant_constant = 'Int -> Bool'
        constant_constant_t = s.typ_parser.inter(constant_constant)

        correct_constant = 'Int'
        correct_constant_t = s.typ_parser.inter(correct_constant)

        self.assertEqual('Bool', str(
            constant_constant_t.unify(correct_constant_t)))

        wrong_constant = 'Bool'
        wrong_constant_t = s.typ_parser.inter(wrong_constant)
        with self.assertRaises(Exception):
            constant_constant_t.unify(wrong_constant_t)

        # ----- domain variable and target constant
        var_constant = 'a -> String'
        var_constant_t = s.typ_parser.inter(var_constant)

        whatever = 'a -> a'
        whatever_t = s.typ_parser.inter(whatever)

        self.assertEqual('String', str(var_constant_t.unify(whatever_t)))

        # ----- domain variable and target variable
        var_var = 'a -> a'
        var_var_t = s.typ_parser.inter(var_var)

        whatever = 'a -> a'
        whatever_t = s.typ_parser.inter(whatever)

        self.assertEqual('a -> a', str(var_var_t.unify(whatever_t)))

        # ----- domain variable and target function
        var_fun = 'a -> b -> a -> b -> a'
        var_fun_t = s.typ_parser.inter(var_fun)
        whatever = 'Bool'
        whatever_t = s.typ_parser.inter(whatever)

        self.assertEqual('b -> Bool -> b -> Bool',
                         str(var_fun_t.unify(whatever_t)))

        # ----- domain function and target function
        fun_fun = '(b -> T) -> (b -> T)'
        fun_fun_t = s.typ_parser.inter(fun_fun)
        whatever = 'E -> c'
        whatever_t = s.typ_parser.inter(whatever)

        self.assertEqual('E -> T',
                         str(fun_fun_t.unify(whatever_t)))

    def test_workflow(self):
        s = TypeSystem()

        s.define('x', 'T')
        self.assertTrue('x' in s.definitions)
        self.assertEqual(str(s.definitions['x']), 'T')

        s.define('f', 't -> T')
        self.assertTrue('f' in s.definitions)
        self.assertEqual(str(s.definitions['f']), 't -> T')

        s.define('g', '(a -> a) -> a')
        self.assertTrue('g' in s.definitions)
        self.assertEqual(str(s.definitions['g']), '(a -> a) -> a')

        self.assertEqual(s.type_of('f'), 't -> T')
        self.assertEqual(s.type_of('f x'), 'T')
        self.assertEqual(s.type_of('g f'), 'T')

        s.define('0', 'Int')
        s.define('1', 'Int')
        s.define('n', 'Int')
        s.define('eq', 'a -> a -> Bool')

        self.assertEqual(s.type_of('eq 0'), 'Int -> Bool')

        with self.assertRaises(Exception):
            s.type_of('eq 2')

        s.define('prod', 'Int -> Int -> Int')
        s.define('dif', 'Int -> Int -> Int')
        s.define('if', 'Bool -> a -> a -> a')

        self.assertEqual(s.type_of('((if ((eq 0) n)) 1) n'), 'Int')

        with self.assertRaises(Exception):
            s.type_of('((if ((eq 0) n)) 1) eq')

        self.assertEqual(s.type_of('(if ((eq 0) n)) if'),
                         '(Bool -> a -> a -> a) -> Bool -> a -> a -> a')

        s.define('fact', 'n')

        self.assertEqual(s.type_of('(eq (fact n)) (((if ((eq n) 0)) 1) ((prod n) (fact ((dif n) 1))))'),
                         'Bool')

        self.assertEqual(s.type_of('(eq fact) (((if ((eq n) 0)) 1) ((prod n) (fact ((dif n) 1))))'),
                         'Bool')
