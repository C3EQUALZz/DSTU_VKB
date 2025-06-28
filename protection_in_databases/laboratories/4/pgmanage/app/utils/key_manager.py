from pgmanage import settings


class KeyManager:

    __users = dict()

    def get(self, current_user):
        user = self.__users.get(current_user.id, None)
        if user is not None:
            return user.get("key", None)
        return None

    def set(self, current_user, _key):
        user = self.__users.get(current_user.id, None)
        if user is None:
            self.__users[current_user.id] = dict(key=_key)
        else:
            user["key"] = _key

    def remove(self, current_user):
        user = self.__users.get(current_user.id, None)
        if user is not None:
            del self.__users[current_user.id]


key_manager = KeyManager()

if settings.DEBUG:
    import os
    from django.contrib.auth import get_user_model

    user_keys_env = os.getenv("PGMANAGE_USER_KEYS")
    if user_keys_env:
        for user_key_pair in user_keys_env.split("|"):
            username, user_key = user_key_pair.split(":")
            user = get_user_model().objects.filter(username=username).first()
            if user:
                key_manager.set(user, user_key)
