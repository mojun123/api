import unittest
import inspect
from openpyxl.styles.colors import RED,GREEN
from libs.ddt import (data, ddt)
from base.base import Base
from common.ParseExcel import do_excel
from common.DataReplace import register_add_class
from common.HandleJson import HandleJson
from common.ParseConfig import ParseConfigFile
from common.ParseConfig import CONFIG_PATH
from common.RecordLog import log
from business.ClassManageApi import classManage


@ddt
class TestAddApi(Base):
    """添加班级接口"""
    test_data = do_excel.get_name_tuple_all_value("class")
    pc_two = ParseConfigFile()
    method = pc_two.getConfValue(CONFIG_PATH, "DeleteClass", "method")
    url = pc_two.getConfValue(CONFIG_PATH, "DeleteClass", "url")
    request_value = pc_two.getConfValue(CONFIG_PATH, "DeleteClass", "data")

    def setUp(self):
        method = self.pc_two.getConfValue(CONFIG_PATH,"ClassSetUp","method")
        url = self.pc_two.getConfValue(CONFIG_PATH,"ClassSetUp","url")
        data = self.pc_two.getConfValue(CONFIG_PATH,"ClassSetUp","data")
        try:
            response=self.request(method,url,data=data)
            log.info(response.json())
        except Exception as e:
            raise e
            log.info("添加班级失败")







    @data(*test_data)
    def test_add_class(self, value):
        pc = ParseConfigFile()
        row = value.CaseId + 1#测试用列的编号
        title = value.Precondition #用列标题
        # url = pc.getConfValue(CONFIG_PATH,"URL","Host_Url") + value.URL #用例URL
        url = "http://ci.ytesting.com/api/3school/school_classes"
        # log.info(url)
        request_value = value.Data #请求参数
        log.info(request_value)
        request_method = value.Method #请求方法
        exist = value.Exist
        log.info("exist的值为{}，数据类型为{}".format(exist,type(exist)))
        log.info('开始执行班级-"{}"测试用例'.format(title))
        if request_method == "get" or request_method == "post" :
            response = self.request(request_method,url,data=request_value)
            request_value = HandleJson.json_to_python(request_value)  # 将传输的数据变成Python格式的数据
            second_response = classManage.get_class_invitecode_and_id(request_value["grade"])  # 获取添加之后的invitecode和id的值
            expect_text = value.Expected  # 得到期望值
            last_expect = register_add_class(str(second_response[0]), str(second_response[1]), expect_text)
            last_expect = HandleJson.json_to_python(last_expect)
        elif request_method == "put":
            if exist:
                exist_Id = HandleJson.json_to_python(exist)
                url = classManage.modify_class_manage(data=exist,grade=exist_Id["grade"])
            else:
                url = classManage.modify_class_manage()
            log.info("修改班级之前获取到的{}和现有的班级{}".format(url,classManage.get_class_invitecode_and_id()))
            response = self.request(request_method,url,data=request_value)
            expect_text = value.Expected
            last_expect = HandleJson.json_to_python(expect_text)
        else:
            self.request(self.method,self.url,data=self.request_value)
            request = HandleJson.json_to_python(self.request_value)
            classId = (classManage.get_class_invitecode_and_id(request["grade"])[1])
            log.info("获取删除的calssId{}".format(classId))
            if exist :
                response = classManage.delete_add_class(classId,exist)
                log.info("当exist不为空的时候返回的值为{},response的值为{}".format(response.json,response))
            else:
                response = classManage.delete_add_class(classId)
                log.info("exist的值为resposne的值为{}".format(response))
            last_expect = value.Expected #得到期望值
            last_expect = HandleJson.json_to_python(last_expect)
        log.info(response.text)
        actual_result = response.json()
        do_excel.write_cell(
            pc.getConfValue(CONFIG_PATH,"SheetName","Class"),
            int(row),
            int(pc.getConfValue(CONFIG_PATH,"ExcelNum","Actual_Column")),
            response.text
        )
        try:
            self.assertEqual(last_expect,actual_result,msg="测试{}失败".format(title))
        except AssertionError as e:
            do_excel.write_cell(
                pc.getConfValue(CONFIG_PATH, "SheetName", "Class"),
                int(row),
               int(pc.getConfValue(CONFIG_PATH, "ExcelNum", "Result_Column")),
                pc.getConfValue(CONFIG_PATH,"Result",'Fail'),
                color=RED
            )
            log.error('{}-测试[{}] :Failed\nDetails:\n{}'.format(inspect.stack()[0][3], title, e))
            raise e

        else:
            do_excel.write_cell(
                pc.getConfValue(CONFIG_PATH, "SheetName", "Class"),
                int(row),
                int(pc.getConfValue(CONFIG_PATH, "ExcelNum", "Result_Column")),
                pc.getConfValue(CONFIG_PATH, "Result", 'Pass'),
                color=GREEN
            )
            log.info('{}-测试[{}] :Passed'.format(inspect.stack()[0][3], title))
        log.info('执行班级-测试用例"{}"结束'.format(title))

    def tearDown(self):
        clament= classManage.get_class_invitecode_and_id()
        for one in clament["retlist"]:
            if one["studentnumber"] is None:
                pass
            else:
                classManage.delete_add_class(one["id"])




if __name__ == "__main__":
    unittest.main()








