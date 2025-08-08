from src.logger import setup_logger

def test_logger_setup(tmp_path):
    log_file = tmp_path / "test.log"
    logger = setup_logger("TestLogger", "DEBUG", str(log_file))
    logger.debug("debug message")
    logger.info("info message")
    logger.error("error message")
    # Check log file exists and contains expected lines
    with open(log_file) as f:
        content = f.read()
    assert "debug message" in content
    assert "info message" in content
    assert "error message" in content
