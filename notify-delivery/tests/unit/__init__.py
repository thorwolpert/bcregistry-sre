# Copyright © 2023 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""The Unit Tests and the helper routines."""
import base64
import json
from random import randrange
from unittest.mock import Mock

from simple_cloudevent import SimpleCloudEvent, to_queue_message

from tests import EPOCH_DATETIME

LEGAL_NAME = "test business"


class Obj:
    """Make a custom object hook used by dict_to_obj."""

    def __init__(self, dict1):
        """Create instance of obj."""
        self.__dict__.update(dict1)


def dict_to_obj(dict1):
    """Convert dict to an object."""
    return json.loads(json.dumps(dict1), object_hook=Obj)


def create_mock_message(message_payload: dict):
    """Return a mock message that can be processed by the queue listener."""
    mock_msg = Mock()
    mock_msg.sequence = randrange(1000)
    mock_msg.data = dict_to_obj(message_payload)
    json_msg_payload = json.dumps(message_payload)
    mock_msg.data.decode = Mock(return_value=json_msg_payload)
    return mock_msg


def helper_create_cloud_event_envelope(
    cloud_event_id: str = None,
    source: str = "fake-for-tests",
    subject: str = "fake-subject",
    type: str = "fake-message-type",
    data: dict = {},
    pubsub_project_id: str = "PUBSUB_PROJECT_ID",
    subscription_id: str = "SUBSCRIPTION_ID",
    message_id: int = 1,
    envelope_id: int = 1,
    attributes: dict = {},
    ce: SimpleCloudEvent = None,
):
    """Create cloud Event envelope helper."""
    if not data:
        data = {
            "email": {
                "type": "bn",
            }
        }
    if not ce:
        ce = SimpleCloudEvent(id=cloud_event_id, source=source, subject=subject, type=type, data=data)
    #
    # This needs to mimic the envelope created by GCP PubSb when call a resource
    #
    envelope = {
        "subscription": f"projects/{pubsub_project_id}/subscriptions/{subscription_id}",
        "message": {
            "data": base64.b64encode(to_queue_message(ce)).decode("UTF-8"),
            "messageId": str(message_id),
            "attributes": attributes,
        },
        "id": envelope_id,
    }
    return envelope


def helper_create_cloud_event(
    cloud_event_id: str = None,
    source: str = "fake-for-tests",
    subject: str = "fake-subject",
    type: str = "fake-type",
    data: dict = {},
):
    """Create cloud Event helper."""
    if not data:
        data = {"notificationId": "29590"}
    ce = SimpleCloudEvent(id=cloud_event_id, source=source, subject=subject, type=type, data=data)
    return ce
