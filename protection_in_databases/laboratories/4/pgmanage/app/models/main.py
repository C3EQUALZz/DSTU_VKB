import os
import shutil

from app.utils.crypto import decrypt, encrypt
from django.contrib.auth.models import User
from django.db import models, transaction, DatabaseError


class Technology(models.Model):
    name = models.CharField(max_length=50, blank=False)


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=50, blank=False,default='light')
    font_size = models.IntegerField(blank=False,default=12)
    csv_encoding = models.CharField(max_length=50, blank=False, default='utf-8')
    csv_delimiter = models.CharField(max_length=10, blank=False, default=',')
    masterpass_check = models.CharField(max_length=256, default='')
    binary_path = models.CharField(max_length=256, null=True)
    date_format = models.CharField(max_length=200, null=True)
    pigz_path = models.CharField(max_length=256, null=True)
    restore_tabs = models.BooleanField(default=True)
    scroll_tree = models.BooleanField(default=True)

    def get_pigz_path(self):

        if self.pigz_path:
            pigz_path = self.pigz_path
        else:
            pigz_path = (
                os.path.dirname(shutil.which("pigz")) if shutil.which("pigz") else ""
            )
        return pigz_path

    def get_binary_path(self):

        if self.binary_path:
            binary_path = self.binary_path
        else:
            binary_path = (
                os.path.dirname(shutil.which("psql")) if shutil.which("psql") else ""
            )
        return binary_path

    def get_editor_theme(self):
        if self.theme == "light":
            return "omnidb"
        return "omnidb_dark"


class Shortcut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=200)
    os = models.CharField(max_length=200)
    ctrl_pressed = models.BooleanField(default=False)
    shift_pressed = models.BooleanField(default=False)
    alt_pressed = models.BooleanField(default=False)
    meta_pressed = models.BooleanField(default=False)
    key = models.CharField(max_length=200)


class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    server = models.CharField(max_length=200, default="")
    port = models.CharField(max_length=50, default="")
    database = models.CharField(max_length=200, default="")
    username = models.CharField(max_length=200, default="")
    password = models.CharField(max_length=200, default="")
    alias = models.CharField(max_length=200, default="")
    ssh_server = models.CharField(max_length=200, default="")
    ssh_port = models.CharField(max_length=50, default="")
    ssh_user = models.CharField(max_length=200, default="")
    ssh_password = models.CharField(max_length=200, default="")
    ssh_key = models.TextField(default="")
    use_tunnel = models.BooleanField(default=False)
    conn_string = models.TextField(default="")
    public = models.BooleanField(default=False)
    connection_params = models.JSONField(default=dict)
    last_used_database = models.CharField(max_length=200, null=True)
    last_access_date = models.DateTimeField(null=True)
    autocomplete = models.BooleanField(default=True)
    color_label = models.IntegerField(default=0)

    @classmethod
    def reencrypt_credentials(cls, user_id: int, old_key: str, new_key: str) -> None:
        """
        Re-encrypts the credentials (password, ssh_password, ssh_key) of all connections
        for the specified user using a new encryption key.

        This method operates within an atomic transaction. If any error occurs during the
        re-encryption process, no changes are saved to the database and the error is raised.

        Args:
            user_id (int): The ID of the user whose connections should be re-encrypted.
            old_key (str): The old encryption key used to decrypt the current values.
            new_key (str): The new encryption key used to encrypt the values.

        Raises:
            DatabaseError: If an error occurs during the transaction.
        """
        try:
            with transaction.atomic():
                for conn in cls.objects.filter(user_id=user_id):
                    conn.reencrypt_field("password", old_key, new_key)
                    conn.reencrypt_field("ssh_password", old_key, new_key)
                    conn.reencrypt_field("ssh_key", old_key, new_key)
                    conn.save()
        except Exception as exc:
            raise DatabaseError(f"Failed to re-encrypt credentials: {exc}") from exc

    def reencrypt_field(self, field_name: str, old_key: str, new_key: str) -> None:
        """
        Re-encrypts a specific field of a connection using the provided new encryption key.

        Args:
            field_name (str): The name of the field to be re-encrypted.
            old_key (str): The old encryption key used to decrypt the current value.
            new_key (str): The new encryption key used to encrypt the value.
        """
        field_value = getattr(self, field_name, "")
        if field_value:
            decrypted_value = decrypt(field_value, old_key)
            if isinstance(decrypted_value, bytes):
                decrypted_value = decrypted_value.decode()
            encrypted_value = encrypt(decrypted_value, new_key)
            setattr(self, field_name, encrypted_value)


class SnippetFolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, default="")
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()


class SnippetFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(SnippetFolder, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, default="")
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    text = models.TextField(default="")


class Tab(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    snippet = models.TextField(default="")
    database = models.CharField(max_length=200, null=True)


class QueryHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.TextField(default="")
    status = models.TextField(default="")
    snippet = models.TextField(default="")
    database = models.CharField(max_length=200, null=True)


class ConsoleHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    snippet = models.TextField(default="")
    database = models.CharField(max_length=200, null=True)


class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_user_group_name"
            )
        ]


class GroupConnection(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "connection"], name="unique_group_connection"
            )
        ]


class MonWidgets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)
    script_chart = models.TextField(default="")
    script_data = models.TextField(default="")
    type = models.TextField(default="")
    title = models.TextField(default="")
    interval = models.IntegerField(default=60)
    editable = models.BooleanField(default=True)


class MonWidgetsConnections(models.Model):
    unit = models.IntegerField(default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    interval = models.IntegerField(default=60)
    plugin_name = models.TextField(default="")
    position = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)


class ConfigHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    config_snapshot = models.TextField()
    commit_comment = models.TextField(blank=True)


class Job(models.Model):
    id = models.TextField(null=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    command = models.TextField()
    description = models.TextField()
    arguments = models.TextField(blank=True)
    logdir = models.TextField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    exit_code = models.IntegerField(null=True)
    utility_pid = models.IntegerField(null=True)
    process_state = models.IntegerField(null=True)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, null=True)
