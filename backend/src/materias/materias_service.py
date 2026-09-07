from . import materias_repository as repository

def list_all():
    return repository.find_all()