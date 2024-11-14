import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import os


@csrf_exempt
def search_ai(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            completion = client.chat.completions.create(
                model="qwen-plus",
                messages=[
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': json.loads(data).get('search_params_v1')}],
            )

            response_data = {
                "message": "Data received successfully",
                "received_data": completion.model_dump_json()
            }
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
