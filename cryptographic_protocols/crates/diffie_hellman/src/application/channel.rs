//! Один сетевой сеанс: DH, получение двух ключей и зашифрованные сообщения.

use chacha20poly1305::aead::{Aead, KeyInit, Payload};
use chacha20poly1305::{ChaCha20Poly1305, Nonce};
use color_eyre::Result;
use color_eyre::eyre::{Context, bail, eyre};
use hkdf::Hkdf;
use num_bigint::BigUint;
use num_traits::Num;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::time::Instant;
use tracing::info;

use crate::domain::dh::{PublicParameters, shared_secret};
use crate::domain::group::DhGroup;
use crate::domain::rng::RandomSource;

const MAX_MESSAGE_BYTES: usize = 8 * 1024;

/// Кадры протокола на границе между сценарием и транспортом.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum Frame {
    Hello {
        p: String,
        q: String,
        g: String,
        public: String,
    },
    Public {
        value: String,
    },
    Data {
        seq: u64,
        body: Vec<u8>,
    },
}

pub trait Transport {
    fn send(&mut self, frame: &Frame) -> Result<()>;
    fn recv(&mut self) -> Result<Frame>;
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
enum Message {
    Text { value: String },
    Close,
    Bye,
}

pub struct SecureSession<T> {
    transport: T,
    send_cipher: ChaCha20Poly1305,
    recv_cipher: ChaCha20Poly1305,
    send_seq: u64,
    recv_seq: u64,
}

fn parse_big(value: &str) -> Result<BigUint> {
    BigUint::from_str_radix(value, 10).wrap_err("неверное большое число в кадре DH")
}

fn derive_keys(
    shared: &BigUint,
    group: &DhGroup,
    server_y: &BigUint,
    client_y: &BigUint,
) -> Result<([u8; 32], [u8; 32])> {
    let mut digest = Sha256::new();
    for n in [
        &group.params.n,
        &group.q,
        &group.params.g,
        server_y,
        client_y,
    ] {
        let encoded = n.to_bytes_be();
        let len = u32::try_from(encoded.len()).wrap_err("слишком длинное значение DH")?;
        digest.update(len.to_be_bytes());
        digest.update(encoded);
    }
    let salt = digest.finalize();
    let hkdf = Hkdf::<Sha256>::new(Some(&salt), &shared.to_bytes_be());
    let mut output = [0u8; 64];
    hkdf.expand(b"diffie-hellman-lab-channel-v1", &mut output)
        .map_err(|_| eyre!("ошибка вывода ключей сеанса"))?;
    let mut server_to_client = [0u8; 32];
    let mut client_to_server = [0u8; 32];
    server_to_client.copy_from_slice(&output[..32]);
    client_to_server.copy_from_slice(&output[32..]);
    Ok((server_to_client, client_to_server))
}

fn nonce(seq: u64) -> [u8; 12] {
    let mut value = [0u8; 12];
    value[4..].copy_from_slice(&seq.to_be_bytes());
    value
}

impl<T: Transport> SecureSession<T> {
    fn new(transport: T, send_key: &[u8; 32], recv_key: &[u8; 32]) -> Result<Self> {
        Ok(Self {
            transport,
            send_cipher: ChaCha20Poly1305::new_from_slice(send_key)
                .map_err(|_| eyre!("неверная длина ключа отправки"))?,
            recv_cipher: ChaCha20Poly1305::new_from_slice(recv_key)
                .map_err(|_| eyre!("неверная длина ключа приёма"))?,
            send_seq: 0,
            recv_seq: 0,
        })
    }

    fn send(&mut self, message: &Message) -> Result<()> {
        let plain = serde_json::to_vec(message)?;
        if plain.len() > MAX_MESSAGE_BYTES {
            bail!("сообщение длиннее {MAX_MESSAGE_BYTES} байт");
        }
        let seq = self.send_seq;
        let body = self
            .send_cipher
            .encrypt(
                Nonce::from_slice(&nonce(seq)),
                Payload {
                    msg: &plain,
                    aad: &seq.to_be_bytes(),
                },
            )
            .map_err(|_| eyre!("не удалось зашифровать сообщение"))?;
        self.transport.send(&Frame::Data { seq, body })?;
        self.send_seq = seq
            .checked_add(1)
            .ok_or_else(|| eyre!("счётчик отправки исчерпан"))?;
        info!(
            seq,
            bytes = plain.len(),
            "зашифрованное сообщение отправлено"
        );
        Ok(())
    }

