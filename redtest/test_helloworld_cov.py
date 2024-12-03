"""
Test case for helloworld API

.. moduleauthor:: Armand BENETEAU <armand.beneteau@iot.bzh>

*Date: 03/12/2024*

*License:*
    *Copyright (C) 2024 "IoT.bzh"*

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

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web import Application
import asyncio
from typing import Any

from redtest_helloworld_api.rtest_hello_api_main import main_init_app

from test_constants import *

class TestRedtestHelloAPI(AioHTTPTestCase):
    """
    Test class made in order to run the unit tests on the redtest-helloworld-api

    It inherits from the AioHTTPTestCase class
    """

    async def get_application(self) -> Application:
        """
        Override the get_application method to return the redtest-helloworld-api application

        :returns: aiohttp.web.Application -- The application to run with web.run_app
        """
        return main_init_app()
    
    async def send_and_check(self, http_method: str, verb: str, status_wanted: int, json_content: dict = None) -> Any:
        """
        Function allowing to send a HTTP request (with or without parameters), check the status of \
        the HTTP answer and returns the content of the answer's body

        :param http_method: HTTP method to use in the HTTP request (for the moment only "POST" or "GET")
        :type http_method: str
        :param verb: Verb URL to use in the HTTP request
        :type verb: str
        :param status_wanted: Status wanted by the client to be checked
        :type status_wanted: int
        :param json_content: json body to send with the request (nothing is passed if value is None)
        :type json_content: dict
        :returns: dict -- answer as a dictionary (containing the status and the json answer)
        """
        # Send the HTTP request
        async with self.client.request(http_method, verb, json=json_content) as answer:
            # Get content type
            content_type = answer.content_type

            # Get the status
            ans_status = answer.status

            if("json" in content_type):
                # Get the json content of the answer
                body_content = await answer.json()
            else:
                # Get the json content of the answer
                body_content = await answer.text()

        # Check the status if wanted
        if status_wanted is not None:
            self.assertEqual(ans_status, status_wanted)

        return body_content
    
    async def test_help_verb(self):
        """
        Test that the help verb is present and return what we expect
        """
        help_answer = await self.send_and_check("GET", "/help", 200)

        # Accumulate all the verb in a list
        verb_list = []
        for dict_item in help_answer[JSON_VERBS_LIST_KEY]:
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

        await asyncio.sleep(0.5)

    async def test_version_verb(self):
        """
        Test that the version verb is present and return what we expect
        """
        version_answer = await self.send_and_check("GET", "/version", 200)

        # Check that the value of the version is what we expect
        self.assertEqual(VERSION, version_answer[JSON_VERSION_KEY])

        await asyncio.sleep(0.5)

    async def test_verbs_list_verb(self):
        """
        Test that the verbs list verb is present and return what we expect
        """
        help_answer = await self.send_and_check("GET", ("/api/" + VERSION + "/verbs/list"), 200)

        # Accumulate all the verb in a list
        verb_list = []
        for dict_item in help_answer[JSON_VERBS_LIST_KEY]:
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

        await asyncio.sleep(0.5)

    async def test_hello_verb(self):
        """
        Test that the hello verb is present and return what we expect
        """
        hello_answer = await self.send_and_check("POST", ("/api/" + VERSION + "/hello"), 200)

        # Check that we have what we expect
        self.assertTrue("Hello" in hello_answer[JSON_MSG_KEY])
        self.assertTrue("RedTests" in hello_answer[JSON_MSG_KEY])
        self.assertTrue("RedPesk" in hello_answer[JSON_MSG_KEY])

        await asyncio.sleep(0.5)

    async def test_goodbye_verb(self):
        """
        Test that the goodbye verb is present and return what we expect
        """
        goodbye_answer = await self.send_and_check("POST", ("/api/" + VERSION + "/goodbye"), 200)

        # Check that we have what we expect
        self.assertTrue("Goodbye" in goodbye_answer[JSON_MSG_KEY])

        await asyncio.sleep(0.5)

    async def test_friendly_api(self):
        """
        Test that the API is friendly when saying goodbye
        """
        goodbye_answer = await self.send_and_check("POST", ("/api/" + VERSION + "/goodbye"), 200)

        # Check that we have what we expect
        self.assertTrue("friend" in goodbye_answer[JSON_MSG_KEY])

        await asyncio.sleep(0.5)
