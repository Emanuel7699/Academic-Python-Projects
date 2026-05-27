from mmn13 import *
import importlib
import sys
import zipfile
import os
import copy
from unittest.mock import patch

class Tester:
    """
    A utility class to test and manage test cases for modules, classes, and functions.

    Attributes:
        module (str): The module name to be tested.
        results (dict): Dictionary storing results for each test grouped by question number.
    """

    def __init__(self, module):
        """
        Initialize the Tester instance with the module name and results dictionary.

        Args:
            module (str): The module name to test.
        """
        self.module = module
        self.results = {}

    def set_print_to_file(self, file_path=None):
        """
        Redirect print output to a specified file for logging test results.

        Args:
            question_num (str): The question number for which logging is performed.
            file_path (str, optional): Path to the output file. Defaults to auto-generated name.
        """
        if file_path is None:
            file_path = f"{self.module}.txt"
        else:
            file_path = f"{file_path}.txt"
        file = open(file_path, 'w')
        print(f'''
              \n
              *********************************************************************************
              ************ The test results will be saved to file {file_path} *****************
              *********************************************************************************
              ''')
        sys.stdout = file

    def close_print_to_file(self):
        """
        Restore the standard output to its original state after redirection.
        """
        sys.stdout.close()
        sys.stdout = sys.__stdout__

    def test_functions(
        self,
        question_num,
        test_name,
        func_name,
        *args,
        expected_return=None,
        expected_error=None,
        functions_to_override = [],
        verify_args_unchanged=False,
        expected_args_after=None,
        sort_before_compare=False,
    ):
        """
        Run a test for a function in the module and log the resaults.

        Args:
            question_num (str): Question number for grouping test results.
            test_name (str): Name of the test case.
            func_name (str): Name of the function to test.
            *args: Arguments to pass to the function.
            expected_return (optional): Expected return value from the function.
            expected_error (tuple, optional): Expected error type and message.
            functions_to_override (list): helper functions to monkeypatch before running the test.
            verify_args_unchanged (bool): When True, fail the test if any positional
                argument is mutated by the tested function.
            expected_args_after (tuple|list|None): Concrete values that each
            sort_before_compare (bool): When True, sort both result and expected_return before comparing.
                positional argument is expected to equal after the call. Length must
                match the number of provided *args.
        """
        if verify_args_unchanged and expected_args_after is not None:
            raise ValueError("Use only one of verify_args_unchanged or expected_args_after.")

        res = self.test_return(
            question_num, test_name, func_name, *args,
            expected_return=expected_return, expected_error=expected_error,
            functions_to_override=functions_to_override,
            verify_args_unchanged=verify_args_unchanged,
            expected_args_after=expected_args_after,
            sort_before_compare=sort_before_compare,
        )

        if question_num in self.results:
            passed, count = self.results[question_num]
            passed += res
            count += 1
            self.results[question_num] = passed, count
        else:
            self.results[question_num] = res, 1

    def test_functions_input(
        self,
        question_num,
        test_name,
        func_name,
        inputs,
        expected_return=None,
        functions_to_override = [],
        func_args=(),
        use_printed_output=False,
    ):
        """
        Run a test for a function in the module and log the resaults.

        Args:
            question_num (str): Question number for grouping test results.
            test_name (str): Name of the test case.
            func_name (str): Name of the function to test.
            inputs: List of inputs to provide to input() calls or expected return for stdout capture.
            expected_return (optional): Expected return value from the function.
            functions_to_override: Functions to override in the module.
            func_args: Arguments to pass to the function.
            use_printed_output (bool): When True, compare the captured stdout
                even if the function returns a non-None value.
        """
        res = self.test_input(
            question_num, test_name, func_name, inputs,
            expected_return=expected_return,
            functions_to_override = functions_to_override,
            func_args=func_args,
            use_printed_output=use_printed_output,
        )

        if question_num in self.results:
            passed, count = self.results[question_num]
            passed += res
            count += 1
            self.results[question_num] = passed, count
        else:
            self.results[question_num] = res, 1

    def test_return(
        self,
        question_num,
        test_name,
        func_name,
        *args,
        expected_return=None,
        expected_error=None,
        functions_to_override = [],
        verify_args_unchanged=False,
        expected_args_after=None,
        sort_before_compare=False,
    ):
        """
        Execute a test and return whether it passed.

        Args:
            question_num (str): Question number for grouping test results.
            test_name (str): Name of the test case.
            func_name (str): Name of the function to test.
            *args: Arguments to pass to the function.
            expected_return (optional): Expected return value from the function.
            expected_error (tuple, optional): Expected error type and message.
            verify_args_unchanged (bool): Fail if function mutates any positional argument.
            expected_args_after (tuple|list|None): Expected argument values after the call.
            sort_before_compare (bool): When True, sort both result and expected_return before comparing.

        Returns:
            int: 1 if the test passed, 0 otherwise.
        """
        arg_checks_needed = verify_args_unchanged or expected_args_after is not None
        args_before_call = copy.deepcopy(args) if arg_checks_needed else None

        try:
            module = importlib.import_module(self.module)
            for fn in functions_to_override:
                setattr(module, fn.__name__, fn)
            func = getattr(module, func_name)

            if expected_error:
                expected_error_type, expected_message = expected_error
                try:
                    func(*args)
                except Exception as e:
                    if isinstance(e, expected_error_type):
                        if expected_message is not None:
                            if str(e) == expected_message:
                                print(
                                    f"Question {question_num} Test {test_name}: passed \n\t{self.module}, {func_name}, args:{args}, "
                                    f"raised: {type(e).__name__} - {e}"
                                )
                                return 1
                            else:
                                print(
                                    f"Question {question_num} Test {test_name}: failed \n\t{self.module}, {func_name}, args:{args}, "
                                    f"raised message: {e}, expected message: {expected_message}"
                                )
                                return 0
                        else:
                            print(
                                f"Question {question_num} Test {test_name}: passed \n\t{self.module}, {func_name}, args:{args}, "
                                f"raised: {type(e).__name__} - {e}"
                            )
                            return 1
                    else:
                        print(
                            f"Question {question_num} Test {test_name}: failed \n\t{self.module}, {func_name}, args:{args}, raised: {type(e).__name__} - {e}, "
                            f"expected: {expected_error_type.__name__}"
                        )
                        return 0
                else:
                    print(
                        f"Question {question_num} Test {test_name}: failed \n\t{self.module}, {func_name}, args:{args}, no error raised, "
                        f"expected: {expected_error_type.__name__}"
                    )
                    return 0
            else:
                result = func(*args)
                if sort_before_compare and hasattr(result, '__iter__'):
                    try:
                        assert sorted(result) == sorted(expected_return)
                    except TypeError:
                        assert result == expected_return
                else:
                    assert result == expected_return

                if arg_checks_needed:
                    if expected_args_after is not None:
                        if len(expected_args_after) != len(args):
                            print(
                                f"Question {question_num} Test {test_name}: failed \n\t{self.module}, {func_name}, expected_args_after length does not match provided args"
                            )
                            return 0
                        comparison_target = tuple(expected_args_after)
                        mismatch_template = (
                            "Question {q} Test {t}: failed \n\t{module}, {func}, argument #{idx} expected {expected!r} after call, got {actual!r}"
                        )
                    else:
                        comparison_target = tuple(args_before_call)
                        mismatch_template = (
                            "Question {q} Test {t}: failed \n\t{module}, {func}, argument #{idx} was mutated. before: {expected!r}, after: {actual!r}"
                        )

                    for idx, actual in enumerate(args):
                        expected_val = comparison_target[idx]
                        if actual != expected_val:
                            print(
                                mismatch_template.format(
                                    q=question_num,
                                    t=test_name,
                                    module=self.module,
                                    func=func_name,
                                    idx=idx,
                                    expected=expected_val,
                                    actual=actual,
                                )
                            )
                            return 0
                print(f"Question {question_num} Test {test_name}: passed \n\t{self.module}, {func_name}, args:{args}, result: {result}")
                return 1

        except AssertionError:
            print(
                f"Question {question_num} Test {test_name}: failed \n\t{self.module}, {func_name}, args:{args}. result: {result} expected result: {expected_return}"
            )
            return 0
        except ModuleNotFoundError:
            print(f"Question {question_num} Test {test_name}: failed \n\t{self.module}, {func_name}, {self.module}.py not found!")
            return 0
        except AttributeError:
            print(f"Question {question_num} Test {test_name}: failed \n\t{self.module}, {func_name}, {func_name} not found in the module!")
            return 0
        except Exception as e:
            print(f"Question {question_num} Test {test_name}: failed \n\t{self.module}, {func_name}, with error: {type(e).__name__} - {e}, args:{args}.")
            return 0

    def test_create(self, question_num, test_name, class_name, *args, expected_error=None):
        """
        Create an object of a class and log the result.

        Args:
            question_num (str): Question number for grouping test results.
            test_name (str): Name of the test case.
            class_name (str): Name of the class to instantiate.
            *args: Arguments to pass to the class constructor.
            expected_error (tuple, optional): Expected error type and message.

        Returns:
            object: The created object if successful, None otherwise.
        """
        try:
            module = importlib.import_module(self.module)
            cls = getattr(module, class_name)

            if expected_error:
                expected_error_type, expected_message = expected_error
                try:
                    obj = cls(*args)
                except Exception as e:
                    if isinstance(e, expected_error_type):
                        if expected_message is not None:
                            if str(e) == expected_message:
                                print(
                                    f"Question {question_num} Test {test_name}: passed \n\t{class_name}, init, args:{args}, "
                                    f"raised: {type(e).__name__} - {e}"
                                )
                                self.results[question_num] = (1, 1)
                            else:
                                print(
                                    f"Question {question_num} Test {test_name}: failed \n\t{class_name}, init, args:{args}, "
                                    f"raised message: {e}, expected message: {expected_message}"
                                )
                                self.results[question_num] = (0, 1)
                        else:
                            print(
                                f"Question {question_num} Test {test_name}: passed \n\t{class_name}, init, args:{args}, "
                                f"raised: {type(e).__name__} - {e}"
                            )
                            self.results[question_num] = (1, 1)
                    else:
                        print(
                            f"Question {question_num} Test {test_name}: failed \n\t{class_name}, init, args:{args}, raised: {type(e).__name__} - {e}, "
                            f"expected: {expected_error_type.__name__}"
                        )
                        self.results[question_num] = (0, 1)
                else:
                    print(
                        f"Question {question_num} Test {test_name}: failed \n\t{class_name}, init, args:{args}, no error raised, "
                        f"expected: {expected_error_type.__name__}"
                    )
                    self.results[question_num] = (0, 1)
                    return None
            else:
                obj = cls(*args)
                print(
                    f"Question {question_num} Test {test_name}: passed \n\t{class_name}, init, args:{args}, object created successfully"
                )
                if question_num in self.results:
                    passed, count = self.results[question_num]
                    self.results[question_num] = (passed + 1, count + 1)
                else:
                    self.results[question_num] = (1, 1)
                return obj

        except ModuleNotFoundError:
            print(
                f"Question {question_num} Test {test_name}: failed \n\t{class_name}, init, {self.module}.py not found!"
            )
            if question_num in self.results:
                passed, count = self.results[question_num]
                self.results[question_num] = (passed, count + 1)
            else:
                self.results[question_num] = (0, 1)
            return None
        except AttributeError:
            print(
                f"Question {question_num} Test {test_name}: failed \n\t{class_name}, init, Class {class_name} not found in the module!"
            )
            if question_num in self.results:
                passed, count = self.results[question_num]
                self.results[question_num] = (passed, count + 1)
            else:
                self.results[question_num] = (0, 1)
            return None
        except Exception as e:
            print(
                f"Question {question_num} Test {test_name}: failed \n\t{class_name}, init, with error: {type(e).__name__} - {e}, args:{args}."
            )
            if question_num in self.results:
                passed, count = self.results[question_num]
                self.results[question_num] = (passed, count + 1)
            else:
                self.results[question_num] = (0, 1)
            return None

    def test_class(self, question_num, test_name, instance, class_name, required_attrs):
        """
        Test the existence of a class and its attributes.

        Args:
            question_num (str): Question number for grouping test results.
            test_name (str): Name of the test case.
            class_name (str): Name of the class to test.
            required_attrs (dict): Dictionary specifying attribute types to check.
                                Keys: "class", "object", "private", "protected".
                                Values: List of attribute names.

        Returns:
            bool: True if the class and its attributes pass the tests, False otherwise.
        """
        try:
            # Import the module and get the class
            module = importlib.import_module(self.module)
            cls = getattr(module, class_name)

            # Check if instance of class_name
            assert isinstance(instance, cls)

            # Check for attributes
            for attr_type, attrs in required_attrs.items():
                for attr in attrs:
                    if attr_type == "private":
                        attr_name = f"_{class_name}__{attr}"  # Mangled name for private attributes
                    elif attr_type == "protected":
                        attr_name = f"_{attr}"  # Convention for protected attributes
                    else:
                        attr_name = attr  # Public attributes

                    # Verify the attribute on the instance
                    if not hasattr(instance, attr_name):
                        print(
                            f"Question {question_num} Test {test_name}: failed\n\tMissing {attr_type} attribute '{attr}' in {class_name}"
                        )
                        self.results[question_num] = self.results.get(question_num, (0, 0))
                        self.results[question_num] = (
                            self.results[question_num][0],
                            self.results[question_num][1] + 1,
                        )
                        return False

            # All checks passed
            print(
                f"Question {question_num} Test {test_name}: passed\n\tClass {class_name} with attributes {required_attrs} exists"
            )
            self.results[question_num] = self.results.get(question_num, (0, 0))
            self.results[question_num] = (
                self.results[question_num][0] + 1,
                self.results[question_num][1] + 1,
            )

            # Import the class to the current module's namespace
            globals()[class_name] = cls

            return True

        except ModuleNotFoundError:
            print(f"Question {question_num} Test {test_name}: failed \n\tModule {self.module} not found")
            self.results[question_num] = self.results.get(question_num, (0, 0))
            self.results[question_num] = (self.results[question_num][0], self.results[question_num][1] + 1)
            return False
        except AttributeError:
            print(f"Question {question_num} Test {test_name}: failed \n\tClass {class_name} does not exist")
            self.results[question_num] = self.results.get(question_num, (0, 0))
            self.results[question_num] = (self.results[question_num][0], self.results[question_num][1] + 1)
            return False
        except AssertionError:
            print(f"Question {question_num} Test {test_name}: failed \n\tObject: {str(instance)} is not instance of {class_name}")
            return False

    def test_class_methods(
        self,
        question_num,
        test_name,
        obj,
        func_name,
        *args,
        expected_return=None,
        expected_error=None,
        aliasing_obj=None,
    ):
        """
        Test a method of a class instance and check for aliasing.

        Args:
            question_num (str): Question number for grouping test results.
            test_name (str): Name of the test case.
            obj (object): Instance of the class to test.
            func_name (str): Name of the method to test.
            *args: Arguments to pass to the method.
            expected_return (optional): Expected return value from the method.
            expected_error (tuple, optional): Expected error type and message.
            aliasing_obj (optional): Object to check for aliasing with the return value.
        """
        try:
            method = getattr(obj, func_name)

            if expected_error:
                expected_error_type, expected_message = expected_error
                try:
                    method(*args)
                except Exception as e:
                    if isinstance(e, expected_error_type):
                        if expected_message is not None:
                            if str(e) == expected_message:
                                print(
                                    f"Question {question_num} Test {test_name}: passed \n\t{repr(obj)}, {func_name}, args:{args}, "
                                    f"raised: {type(e).__name__} - {e}"
                                )
                                if question_num in self.results:
                                    passed, count = self.results[question_num]
                                    self.results[question_num] = (passed + 1, count + 1)
                                else:
                                    self.results[question_num] = (1, 1)
                            else:
                                print(
                                    f"Question {question_num} Test {test_name}: failed \n\t{repr(obj)}, {func_name}, args:{args}, "
                                    f"raised message: {e}, expected message: {expected_message}"
                                )
                                if question_num in self.results:
                                    passed, count = self.results[question_num]
                                    self.results[question_num] = (passed, count + 1)
                                else:
                                    self.results[question_num] = (0, 1)
                        else:
                            print(
                                f"Question {question_num} Test {test_name}: passed \n\t{repr(obj)}, {func_name}, args:{args}, "
                                f"raised: {type(e).__name__} - Message wasn't checked"
                            )
                            if question_num in self.results:
                                passed, count = self.results[question_num]
                                self.results[question_num] = (passed + 1, count + 1)
                            else:
                                self.results[question_num] = (1, 1)
                    else:
                        print(
                            f"Question {question_num} Test {test_name}: failed \n\t{repr(obj)}, {func_name}, args:{args}, raised: {type(e).__name__} - {e}, "
                            f"expected: {expected_error_type.__name__}"
                        )
                        if question_num in self.results:
                            passed, count = self.results[question_num]
                            self.results[question_num] = (passed, count + 1)
                        else:
                            self.results[question_num] = (0, 1)
                else:
                    print(
                        f"Question {question_num} Test {test_name}: failed \n\t{repr(obj)}, {func_name}, args:{args}, no error raised, "
                        f"expected: {expected_error_type.__name__}"
                    )
                    if question_num in self.results:
                        passed, count = self.results[question_num]
                        self.results[question_num] = (passed, count + 1)
                    else:
                        self.results[question_num] = (0, 1)
            else:
                result = method(*args)

                # Check if the return value matches the expected return value
                assert result == expected_return, (
                    f"Question {question_num} Test {test_name}: failed \n\t{repr(obj)}, {func_name}, args:{args}. result: {result}, expected result: {expected_return}"
                )

                # Check for aliasing
                if aliasing_obj is not None and id(result) == id(aliasing_obj):
                    print(
                        f"Question {question_num} Test {test_name}: failed \n\t{repr(obj)}, {func_name}, args:{args}. result is aliasing aliasing_obj."
                    )
                    if question_num in self.results:
                        passed, count = self.results[question_num]
                        self.results[question_num] = (passed, count + 1)
                    else:
                        self.results[question_num] = (0, 1)
                    return

                print(f"Question {question_num} Test {test_name}: passed \n\t{repr(obj)}, {func_name}, args:{args}, result: {result}")
                if question_num in self.results:
                    passed, count = self.results[question_num]
                    self.results[question_num] = (passed + 1, count + 1)
                else:
                    self.results[question_num] = (1, 1)

        except AssertionError as e:
            print(e)
            if question_num in self.results:
                passed, count = self.results[question_num]
                self.results[question_num] = (passed, count + 1)
            else:
                self.results[question_num] = (0, 1)
        except AttributeError:
            print(f"Question {question_num} Test {test_name}: failed \n\t{repr(obj)}, {func_name}, method not found!")
            if question_num in self.results:
                passed, count = self.results[question_num]
                self.results[question_num] = (passed, count + 1)
            else:
                self.results[question_num] = (0, 1)
        except Exception as e:
            print(
                f"Question {question_num} Test {test_name}: failed \n\t{repr(obj)}, {func_name}, with error: {type(e).__name__} - {e}, args:{args}."
            )
            if question_num in self.results:
                passed, count = self.results[question_num]
                self.results[question_num] = (passed, count + 1)
            else:
                self.results[question_num] = (0, 1)

    def get_private_attribute(self, obj, private_attr_name):
        """
        Retrieve the value of a private attribute using name mangling.

        Args:
            obj (object): The class instance.
            private_attr_name (str): Name of the private attribute (without mangling).

        Returns:
            The value of the private attribute.
        """
        return getattr(obj, f"_{type(obj).__name__}__{private_attr_name}")

    def test_aliasing(self, question_num, test_name, obj, attr_name, target_obj):
        """
        Test if an attribute of a class instance is not aliasing the provided object.

        Args:
            question_num (str): Question number for grouping test results.
            test_name (str): Name of the test case.
            obj (object): Instance of the class to test.
            attr_name (str): Name of the attribute to check.
            target_obj (object): The object to check aliasing against.
        """
        try:
            # Handle private attributes
            if attr_name.startswith("__"):
                class_name = obj.__class__.__name__
                attr_name = f"_{class_name}{attr_name}"

            # Retrieve the attribute
            attribute = getattr(obj, attr_name)

            # Check for aliasing
            if id(attribute) == id(target_obj):
                print(
                    f"Question {question_num} Test {test_name}: failed \n\t{repr(obj)}, {attr_name} is aliasing target_obj."
                )
                if question_num in self.results:
                    passed, count = self.results[question_num]
                    self.results[question_num] = (passed, count + 1)
                else:
                    self.results[question_num] = (0, 1)
            else:
                print(
                    f"Question {question_num} Test {test_name}: passed \n\t{repr(obj)}, {attr_name} is not aliasing target_obj."
                )
                if question_num in self.results:
                    passed, count = self.results[question_num]
                    self.results[question_num] = (passed + 1, count + 1)
                else:
                    self.results[question_num] = (1, 1)

        except AttributeError:
            print(f"Question {question_num} Test {test_name}: failed \n\t{repr(obj)}, {attr_name} not found!")
            if question_num in self.results:
                passed, count = self.results[question_num]
                self.results[question_num] = (passed, count + 1)
            else:
                self.results[question_num] = (0, 1)
        except Exception as e:
            print(
                f"Question {question_num} Test {test_name}: failed \n\t{repr(obj)}, {attr_name}, with error: {type(e).__name__} - {e}."
            )
            if question_num in self.results:
                passed, count = self.results[question_num]
                self.results[question_num] = (passed, count + 1)
            else:
                self.results[question_num] = (0, 1)
    
    def print_score(self):
        """
        Print the summary of test results for all questions.

        The results are stored in the `results` attribute, which is a dictionary
        where the key is the question number and the value is a tuple of
        (number of passed tests, total number of tests).
        """
        print('\n', '*' * 10, "Final Score", '*' * 10)
        for question_num, result in self.results.items():
            passed, count = result
            print(f"Question {question_num}: {passed} / {count}")

    def check_and_open (self):
        py_path = f"{self.module}.py"
        zip_path = f"{self.module}.zip"
        
        print("*" * 20, "Extracting .... ", "*" * 20)
        
        # Step 1: Check if myfile.py exists
        if os.path.isfile(py_path):
            return True

        # Step 2: If not, check if myfile.zip exists
        if not os.path.isfile(zip_path):
            print(f"Problem: Neither {module}.py nor {module}.zip found.\n")
            return False

        # Step 3: Try to extract myfile.zip
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(".")
        except zipfile.BadZipFile:
            print(f"Problem: {module}.zip is not a valid zip file or extraction failed.\n")
            return False

        # Step 4: Check again for myfile.py after extraction
        if os.path.isfile(py_path):
            return True
        else:
            print(f"Problem: {module}.zip was extracted but {module}.py not found.\n")
            return False
        
    def test_input(
        self,
        question_num,
        test_name,
        func_name,
        inputs,
        expected_return,
        functions_to_override = [],
        func_args=(),
        use_printed_output=False,
    ):
        """
        Tests a function that reads from input(), with optional arguments,
        and can capture and compare printed output instead of return values.

        Args:
            question_num (str): Identifier for grouping results.
            test_name (str): Name of this test case.
            func_name (str): Name of the function to import from self.module.
            inputs (list[str|int]): Values to feed, one per input() call.
            expected_return: The value expected to be returned by func() or printed output.
            functions_to_override (iterable): Callables whose names will
                replace same‑named objects in the module before calling.
            func_args: Arguments to pass to the function.
            use_printed_output (bool): When True, compare the captured stdout even
                if the function returns a non-None value.

        Returns:
            int: 1 if test passed, 0 otherwise.
        """
        from io import StringIO
        import sys
        
        # 1. import module
        try:
            module = importlib.import_module(self.module)
        except ModuleNotFoundError:
            print(f"Question {question_num} Test {test_name}: failed\n\tModule {self.module!r} not found")
            return 0

        # 2. override any helper functions
        for fn in functions_to_override:
            setattr(module, fn.__name__, fn)

        # 3. get the function
        try:
            func = getattr(module, func_name)
        except AttributeError:
            print(f"Question {question_num} Test {test_name}: failed\n\tFunction {func_name!r} not found in module {self.module}")
            return 0

        # 4. ensure inputs mimic real input() behavior
        str_inputs = [str(i) for i in inputs]

        # 5. run with input() mocked and capture output
        with patch('builtins.input', side_effect=str_inputs):
            # Capture stdout to handle functions that print instead of return
            captured_output = StringIO()
            old_stdout = sys.stdout
            sys.stdout = captured_output
            
            try:
                if func_args:
                    result = func(*func_args)
                else:
                    result = func()
                sys.stdout = old_stdout
                
                # Get printed output
                printed_output = captured_output.getvalue().strip()
                
                if use_printed_output:
                    actual_result = printed_output
                else:
                    # If function returns something meaningful, use that; otherwise use printed output
                    if result is not None:
                        actual_result = result
                    else:
                        actual_result = printed_output
                    
            except Exception as e:
                sys.stdout = old_stdout
                print(
                    f"Question {question_num} Test {test_name}: failed\n\t"
                    f"{func_name} raised unexpected {type(e).__name__}: {e}"
                )
                return 0

        # 6. verify output
        if actual_result == expected_return:
            print(
                f"Question {question_num} Test {test_name}: passed\n\t"
                f"{self.module}.{func_name}() -> {actual_result!r}"
            )
            return 1
        else:
            print(
                f"Question {question_num} Test {test_name}: failed\n\t"
                f"Got {actual_result!r}, expected {expected_return!r}"
            )
            return 0

