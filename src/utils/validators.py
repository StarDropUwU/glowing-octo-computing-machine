def validate_operation_data(data):
    """
    Valida os dados de uma operação financeira.

    Verifica se:
    - 'tipo_operacao' está presente e é uma string não vazia.
    - 'valor' está presente e é um número (int ou float) maior que zero.

    :param data: Dicionário contendo os dados da operação.
    :return: True se os dados forem válidos, False caso contrário.
    """
    # Valida o campo 'tipo_operacao' (deve ser uma string não vazia)
    tipo_operacao = data.get('tipo_operacao')
    if not isinstance(tipo_operacao, str) or not tipo_operacao.strip():
        return False

    # Valida o campo 'valor' (deve ser um número e maior que zero)
    valor = data.get('valor')
    if not isinstance(valor, (int, float)) or valor <= 0:
        return False

    return True
