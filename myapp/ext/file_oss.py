# encoding: utf-8

"""
    zuohaoshi oss
    Good man is well
"""
import time
from oss.oss_api import *
from oss.oss_xml_handler import *

endpoint="oss-cn-beijing.aliyuncs.com"
ACCESS_ID = "O4LzRirHOopmmAak"
SECRET_ACCESS_KEY = "q5XcjfAbqcC91iFUEhoRFPjHrOXVPm"
accessKeyId, accessKeySecret = ACCESS_ID, SECRET_ACCESS_KEY

BUCKET = "xinsongkeji"
oss = OssAPI(endpoint, accessKeyId, accessKeySecret)


def oss_upload_file(path, filename, localfile):
    res = oss.put_object_from_file(BUCKET, "%s/%s" % (path, filename), localfile)
    print "%s\n%s" % (res.status, res.read())
    return res


def oss_download_file(path, filename, localfile):
    pass

def oss_delete_file(path, filename):
    pass