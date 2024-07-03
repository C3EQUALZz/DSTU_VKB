import atexit
import json
import logging.config
import logging.handlers
import pathlib


def setup_logger() -> None:
    project_root = next(p for p in pathlib.Path(__file__).parents if p.parts[-1] == 'DSTU_VKB')

    logs_path = project_root / "python_language/theory_of_information/logs"
    logs_path.mkdir(exist_ok=True)

    config_file = project_root / "python_language/theory_of_information/core/config/logger_config.json"

    with open(config_file) as f_in:
        config = json.load(f_in)

    config["handlers"]["file_json"]["filename"] = project_root / config["handlers"]["file_json"]["filename"]

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()  # type: ignore
        atexit.register(queue_handler.listener.stop)  # type: ignore
