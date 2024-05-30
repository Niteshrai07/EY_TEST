from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .serializers import PayloadModel
import json
from multiprocessing import Pool
import logging
from datetime import datetime

logger = logging.getLogger('django')

def add_lists(input_lists):
    return [sum(lst) for lst in input_lists]

def validate_and_process_request(request):
    try:
        data = json.loads(request.body)
        payload = PayloadModel(**data)
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return JsonResponse({'error': str(e)}, status=400)

    start_time = datetime.utcnow().isoformat()
    try:
        with Pool() as pool:
            results = pool.map(add_lists, [payload.payload])
        response = results[0]
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    end_time = datetime.utcnow().isoformat()

    return JsonResponse({
        'batchid': payload.batchid,
        'response': response,
        'status': 'complete',
        'started_at': start_time,
        'completed_at': end_time
    })

