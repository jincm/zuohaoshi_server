# coding = "utf-8"

"""
    Good man is well
"""
import time
import requests

facepp_api_key = "58d296e0f2c54f238edfa1556201807b"
facepp_api_secret = "4eAtNRcN0Vnj8rA5dVa0XAdFGK0YdxWL"
facepp_url = "apicn.faceplusplus.com/v2"

# Image/Face/Person/Faceset/Group


class FaceSearch(object):
    def submit_lost_info(self, image_url, from_url):
        pass

    def submit_suspicious(self, image_url, from_url):
        pass

    def face_match(self, img1, img2):
        pass


class FacePPSearch(FaceSearch):
    def __init__(self, mylogger, type, city):
        self.url = "https://" + facepp_url

        self.logger = mylogger
        # self.city = city
        self.faceset_name = city + type  # type is lost or suspicious

        self._faceset_create(self.faceset_name)

        self.logger.info("FacePPSearch init\n")

    def submit_lost_info(self, image_url, from_url, reversetype='suspicious'):
        self.logger.info("\n\nsubmit_info:reversetype:[%s][%s][%s]\n", reversetype, image_url, from_url)
        face_id = self._detection_detect(image_url, from_url)
        if face_id is None:
            self.logger.error("error:detection_detect[%s][%s]\n", image_url, from_url)
            return {'fail': 'error:detection_detect'}

        self.logger.info("add face start:[%s][%s]\n", face_id, from_url)
        result = self._faceset_add_face(self.faceset_name, face_id)
        if not result:
            self.logger.error("err:fs_add_face[%s][%s][%s:%s]\n", image_url, from_url, self.faceset_name, face_id)
            return {'fail': 'error:faceset_add_face'}

        result = self._train_search(self.faceset_name)
        if not result:
            self.logger.error("err:_train_search[%s][%s][%s:%s]\n", image_url, from_url, self.faceset_name, face_id)
            return {'fail': 'error:_train_search'}

        faceset_list = self.info_get_faceset_list(reversetype)
        if faceset_list is None:
            self.logger.error("error:info_get_faceset_list[%s][%s]\n", image_url, from_url)
            return {'fail': 'error:info_get_faceset_list'}

        result = {}
        for one_faceset in faceset_list:
            search_result = self._recognition_search(face_id, one_faceset['faceset_name'])
            self.logger.info("recognition_search result:[%s][%s]\n", search_result, one_faceset)
            if search_result is None:
                continue
            for one in search_result:
                tmp = self._recognition_compare(one.get('face_id'), face_id)
                if tmp is None:
                    continue
                self.logger.info("recognition_compare end:[%s][%s]\n", one, face_id)
                result['%s' % one.get('face_id')] = tmp

        ret = dict()
        ret['%s' % image_url] = result
        self.logger.info("submit end:[%s][%s]\n", image_url, ret)
        print ret
        return ret


    def submit_suspicious(self, image_url, from_url):
        return self.submit_lost_info(image_url, from_url, 'lost')

    # one faceset 10000 face;and 5 faceset;
    def _faceset_create(self, faceset_name):
        # get faceset's num, if more than 10000, then set faceset_name_index+1
        # https://url/v2/faceset/get_info?api_secret=YOUR_API_SECRET&api_key=YOUR_API_KEY&faceset_name=NicolasCage
        try:
            url = self.url + "/faceset/create"
            payload = dict()
            payload['api_key'] = facepp_api_key
            payload['api_secret'] = facepp_api_secret
            payload['faceset_name'] = self.faceset_name  #+ str(index)
            resp = requests.get(url, params=payload)
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                self.logger.info("response:%s\n", resp.json())
                return resp.json().get('faceset_name')
            else:
                if resp.status_code == 453:
                    return self.faceset_name
                self.logger.error("error is coming...[%d, %s]\n", resp.status_code, resp.text)
                return None

    def _faceset_delete(self, city):
        pass

    def info_get_face(self, face_id):
        try:
            url = self.url + "/info/get_face"
            payload = dict()
            payload['api_key'] = facepp_api_key
            payload['api_secret'] = facepp_api_secret
            payload['face_id'] = face_id
            resp = requests.get(url, params=payload)
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                self.logger.info("info_get_face response:%s\n", resp.json())
                return resp.json()
            else:
                self.logger.error("error is coming...[%d, %s]\n", resp.status_code, resp.text)
                return None

    def faceset_getinfo(self, faceset_name):
        try:
            url = self.url + "/faceset/get_info"
            payload = dict()
            payload['api_key'] = facepp_api_key
            payload['api_secret'] = facepp_api_secret
            payload['faceset_name'] = faceset_name
            resp = requests.get(url, params=payload)
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                self.logger.info("faceset_getinfo response:%s\n", resp.json())
                result = []
                fsets = resp.json().get('face')
                for onefs in fsets:
                    face_id = onefs.get('face_id')
                    if face_id:
                        result.append(face_id)
                self.logger.info("faceset_getinfo response:%s\n", result)
                return result
            else:
                self.logger.error("error is coming...[%d, %s]\n", resp.status_code, resp.text)
                return None

    def info_get_faceset_list(self, scope_type):
        try:
            url = self.url + "/info/get_faceset_list"
            payload = dict()
            payload['api_key'] = facepp_api_key
            payload['api_secret'] = facepp_api_secret
            resp = requests.get(url, params=payload)
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                self.logger.info("info_get_faceset_list response:%s\n", resp.json())
                result = []
                fsets = resp.json().get('faceset')
                for onefs in fsets:
                    if scope_type in onefs.get('faceset_name'):
                        result.append(onefs)
                return result
            else:
                self.logger.error("error is coming...[%d, %s]\n", resp.status_code, resp.text)
                return None

    def _detection_detect(self, imgurl, tag):
        try:
            url = self.url + "/detection/detect"
            payload = dict()
            payload['api_key'] = facepp_api_key
            payload['api_secret'] = facepp_api_secret
            payload['url'] = imgurl
            payload['tag'] = tag
            # http://apicn.faceplusplus.com/v2/detection/detect?api_key=58d296e0f2c54f238edfa1556201807b&
            # api_secret=4eAtNRcN0Vnj8rA5dVa0XAdFGK0YdxWL&url=http%3A%2F%2Ffaceplusplus.com%2Fstatic%2Fimg%2Fdemo%2F1.jpg&attribute=glass,pose,gender,age,race,smiling
            resp = requests.get(url, params=payload)

            self.logger.info("_detection_detecting...:[%d][%s]\n", resp.status_code, payload)
        except Exception, e:
            self.logger.error("res error info:%s,error:%s\n", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                self.logger.info("response:%s,[%s]\n", resp.json(), resp.json().get('face_id'))
                return resp.json().get('face')[0].get('face_id')
            else:
                self.logger.error("error is coming...[%d, %s]\n", resp.status_code, resp.text)
                return None

    def _info_get_session(self, sess_id):
        try:
            url = self.url + "/info/get_session"
            payload = dict()
            payload['api_key'] = facepp_api_key
            payload['api_secret'] = facepp_api_secret
            payload['session_id'] = sess_id
            resp = requests.get(url, params=payload)

            self.logger.info("_info_get_session...:[%d][%s]\n", resp.status_code, sess_id)
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return False
        finally:
            if resp.status_code == requests.codes.ok:
                self.logger.info("response:%s\n", resp.json())
                status = resp.json().get('status')
                if status == 'SUCC':
                    return True
                else:
                    self.logger.error("res error info:status not SUCC\n")
                    return False
            else:
                self.logger.error("error is coming...[%d, %s]\n", resp.status_code, resp.text)
                return False

    def _train_search(self, faceset_name):
        try:
            url = self.url + "/train/search"
            payload = dict()
            payload['api_key'] = facepp_api_key
            payload['api_secret'] = facepp_api_secret
            payload['faceset_name'] = faceset_name
            resp = requests.get(url, params=payload)

            self.logger.info("_train_searching...:[%d][%s]\n", resp.status_code, faceset_name)
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return False
        finally:
            if resp.status_code == requests.codes.ok:
                self.logger.info("response:%s\n", resp.json())
                sess_id = resp.json().get('session_id')
                if sess_id is None:
                    self.logger.error("_train_searching response[%s]\n", resp.json())
                    return False
            else:
                self.logger.error("error is coming...[%d, %s]\n", resp.status_code, resp.text)
                return False

        for loop in xrange(1, 5):
            result = self._info_get_session(sess_id)
            if result:
                return True
            else:
                time.sleep(10)

        self.logger.error("_train_searching last for 50s [%s]\n", sess_id)
        return True

    def _recognition_search(self, key_face_id, faceset_name):
        try:
            url = self.url + "/recognition/search"
            payload = dict()
            payload['api_key'] = facepp_api_key
            payload['api_secret'] = facepp_api_secret
            payload['key_face_id'] = key_face_id
            payload['faceset_name'] = faceset_name
            payload['count'] = 5
            payload['async'] = False
            resp = requests.get(url, params=payload)
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                self.logger.info("recognition_search response:%s\n", resp.json())
                return resp.json().get('candidate')  # not candidates,api doc is error
            else:
                self.logger.error("error is coming...[%d, %s]\n", resp.status_code, resp.text)
                return None

    def _recognition_compare(self, face_id1, face_id2):
        try:
            url = self.url + "/recognition/compare"
            payload = dict()
            payload['api_key'] = facepp_api_key
            payload['api_secret'] = facepp_api_secret
            payload['face_id1'] = face_id1
            payload['face_id2'] = face_id2
            payload['async'] = False
            resp = requests.get(url, params=payload)
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                self.logger.info("recognition_compare response:%s\n", resp.json())
                return resp.json().get('similarity')
            else:
                self.logger.error("error is coming...[%d, %s]\n", resp.status_code, resp.text)
                return None

    def _faceset_add_face(self, faceset_name, face_id):
        try:
            url = self.url + "/faceset/add_face"
            payload = dict()
            payload['api_key'] = facepp_api_key
            payload['api_secret'] = facepp_api_secret
            payload['faceset_name'] = faceset_name
            payload['face_id'] = face_id
            resp = requests.get(url, params=payload)

            self.logger.info("_faceset_add_faceing...:[%d][%s]\n", resp.status_code, payload)
        except Exception, e:
            self.logger.error("res error info:%s,error:%s\n", resp.text, e)
            return False
        finally:
            if resp.status_code == requests.codes.ok:
                self.logger.info("response:%s\n", resp.json())
                return resp.json().get('success')
            else:
                self.logger.error("error is coming...[%d, %s]\n", resp.status_code, resp.text)
                return False

    def _faceset_remove_face(self, face_id):
        pass

    def face_match(self, img1, img2):
        self.logger.info("imgs is %s,%s\n", img1,img2)
        return {"score": 30}


##################################################################################
#######################Test#######################################################
##################################################################################
if __name__ == '__main__':
    #when test,you must cd /home/jincm/zuohaoshi/server first,also is myapp's parent dir
    #and then "sudo python myapp/ext/face_match.py"
    import logging
    import random

    logger = logging.getLogger()
    fh = logging.FileHandler('/tmp/face++_match.log', 'a+')
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)


    ali_url = "xinsongkeji.oss-cn-beijing-internal.aliyuncs.com/"
    # "http://xinsongkeji.oss-cn-beijing.aliyuncs.com//10.jpg"
    """
    num = 18
    for i in xrange(1, num):
        test_url = "zuohaoshi/2015/test/lost/"
        face_search_obj = FacePPSearch(logger, "test", "lost")
        lost_url = "http://" + ali_url + test_url + str(i) + ".jpg"
        from_url = "lost" + str(i)
        face_search_obj.submit_lost_info(lost_url, from_url)

    for i in xrange(1, num):
        test_url = "zuohaoshi/2015/test/suspicious/"
        face_search_obj = FacePPSearch(logger, "test", "suspicious")
        lost_url = "http://" + ali_url + test_url + str(i) + ".jpg"
        from_url = "suspicious" + str(i)
        face_search_obj.submit_suspicious(lost_url, from_url)
    """
    face_search_obj = FacePPSearch(logger, "test", "lost")
    faceset_list = face_search_obj.info_get_faceset_list('lost')
    if faceset_list is None:
        logger.error("error:info_get_faceset_list is none\n")
        exit(1)

    result = {}
    for one_faceset in faceset_list:
        face_ids = face_search_obj.faceset_getinfo(one_faceset['faceset_name'])
        logger.info("face_ids:%s\n", face_ids)
        for one_face_id in face_ids:
            logger.info("one face_id:%s\n", one_face_id)
            ret = face_search_obj.info_get_face(one_face_id)
            print ret