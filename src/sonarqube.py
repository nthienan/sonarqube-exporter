import requests
import logging
from .config import Config
from prometheus_client.core import Gauge
import base64


CONF = Config()

class SonarQubeClient:

    def __init__(self, url, user_token, **kwargs):
        if url.endswith("/"):
            url = url[:-1]
        self._url = url
        self._user_token = user_token
        self._basic_authen = base64.b64encode(("%s:" % self._user_token).encode("ascii")).decode("ascii")
        self._authenticate_header = {"Authorization": "Basic %s" % self._basic_authen}
        self._kwargs = kwargs
        logging.debug("Initialized SonarQube: url: %s, userToken: ****, %s" % (self._url, self._kwargs))

    def _request(self, endpoint):
        res = requests.get("{}/{}".format(self._url, endpoint), headers=self._authenticate_header, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def get_projects(self, page_index=1, page_size=100):
        return self._request(endpoint="api/components/search?qualifiers=TRK&p={}&ps={}".format(page_index, page_size))

    def get_metrics(self):
        return self._request(endpoint="api/metrics/search")

    def get_measures(self, component_key, metric_key):
        return self._request(endpoint="api/measures/component?component={}&metricKeys={}".format(component_key, metric_key))


class Metric:

    def __init__(self):
        self._key = None
        self._values = []
        self._description = None
        self._domain = None
        self._type = None
        self._tranform = False
        self._tranform_map = {}

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values.extend(value)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        self._domain = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def tranform(self):
        return self._tranform

    @tranform.setter
    def tranform(self, value):
        self._tranform = value

    @property
    def tranform_map(self):
        return self._tranform_map

    @tranform_map.setter
    def tranform_map(self, value):
        self._tranform_map = value


class SonarQubeCollector:

    def __init__(self, sonar_client : SonarQubeClient):
        self._sonar_client = sonar_client
        self._cached_metrics = []

        # initialize gauges
        logging.info("Intitializing...")
        self._metrics = {}
        raw_metrics = self._sonar_client.get_metrics()["metrics"]
        for raw_metric in raw_metrics:
            metric = Metric()
            for supported_m in CONF.supported_keys:
                if "domain" in raw_metric and raw_metric["domain"] == supported_m["domain"] and raw_metric["key"] in supported_m["keys"]:
                    metric.domain = raw_metric["domain"]
                    metric.key = raw_metric["key"]
                    metric.type = raw_metric["type"]
                    if "description" in raw_metric:
                        metric.description = raw_metric["description"]
                    else:
                        metric.description = raw_metric["name"]
                    if "tranformKeys" in supported_m and raw_metric["key"] in supported_m["tranformKeys"].keys():
                        metric.tranform = True
                        metric.tranform_map = supported_m["tranformKeys"][raw_metric["key"]]
                    self._metrics[metric.key] = metric
        self._queried_metrics = str()
        self._gauges = {}
        for key, m in self._metrics.items():
            self._gauges[m.key] = Gauge (name="sonar_{}".format(m.key), documentation=m.description, labelnames=("id", "key", "name", "domain", "type"))
            self._queried_metrics = "{},{}".format(m.key, self._queried_metrics)
        logging.info("Initialized %s metrics." % len(self._metrics.keys()))

    def collect(self):
        return self._cached_metrics

    def run(self):
        logging.info("Collecting data from SonarQube...")
        response  = self._sonar_client.get_projects()
        total_projects = int(response['paging']['total'])
        logging.info("There are %s projects in SonarQube" % total_projects)
        processed_projects = 0
        page_index = 1
        while processed_projects < total_projects:
            projects  = self._sonar_client.get_projects(page_index=page_index)["components"]
            for p in projects:
                measures = self._sonar_client.get_measures(component_key=p["key"], metric_key=self._queried_metrics)["component"]["measures"]
                for measure in measures:
                    value = measure["value"]
                    m = self._metrics[measure["metric"]]
                    if m.tranform:
                        value = m.tranform_map[measure["value"]]
                    gauge = self._gauges[measure["metric"]]
                    gauge.labels(p["id"], p["key"], p["name"], m.domain, m.type).set(value)
                processed_projects += processed_projects
            page_index += 1
            logging.info("{} projects were processed, {} project remaining".format(processed_projects, (total_projects - processed_projects)))
        data = []
        for key, g in self._gauges.items():
            data.extend(g.collect())
        self._cached_metrics = data
        logging.info("SonarQube's data collected")
