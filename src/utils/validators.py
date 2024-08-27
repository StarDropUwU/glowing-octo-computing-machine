def validate_operation_data(data):
    print(data)
    if not isinstance(data.get('tipo_operacao'), str) or not isinstance(data.get('valor'), (int, float)):
        return False
    return True