    fn recv(&mut self) -> Result<Message> {
        let Frame::Data { seq, body } = self.transport.recv()? else {
            bail!("ожидался зашифрованный кадр");
        };
        if seq != self.recv_seq {
            bail!(
                "неверный номер входящего сообщения: ожидался {}, получен {seq}",
                self.recv_seq
            );
        }
        let plain = self
            .recv_cipher
            .decrypt(
                Nonce::from_slice(&nonce(seq)),
                Payload {
                    msg: &body,
                    aad: &seq.to_be_bytes(),
                },
            )
            .map_err(|_| eyre!("ошибка проверки подлинности зашифрованного сообщения"))?;
        self.recv_seq = seq
            .checked_add(1)
            .ok_or_else(|| eyre!("счётчик приёма исчерпан"))?;
        info!(
            seq,
            bytes = plain.len(),
            "зашифрованное сообщение получено и проверено"
        );
        serde_json::from_slice(&plain).wrap_err("неверное содержимое сообщения")
    }
}

pub fn accept<T: Transport, R: RandomSource>(
    mut transport: T,
    bits: u32,
    rounds: u32,
    rng: &mut R,
) -> Result<SecureSession<T>> {
    let started = Instant::now();
    let (group, stats) = DhGroup::generate(bits, rounds, 1000, rng)?;
    info!(bits, p_candidates = stats.p_candidates, q_candidates = stats.q_candidates, elapsed = ?started.elapsed(), "параметры DH сгенерированы");
    let server = group.random_party(rounds, rng)?;
    info!(p = %group.params.n, q = %group.q, g = %group.params.g, public = %server.y, "сервер отправляет открытые параметры и своё значение");
    transport.send(&Frame::Hello {
        p: group.params.n.to_string(),
        q: group.q.to_string(),
        g: group.params.g.to_string(),
        public: server.y.to_string(),
    })?;
    let Frame::Public { value } = transport.recv()? else {
        bail!("ожидалось открытое значение клиента");
    };
    let client_y = parse_big(&value)?;
    group.validate_peer_public(&client_y)?;
    info!(public = %client_y, "сервер получил открытое значение клиента");
    let shared = shared_secret(&server.x, &client_y, &group.params.n);
    let (s2c, c2s) = derive_keys(&shared, &group, &server.y, &client_y)?;
    info!("сервер вывел ключи сеанса; секрет не записывается в лог");
    SecureSession::new(transport, &s2c, &c2s)
}

pub fn connect<T: Transport, R: RandomSource>(
    mut transport: T,
    rounds: u32,
    rng: &mut R,
) -> Result<SecureSession<T>> {
    let Frame::Hello { p, q, g, public } = transport.recv()? else {
        bail!("ожидались параметры DH от сервера");
    };
    let group = DhGroup {
        params: PublicParameters {
            n: parse_big(&p)?,
            g: parse_big(&g)?,
        },
        q: parse_big(&q)?,
    };
    group.validate(rounds, rng)?;
    let server_y = parse_big(&public)?;
    group.validate_peer_public(&server_y)?;
    info!(p = %group.params.n, q = %group.q, g = %group.params.g, public = %server_y, "клиент проверил параметры и открытое значение сервера");
    let client = group.random_party(rounds, rng)?;
    transport.send(&Frame::Public {
        value: client.y.to_string(),
    })?;
    info!(public = %client.y, "клиент отправил своё открытое значение");
    let shared = shared_secret(&client.x, &server_y, &group.params.n);
    let (s2c, c2s) = derive_keys(&shared, &group, &server_y, &client.y)?;
    info!("клиент вывел ключи сеанса; секрет не записывается в лог");
    SecureSession::new(transport, &c2s, &s2c)
}

pub fn serve_messages<T: Transport>(session: &mut SecureSession<T>) -> Result<()> {
    loop {
        match session.recv()? {
            Message::Text { value } => {
                info!(message = %value, "сервер получил текст");
                let answer = value.to_uppercase();
                info!(response = %answer, "сервер преобразовал текст в верхний регистр");
                session.send(&Message::Text { value: answer })?;
            }
            Message::Close => {
                info!("клиент запросил завершение сеанса");
                session.send(&Message::Bye)?;
                return Ok(());
            }
            Message::Bye => bail!("сервер получил неожиданный ответ bye"),
        }
    }
}

pub fn send_text<T: Transport>(session: &mut SecureSession<T>, text: String) -> Result<String> {
    info!(message = %text, "клиент отправляет текст");
    session.send(&Message::Text { value: text })?;
    match session.recv()? {
        Message::Text { value } => {
            info!(response = %value, "клиент получил обработанный ответ");
            Ok(value)
        }
        _ => bail!("ожидался текстовый ответ сервера"),
    }
}

pub fn close<T: Transport>(session: &mut SecureSession<T>) -> Result<()> {
    session.send(&Message::Close)?;
    if !matches!(session.recv()?, Message::Bye) {
        bail!("ожидалось подтверждение завершения сеанса");
    }
    info!("сеанс связи завершён");
    Ok(())
}

#[cfg(test)]
mod tests {
    use std::cell::RefCell;
    use std::collections::VecDeque;
    use std::rc::Rc;

