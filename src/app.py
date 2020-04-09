import argparse
import logging
import os
import signal
import sys
from argparse import Action

from prometheus_client import REGISTRY, start_http_server

from .sonarqube import SonarQubeClient, SonarQubeCollector
from .schedule import Scheduler


def init_logger(level):
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


class EnvAction(Action):
    def __init__(self, env, required=True, default=None, **kwargs):
        if not default and env:
            if env in os.environ:
                default = os.environ[env]
        if required and default:
            required = False
        super(EnvAction, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def parse_opts(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", env="SQE_URL", dest="url", action=EnvAction,
                        help="SonarQube URL which will be monitored")
    parser.add_argument("--user-token", env="SQE_USER_TOKEN", dest="user_token", action=EnvAction,
                        help="User token used for authentication againsts SonarQube")
    parser.add_argument("--interval", env="SQE_INTERVAL", default=120, dest="interval", action=EnvAction,
                        help="Interval in seconds")
    parser.add_argument("--ignore-ssl-verification", dest="ignore_ssl", action="store_false")
    parser.add_argument("--log-level", env="SQE_LOG_LEVEL", default="INFO", dest="log_level", action=EnvAction,
                        help="Log level. It can be DEBUG, INFO, WARNING, ERROR, CRITICAL. Default is INFO")
    parser.add_argument("--port", "-p", env="SQE_PORT", default=8998, dest="port", action=EnvAction,
                        help="The port that SQE will listen on. Default is 8999")

    return parser.parse_args(args)


def main():
    opts = parse_opts(sys.argv[1:])
    init_logger(opts.log_level)

    scheduler = Scheduler()

    def sigterm_handler(signum, frame):
        if scheduler and signal.SIGTERM == signum:
            scheduler.shutdown()

    signal.signal(signal.SIGTERM, sigterm_handler)

    sonarqube_client = SonarQubeClient(opts.url, opts.user_token, **{"verify": opts.ignore_ssl})
    sonar_collector = SonarQubeCollector(sonarqube_client)
    REGISTRY.register(sonar_collector)

    scheduler.schedule(sonar_collector, int(opts.interval))
    scheduler.start()

    start_http_server(int(opts.port))
    sys.exit(scheduler.wait())
