from django.http import JsonResponse
import json

from apps.config.milvus_init import milvus_client as client


def search_json(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response_data = {
                "message": "Data received successfully",
                "received_data": query_vectory(json.loads(data).get('search_params_v1'))
            }
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)


def query_vectory(request_str):
    client.queryVector(collection_name=client.collection_name, text=request_str, top_k=5)
