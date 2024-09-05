def validate_operation_data(data):
    if not isinstance(data.get('tipo_operacao'), str) or not isinstance(data.get('valor'), (int, float)):
        return False
    return True
"""
Validador de dados para operações financeiras. Verifica se 'tipo_operacao" é uma string e 'valor' é um número.
Caso os dados não sejam válidos, retorna False. Caso contrário, retorna True, dando andamento ao request feito.
"""
