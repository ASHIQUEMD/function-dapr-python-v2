import json
import azure.functions as func
import logging

dapp = func.DaprFunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@dapp.function_name(name="CreateOrder")
@dapp.dapr_service_invocation_trigger(arg_name="payload", method_name="CreateOrder")
@dapp.dapr_state_output(arg_name="state", state_store="statestore", key="order")
def main(payload: str, state: func.Out[str] ) :
    """
    See https://aka.ms/azure-functions-dapr for more information about using this binding
    
    These tasks should be completed prior to running :
         1. Install Dapr
         2. Change the bundle name in host.json to "Microsoft.Azure.Functions.ExtensionBundle.Preview" and the version to "[4.*, 5.0.0)"
    Run the app with below steps
         1. Start function app with Dapr: dapr run --app-id functionapp --app-port 3001 --dapr-http-port 3501 -- func host start
         2. Invoke function app by dapr cli: dapr invoke --app-id functionapp --method {yourFunctionName}  --data '{ "data": {"value": { "orderId": "41" } } }'
    """
    logging.info('Azure function triggered by Dapr Service Invocation Trigger.')
    logging.info("Dapr service invocation trigger payload: %s", payload)
    state.set(payload)