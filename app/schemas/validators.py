def validar_texto(
    value: str,
    campo: str,
    min_length: int = 3,
    max_length: int = 100,
) -> str:
    
    value = value.strip()

    if not value:
        raise ValueError(f"{campo} é obrigatório.")

    if len(value) < min_length:
        raise ValueError(
            f"{campo} deve ter no mínimo {min_length} caracteres."
        )

    if len(value) > max_length:
        raise ValueError(
            f"{campo} deve ter no máximo {max_length} caracteres."
        )

    return value