//! Кросс-платформенный выбор криптопровайдера (Strategy pattern + cfg).
//!
//! По одному модулю на ОС, активируется через `cfg(target_os = …)`. Внешний
//! код использует тип-алиас [`ActiveProvider`] и функцию [`active`] —
//! то и другое статически разрешается в компилируемую под текущую ОС
//! реализацию. Никакого runtime-диспетча не нужно: все вызовы trait'а
//! инлайнятся компилятором.

#[cfg(target_os = "macos")]
pub mod macos;
#[cfg(target_os = "macos")]
pub type ActiveProvider = macos::CommonCryptoProvider;

#[cfg(target_os = "linux")]
pub mod linux;
#[cfg(target_os = "linux")]
pub type ActiveProvider = linux::OpenSslProvider;

#[cfg(target_os = "windows")]
pub mod windows;
#[cfg(target_os = "windows")]
pub type ActiveProvider = windows::CngProvider;

#[cfg(not(any(target_os = "macos", target_os = "linux", target_os = "windows")))]
compile_error!(
    "Лаб 6 поддерживает macOS, Linux и Windows. \
     Чтобы добавить новую платформу — реализуй SymmetricCryptoProvider \
     и пропиши тип сюда."
);

/// Создать провайдер, активный для текущей ОС.
#[must_use]
pub fn active() -> ActiveProvider {
    ActiveProvider::new()
}
