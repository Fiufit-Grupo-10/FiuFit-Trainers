from collections.abc import Iterable
import os
import structlog
import logging

from structlog.types import Processor

DEFAULT_LEVEL = "INFO"
LOGGER_NAME = "Trainings"


def get_log_level() -> int:
    level = os.getenv("LOG_LEVEL", DEFAULT_LEVEL)
    return logging.getLevelName(level)


structlog_processors = [
    structlog.processors.dict_tracebacks,
    structlog.processors.JSONRenderer(),
]

DEV_ENV = os.getenv("DEV", "false").lower()
METRICS_URL = os.getenv("METRICS_SERVICE_URL", None)

def get_processors() -> Iterable[Processor]:
    timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
    processors = [
        structlog.processors.add_log_level,
        structlog.contextvars.merge_contextvars,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        timestamper,
    ]

    # json_processors = [
    #     structlog.processors.dict_tracebacks,
    #     structlog.processors.JSONRenderer(),
    # ]
    # if DEV_ENV == "false":
    #     processors += json_processors
    # else:
    processors += [structlog.dev.ConsoleRenderer()]

    return processors


structlog.configure(
    processors=get_processors(),
    wrapper_class=structlog.make_filtering_bound_logger(get_log_level()),
    logger_factory=structlog.WriteLoggerFactory(),
    cache_logger_on_first_use=False,
)

logger = structlog.getLogger(name=LOGGER_NAME)
logger.debug(f"METRICS_URL={METRICS_URL}")
