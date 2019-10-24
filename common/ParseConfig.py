import configparser
from config.config import CONFIG_PATH

from common.RecordLog import log

class ParseConfigFile(object):


    def __init__(self):
        """
        :param filename
        """
        self.cf = configparser.ConfigParser()

    def getConfValue(self,filename,section,name):
        """

        :param filename:
        :param section:
        :param name:
        :return:
        """
        try:
            self.cf.read(filename,encoding="UTF-8")
            value = self.cf.get(section,name)
        except Exception as e:
            log.info('read file [%s] for [%s] failed , did not get the value' %(filename,section))
            raise e
        else:
            log.info('read excel value [%s] successed! ' %value)
            return value


    def writeConfValue(self,filename,section,name,value):
        """

        :param filename:
        :param section:
        :param name:
        :param value:
        :return:
        """
        try:
            self.cf.add_section(section)
            self.cf.set(section,name,value)
            self.cf.write(open(filename,"w"))
        except Exception:
            log.logger.exception('section %s has been exist!' % section)
            raise configparser.DuplicateSectionError(section)
        else:
            log.logger.info('write section' + section + 'with value ' + value + ' successed!')




if __name__ == "__main__":
    pc = ParseConfigFile()
    data = pc.getConfValue(CONFIG_PATH,"URL","Host_Url")
    ploay = pc.getConfValue(CONFIG_PATH,"ClassSetUp","data")
    print(type(ploay))


