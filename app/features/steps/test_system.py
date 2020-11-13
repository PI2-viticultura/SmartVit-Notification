from behave import given, when, then
import requests

request_headers = {}
request_bodies = {}
response_codes = {}
api_url = None


@given('a conexao com o sistema da notificao')
def step_impl_given(context):
    global api_url
    api_url = 'https://smartvit-notification-stg.herokuapp.com/notification'
    print('url :'+api_url)


@when('o sistema seja ativado')
def step_impl_when(context):
    request_bodies['POST'] = {"type": "water",
                              "title": "Sistema de Irrigação",
                              "winery": "5fad331b38b2670687db57e2",
                              "message": "Sistema de Irrigação Ativado"}
    response = requests.post(
                            api_url,
                            json=request_bodies['POST']
                            )
    statuscode = response.status_code
    response_codes['POST'] = statuscode


@then('o alerta seja enviado')
def step_impl_then(context):
    print('Post rep code ;'+str(response_codes['POST']))
    assert response_codes['POST'] != 200
