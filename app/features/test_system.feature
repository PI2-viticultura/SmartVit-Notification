Feature: Testar se a notificação envia o alerta do sistema de irrigacao ao usuario desejado
  Como Sistema, desejo notificar ao usuario um alerta quando acionado o sistema de irrigacao

  Context: O usuario recebe o alerta

    Scenario: Sistema manda um alerta ao usuario do sistema de irrigacao
        Given a conexao com o sistema da notificao
        When o sistema seja ativado
        Then o alerta seja enviado