    use super::*;

    #[derive(Clone)]
    struct MemoryTransport {
        incoming: Rc<RefCell<VecDeque<Frame>>>,
        outgoing: Rc<RefCell<VecDeque<Frame>>>,
    }

    impl Transport for MemoryTransport {
        fn send(&mut self, frame: &Frame) -> Result<()> {
            self.outgoing.borrow_mut().push_back(frame.clone());
            Ok(())
        }

        fn recv(&mut self) -> Result<Frame> {
            self.incoming
                .borrow_mut()
                .pop_front()
                .ok_or_else(|| eyre!("нет кадра"))
        }
    }

    fn pair() -> (
        SecureSession<MemoryTransport>,
        SecureSession<MemoryTransport>,
        Rc<RefCell<VecDeque<Frame>>>,
    ) {
        let to_server = Rc::new(RefCell::new(VecDeque::new()));
        let to_client = Rc::new(RefCell::new(VecDeque::new()));
        let client = SecureSession::new(
            MemoryTransport {
                incoming: to_client.clone(),
                outgoing: to_server.clone(),
            },
            &[1; 32],
            &[2; 32],
        )
        .unwrap();
        let server = SecureSession::new(
            MemoryTransport {
                incoming: to_server.clone(),
                outgoing: to_client,
            },
            &[2; 32],
            &[1; 32],
        )
        .unwrap();
        (client, server, to_server)
    }

    #[test]
    fn two_messages_in_one_session_and_replay_is_rejected() {
        let (mut client, mut server, to_server) = pair();
        for value in ["Привет", "ещё сообщение"] {
            client
                .send(&Message::Text {
                    value: value.to_owned(),
                })
                .unwrap();
            let saved = to_server.borrow().front().unwrap().clone();
            let received = match server.recv().unwrap() {
                Message::Text { value } => Some(value),
                _ => None,
            };
            let received = received.expect("ожидался текст");
            assert_eq!(received, value);
            server
                .send(&Message::Text {
                    value: received.to_uppercase(),
                })
                .unwrap();
            let answer = match client.recv().unwrap() {
                Message::Text { value } => Some(value),
                _ => None,
            };
            let answer = answer.expect("ожидался ответ");
            assert_eq!(answer, value.to_uppercase());
            to_server.borrow_mut().push_back(saved);
            assert!(server.recv().is_err());
        }
    }

    #[test]
    fn altered_ciphertext_is_rejected() {
        let (mut client, mut server, to_server) = pair();
        client
            .send(&Message::Text {
                value: "тайна".to_owned(),
            })
            .unwrap();
        if let Some(Frame::Data { body, .. }) = to_server.borrow_mut().front_mut() {
            body[0] ^= 1;
        }
        assert!(server.recv().is_err());
    }
}