module = "mmn13"
tester = Tester(module)

tester.set_print_to_file("mmn13")



#region ################################# Question 1 - find_missing_index ###################################
print (f'################################ Question 1 - find_missing_index ################################\n')

# --- logic tests (no mutation check) ---

# gap in the middle (PDF example 1): d=2, missing 28,30 → first missing at index 3
lst_q1_1 = [22, 24, 26, 32, 34, 36, 38, 40]
tester.test_functions("1", "1", "find_missing_index", lst_q1_1, expected_return=3)

# gap at the start (PDF example 2): d=2, missing 24 → first missing at index 1
lst_q1_2 = [22, 26, 28]
tester.test_functions("1", "2", "find_missing_index", lst_q1_2, expected_return=1)

# no gap (PDF example 3): d=2, complete series → returns len(lst) = 5
lst_q1_3 = [2, 4, 6, 8, 10]
tester.test_functions("1", "3", "find_missing_index", lst_q1_3, expected_return=5)

# decreasing series with gap (PDF example 4): d=-2, missing 24 → first missing at index 2
lst_q1_4 = [28, 26, 22]
tester.test_functions("1", "4", "find_missing_index", lst_q1_4, expected_return=2)

# empty list → ValueError
tester.test_functions("1", "5", "find_missing_index", [], expected_error=(ValueError, None))

