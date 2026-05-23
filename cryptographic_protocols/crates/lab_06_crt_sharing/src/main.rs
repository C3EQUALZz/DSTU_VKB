use color_eyre::Result;

fn main() -> Result<()> {
    shared::logging::init()?;
    lab_06_crt_sharing::presentation::cli::run()
}
