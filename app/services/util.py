from fastapi import HTTPException, status


def execute(func: callable):
    try:
        return func()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
