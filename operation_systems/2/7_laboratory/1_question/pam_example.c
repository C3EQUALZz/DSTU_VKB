#include <security/pam_appl.h>
#include <security/pam_misc.h>
#include <stdio.h>
#include <stdlib.h>

static struct pam_conv conv = {
    misc_conv, // Используем стандартный диалог PAM
    NULL
};

int main(int argc, char *argv[]) {
    pam_handle_t *pamh = NULL;
    int retval;
    const char *user = NULL;

    if(argc != 2) {
        fprintf(stderr, "Usage: %s username\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    user = argv[1];

    // Инициализация PAM
    retval = pam_start("my_pam_app", user, &conv, &pamh);
    if(retval != PAM_SUCCESS) {
        fprintf(stderr, "pam_start failed: %s\n", pam_strerror(pamh, retval));
        return EXIT_FAILURE;
    }

    // Аутентификация пользователя
    retval = pam_authenticate(pamh, 0);
    if(retval != PAM_SUCCESS) {
        fprintf(stderr, "Authentication failed: %s\n", pam_strerror(pamh, retval));
        pam_end(pamh, retval);
        return EXIT_FAILURE;
    }

    // Проверка учетной записи
    retval = pam_acct_mgmt(pamh, 0);
    if(retval != PAM_SUCCESS) {
        fprintf(stderr, "Account validation failed: %s\n", pam_strerror(pamh, retval));
        pam_end(pamh, retval);
        return EXIT_FAILURE;
    }

    // Открытие сессии
    retval = pam_open_session(pamh, 0);
    if(retval != PAM_SUCCESS) {
        fprintf(stderr, "Session opening failed: %s\n", pam_strerror(pamh, retval));
        pam_end(pamh, retval);
        return EXIT_FAILURE;
    }

    printf("Session successfully opened\n");
    printf("User environment created\n");

    // Здесь можно выполнять действия от имени пользователя...

    // Закрытие сессии
    retval = pam_close_session(pamh, 0);
    if(retval != PAM_SUCCESS) {
        fprintf(stderr, "Session closing failed: %s\n", pam_strerror(pamh, retval));
    }

    // Завершение работы с PAM
    pam_end(pamh, PAM_SUCCESS);
    printf("PAM session closed\n");

    return EXIT_SUCCESS;
}