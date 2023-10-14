from common.str_utils import sluggify


def test_sluggify():
    assert sluggify("hello world") == "hello_world"
    assert sluggify("hello_world") == "hello_world"
    assert sluggify("helloWorld") == "helloworld"
    assert sluggify("HelloWorld") == "helloworld"
    assert sluggify("Hello World") == "hello_world"
    assert sluggify("hell!World") == "hell_world"


def test_sluggify_with_numbers():
    assert sluggify("hello world 123") == "hello_world_123"
    assert sluggify("hello_world_123") == "hello_world_123"
    assert sluggify("helloWorld123") == "helloworld123"
    assert sluggify("HelloWorld123") == "helloworld123"
    assert sluggify("Hello World 123") == "hello_world_123"
    assert sluggify("hell!World123") == "hell_world123"
    assert sluggify("123hello world") == "hello_world"


def test_sluggify_with_symbols():
    assert sluggify("!hello world") == "hello_world"
    assert sluggify("hello_world!") == "hello_world"


def test_sluggify_with_spaces():
    assert sluggify("hello world 123") == "hello_world_123"
    assert sluggify("hello       world") == "hello_world"
    assert sluggify("    hello_world") == "hello_world"
    assert sluggify("hello_world    ") == "hello_world"
    assert sluggify("h e l l o ") == "h_e_l_l_o"
    assert sluggify("       ") == ""

