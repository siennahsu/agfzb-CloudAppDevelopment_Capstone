import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    api_key = kwargs.get("api_key")
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            requests.get(url, params=params, headers={'Content-Type': 'application/json'}, \
                         auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, \
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the body list in JSON as dealers
        # dealers = json_result["body"]
        dealers = json_result

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(id=dealer_doc["id"], city=dealer_doc["city"], \
                                   state=dealer_doc["state"], st=dealer_doc["st"], \
                                   address=dealer_doc["address"], zip=dealer_doc["zip"], \
                                   lat=dealer_doc["lat"], long=dealer_doc["long"], \
                                   short_name=dealer_doc["short_name"], \
                                   full_name=dealer_doc["full_name"])
            results.append(dealer_obj)
    return results


def get_dealer_by_id(url, dealerId):
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerId)
    if json_result:
        # Get the body list in JSON as dealers
        # dealers = json_result["body"]
        dealer_doc = json_result[0]

        dealer_obj = CarDealer(id=dealer_doc["id"], city=dealer_doc["city"], \
                               state=dealer_doc["state"], st=dealer_doc["st"], \
                               address=dealer_doc["address"], zip=dealer_doc["zip"], \
                               lat=dealer_doc["lat"], long=dealer_doc["long"], \
                               short_name=dealer_doc["short_name"], \
                               full_name=dealer_doc["full_name"])

        return dealer_obj


def get_dealers_by_state(url, st):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, st=st)
    if json_result:
        # Get the body list in JSON as dealers
        # dealers = json_result["body"]
        dealers = json_result

        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(id=dealer_doc["id"], city=dealer_doc["city"], \
                                   state=dealer_doc["state"], st=dealer_doc["st"], \
                                   address=dealer_doc["address"], zip=dealer_doc["zip"], \
                                   lat=dealer_doc["lat"], long=dealer_doc["long"], \
                                   short_name=dealer_doc["short_name"], \
                                   full_name=dealer_doc["full_name"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealers_reviews_from_cf(url, id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)
    if json_result:
        reviews = json_result["data"]["docs"]

        # For each review object
        for review in reviews:
            # Create a CarDealer object with values in `doc` object
            review_text = review["review"]
            sentiment = analyze_review_sentiments(review_text)
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], \
                                      purchase=review["purchase"], review=review["review"], \
                                      purchase_date=review["purchase_date"], car_make=review["car_make"], \
                                      car_model=review["car_model"], car_year=review["car_year"], \
                                      id=review["id"], sentiment=sentiment)
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.jp-tok.natural-language-understanding.watson.cloud.ibm.com/instances/9c515d37-0215-4d33-a3cb-5f4c21b0801a"
    api_key = "PSG3a41O5lk4MegebNmqjFw7fbeCGEkZqQWXBboaQKTC"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(text=text+"hello hello hello", features=Features(
        sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']

    return (label)
