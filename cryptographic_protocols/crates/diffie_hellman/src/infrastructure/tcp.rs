//! JSON-кадры поверх TCP с 32-битным префиксом длины.

use std::io::{Read, Write};
use std::net::TcpStream;
use std::time::Duration;

use color_eyre::Result;
use color_eyre::eyre::{Context, bail};

use crate::application::channel::{Frame, Transport};

const MAX_FRAME: usize = 64 * 1024;

pub struct TcpTransport {
    stream: TcpStream,
}

impl TcpTransport {
    pub fn new(stream: TcpStream) -> Result<Self> {
        stream.set_read_timeout(Some(Duration::from_secs(120)))?;
        stream.set_write_timeout(Some(Duration::from_secs(120)))?;
        stream.set_nodelay(true)?;
        Ok(Self { stream })
    }
}

impl Transport for TcpTransport {
    fn send(&mut self, frame: &Frame) -> Result<()> {
        let encoded = serde_json::to_vec(frame)?;
        if encoded.len() > MAX_FRAME {
            bail!("сетевой кадр слишком велик");
        }
        let len = u32::try_from(encoded.len()).wrap_err("сетевой кадр слишком велик")?;
        self.stream.write_all(&len.to_be_bytes())?;
        self.stream.write_all(&encoded)?;
        Ok(())
    }

    fn recv(&mut self) -> Result<Frame> {
        let mut len_bytes = [0u8; 4];
        self.stream.read_exact(&mut len_bytes)?;
        let len = usize::try_from(u32::from_be_bytes(len_bytes))?;
        if len == 0 || len > MAX_FRAME {
            bail!("недопустимая длина сетевого кадра: {len}");
        }
        let mut encoded = vec![0u8; len];
        self.stream.read_exact(&mut encoded)?;
        serde_json::from_slice(&encoded).wrap_err("неверный формат сетевого кадра")
    }
}
