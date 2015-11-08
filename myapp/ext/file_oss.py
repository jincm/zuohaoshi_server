# encoding: utf-8

"""
    zuohaoshi oss
    Good man is well
"""
import time
from oss.oss_api import *
from oss.oss_xml_handler import *

ACCESS_ID = "O4LzRirHOopmmAak"
SECRET_ACCESS_KEY = "q5XcjfAbqcC91iFUEhoRFPjHrOXVPm"
accessKeyId, accessKeySecret = ACCESS_ID, SECRET_ACCESS_KEY

endpoint = "oss-cn-beijing.aliyuncs.com"
BUCKET = "xinsongkeji"
private_endpoint = BUCKET + ".oss-cn-beijing-internal.aliyuncs.com"
public_endpoint = BUCKET + ".oss-cn-beijing.aliyuncs.com"

oss = OssAPI(endpoint, accessKeyId, accessKeySecret)


def oss_upload_file(path, filename, localfile):
    res = oss.put_object_from_file(BUCKET, "%s/%s" % (path, filename), localfile)
    if res.status == 200:
        # return "http://xinsongkeji.oss-cn-beijing.aliyuncs.com/zuohaoshi/test/test.jpg"
        file_url = "http://" + public_endpoint + path + "/" + filename
        return file_url
    # print "%s\n%s" % (res.status, res.read())
    return None


def oss_download_file(path, filename, localfile):
    pass

def oss_delete_file(path, filename):
    pass

if __name__ == '__main__':
    res = oss_upload_file('zuohaoshi/test', 'test.jpg', '/home/jincm/zuohaoshi/server/test/1.png')
    print res