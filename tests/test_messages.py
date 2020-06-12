from messages import Message
from testfixtures import TempDirectory
import mock
import json


@mock.patch('os.path')
def test_assert_file_do_not_exist(mock_path):
    mock_path.exists.return_value = False
    message = Message('jovem.json')
    assert message.document_name == 'jovem.json'
    assert message.document_content == {}


def test_assert_file_exists():
    random_json = b"{\"airtonzanon\": [1, 2, 3]}"

    with TempDirectory() as d:
        d.write('jovem.json', random_json)
        path = d.path + '/jovem.json'
        message = Message(path)

        assert path == message.document_name
        assert json.loads(random_json.decode()) == message.document_content


def test_write_on_file():
    with TempDirectory() as d:
        d.write('jovem.json', b'')
        path = d.path + '/jovem.json'
        message = Message(path)

        message.add_message('chave', 'valor')
        assert json.loads("{\"chave\": [\"valor\"]}") == message.read_file()
        assert path == message.document_name


def test_verify_if_exists():
    with TempDirectory() as d:
        d.write('jovem.json', b'')
        path = d.path + '/jovem.json'
        message = Message(path)

        message.add_message('chave', 'valor')
        assert json.loads("{\"chave\": [\"valor\"]}") == message.read_file()
        assert True is message.verify_exists('chave', 'valor')
        assert path == message.document_name

