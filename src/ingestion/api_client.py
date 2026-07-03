import requests
from src.config import settings

def get_top_anime(page):
    url = f"{settings.BASE_URL}/top/anime?page={page}"
    
    try:
        response = requests.get(
        url,
        timeout=settings.REQUEST_TIMEOUT,
    )
    
    except requests.exceptions.Timeout: #“Se a requisição estourar o tempo limite, capture esse erro aqui.”
        raise TimeoutError("The request timed out. Please try again later.")
    
    except requests.exceptions.RequestException as e: #“Se ocorrer algum outro erro de requisição, capture esse erro aqui.”
        raise Exception(f"Error occurred while fetching API data: {e}")
    
    if response.status_code == 200:
        return response.json()

    elif response.status_code == 404:
        raise Exception("Not found")

    elif response.status_code == 429:
        raise Exception("Rate limit exceeded")

    elif response.status_code >= 500:
        raise Exception("Internal server error")

    else:
        raise Exception(f"Unexpected error: {response.status_code}")

# Testando a função get_top_anime chamando-a com a página 1 e imprimindo o resultado
# print(get_top_anime(1))