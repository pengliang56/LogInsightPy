import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.config.milvus_init import milvus_client as client


@csrf_exempt
def main_json(request):
    if request.method == 'POST':
        try:
            response_data = {
                "message": "Data received successfully",
                "received_data": query_vectory('error')
            }
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)


def query_vectory(request_str):
    client.queryVector(collection_name=client.collection_name, text=request_str, top_k=5)