# single element → ValueError
tester.test_functions("1", "6", "find_missing_index", [5], expected_error=(ValueError, None))

# gap near the end: d=2, missing 10 → first missing at index 4
lst_q1_7 = [2, 4, 6, 8, 12]
tester.test_functions("1", "7", "find_missing_index", lst_q1_7, expected_return=4)

# large gap (many elements missing): d=1, missing 4-9 → first missing at index 3
lst_q1_8 = [1, 2, 3, 10, 11, 12]
tester.test_functions("1", "8", "find_missing_index", lst_q1_8, expected_return=3)

# --- mutation tests (checks that lst is not modified) ---

# one element missing with larger step: d=10, missing 40 → first missing at index 3
lst_q1_9 = [10, 20, 30, 50, 60]
tester.test_functions("1", "9 (no mutation)", "find_missing_index", lst_q1_9, expected_return=3, verify_args_unchanged=True)

# no gap, d=100 → returns len(lst) = 4
lst_q1_10 = [100, 200, 300, 400]
tester.test_functions("1", "10 (no mutation)", "find_missing_index", lst_q1_10, expected_return=4, verify_args_unchanged=True)

#endregion

#region ################################# Question 2 - count_triples ###################################
print (f'################################ Question 2 - count_triples################################\n')
lst = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 18, 19, 22]
lst2 = [1, 2, 4, 5, 10, 20]

