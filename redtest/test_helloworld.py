"""
Test case for helloworld API

.. moduleauthor:: Armand BENETEAU <armand.beneteau@iot.bzh>

*Date: 06/03/2020*

*License:*
    *Copyright (C) 2020-2025 IoT.bzh Company*

    *Licensed under the Apache License, Version 2.0 (the "License");\
    you may not use this file except in compliance with the License.\
    You may obtain a copy of the License at:*

    *http://www.apache.org/licenses/LICENSE-2.0*

    *Unless required by applicable law or agreed to in writing, software\
    distributed under the License is distributed on an "AS IS" BASIS,\
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or\
    implied.*
    *See the License for the specific language governing permissions and\
    limitations under the License.*
"""
# Imports
import unittest
import requests
import time

from test_constants import *


class TestHelloworldAPI(unittest.TestCase):
    """
    Class used to run Unit tests on the helloworld API
    """

    def test_help_verb(self):
        """
        Test that the help verb is present and return what we expect
        """
        help_answer = requests.get(SRV_URL + "/help")
        answer_data = help_answer.json()

        # Check that the http status is at 200
        self.assertEqual(help_answer.status_code, 200)

        # Accumulate all the verb in a list
        verb_list = []
        for dict_item in answer_data[JSON_VERBS_LIST_KEY]:
            verb_list.append(dict_item[JSON_VERB_KEY])

        # Check that the help verb is in the verb list
        self.assertTrue("/help" in verb_list)
        # Check that the version verb is in the list
        self.assertTrue("/version" in verb_list)
        # Check that the verb list verb is in the list 
        self.assertTrue(("/api/" + VERSION + "/verbs/list") in verb_list)
        # Check that the hello verb is in the list
        self.assertTrue(("/api/" + VERSION + "/hello") in verb_list)
        # Check that the goodbye verb is in the list
        self.assertTrue(("/api/" + VERSION + "/goodbye") in verb_list)

        time.sleep(1)

    def test_version_verb(self):
        """
        Test that the version verb is present and return what we expect
        """
        version_answer = requests.get(SRV_URL + "/version")
        answer_data = version_answer.json()

        # Check that the http status is at 200
        self.assertEqual(version_answer.status_code, 200)

        # Check that the value of the version is what we expect
        self.assertEqual(VERSION, answer_data[JSON_VERSION_KEY])

        time.sleep(1)

    def test_verbs_list_verb(self):
        """
        Test that the verbs list verb is present and return what we expect
        """
        help_answer = requests.get(SRV_URL + ("/api/" + VERSION + "/verbs/list"))
        answer_data = help_answer.json()

        # Check that the http status is at 200
        self.assertEqual(help_answer.status_code, 200)

        # Accumulate all the verb in a list
        verb_list = []
        for dict_item in answer_data[JSON_VERBS_LIST_KEY]:
            verb_list.append(dict_item[JSON_VERB_KEY])

        # Check that the help verb is in the verb list
        self.assertTrue("/help" in verb_list)
        # Check that the version verb is in the list
        self.assertTrue("/version" in verb_list)
        # Check that the verb list verb is in the list 
        self.assertTrue(("/api/" + VERSION + "/verbs/list") in verb_list)
        # Check that the hello verb is in the list
        self.assertTrue(("/api/" + VERSION + "/hello") in verb_list)
        # Check that the goodbye verb is in the list
        self.assertTrue(("/api/" + VERSION + "/goodbye") in verb_list)

        time.sleep(1)

    def test_hello_verb(self):
        """
        Test that the hello verb is present and return what we expect
        """

        hello_answer = requests.post(SRV_URL + ("/api/" + VERSION + "/hello"))
        answer_data = hello_answer.json()

        # Check that the http status is at 200
        self.assertEqual(hello_answer.status_code, 200)

        # Check that we have what we expect
        self.assertTrue("Hello" in answer_data[JSON_MSG_KEY])
        self.assertTrue("RedTests" in answer_data[JSON_MSG_KEY])
        self.assertTrue("RedPesk" in answer_data[JSON_MSG_KEY])

        time.sleep(1)

    def test_goodbye_verb(self):
        """
        Test that the goodbye verb is present and return what we expect
        """

        goodbye_answer = requests.post(SRV_URL + ("/api/" + VERSION + "/goodbye"))
        answer_data = goodbye_answer.json()

        # Check that the http status is at 200
        self.assertEqual(goodbye_answer.status_code, 200)

        # Check that we have what we expect
        self.assertTrue("Goodbye" in answer_data[JSON_MSG_KEY])

        time.sleep(1)

    def test_friendly_api(self):
        """
        Test that the API is friendly when saying goodbye
        """

        goodbye_answer = requests.post(SRV_URL + ("/api/" + VERSION + "/goodbye"))
        answer_data = goodbye_answer.json()

        # Check that the http status is at 200
        self.assertEqual(goodbye_answer.status_code, 200)

        # Check that we have what we expect
        self.assertTrue("friend" in answer_data[JSON_MSG_KEY])

        time.sleep(1)
