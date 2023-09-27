import json
import azure.functions as func
import logging

dapp = func.DaprFunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@dapp.function_name(name="InvokeOutputBinding")
@dapp.route(route="invoke/{appId}/{methodName}", auth_level=dapp.auth_level.ANONYMOUS)
@dapp.dapr_invoke_output(arg_name = "payload", app_id = "{appId}", method_name = "{methodName}", http_verb = "post")
def main(req: func.HttpRequest, payload: func.Out[str] ) -> str:
    """
    Sample to use a Dapr Invoke Output Binding to perform a Dapr Server Invocation operation hosted in another Darp'd app.
    Here this function acts like a proxy
    Invoke Dapr Service invocation trigger using Windows PowerShell with below request

    Invoke-RestMethod -Uri 'http://localhost:7071/api/invoke/functionapp/DaprServiceInvocationTriggerPython' -Method POST -Headers @{
    'Content-Type' = 'application/json'
     } -Body '{
     "data": {
          "value": {
               "orderId": "122"
               }
          }
     }'
    """
    logging.info('Python HTTP trigger function processed a request..')
    logging.info(req.params)
    data = req.params.get('data')
    if not data:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            data = req_body.get('data')

    if data:
        logging.info(f"Url: {req.url}, Data: {data}")
        payload.set(json.dumps({"body": data}).encode('utf-8'))
        return 'Successfully performed service invocation using Dapr invoke output binding.'
    else:
        return func.HttpResponse(
            "Please pass a data on the query string or in the request body",
            status_code=400
        )