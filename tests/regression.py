from testflows.core import *

from helpers.argparser import argparser
from helpers.cluster import Cluster
from requirements.requirements import *

xfails = {
    # test_operator.py
    "/regression/e2e.test_operator/test_023*": [(Fail, "Template annotations do not work")],

    # test_clickhouse.py
    "/regression/e2e.test_clickhouse/test_ch_001*": [(Fail, "Insert Quorum test need to refactoring")],

    # test_metrics_alerts.py
    "/regression/e2e.test_metrics_alerts/test_clickhouse_dns_errors*": [
        (Fail, "DNSError behavior changed on 21.9, look https://github.com/ClickHouse/ClickHouse/issues/29624")
    ],

    # test_keeper.py
    "/regression/e2e.test_keeper/test_clickhouse_keeper_rescale*": [
        (Fail, "need `ruok` before quorum https://github.com/ClickHouse/ClickHouse/issues/35464, need apply file config instead use commited data for quorum https://github.com/ClickHouse/ClickHouse/issues/35465")
    ],
}


@TestSuite
@XFails(xfails)
@ArgumentParser(argparser)
@Specifications(
    QA_SRS026_ClickHouse_Operator
)
def regression(self, native, keeper_type):
    """ClickHouse Operator test regression suite.
    """
    def run_features():
        features = [
            "e2e.test_metrics_exporter",
            "e2e.test_metrics_alerts",
            "e2e.test_backup_alerts",
            "e2e.test_operator",
            "e2e.test_clickhouse",
            "e2e.test_examples",
            "e2e.test_keeper",
        ]
        for feature_name in features:
            Feature(run=load(feature_name, "test"))

    self.context.native = native
    self.context.keeper_type = keeper_type
    if native:
        run_features()
    else:
        with Cluster():
            run_features()


if main():
    regression()
