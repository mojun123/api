import os
import unittest


from libs import HTMLTestRunnerNew

from config.config import CASE_DIR,ENVIRONMENT,REPORT_DIR,CONFIG_PATH
from common.CreatePath import ModelsClass
from common.ParseConfig import ParseConfigFile




pc = ParseConfigFile()
def tc_suite():
    """测试套件"""
    discover = unittest.defaultTestLoader.discover(CASE_DIR,"test_*.py")
    return discover


if __name__ == "__main__":
    report_dir = ModelsClass.create_dir(REPORT_DIR)
    report_file_name = ModelsClass.file_name("html")

    with open(report_dir + "/" + report_file_name,"wb") as f:
        runner = HTMLTestRunnerNew.HTMLTestRunner(
            stream=f,
            description=ENVIRONMENT,
            title= pc.getConfValue(CONFIG_PATH,"Project","PRO_NAME"),
            tester="Anton Zhang",
            verbosity=2
        )
        runner.run(tc_suite())
