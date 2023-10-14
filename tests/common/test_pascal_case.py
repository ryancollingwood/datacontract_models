from common.str_utils import pascal_case


def test_pascal_case():
    assert pascal_case("hello world") == "HelloWorld"
    assert pascal_case("hello_world") == "HelloWorld"
    assert pascal_case("helloWorld") == "Helloworld"
    assert pascal_case("HelloWorld") == "Helloworld"
    assert pascal_case("Hello World") == "HelloWorld"
    assert pascal_case("hell!World") == "Hell!World"