# -*- coding: utf-8 -*-

import time
import TencentYoutuyun

appid = '1006408'
secret_id = 'AKID4J1QOUxGl8I7XzPgvhhNAdq9t1q0rBXk'
secret_key = 'TqoPiYzqJFHk0VlioiC2Ax8rF2E7Pjk0'

userid = '1234567'
#end_point = TencentYoutuyun.conf.API_TENCENTYUN_END_POINT 
end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT

youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, userid, end_point)

ret = youtu.FaceCompare('http://xinsongkeji.oss-cn-beijing.aliyuncs.com/zuohaoshi/lost/test/7.jpg',
                        'http://xinsongkeji.oss-cn-beijing.aliyuncs.com/zuohaoshi/lost/test/8.jpg',data_type = 1)
#ret = youtu.FaceCompare('/tmp/face1.jpg','/tmp/face4.jpg',data_type = 0)
#print ret
#ret = youtu.FaceCompare('/tmp/face1.jpg','/tmp/face11.jpg',data_type = 0)
print ret