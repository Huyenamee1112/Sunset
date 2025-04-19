from django.http import JsonResponse

def chart_data(request):
    data = {
        "visitor": {
            "categories": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "series": [
                {
                    "name": "Page Views",
                    "data": [31, 40, 28, 51, 42, 109, 101]
                },
                {
                    "name": "Sessions",
                    "data": [11, 32, 45, 32, 34, 52, 41]
                }
            ]   
        },
        "income": {
            "categories": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", 'Sun'],
            "series": [
                {
                    "data": [80, 95, 70, 42, 65, 55, 78]
                }
            ]
        }
    }
    return JsonResponse(data)