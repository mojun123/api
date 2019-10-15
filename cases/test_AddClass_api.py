import unittest
import inspect
from openpyxl.styles.colors import RED,GREEN
from libs.ddt import (data,ddt)
from base.base import Base
from common.ParseExcel import do_excel
from common.DataReplace import DataReplace
from common.HandleJson import HandleJson
from common.ParseConfig import ParseConfigFile
from common.ParseConfig import CONFIG_PATH
from common.RecordLog import log

@ddt
class TestAddApi(Base):
    """添加班级接口"""
    test_data = do_excel.get_name_tuple_all_value("class")


    @data(*test_data)
    def test_add_class(self,value):
        pc = ParseConfigFile()
        row = value.CaseId + 1#测试用列的编号
        title = value.Title #用列标题
        url = pc.getConfValue(CONFIG_PATH,"URL","Host_Url") + value.URL #用例URL
        request_value = value.Data #请求参数
        request_method = value.Method #请求方法
        expected = HandleJson.json_to_python(value.Expected) #期望结果
        log.info('开始执行登录-"{}"测试用例'.format(title))
        response = self.request(request_method,url,data=request_value)
