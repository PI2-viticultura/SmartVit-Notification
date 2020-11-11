Feature: Testar se a notificação envia o alerta ao usuario desejado
  Como Sistema, desejo notificar ao usuario um alerta de clima

  Context: O usuario recebe o alerta

    Scenario: Sistema manda um alerta ao usuario do clima
        Given a conexao com o sistema da notificao do clima
        When a conexao esteja estavel
        Then o alerta seja enviado ao usuario