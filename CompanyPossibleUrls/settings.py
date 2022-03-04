SEARCH_URL = "https://api.cognitive.microsoft.com/bing/v7.0/search"
BING_SECRET_ID = 'arn:aws:secretsmanager:eu-west-3:177285995440:secret:bing_key-LmGR6N'
BING_PARAMS = {
            "count": 20,
            'offsef': 0,
            "cc": "fr-FR",
            "textDecorations": True,
            "textFormat": "HTML"
                      }