# PDF example: only (2,3,5) → product=30
tester.test_functions("2", "1 (no mutation)", "count_triples", lst, 30, expected_return=1, verify_args_unchanged=True)

# PDF example: (2,3,10), (2,5,6), (3,4,5) → product=60
tester.test_functions("2", "2", "count_triples", lst, 60, expected_return=3)

# PDF example: (2,4,10), (2,5,8) → product=80
tester.test_functions("2", "3", "count_triples", lst, 80, expected_return=2)

# no triple has product=20 in lst
tester.test_functions("2", "4", "count_triples", lst, 20, expected_return=0)

# empty list → 0
tester.test_functions("2", "5", "count_triples", [], 80, expected_return=0)

# fewer than 3 elements → 0
tester.test_functions("2", "6", "count_triples", [2, 3], 20, expected_return=0)

# lst2: (1,2,10), (1,4,5) → product=20
tester.test_functions("2", "7", "count_triples", lst2, 20, expected_return=2)

# lst2: (1,2,20), (1,4,10), (2,4,5) → product=40
tester.test_functions("2", "8", "count_triples", lst2, 40, expected_return=3)

# lst2: only (5,10,20) → product=1000
tester.test_functions("2", "9", "count_triples", lst2, 1*10*20*5, expected_return=1)

