# coding:utf-8

import re
import os
import sys
sys.path.insert(0, os.path.abspath('../'))

import time
import shutil
import unittest
import requests
import subprocess
import fpage


class Tests(unittest.TestCase):
    process = []
    dir_lst = []
    dir_to_port = {}

    @classmethod
    def setUpClass(cls):
        prefix = 'fp_test'
        cur_dir = os.getcwd()
        for tmpl in ['mako', 'jinja2', 'tornado']:
            for orm in ['peewee', 'sqlalchemy']:
                name = '_'.join([prefix, tmpl, orm])
                cls.dir_lst.append(name)
                if os.path.exists(name):
                    shutil.rmtree(name)
                fpage.gen(name, name, tmpl, orm)

        i = 1
        for name in cls.dir_lst:
            os.chdir(name)
            appfile = os.path.join(os.getcwd(), 'app.py')
            port = '90%02d' % i
            #cls.process.append(subprocess.Popen('python ' + appfile + ' -port=' + port))
            cls.process.append(os.popen('python ' + appfile + ' -port=' + port))
            cls.dir_to_port[name] = port
            os.chdir(cur_dir)
            i += 1
            time.sleep(0.5)
            
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        '''for i in cls.process:
            i.kill()'''

        '''time.sleep(3)

        try:
            for name in cls.dir_lst:
                shutil.rmtree(name)
        except:
            pass'''

    def test_index(self):
        for i in self.dir_lst:
            with self.subTest(i):
                resp = requests.get('http://127.0.0.1:%s/' % self.dir_to_port[i])
                self.assertEqual(resp.status_code, 200)
                time.sleep(0.5)

    def test_about(self):
        for i in self.dir_lst:
            with self.subTest(i):
                resp = requests.get('http://127.0.0.1:%s/about' % self.dir_to_port[i])
                self.assertEqual(resp.status_code, 200)
                time.sleep(0.5)
                
    def test_jump_page(self):
        for i in self.dir_lst:
            with self.subTest(i):
                resp = requests.get('http://127.0.0.1:%s/jump_test' % self.dir_to_port[i])
                self.assertEqual(resp.status_code, 200)
                self.assertTrue(u'Message Test: Error' in resp.text)
                self.assertTrue(u'中文测试' in resp.text)
                time.sleep(0.5)

    def test_logout_without_login(self):
        for i in self.dir_lst:
            with self.subTest(i):
                resp = requests.get('http://127.0.0.1:%s/signout' % self.dir_to_port[i])
                self.assertEqual(resp.history[0].status_code, 302)
                time.sleep(0.5)

    def test_sign_up(self):
        for i in self.dir_lst:
            with self.subTest(i):
                url = 'http://127.0.0.1:%s/signup' % self.dir_to_port[i]
                resp = requests.get(url)
                self.assertEqual(resp.status_code, 200)
                
                session = requests.Session()

                # length of username must not be less than 3
                resp = session.get(url)
                xsrf = re.search(r'"_xsrf" value="([a-z0-9|]+)"', resp.text).group(1)
                resp = session.post(url, {'username': 'ab', 'password': '1234', 'password_again': '1234', '_xsrf': xsrf})
                self.assertTrue(u'用户名长度必须在 3-15 之间' in resp.text)

                # length of username must not be more than 15
                resp = session.get(url)
                xsrf = re.search(r'"_xsrf" value="([a-z0-9|]+)"', resp.text).group(1)
                resp = session.post(url, {'username': 'a' * 16, 'password': '1234', 'password_again': '1234', '_xsrf': xsrf})
                self.assertTrue(u'用户名长度必须在 3-15 之间' in resp.text)

                # password not same
                resp = session.get(url)
                xsrf = re.search(r'"_xsrf" value="([a-z0-9|]+)"', resp.text).group(1)
                resp = session.post(url, {'username': 'abc', 'password': '1234', 'password_again': '12345', '_xsrf': xsrf})
                self.assertTrue(u'两次输入的密码不一致！' in resp.text)
                
                # success
                resp = session.get(url)
                xsrf = re.search(r'"_xsrf" value="([a-z0-9|]+)"', resp.text).group(1)
                resp = session.post(url, {'username': 'abc', 'password': '1234', 'password_again': '1234', '_xsrf': xsrf})
                self.assertTrue(u'账户创建成功！' in resp.text)
                
                # user exists
                resp = session.get(url)
                xsrf = re.search(r'"_xsrf" value="([a-z0-9|]+)"', resp.text).group(1)
                resp = session.post(url, {'username': 'abc', 'password': '1234', 'password_again': '1234', '_xsrf': xsrf})
                self.assertTrue(u'用户已存在！' in resp.text)

                del session
                time.sleep(0.5)


if __name__ == '__main__':
    unittest.main()
