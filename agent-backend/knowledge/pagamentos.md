# Pagamentos — Banco Nexus

## Métodos de Pagamento Disponíveis

O Banco Nexus oferece os seguintes métodos de pagamento para pessoas físicas e jurídicas:

- **PIX**: transferência instantânea disponível 24 horas por dia, 7 dias por semana, inclusive feriados.
- **Cartão de Crédito**: pagamentos parcelados em até 12 vezes para compras acima de R$ 50,00.
- **Cartão de Débito**: débito imediato na conta corrente do cliente.
- **Boleto Bancário**: prazo de vencimento de até 3 dias úteis após a emissão.
- **TED (Transferência Eletrônica Disponível)**: disponível em dias úteis, das 6h30 às 17h00.

Cada método possui limites, prazos e taxas específicos descritos nas seções seguintes.

## Status de Pagamentos

Cada pagamento no sistema possui um dos seguintes status:

- **pago**: transação confirmada e liquidada com sucesso.
- **pendente**: aguardando confirmação da instituição financeira ou do cliente.
- **falhou**: transação rejeitada por saldo insuficiente, dados incorretos ou recusa do emissor.
- **reembolsado**: valor devolvido ao cliente após solicitação aprovada.
- **chargeback**: contestação iniciada pelo cliente junto à operadora do cartão.
- **expirado**: boleto ou link de pagamento não pago dentro do prazo de vencimento.

## Prazos de Processamento

Os prazos variam conforme o método utilizado:

| Método           | Prazo de Compensação        |
|------------------|-----------------------------|
| PIX              | Imediato (até 10 segundos)  |
| Cartão de Crédito| 1 a 2 dias úteis            |
| Cartão de Débito | Imediato                    |
| Boleto Bancário  | 1 a 3 dias úteis            |
| TED              | Mesmo dia (se enviado até 17h) |

Pagamentos realizados após o horário de corte ou em dias não úteis são processados no próximo dia útil.

## Erros Comuns em Pagamentos

Os erros mais frequentes e suas causas:

- **Saldo insuficiente**: o cliente não possui saldo disponível para cobrir o valor da transação.
- **Cartão expirado**: a data de validade do cartão ultrapassou a data atual.
- **Dados inválidos**: número de cartão, CVV ou data de validade incorretos.
- **Limite excedido**: o valor da transação ultrapassa o limite diário configurado na conta.
- **Conta bloqueada**: a conta do cliente está suspensa por suspeita de fraude ou inadimplência.
- **Banco recusou**: a instituição emissora do cartão recusou a transação sem motivo específico divulgado.

Em caso de erro, o cliente deve verificar os dados informados e tentar novamente. Se o problema persistir, entrar em contato com o suporte via Telegram ou app.

## Cancelamento de Pagamentos

Pagamentos com status **pendente** podem ser cancelados pelo cliente diretamente pelo aplicativo em até 30 minutos após a criação. Após esse prazo, é necessário solicitar reembolso. Pagamentos com status **pago** não podem ser cancelados — apenas reembolsados.