# exactly 3 elements forming one triple; mutation check
tester.test_functions("2", "10 (no mutation)", "count_triples", [3, 4, 5], 60, expected_return=1, verify_args_unchanged=True)


#endregion


#region ################################# Question 3 - pair_sum ###################################
print (f'################################ Question 3 - pair_sum ################################\n')
lst_q4 = [2, 0, 4, -2, 1, 6, 5]

# PDF example 1: (2,4), (0,6), (1,5)
tester.test_functions("4", "1", "pair_sum", lst_q4, 6, expected_return=[(2,4), (0,6), (1,5)], sort_before_compare=True)

# PDF example 2: (2,0), (4,-2)
tester.test_functions("4", "2", "pair_sum", lst_q4, 2, expected_return=[(2,0), (4,-2)], sort_before_compare=True)

# PDF example 3: no pairs
tester.test_functions("4", "3", "pair_sum", lst_q4, 12, expected_return=[])

# empty list → []
tester.test_functions("4", "4", "pair_sum", [], 6, expected_return=[])

# single element → []
tester.test_functions("4", "5", "pair_sum", [5], 10, expected_return=[])

# exactly two elements, valid pair
tester.test_functions("4", "6", "pair_sum", [3, 5], 8, expected_return=[(3,5)], sort_before_compare=True)

