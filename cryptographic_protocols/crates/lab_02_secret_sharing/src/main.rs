use color_eyre::Result;

fn main() -> Result<()> {
    shared::logging::init()?;
    lab_02_secret_sharing::presentation::cli::run()
}
