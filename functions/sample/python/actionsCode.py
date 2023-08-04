import sys 
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict): 
    authenticator = IAMAuthenticator("kd1Cl515onirvb1ZB0B1a9mafZ8Ld1z1VyQ7CFYbvgcJ")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://1f70d18e-2c41-41f7-9fe4-c7806acd9a8e-bluemix.cloudantnosqldb.appdomain.cloud")
    
    if ('id' in dict):
        response = service.post_find(
                    db='reviews',
                    selector={'dealership': {'$eq': int(dict['id'])}},
                ).get_result()
        try: 
            # result_by_filter=my_database.get_query_result(selector,raw_result=True) 
            result= {
                'headers': {'Content-Type':'application/json'}, 
                'body': {'data':response} 
                }        
            return result
        except:  
            return { 
                'statusCode': 404, 
                'message': 'Something went wrong'
                }
    elif ('review' in dict):
        response = service.post_document(db='reviews', document=dict["review"]).get_result()
        try:
        # result_by_filter=my_database.get_query_result(selector,raw_result=True)
            result= {
            'headers': {'Content-Type':'application/json'},
            'body': {'data':response}
            }
            return result
        except:
            return {
            'statusCode': 404,
            'message': 'Something went wrong'
            }