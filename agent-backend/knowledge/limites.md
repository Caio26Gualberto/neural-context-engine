# Limites de Transações — Banco Nexus

## Estrutura de Tiers de Conta

O Banco Nexus organiza seus clientes em três tiers, cada um com limites diferenciados de acordo com o nível de verificação e perfil de uso:

- **Básico**: clientes com CPF validado e selfie aprovada.
- **Premium**: clientes com comprovante de renda e residência verificados.
- **Empresarial**: pessoas jurídicas com CNPJ e documentação societária aprovados.

## Limites de PIX

| Tipo de Limite       | Básico          | Premium          | Empresarial       |
|----------------------|-----------------|------------------|-------------------|
| Diário (diurno)      | R$ 5.000,00     | R$ 20.000,00     | R$ 100.000,00     |
| Por transação noturno| R$ 1.000,00     | R$ 5.000,00      | R$ 20.000,00      |
| Mensal               | R$ 50.000,00    | R$ 200.000,00    | R$ 1.000.000,00   |
| Máximo por chave/dia | R$ 2.500,00     | R$ 10.000,00     | R$ 50.000,00      |

Horário noturno: das 20h00 às 06h00.

## Limites de TED e DOC

| Tipo de Limite       | Básico          | Premium          | Empresarial       |
|----------------------|-----------------|------------------|-------------------|
| Por transação        | R$ 10.000,00    | R$ 50.000,00     | R$ 500.000,00     |
| Diário               | R$ 20.000,00    | R$ 100.000,00    | R$ 1.000.000,00   |

TED disponível em dias úteis das 06h30 às 17h00. Solicitações após este horário são agendadas para o próximo dia útil.

## Limites de Cartão de Crédito

Limites de cartão de crédito são individuais por cliente, definidos na análise de crédito. Veja detalhes completos em `cartao.md`.

- Limite de compra por transação: até 100% do limite disponível.
- Limite de saque no crédito: até 30% do limite total (sujeito a taxas adicionais).
- Parcelamento máximo: 12 vezes.

## Limites de Cartão de Débito

| Tipo de Operação     | Básico          | Premium          | Empresarial       |
|----------------------|-----------------|------------------|-------------------|
| Compra presencial/dia| R$ 5.000,00     | R$ 20.000,00     | R$ 50.000,00      |
| Compra online/dia    | R$ 3.000,00     | R$ 15.000,00     | R$ 30.000,00      |
| Saque em caixa/dia   | R$ 1.000,00     | R$ 3.000,00      | R$ 5.000,00       |

## Ajuste de Limites pelo Cliente

O cliente pode ajustar seus limites de PIX e débito dentro das faixas permitidas para o seu tier:

- **Aumento de limite**: solicitado pelo app, válido após 24 horas para evitar fraudes.
- **Redução de limite**: efetiva imediatamente.
- **Limite temporário**: o cliente pode aumentar o limite por até 24 horas para uma transação específica, sujeito à aprovação.

Limites acima do máximo do tier exigem upgrade de conta e nova análise de perfil.

## Limites de Boleto Bancário

- Valor mínimo por boleto: R$ 1,00.
- Valor máximo por boleto (Básico): R$ 10.000,00.
- Valor máximo por boleto (Premium): R$ 50.000,00.
- Valor máximo por boleto (Empresarial): sem limite pré-definido, sujeito à análise.
- Máximo de boletos ativos simultâneos: 10 (Básico), 50 (Premium), 200 (Empresarial).
