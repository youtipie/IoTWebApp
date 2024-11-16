import unittest
import asyncio
import json
import os
import random
from unittest.mock import AsyncMock, patch, MagicMock, Mock
from aiocoap import Message, Code
from IoTEmulator import DeviceEmulator, ConfigType


class TestDeviceEmulatorBase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.config = ConfigType(
            name="name",
            description="desc",
            parameters={
                "temperature": {"type": "range", "min": 10, "max": 30, "default": 20},
                "is_on": {"type": "bool", "default": False}
            },
            readings={}
        )

        port = random.randint(10000, 30000)
        self.datafile_location = "temp_data.json"
        self.emulator = DeviceEmulator(ip="127.0.0.1", port=port, datafile_location=self.datafile_location,
                                       config=self.config)
        self.uri = "coap://127.0.0.1:9999"
        self.server_task = asyncio.create_task(self.emulator.run())
        await asyncio.sleep(1)

    async def asyncTearDown(self):
        self.server_task.cancel()
        try:
            await self.server_task
        except asyncio.CancelledError:
            pass
        if os.path.exists(self.datafile_location):
            os.remove(self.datafile_location)

        await asyncio.sleep(0.1)


class TestDeviceEmulator(TestDeviceEmulatorBase):
    async def test_resume_observations(self):
        self.emulator.observed_publishers.append({"ip": "127.0.0.1", "port": 10000})
        with patch.object(self.emulator, "observe_device_state", new=AsyncMock()):
            await self.emulator.resume_observations()
            self.assertEqual(self.emulator.observe_device_state.call_count, len(self.emulator.observed_publishers))

    async def test_resume_observations_with_failure(self):
        self.emulator.observed_publishers.append({"ip": "127.0.0.1", "port": 9999})

        with patch.object(self.emulator, "observe_device_state", side_effect=Exception("Unreachable")):
            await self.emulator.resume_observations()
            self.assertEqual(self.emulator.observe_device_state.call_count, len(self.emulator.observed_publishers))

    async def test_cancel_all_observations(self):
        mock_observation = asyncio.Future()
        mock_observation.set_result(None)
        mock_observation.cancel = Mock()

        self.emulator.observations = {("192.168.0.1", 5684): mock_observation}
        await self.emulator.cancel_all_observations()
        mock_observation.cancel.assert_called_once()
        self.assertEqual(self.emulator.observations, {})

    async def test_cancel_observation_for_specific_device(self):
        mock_observation = asyncio.Future()
        mock_observation.set_result(None)
        mock_observation.cancel = Mock()

        self.emulator.observations = {
            ("192.168.0.1", 5684): mock_observation,
            ("127.0.0.1", 10000): mock_observation
        }

        await self.emulator.cancel_observation(("192.168.0.1", 5684))

        mock_observation.cancel.assert_called_once()
        self.assertNotIn(("192.168.0.1", 5684), self.emulator.observations)
        self.assertIn(("127.0.0.1", 10000), self.emulator.observations)

    async def test_validate_state_update_invalid_type(self):
        invalid_value = "not_an_integer"
        message = self.emulator.validate_state_update("temperature", invalid_value)
        self.assertEqual(
            message,
            "Invalid type: expected 'range', got 'str'",
            "Expected type mismatch message when passing incorrect type for 'temperature'"
        )

    async def test_validate_state_update_out_of_range(self):
        out_of_range_value = 150
        message = self.emulator.validate_state_update("temperature", out_of_range_value)
        self.assertIn(
            "'temperature' have to be in range",
            message,
            "Expected out of range message when passing too high of a value for 'temperature'"
        )

    async def test_generate_state_with_default_values(self):
        generated_state = self.emulator.generate_state()
        self.assertEqual(generated_state["temperature"], 20, "Default value for temperature should be 20")

    @patch("aiocoap.Context.create_client_context")
    async def test_observe_device_state_success(self, mock_create_context):
        mock_context = MagicMock()
        mock_create_context.return_value = mock_context

        response1 = Message(
            payload=json.dumps({"success": True, "state": {"temperature": 23, "humidity": 50}}).encode("utf-8"))
        response2 = Message(
            payload=json.dumps({"success": True, "state": {"temperature": 24, "humidity": 55}}).encode("utf-8"))

        async def mock_observation_stream():
            yield response1
            yield response2

        mock_pr = MagicMock()
        mock_pr.observation = mock_observation_stream()
        mock_context.request.return_value = mock_pr
        await self.emulator.observe_device_state("127.0.0.1", 5683)

        self.assertIn(("127.0.0.1", 5683), self.emulator.publisher_states)
        self.assertEqual(self.emulator.publisher_states[("127.0.0.1", 5683)]["temperature"], 24)
        self.assertEqual(self.emulator.publisher_states[("127.0.0.1", 5683)]["humidity"], 55)

    async def test_observe_device_state_failure(self):
        await self.emulator.observe_device_state("127.0.0.1", 5683)

        self.assertNotIn(("127.0.0.1", 5683), self.emulator.publisher_states)


