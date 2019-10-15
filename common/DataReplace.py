import re


from common.RecordLog import log



class DataReplace(object):
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
