from common.SendRequests import request
from common.ParseConfig import ParseConfigFile
from common.RecordLog import log
from config.config import CONFIG_PATH


class ClassManageApi(object):
    request = request
    pc = ParseConfigFile()
    def class_mannge_api(self,method,url,data):
        response = self.request(method=method,
                                url=url,
                                data=data
                                )
        # log.info('班级管理：{}接口'.format(data['grade']))
        return response


    def get_class_invitecode_and_id(self,grade=None):
        method = "get"
        url = "http://ci.ytesting.com/api/3school/school_classes"
        if grade != None:
            data = {
                "vcode":pc.getConfValue(CONFIG_PATH,"vcode","vcode"),
                "action":"list_classes_by_schoolgrade",
                "gradeid":grade
            }
        else:
            data = {
                "vcode": pc.getConfValue(CONFIG_PATH, "vcode", "vcode"),
                "action": "list_classes_by_schoolgrade"
            }
        response = self.class_mannge_api(method,url,data=data)
        bodyDict =response.json()
        log.info("展示出的班级为{}".format(bodyDict))
        last_txt = bodyDict["retlist"][0]
        print(last_txt)
        intvitecode = last_txt["invitecode"]
        id = last_txt["id"]
        return intvitecode,id


    def delete_add_class(self,classid):
        method = "delete"
        url = "http://ci.ytesting.com/api/3school/school_classes/" + str(classid)
        log.info("删除的url：{}".format(url))
        data = {
            "vcode":pc.getConfValue(CONFIG_PATH, "vcode", "vcode")
        }
        respones = self.class_mannge_api(method,url,data=data)
        log.info("删除成功，放回的结果为{}".format(respones))










    def close(self):
        log.info('关闭登录请求...')
        self.request.close_session()





classManage = ClassManageApi()


if __name__ == "__main__":
    classManage = ClassManageApi()
    pc = ParseConfigFile()
    ac = classManage.get_class_invitecode_and_id()
    print(ac)
    bc= classManage.delete_add_class(ac[1])
    print(ac)
    print(bc)
    classManage.close()