# exactly two elements, no pair
tester.test_functions("4", "7", "pair_sum", [3, 5], 10, expected_return=[])

# multiple pairs, all elements used: (1,4), (2,3)
tester.test_functions("4", "8", "pair_sum", [1, 4, 2, 3], 5, expected_return=[(1,4), (2,3)], sort_before_compare=True)

# negative target: only (-3,-1)
tester.test_functions("4", "9", "pair_sum", [-3, 1, -1, 2], -4, expected_return=[(-3,-1)], sort_before_compare=True)

# mutation check
tester.test_functions("4", "10 (no mutation)", "pair_sum", lst_q4, 6, expected_return=[(2,4), (0,6), (1,5)], verify_args_unchanged=True, sort_before_compare=True)

#endregion

#region ################################# Question 4 - count_triples_rec ###################################
print (f'################################ Question 3 - count_triples_rec ################################\n')
lst_q3 = [2, 0, 3, -2, 1, 8, 5]

# PDF example 1: (2,3,1), (0,1,5), (0,-2,8), (3,-2,5) → 4
tester.test_functions("3", "1", "count_triples_rec", lst_q3, 6, expected_return=4)

# PDF example 2: (2,0,3), (2,-2,5) → 2
tester.test_functions("3", "2", "count_triples_rec", lst_q3, 5, expected_return=2)

