//! Заглушка — будет наполнена в соответствующей задаче.
fn main() -> color_eyre::Result<()> {
    shared::logging::init()?;
    tracing::warn!("crate ещё не реализован");
    Ok(())
}
