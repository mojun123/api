import re


from common.RecordLog import log
from common.ParseConfig import ParseConfigFile
from config.config import CONFIG_PATH




class DataReplace(object):
    pc = ParseConfigFile()
    pattern_exist_invitecode = re.compile(pc.getConfValue(CONFIG_PATH,"Expression","exist_invitecode"))
    pattern_exist_id = re.compile(pc.getConfValue(CONFIG_PATH,"Expression","exist_id"))



    def __init__(self):
        pass


    @staticmethod
    def re_replace(re_expression,data,source):
        """

        :param re_expression: 正则表达式
        :param data: 被替换字符串如结果
        :param source: 目标源字符串
        :return:
        """
        if isinstance(data,str):
            pattern = re.compile(re_expression)
            if re.search(pattern,source):
                source = re.sub(pattern,data,source)
            log.info("测试数据{}通过正则匹配为: {}".format(source, source))
            return source
        else:
            log.error("正则匹配测试数据失败: data '{}' must be string".format(data))
            raise TypeError("data '{}' must be string".format(data))


    #--------增加班级中期望值的替换操作-------------
    @classmethod
    def replace_exist_invitecode(cls,exist_invitecode,data):
        """将得到的invitecode替换得到期望值中"""
        data = cls.re_replace(cls.pattern_exist_invitecode,exist_invitecode,data)
        log.info("替换的值为{}".format(data))
        return data

    @classmethod
    def replace_exist_idnumber(cls,exist_idnumber,data):
        """将得到的idnumber替换道期望值中"""
        data = cls.re_replace(cls.pattern_exist_id,exist_idnumber,data)
        log.info("替换的值为{}".format(data))
        return data

    @classmethod
    def add_class_exist_data(cls,exist_invitecod,exist_idnumber,data):
        """将得到的invitecode和id替换得到期望值中"""
        first_exist = cls.replace_exist_invitecode(exist_invitecod,data)
        data = cls.replace_exist_idnumber(exist_idnumber,first_exist)
        log.info("替换的值为{}".format(data))
        return data


register_add_class= getattr(DataReplace,"add_class_exist_data")


if __name__ == "__main__":
    one = "123333"
    two = "23333"
    data = '{"invitecode":"${invitecodenumber}","retcode":0,"id":"${idnumber}"}'
    print(register_add_class(one,two,data))



