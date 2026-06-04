# Telegram — Banco Nexus

## Bot Oficial do Banco Nexus

O Bot Telegram do Banco Nexus (@NexusBancoBot) é um canal oficial de suporte e notificações. Ele permite que o cliente realize consultas, receba alertas em tempo real e solicite serviços sem precisar acessar o aplicativo.

Para ativar, acesse o Telegram, pesquise por @NexusBancoBot e envie `/start`. Será solicitada autenticação via código enviado ao celular cadastrado na conta.

## Comandos Disponíveis

| Comando                    | Descrição                                                      |
|----------------------------|----------------------------------------------------------------|
| `/start`                   | Inicia o bot e autentica o cliente                             |
| `/saldo`                   | Exibe o saldo atual da conta                                   |
| `/extrato [dias]`          | Exibe as últimas transações (padrão: 7 dias, máximo: 90 dias)  |
| `/pagamento [id]`          | Consulta o status de um pagamento pelo ID                      |
| `/reembolso [id]`          | Abre solicitação de reembolso para uma transação               |
| `/bloquear_cartao`         | Bloqueia temporariamente o cartão (crédito ou débito)          |
| `/desbloquear_cartao`      | Desbloqueia o cartão previamente bloqueado                     |
| `/limite_pix [valor]`      | Ajusta o limite diário de PIX                                  |
| `/alertas`                 | Gerencia as notificações ativas                                |
| `/ajuda`                   | Exibe a lista completa de comandos                             |
| `/suporte`                 | Encaminha para atendimento humano                              |

## Tipos de Notificação

O bot pode enviar alertas automáticos para os seguintes eventos:

- **Pagamento recebido**: notificação imediata ao receber qualquer crédito.
- **Pagamento enviado**: confirmação de débito na conta.
- **Pagamento falhou**: alerta quando uma transação é recusada.
- **Tentativa de fraude**: aviso de transação suspeita bloqueada pelo sistema.
- **Chargeback aberto**: notificação quando uma contestação é registrada.
- **Reembolso aprovado/recusado**: resultado da análise de reembolso.
- **Fatura próxima do vencimento**: lembrete 3 dias antes do vencimento do boleto.
- **Limite de PIX atingido**: aviso quando o limite diário é atingido.

## Ativar e Desativar Alertas

Para gerenciar alertas, envie `/alertas` no bot. O sistema exibirá um menu interativo com todos os tipos de notificação disponíveis e seus status atuais (ativado/desativado). Cada tipo pode ser ativado ou desativado individualmente.

Exemplo de resposta do comando `/alertas`:
```
✅ Pagamento recebido: ATIVO
✅ Pagamento enviado: ATIVO
❌ Fatura próxima: INATIVO
✅ Tentativa de fraude: ATIVO
```

## Segurança do Bot

O bot nunca solicitará senha completa, token de segurança ou dados de cartão. Mensagens solicitando esses dados são golpes. O bot oficial só envia mensagens após um comando do cliente ou em resposta a eventos da conta autenticada. Em caso de suspeita, encerre a sessão com `/sair` e entre em contato com o suporte.

## Limitações do Bot

- O bot não realiza transferências ou pagamentos — apenas consultas e solicitações.
- Sessões expiram automaticamente após 30 minutos de inatividade.
- Máximo de 20 comandos por minuto por conta.
