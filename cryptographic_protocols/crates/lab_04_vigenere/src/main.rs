use color_eyre::Result;

fn main() -> Result<()> {
    shared::logging::init()?;
    lab_04_vigenere::presentation::cli::run()
}
