//! Кросс-платформенный выбор криптопровайдера (Strategy + cfg).

// macOS и Linux используют один и тот же openssl-провайдер, потому что
// Apple deprecated низкоуровневые `SecKey*` API для импорта/экспорта raw RSA.
// Реализация одна, но `name()` сообщает, на какой ОС она работает —
// чтобы пользователь видел в логах, какой именно libcrypto подцеплен.

#[cfg(any(target_os = "macos", target_os = "linux"))]
pub mod openssl_provider;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub type ActiveProvider = openssl_provider::OpenSslProvider;

#[cfg(target_os = "windows")]
pub mod windows;
#[cfg(target_os = "windows")]
pub type ActiveProvider = windows::CngProvider;

#[cfg(not(any(target_os = "macos", target_os = "linux", target_os = "windows")))]
compile_error!("Лаб 7 поддерживает macOS, Linux и Windows.");

#[must_use]
pub fn active() -> ActiveProvider {
    ActiveProvider::new()
}
