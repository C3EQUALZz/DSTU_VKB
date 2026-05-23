//! Единая инициализация tracing + color-eyre для всех CLI лабораторных.

use color_eyre::Result;
use tracing::Level;
use tracing_subscriber::{EnvFilter, fmt, prelude::*};

/// Инициализирует pretty-логгер и color-eyre отчёты.
///
/// Использует переменную `RUST_LOG` для фильтра. По умолчанию — `INFO`.
/// Пример: `RUST_LOG=debug cargo run -p lab_01_dh`.
pub fn init() -> Result<()> {
    init_with_default(Level::INFO)
}

/// Тот же `init`, но позволяет задать уровень по умолчанию.
pub fn init_with_default(default_level: Level) -> Result<()> {
    color_eyre::install()?;

    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new(default_level.to_string()));

    let fmt_layer = fmt::layer()
        .with_target(true)
        .with_thread_ids(false)
        .with_thread_names(false)
        .with_file(false)
        .with_line_number(false)
        .with_level(true)
        .pretty();

    tracing_subscriber::registry()
        .with(filter)
        .with(fmt_layer)
        .try_init()
        .map_err(|e| color_eyre::eyre::eyre!("failed to init tracing subscriber: {e}"))?;

    tracing::info!(version = env!("CARGO_PKG_VERSION"), "logger initialised");

    Ok(())
}
