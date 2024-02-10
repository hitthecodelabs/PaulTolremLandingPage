import json
import requests

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

def candlestick_chart(request):
    return render(request, 'charts/candlestick_chart.html')

def get_chart_data0(request):
    apiUrl = "https://fapi.binance.com/fapi/v1/klines"
    symbol = request.GET.get('symbol', 'BTCUSDT')  # Default to BTCUSDT if no symbol is provided
    interval = request.GET.get('interval', '1m')  # Default to 1m if no interval is provided
    limit = 72
    fullUrl = f"{apiUrl}?symbol={symbol}&interval={interval}&limit={limit}"

    response = requests.get(fullUrl)

    if response.status_code == 200:
        try:
            data = response.json()
            return JsonResponse(data, safe=False)
        except ValueError as e:
            return JsonResponse({'error': 'Unable to parse response data'}, status=500)
    else:
        return JsonResponse({'error': 'Could not fetch data from Binance API'}, status=500)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])

@login_required
@api_view(['GET'])
def get_chart_data(request, symbol='BTCUSDT', interval='1m', timestamp='', location=''):

    ### http://127.0.0.1:8880/api/get_chart_data/BTCUSDT/1m/1688247304673/com/
    url = f"http://paultolrem.com/api/get_chart_data2/{symbol}/{interval}/{timestamp}/{location}/"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            combined_data = data
            return JsonResponse(combined_data, safe=False)
        except ValueError as e:
            return JsonResponse({'error': 'Unable to parse response data'}, status=500)
    else:
        return JsonResponse({'error': 'Could not fetch data from Binance API'}, status=500)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])

@login_required
@api_view(['GET'])
def get_xtimes_preds(request, coin_type, interval):

    # if not request.is_ajax():
    #     return JsonResponse({"error": "Access Denied"}, status=403)

    apiUrl = "https://www.paultolrem.com/api/futures_predictions/" 
    # symbol = request.GET.get('symbol', 'BTCUSDT').lower().replace("usdt", "")
    limit = 72
    fullUrl = f"{apiUrl}{coin_type}/{interval}/"

    response = requests.get(fullUrl)

    if response.status_code == 200:
        try: 
            data = response.json()
            return JsonResponse(data, safe=False)
        except ValueError as e:
            return JsonResponse({'error': 'Unable to parse response data'}, status=500)
    else:
        return JsonResponse({'error': 'Could not fetch data from Binance API'}, status=500)

def get_timezone_offset(request):
    # First, get the client's public IP address
    ip_address = requests.get('https://api.ipify.org?format=json').json()['ip']

    # Then, pass that IP address to ipapi.co
    response = requests.get(f"https://ipapi.co/{ip_address}/json")

    if response.status_code == 200:
        data = response.json()

        # Convert the utc_offset string to milliseconds
        def offset_string_to_milliseconds(offset):
            sign = -1 if offset[0] == '-' else 1
            hours = int(offset[1:3])
            minutes = int(offset[3:5])
            return sign * ((hours * 60 + minutes) * 60 * 1000)

        timezone_offset = offset_string_to_milliseconds(data['utc_offset'])
        return JsonResponse({'timezoneOffset': timezone_offset}, safe=False)
    else:
        return JsonResponse({'error': 'Could not fetch data from ipapi.co'}, status=500)
