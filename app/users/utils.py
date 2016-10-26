from app import login_manager
from .repository import UsersRepository


@login_manager.user_loader
def load_user(google_id):
    if google_id is None:
        return None
    return UsersRepository.get_user_by_google_id(str(google_id))
