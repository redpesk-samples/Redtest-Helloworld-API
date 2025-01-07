"""
Main file used to run the Redtest Helloworld API.

.. moduleauthor:: Armand BENETEAU <armand.beneteau@iot.bzh>

*Date: 06/03/2020*

*License:*
    *Copyright (C) 2019-2025 IoT.bzh Company*

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

# Import web utilities from the Asynchrone IO HTTP
from aiohttp import web
import asyncio
import os
import signal
import sys

# Import constants
from redtest_helloworld_api.rtest_hello_shared_constants import *

# Create the list of available verbs in the API
available_verbs = []
# List of all the task's coroutine names to handle at the end
tasks_coro_to_handle = [
    "_service_task"  # Task from asyncio_server from engineio
    ]


async def version(request):
    """
    Verb handler that gives the version of the API.

    :param request: A request used for receiving request’s information by web \
    handler
    :type request: aiohttp.web.Request
    :returns:  aiohttp.web.Response -- Response class used to send HTTP \
    response by aiohttp
    """

    # Set the json answer with the right version
    json_answer = {
                   JSON_VERSION_KEY: VERSION
                  }

    # Prepare the answer to send
    answer = web.json_response(json_answer)

    return answer


async def verbs_list(request):
    """
    Verb handler that gives the list of verbs in this API.

    :param request: A request used for receiving request’s information by web \
    handler
    :type request: aiohttp.web.Request
    :returns:  aiohttp.web.Response -- Response class used to send HTTP \
    response by aiohttp
    """

    # Set the json answer
    json_answer = {}

    # Add an empty list in the json dictionnary
    json_answer[JSON_VERBS_LIST_KEY] = []
    # Get all the verbs allowed in this API
    verbs_list = available_verbs

    # Add all the events to the dict object
    for verb in verbs_list:
        json_answer[JSON_VERBS_LIST_KEY].append({JSON_VERB_KEY: verb})

    # Prepare the answer to send
    answer = web.json_response(json_answer)

    return answer

async def hello_handler(request):
    """
    Verb handler that says hello to the client

    :param request: A request used for receiving request’s information by web \
    handler
    :type request: aiohttp.web.Request
    :returns:  aiohttp.web.Response -- Response class used to send HTTP \
    response by aiohttp
    """

    # Set the json answer with the right version
    json_answer = {
                   JSON_MSG_KEY: HELLO_MSG
                  }

    # Prepare the answer to send
    answer = web.json_response(json_answer)

    return answer

async def goodbye_handler(request):
    """
    Verb handler that says goodbye to the client

    :param request: A request used for receiving request’s information by web \
    handler
    :type request: aiohttp.web.Request
    :returns:  aiohttp.web.Response -- Response class used to send HTTP \
    response by aiohttp
    """

    # Set the json answer with the right version
    json_answer = {
                   JSON_MSG_KEY: GOODBYE_MSG
                  }

    # Prepare the answer to send
    answer = web.json_response(json_answer)

    return answer

def main_init_app():
    """
    Main Initialization function called to prepare the API.
    It initializes all the modules used (for verbs, and other \
    management), it sets the routes of the API and it starts the background \
    task.

    :returns:  aiohttp.web.Application -- The application to run with \
    web.run_app
    """

    global available_verbs

    # Create asynchrone application instance (aiohttp)
    app = web.Application()

    # Create the application mapping
    app.add_routes([
                    web.get("/help", verbs_list),
                    web.get("/version", version),
                    web.get(("/api/" + VERSION + "/verbs/list"), verbs_list),
                    web.post(("/api/" + VERSION + "/hello"), hello_handler),
                    web.post(("/api/" + VERSION + "/goodbye"), goodbye_handler),
                    ])

    # Set the available verbs
    available_verbs = [
                        ("/help"),
                        ("/version"),
                        ("/api/" + VERSION + "/verbs/list"),
                        ("/api/" + VERSION + "/hello"),
                        ("/api/" + VERSION + "/goodbye")
                      ]

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: asyncio.ensure_future(stop_handler1()))

    return app


async def stop_RTest_hello_API():
    """
    Coroutine called to stop cleanly the API.
    It ends the background task, the timer used for the cookies manager \
    and all the tasks needed to be stopped properly.
    """
    # Stop the other tasks badly managed elsewhere
    # Get all the tasks running (according to python version)
    if sys.version_info >= (3, 7):
        all_tasks = asyncio.all_tasks()
    else:
        all_tasks = asyncio.Task.all_tasks()

    for task in all_tasks:
        # Get the name of each coroutine
        coroname = task._coro.__name__
        # Check if it is a task to stop
        if(coroname in tasks_coro_to_handle):
            task.cancel()


async def stop_handler1():
    """
    This code comes from https://github.com/aio-libs/aiohttp/issues/3593
    on_cleanup / on_shutdown are called after active tasks on the event
    loop are canceled

    This function runs asynchronously. While this code
    runs, asyncio is running as if SIGTERM/SIGINT were
    never caught
    """
    await stop_RTest_hello_API()

    # Now send TERM to asyncio and handle it in stop_handler2
    loop = asyncio.get_event_loop()
    loop.remove_signal_handler(signal.SIGINT)
    sig = signal.SIGTERM
    loop.remove_signal_handler(sig)
    loop.add_signal_handler(sig, stop_handler2)
    os.kill(os.getpid(), sig)


def stop_handler2():
    # This function must run synchronously
    loop = asyncio.get_event_loop()
    loop.remove_signal_handler(signal.SIGTERM)
    raise web.GracefulExit()
