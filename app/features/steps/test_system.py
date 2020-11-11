from behave import given, when, then
import requests

request_headers = {}
request_bodies = {}
response_codes = {}
api_url = None


@given('a conexao com o sistema da notificao')
def step_impl_given(context):
    global api_url
    api_url = 'https://smartvit-notification-dev.herokuapp.com/notification'
    print('url :'+api_url)


@when('o sistema seja ativado')
def step_impl_when(context):
    request_bodies['POST'] = {"type": "water",
                              "title": "Sistema de Irrigacao Ativo",
                              "winery": "5f87a0efbf0df955915a3ebb",
	                          "message":"Sistema de Irrigacao Ativado"}
    response = requests.post(
                            'https://smartvit-notification-dev.herokuapp.com/notification',
                            json=request_bodies['POST']
                            )
    statuscode = response.status_code
    response_codes['POST'] = statuscode


@then('o alerta seja enviado')
def step_impl_then(context):
    print('Post rep code ;'+str(response_codes['POST']))
    assert response_codes['POST'] == 200