# PDF example 3: no triple sums to 17 → 0
tester.test_functions("3", "3", "count_triples_rec", lst_q3, 17, expected_return=0)

# empty list → 0
tester.test_functions("3", "4", "count_triples_rec", [], 6, expected_return=0)

# fewer than 3 elements → 0
tester.test_functions("3", "5", "count_triples_rec", [1, 2], 3, expected_return=0)

# exactly 3 elements, one valid triple
tester.test_functions("3", "6", "count_triples_rec", [1, 2, 3], 6, expected_return=1)

# exactly 3 elements, no valid triple
tester.test_functions("3", "7", "count_triples_rec", [1, 2, 3], 10, expected_return=0)

# positive elements only: [1,2,3,4,5], num=9: (1,3,5), (2,3,4) → 2
tester.test_functions("3", "8", "count_triples_rec", [1, 2, 3, 4, 5], 9, expected_return=2)

# negative target: [-3,-2,-1,0,1], num=-6: only (-3,-2,-1) → 1
tester.test_functions("3", "9", "count_triples_rec", [-3, -2, -1, 0, 1], -6, expected_return=1)

# mutation check
tester.test_functions("3", "10 (no mutation)", "count_triples_rec", lst_q3, 6, expected_return=4, verify_args_unchanged=True)

#endregion

print (f'\n################################ Summary ################################\n')
tester.print_score()
tester.close_print_to_file()
tester.print_score()