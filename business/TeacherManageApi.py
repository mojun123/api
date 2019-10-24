from common.SendRequests import request
from common.ParseConfig import ParseConfigFile
from common.RecordLog import log
from config.config import CONFIG_PATH



class TeacherManageApi(object):
    request = request
    pc = ParseConfigFile()

    def teacher_manage_api(self,method,url,data):
        response = self.request(method=method,
                                url = url,
                                data = data)
        return response

    def close(self):
        log.info("关闭登录请求...")
        self.request.close_session()

teacherManage = TeacherManageApi()


if __name__ == "__main__":
    pass
