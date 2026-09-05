use color_eyre::Result;

fn main() -> Result<()> {
    shared::logging::init()?;
    let result = lab_04_vigenere::presentation::cli::run();
    if result.is_err() {
        tracing::error!("операция завершилась ошибкой; описание ниже");
    }
    result
}