class TestDeviceEmulatorWhoAmIResource(TestDeviceEmulatorBase):
    async def test_whoami(self):
        whoami_resource = self.emulator.WhoAmI(self.emulator)
        request = Message(code=Code.GET)
        request.remote = Mock(uri_base_local="temp_uri")

        response = await whoami_resource.render_get(request)
        self.assertIsNotNone(response.payload)
        payload = json.loads(response.payload)
        self.assertEqual(payload, self.emulator.config)


class TestDeviceEmulatorStateResource(TestDeviceEmulatorBase):

    async def test_state_get(self):
        state_resource = self.emulator.State(self.emulator)
        request = Message(code=Code.GET)
        request.remote = Mock(uri_base_local="temp_uri")

        response = await state_resource.render_get(request)
        self.assertIsNotNone(response.payload)
        payload = json.loads(response.payload)
        self.assertTrue(payload["success"])
        self.assertIsInstance(payload["state"], dict)
        self.assertEqual(("temperature", "is_on"), tuple(payload["state"].keys()))
        self.assertIsInstance(payload["state"]["temperature"], (float, int))
        self.assertIsInstance(payload["state"]["is_on"], bool)

    async def test_state_put_valid_range(self):
        state_resource = self.emulator.State(self.emulator)
        request_data = {"name": "temperature", "value": 25}
        request = Message(code=Code.PUT, payload=json.dumps(request_data).encode("utf-8"))
        request.remote = Mock(uri_base_local="temp_uri")

        response = await state_resource.render_put(request)
        self.assertIsNotNone(response.payload)
        payload = json.loads(response.payload)
        self.assertTrue(payload["success"])
        self.assertEqual(self.emulator.state["temperature"], 25)

    async def test_state_put_valid_bool(self):
        new_value = not self.emulator.state["is_on"]
        state_resource = self.emulator.State(self.emulator)
        request_data = {"name": "is_on", "value": new_value}
        request = Message(code=Code.PUT, payload=json.dumps(request_data).encode("utf-8"))
        request.remote = Mock(uri_base_local="temp_uri")

        response = await state_resource.render_put(request)
        self.assertIsNotNone(response.payload)
        payload = json.loads(response.payload)
        self.assertTrue(payload["success"])
        self.assertEqual(self.emulator.state["is_on"], new_value)

    async def test_state_put_invalid_range(self):
        old_value = self.emulator.state["temperature"]
        state_resource = self.emulator.State(self.emulator)
        request_data = {"name": "temperature", "value": 50}
        request = Message(code=Code.PUT, payload=json.dumps(request_data).encode("utf-8"))
        request.remote = Mock(uri_base_local="temp_uri")

        response = await state_resource.render_put(request)
        payload = json.loads(response.payload)
        self.assertFalse(payload["success"])
        self.assertIn("have to be in range", payload["message"])
        self.assertEqual(self.emulator.state["temperature"], old_value)

    async def test_state_put_invalid_bool(self):
        old_value = self.emulator.state["is_on"]
        state_resource = self.emulator.State(self.emulator)
        request_data = {"name": "is_on", "value": 1}
        request = Message(code=Code.PUT, payload=json.dumps(request_data).encode("utf-8"))
        request.remote = Mock(uri_base_local="temp_uri")

        response = await state_resource.render_put(request)
        payload = json.loads(response.payload)
        self.assertFalse(payload["success"])
        self.assertIn("Invalid type: expected 'bool', got", payload["message"])
        self.assertEqual(self.emulator.state["is_on"], old_value)


