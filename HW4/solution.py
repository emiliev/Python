import ast
import re
from collections import defaultdict


class AbstractTreeAnalysis():

    DEFAULT_REULES = {
        "line_length": 79,
        "forbid_semicolons": True,
        "max_nesting": 1,
        "indentation_size": 4,
        "methods_per_class": None,
        "max_arity": 2,
        "forbid_trailing_whitespace": True,
        "max_lines_per_function": None,
    }

    def __init__(self):
        self.result = defaultdict(list)

    def check_line_length(self, code_lines):
        for line in range(len(code_lines)):
            if len(code_lines[line]) > self.DEFAULT_REULES["line_length"]:
                self.result[line + 1].append(
                    self.line_length_error(code_lines[line]))

    def methods_per_class(self, tree):
        if self.allowed_rule(self.DEFAULT_REULES["methods_per_class"]):
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    method_counter = 0
                    for func in node.body:
                        if isinstance(func, ast.FunctionDef):
                            method_counter += 1
                    if (method_counter >
                            self.DEFAULT_REULES["methods_per_class"]):
                        self.result[node.lineno].append(
                            self.methods_error(method_counter))

    def arguments_per_method(self, tree):
        if self.allowed_rule(self.DEFAULT_REULES["max_arity"]):
            for node in ast.walk(tree):
                arguments_count = 0
                if isinstance(node, ast.FunctionDef):
                    arguments_count += len(node.args.args)
                    arguments_count += len(node.args.defaults)
                    if node.args.kwarg:
                        arguments_count += 1
                    if node.args.vararg:
                        arguments_count += 1
                if self.DEFAULT_REULES["max_arity"] < arguments_count:
                    self.result[node.lineno].append(
                        self.arguments_error(arguments_count))

    def check_for_trailing_whitespace(self, code_lines):
        if (self.allowed_rule(
                self.DEFAULT_REULES["forbid_trailing_whitespace"])):
            for index, item in enumerate(code_lines):
                if re.search("\s+$", item):
                    self.result[index + 1].append('trailing whitespace')

    def check_for_semicolons(self, code_lines):
        if self.allowed_rule(self.DEFAULT_REULES["forbid_semicolons"]):
            for index, item in enumerate(code_lines):
                found = item.find(";")
                last_char = len(item) - 1
                while -1 < found:
                    if found != last_char:
                        self.result[index + 1].append(self.multiline_error())
                        break
                    found = item.find(";", found + 1)

    def max_nesting(self, tree):
        if self.allowed_rule(self.DEFAULT_REULES["max_nesting"]):
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    report = self.check_for_nesting(node)
                    if report[0]:
                        self.result[report[1]].append(
                            self.max_nesting_error(report[2]))

    def generate_result(self, code, **rules):
        self.DEFAULT_REULES.update(rules)
        tree = ast.parse(code)
        code_lines = code.splitlines()
        self.check_line_length(code_lines)
        self.methods_per_class(tree)
        self.arguments_per_method(tree)
        self.check_for_trailing_whitespace(code_lines)
        self.check_for_semicolons(code_lines)
        self.max_nesting(tree)

        return self.result

    # help functions
    def check_for_nesting(self, node, nesting_count=0):
        control_nodes = (ast.If, ast.While, ast.For, ast.With,
                         ast.Try, ast.ExceptHandler)
        line_number = 0
        for body_node in node.body:
            if nesting_count > self.DEFAULT_REULES["max_nesting"]:
                line_number = body_node.lineno
            if isinstance(body_node, control_nodes):
                return self.check_for_nesting(body_node, nesting_count + 1)
        return (nesting_count > self.DEFAULT_REULES["max_nesting"],
                line_number, nesting_count)

    def line_length_error(self, line):
        return "line too long ({} > {})".format(
            len(line), self.DEFAULT_REULES["line_length"])

    def methods_error(self, methods_number):
        return "too many methods in class({} > {})".format(
            methods_number, self.DEFAULT_REULES["methods_per_class"])

    def arguments_error(self, arguments_number):
        return "too many arguments({} > {})".format(
            arguments_number, self.DEFAULT_REULES["max_arity"])

    def multiline_error(self):
        return "multiple expressions on the same line"

    def max_nesting_error(self, current_nesting):
        return "nesting too deep ({} > {})".format(
            current_nesting, self.DEFAULT_REULES["max_nesting"])

    def allowed_rule(self, rule):
        if rule is None or rule == 0:
            return False
        return True


def critic(code, **rules):
    abstract_tree = AbstractTreeAnalysis()
    return abstract_tree.generate_result(code, **rules)


code = """
class User():

    def __init__(self, name, solo=1):
        self.full_name = name
        self.uuid = uuid.uuid4() 
        self.posts = []
        self.followers = set()

    def add_post(self, post_content):
        new_post = Post(self.uuid,post_content)
        self.posts.append(new_post)
        if len(self.posts) > 50:
            self.posts[1] = self.posts[1:]

    def get_post(self):
        return (post for post in self.posts)

    def add_follower(self, uuid):
        self.followers.add(uuid); 

    def remove_follower(self, uuid,ala,bala,mala):
        self.followers.discard(uuid); bykvarcheto_e_mlako_dulgo_no_tova_ne_prechi = 15209876123 

    def show_followers(self):
        return self.followers

    def search_follower(self,uuid):
        if uuid in self.followers:
            a = 2; b = 3; bykvarcheto_e_mlako_dulgo_no_tova_ne_prechi = 15209876123
            if a == 2:
                return True
        return False
    "при функции с твърде много редове: 'method with too many lines (<<actual>> > <<allowed>>)'"

"при функции с твърде много редове: 'method with too many lines (<<actual>> > <<allowed>>)'"

"""

test = critic(code, methods_per_class=4)
for error in test:
    print("{} : {}".format(error,test[error]))















