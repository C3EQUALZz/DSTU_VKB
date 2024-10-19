import React, { useState } from 'react';
import axios from 'axios';
import { Form, Input, Button, Typography, Layout, message, Radio, Row, Col } from 'antd';

import { RadioChangeEvent } from 'antd/lib/radio';

const { Title } = Typography;
const { Header, Content } = Layout;

type AlgorithmType = 'huffman-encode' | 'lz77-encode' | 'lz78-encode' | 'lzw-encode';

const ALGORITHM_URLS: Record<AlgorithmType, string> = {
    'huffman-encode': '/fifth_semester/third_laboratory/encode-huffman',
    'lz77-encode': '/fifth_semester/third_laboratory/encode-lz77',
    'lz78-encode': '/fifth_semester/third_laboratory/encode-lz78',
    'lzw-encode': '/fifth_semester/third_laboratory/encode-lzw',
};

export function ThirdLaboratory() {
    const [file, setFile] = useState<File | null>(null);
    const [selectedAlgorithm, setSelectedAlgorithm] = useState<AlgorithmType>('huffman-encode');

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            setFile(event.target.files[0]);
        }
    };

    const handleAlgorithmChange = (event: RadioChangeEvent) => {
        setSelectedAlgorithm(event.target.value as AlgorithmType);
    };

    const handleSubmit = async () => {
        if (!file) {
            message.error("Пожалуйста, выберите файл для загрузки.");
            return;
        }

        const formData = new FormData();
        formData.append('file_input', file);

        // Формируем URL динамически на основе выбранного алгоритма
        const url = `http://localhost:8002/api${ALGORITHM_URLS[selectedAlgorithm]}`;

        try {
            const response = await axios.post(url, formData, {
                responseType: 'blob', // Для загрузки файла
            });

            const urlBlob = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = urlBlob;
            link.setAttribute('download', 'output.txt'); // Имя файла при загрузке
            document.body.appendChild(link);
            link.click();
            link.remove();

            message.success("Файл успешно закодирован!");

        } catch (error) {
            message.error("Произошла ошибка при обработке файла.");
            console.error(error);
        }
    };

    return (
        <Layout>
            <Header style={{ padding: '0 24px', background: '#fff', textAlign: 'center' }}>
                <Title level={1}>Лабораторная работа №3 «Сжатие данных»</Title>
            </Header>
            <Content style={{ padding: '24px' }}>
                <Typography style={{ marginBottom: "10px" }}>
                    Необходимо закодировать текст, хранящийся в файле <br /> <br />

                    <b> Входные данные: </b> <br />
                    Файл с текстом, работайте со всеми символами в нем (пробел тоже символ!) <br /> <br />

                    <b> Выходные данные: </b> <br />
                    Закодированные последовательности 3х алгоритмов <br /> <br />

                    Выберите алгоритм и загрузите файл для кодирования. <br />
                </Typography>

                <Typography>
                    <b> Алгоритм Хаффана </b> <br/>
                    Используя данный алгоритм и кодируете, и декодируете.
                    При кодировании выводите таблицу соответствия «символ – битовая строка». Далее
                    закодированный текст сохраняете либо в тот же файл, где был исходный, либо в другой,
                    но для декодирования считываете также всю кодовую строку из файла. При
                    декодировании можно использовать уже построенную таблицу соответствий «символ –
                    битовая строка» (напомню, в жизни при декодировании чаще используется вариант
                    нового построения дерева, но для этого передают закодированную последовательность, а
                    также символ + его частота). <br/> <br/>

                    <b> Алгоритмы LZ77, LZ78 </b> <br/>
                    Здесь делаете по вариантам, у кого номер по списку четный – 78, у кого нечетный 77. Только
                    кодируете.
                    Одним из этих алгоритмов кодируете, выводите в файл и(или) на экран (в интерфейсе)
                    результат, т.е. сам пакет, всю таблицу выводить не обязательно, ориентироваться и уметь
                    объяснить почему пакет выглядит так или иначе. <br/> <br/>

                    <b> Алгоритм LZW. </b> <br/>
                    Только кодируете. Результат в битовом представлении выводите в файл и(или) на экран (в интерфейсе).
                    Но, все промежуточные таблицы выводите в файл (можно в два разных файла, если удобнее
                    так). Файл с любым расширением, возможно, будет удобнее csv, xls.
                    Язык: любой, кроме Паскаля, Делфи, Бейсика и подобных
                    Интерфейс – нужен, при чем не одна кнопка, которая сразу все запускает, а для каждого
                    действия необходимо его вызвать нажатием, либо выбором файла. <br/> <br/>
                </Typography>

                <Form onFinish={handleSubmit} layout="vertical">
                    <Form.Item>
                        <Input type="file" onChange={handleFileChange} />
                    </Form.Item>
                     <Form.Item label="Выберите алгоритм">
                        <Radio.Group onChange={handleAlgorithmChange} value={selectedAlgorithm}>
                            <Row gutter={[7, 7]}>
                                <Col span={5}>
                                    <Radio value="huffman-encode">Алгоритм Хаффмана (Кодирование)</Radio>
                                </Col>
                                <Col span={5}>
                                    <Radio value="lz77-encode">Алгоритм LZ77 (Кодирование)</Radio>
                                </Col>
                                <Col span={5}>
                                    <Radio value="lz78-encode">Алгоритм LZ78 (Кодирование)</Radio>
                                </Col>
                                <Col span={5}>
                                    <Radio value="lzw-encode">Алгоритм LZW (Кодирование)</Radio>
                                </Col>
                                <Col span={5}>
                                    <Radio value="huffman-decode">Алгоритм Хаффмана (Декодирование)</Radio>
                                </Col>
                                <Col span={5}>
                                    <Radio value="lz77-decode">Алгоритм LZ77 (Декодирование)</Radio>
                                </Col>
                                <Col span={5}>
                                    <Radio value="lz78-decode">Алгоритм LZ78 (Декодирование)</Radio>
                                </Col>
                                <Col span={5}>
                                    <Radio value="lzw-decode">Алгоритм LZW (Декодирование)</Radio>
                                </Col>
                            </Row>
                        </Radio.Group>
                    </Form.Item>

                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Выполнить
                        </Button>
                    </Form.Item>
                </Form>
            </Content>
        </Layout>
    );
}