class TestDeviceEmulatorSubscribeResource(TestDeviceEmulatorBase):
    @patch("IoTEmulator.CoAPClient.get")
    async def test_subscribe_post_valid(self, mock_get):
        state_response = {"success": True, "state": {"temperature": 25, "humidity": 60}}
        whoami_response = {
            "parameters": {
                "temperature": {"type": "range", "min": 0, "max": 100, "default": 20}
            },
            "readings": {
                "humidity": {"type": "range", "min": 0, "max": 100, "default": 50}
            }
        }

        async def mock_get_side_effect(endpoint=""):
            if endpoint == "/state":
                return state_response
            elif endpoint == "/whoami":
                return whoami_response

        mock_get.side_effect = mock_get_side_effect

        control_config = {
            "match": "all",
            "instructions": [
                {"device": ["127.0.0.1", 5683], "name": "temperature", "operator": ">", "value": 15}
            ],
            "actions": [
                {"name": "temperature", "value": 20}
            ]
        }

        request = Message(payload=json.dumps(control_config).encode("utf-8"))
        request.remote = Mock(uri_base_local="temp_uri")

        result = await self.emulator.Subscribe(self.emulator).render_post(request)
        result_payload = json.loads(result.payload.decode("utf-8"))

        self.assertTrue(result_payload["success"], "Subscription should succeed with valid data.")
        self.assertIn("subscription_id", result_payload, "Result should include a subscription ID.")

        self.assertEqual(mock_get.call_count, 2)
        mock_get.assert_any_call("/state")
        mock_get.assert_any_call("/whoami")

    @patch("IoTEmulator.CoAPClient.get")
    async def test_subscribe_post_invalid_data(self, mock_get):
        state_response = {"success": True, "state": {"temperature": 25, "humidity": 60}}
        whoami_response = {
            "parameters": {
                "temperature": {"type": "range", "min": 0, "max": 100, "default": 20}
            },
            "readings": {
                "humidity": {"type": "range", "min": 0, "max": 100, "default": 50}
            }
        }

        async def mock_get_side_effect(endpoint=""):
            if endpoint == "/state":
                return state_response
            elif endpoint == "/whoami":
                return whoami_response

        mock_get.side_effect = mock_get_side_effect

        invalid_control_config = {
            "match": "all",
            "instructions": [
                {"device": ["127.0.0.1", 5683], "name": "temperature", "operator": "%", "value": 15}
            ],
            "actions": [
                {"name": "temperature", "value": 20}
            ]
        }

        request = Mock(payload=json.dumps(invalid_control_config).encode("utf-8"))
        request.remote = Mock(uri_base_local="temp_uri")

        result = await self.emulator.Subscribe(self.emulator).render_post(request)
        result_payload = json.loads(result.payload.decode("utf-8"))

        self.assertFalse(result_payload["success"], "Subscription should fail with invalid operator.")
        self.assertIn("Invalid operator", result_payload["message"], "Error message should indicate invalid operator.")

        self.assertEqual(mock_get.call_count, 2)
        mock_get.assert_any_call("/state")
        mock_get.assert_any_call("/whoami")

    @patch("IoTEmulator.CoAPClient.get")
    async def test_subscribe_post_invalid_value(self, mock_get):
        state_response = {"success": True, "state": {"temperature": 25, "humidity": 60}}
        whoami_response = {
            "parameters": {
                "temperature": {"type": "range", "min": 0, "max": 100, "default": 20}
            },
            "readings": {
                "humidity": {"type": "range", "min": 0, "max": 100, "default": 50}
            }
        }

        async def mock_get_side_effect(endpoint=""):
            # Not going to be called
            pass

        mock_get.side_effect = mock_get_side_effect

        invalid_control_config = {
            "match": "all",
            "instructions": [
                {"device": ["127.0.0.1", 5683], "name": "temperature", "operator": ">", "value": 150}
            ],
            "actions": [
                {"name": "temperature", "value": 150}
            ]
        }

        request = Mock(payload=json.dumps(invalid_control_config).encode("utf-8"))
        request.remote = Mock(uri_base_local="temp_uri")

        result = await self.emulator.Subscribe(self.emulator).render_post(request)
        result_payload = json.loads(result.payload.decode("utf-8"))

        self.assertFalse(result_payload["success"], "Subscription should fail with invalid value.")
        self.assertIn("have to be in range", result_payload["message"], "Error message should indicate invalid value.")

        self.assertEqual(mock_get.call_count, 0)

    @patch("IoTEmulator.CoAPClient.get")
    async def test_subscribe_post_invalid_parameter(self, mock_get):
        state_response = {"success": True, "state": {"temperature": 25, "humidity": 60}}
        whoami_response = {
            "parameters": {
                "temperature": {"type": "range", "min": 0, "max": 100, "default": 20}
            },
            "readings": {
                "humidity": {"type": "range", "min": 0, "max": 100, "default": 50}
            }
        }

        async def mock_get_side_effect(endpoint=""):
            # Not going to be called
            pass

        mock_get.side_effect = mock_get_side_effect

        invalid_control_config = {
            "match": "all",
            "instructions": [
                {"device": ["127.0.0.1", 5683], "name": "nonexistent_param", "operator": ">", "value": 15}
            ],
            "actions": [
                {"name": "nonexistent_param", "value": 20}
            ]
        }

        request = Mock(payload=json.dumps(invalid_control_config).encode("utf-8"))
        request.remote = Mock(uri_base_local="temp_uri")

        result = await self.emulator.Subscribe(self.emulator).render_post(request)
        result_payload = json.loads(result.payload.decode("utf-8"))

        self.assertFalse(result_payload["success"], "Subscription should fail with nonexistent parameter.")
        self.assertIn("Parameter 'nonexistent_param' cannot be modified or doesn't exist", result_payload["message"],
                      "Error message should indicate invalid parameter.")

        self.assertEqual(mock_get.call_count, 0)

    @patch("IoTEmulator.CoAPClient.get")
    async def test_subscribe_post_device_off(self, mock_get):
        async def mock_get_side_effect(endpoint=""):
            if endpoint == "/state":
                return {"success": False, "message": "Device is unreachable"}

        mock_get.side_effect = mock_get_side_effect

        control_config = {
            "match": "all",
            "instructions": [
                {"device": ["127.0.0.1", 5683], "name": "temperature", "operator": ">", "value": 15}
            ],
            "actions": [
                {"name": "temperature", "value": 20}
            ]
        }

        request = Mock(payload=json.dumps(control_config).encode("utf-8"))
        request.remote = Mock(uri_base_local="temp_uri")

        result = await self.emulator.Subscribe(self.emulator).render_post(request)
        result_payload = json.loads(result.payload.decode("utf-8"))

        self.assertFalse(result_payload["success"], "Subscription should fail when the device is off.")
        self.assertIn("One of the devices is inaccessible", result_payload["message"],
                      "Error message should indicate the device is off.")

        self.assertEqual(mock_get.call_count, 1)
        mock_get.assert_any_call("/state")

    async def test_subscribe_delete(self):
        subscribe_resource = self.emulator.Subscribe(self.emulator)
        subscription_id = "test_subscription_id"
        self.emulator.instructions.append({"id": subscription_id})

        request = Message(code=Code.DELETE, payload=json.dumps(subscription_id).encode("utf-8"))
        request.remote = Mock(uri_base_local="temp_uri")

        response = await subscribe_resource.render_delete(request)
        payload = json.loads(response.payload)
        self.assertTrue(payload["success"])
        self.assertEqual(payload["message"], f"Subscription successfully canceled: {subscription_id}")
        self.assertTrue(all(sub["id"] != subscription_id for sub in self.emulator.instructions))

    async def test_subscribe_with_empty_actions(self):
        control_config = {
            "match": "all",
            "instructions": [
                {"device": ["127.0.0.1", 5683], "name": "temperature", "operator": ">", "value": 15}
            ],
            "actions": []
        }

        request = Mock(payload=json.dumps(control_config).encode("utf-8"))
        request.remote = Mock(uri_base_local="temp_uri")

        result = await self.emulator.Subscribe(self.emulator).render_post(request)
        result_payload = json.loads(result.payload.decode("utf-8"))

        self.assertFalse(result_payload["success"], "Subscription should fail with empty actions.")
        self.assertIn("No actions received!", result_payload["message"])


if __name__ == "__main__":
    unittest.main()
