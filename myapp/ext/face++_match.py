# coding = "utf-8"

"""
    zuohaoshi db
    Good man is well
"""
import time
import requests

facepp_api_key = "58d296e0f2c54f238edfa1556201807b"
facepp_api_secret = "4eAtNRcN0Vnj8rA5dVa0XAdFGK0YdxWL"
facepp_url = "apicn.faceplusplus.com/v2"

# Image，Face，Person，Faceset Group


class FaceSearch(object):
    def submit_lost_info(self, image_url, from_url):
        pass

    def submit_suspicious(self, image_url, from_url):
        pass


class FacePPSearch(FaceSearch):
    def __init__(self, mylogger, type, city):
        self.url = "https://" + facepp_url

        self.logger = mylogger
        # self.city = city
        self.faceset_name = city + type  # type is lost or suspicious

        self._faceset_create(self.faceset_name)

        self.logger.info("FacePPSearch init\n")

    def submit_lost_info(self, image_url, from_url):
        self.logger.info("submit_lost_info:[%s][%s]", image_url, from_url)
        face_id = self._detection_detect(image_url, from_url)
        self._faceset_add_face(face_id)
        self._train_search()

        faceset_list = self._info_get_faceset_list("suspicious")

        for one_faceset in faceset_list:
            search_result = self._recognition_search(face_id)
            for one in search_result:
                result = self._recognition_compare(one, face_id)


    def submit_suspicious(self, image_url, from_url):
        self.logger.info("submit_lost_info:[%s][%s]", image_url, from_url)
        face_id = self._detection_detect(image_url, from_url)
        self._faceset_add_face(face_id)
        self._train_search()

        faceset_list = self._info_get_faceset_list("lost")

        for one_faceset in faceset_list:
            search_result = self._recognition_search(face_id)
            for one in search_result:
                result = self._recognition_compare(one, face_id)


    # 一个Faceset最多允许包含10000个Face。开发版最多允许创建5个Faceset。
    def _faceset_create(self, city):
        # get faceset's num, if more than 10000, then set faceset_name_index+1
        # https://url/v2/faceset/get_info?api_secret=YOUR_API_SECRET&api_key=YOUR_API_KEY&faceset_name=NicolasCage
        try:
            index = 1  # it would use while in the future if one city has more 1w's pictures
            url = self.url + "/faceset/get_info"
            my_headers = dict()
            my_headers['api_key'] = facepp_api_key
            my_headers['api_secret'] = facepp_api_secret
            my_headers['faceset_name'] = self.faceset_name + str(index)
            res = requests.get(url, headers=my_headers)

            if "face" in res.text:
                self.logger.info("faceset's face num is:%d", len(res.text['face']))

        except Exception, e:
            self.logger.error("requests for get_faceset error:%s,error:%s", self.faceset_name, e)
            return None

        if res.status_code == 200:
            pass

        try:
            url = self.url + "/faceset/create"
            self.my_headers['faceset_name'] = self.faceset_name + str(index)
            res = requests.get(url, hearders=self.my_headers)
            if res.status_code == 200:
                self.logger.info("response:%s", res.json())
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", res.text, e)
            return None

        return res.json()

    def _faceset_delete(self, city):
        pass

    def _info_get_faceset_list(self, type):
        try:
            url = self.url + "/info/get_faceset_list"

            my_headers = dict()
            my_headers['api_key'] = facepp_api_key
            my_headers['api_secret'] = facepp_api_secret

            resp = requests.get(url, hearders=self.my_headers)

            if resp.status_code == 200:
                self.logger.info("response:%s", resp.json())
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                return True, resp.json()
            else:
                print "error is coming......................."
                return False, resp.text

    def _detection_detect(self, imgurl, tag):
        try:
            url = self.url + "/detection/detect"

            my_headers = dict()
            my_headers['api_key'] = facepp_api_key
            my_headers['api_secret'] = facepp_api_secret
            my_headers['url'] = imgurl
            my_headers['tag'] = tag

            resp = requests.get(url, hearders=my_headers)

            if resp.status_code == 200:
                self.logger.info("response:%s", resp.json())
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                return True, resp.json()
            else:
                print "error is coming......................."
                return False, resp.text

    def _train_search(self, faceset_name):
        try:
            url = self.url + "/train/search"

            my_headers = dict()
            my_headers['api_key'] = facepp_api_key
            my_headers['api_secret'] = facepp_api_secret
            my_headers['faceset_name'] = faceset_name

            resp = requests.get(url, hearders=my_headers)

            if resp.status_code == 200:
                self.logger.info("response:%s", resp.json())
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                return True, resp.json()
            else:
                print "error is coming......................."
                return False, resp.text

    def _recognition_search(self, key_face_id, faceset_name):
        try:
            url = self.url + "/recognition/search"

            my_headers = dict()
            my_headers['api_key'] = facepp_api_key
            my_headers['api_secret'] = facepp_api_secret
            my_headers['key_face_id'] = key_face_id
            my_headers['faceset_name'] = faceset_name
            my_headers['count'] = 5
            my_headers['async'] = 'true'

            resp = requests.get(url, hearders=my_headers)

            if resp.status_code == 200:
                self.logger.info("response:%s", resp.json())
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                return True, resp.json()
            else:
                print "error is coming......................."
                return False, resp.text

    def _recognition_compare(self, face_id1, face_id2):
        try:
            url = self.url + "/recognition/compare"

            my_headers = dict()
            my_headers['api_key'] = facepp_api_key
            my_headers['api_secret'] = facepp_api_secret
            my_headers['face_id1'] = face_id1
            my_headers['face_id2'] = face_id2
            my_headers['async'] = 'false'

            resp = requests.get(url, hearders=my_headers)

            if resp.status_code == 200:
                self.logger.info("response:%s", resp.json())
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                return True, resp.json()
            else:
                print "error is coming......................."
                return False, resp.text

    def _faceset_add_face(self, faceset_name, face_id):
        try:
            url = self.url + "/recognition/compare"

            my_headers = dict()
            my_headers['api_key'] = facepp_api_key
            my_headers['api_secret'] = facepp_api_secret
            my_headers['faceset_name'] = faceset_name
            my_headers['face_id'] = face_id

            resp = requests.get(url, hearders=my_headers)

            if resp.status_code == 200:
                self.logger.info("response:%s", resp.json())
        except Exception, e:
            self.logger.error("res error info:%s,error:%s", resp.text, e)
            return None
        finally:
            if resp.status_code == requests.codes.ok:
                return True, resp.json()
            else:
                print "error is coming......................."
                return False, resp.text

    def _faceset_remove_face(self, face_id):
        pass


##################################################################################
#######################Test#######################################################
##################################################################################
if __name__ == '__main__':
    #when test,you must cd /home/jincm/zuohaoshi/server first,also is myapp's parent dir
    #and then "sudo python myapp/ext/face++_match.py"
    import logging
    import random

    logger = logging.getLogger()
    fh = logging.FileHandler('/tmp/face++_match.log', 'a+')
    logger.addHandler(fh)
    logger.setLevel(logging.DEBUG)

    face_search_obj = FacePPSearch(logger)
    for i in xrange(1, 10):
        lost_url = str(i)
        from_url = str(i)
        face_search_obj.submit_lost_info(lost_url, from_url)

    for i in xrange(1, 10):
        lost_url = str(i)
        from_url = str(i)
        face_search_obj.submit_suspicious(lost_url, from_url)






