import pytest
from logger import Logger, LogLevel

def test_file_writing(tmp_path):
    temp_file = tmp_path / "test_logs.log"
    log = Logger(log_file_path=str(temp_file))
    log.info("Test message")

    content = temp_file.read_text()
    assert "INFO" in content
    assert "Test message" in content

def test_console_output(capsys):
    log = Logger(print_console=True, save_to_log=False)
    log.error("Boom")

    captured = capsys.readouterr()

    assert "ERROR" in captured.out
    assert "Boom" in captured.out

def test_login_required_block_access():
    log = Logger(user_logined=False)

    with pytest.raises(PermissionError) as exc_info:
        log.info("This should not work")

    assert "User must be logged in" in str(exc_info.value)