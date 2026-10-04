import httpx

class SessionAPI:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8080"
        self.session_list_api = "/api/v1/sessions"
        self.send_task_api = lambda a_id: f"/api/v1/agents/{a_id}/task"

    async def get(self, api: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url + api)
            return response.json()

    async def post(self, api: str, data: dict):
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url + api, json=data)
            return response.json()

    async def get_session_list(self):
        return await self.get(self.session_list_api)