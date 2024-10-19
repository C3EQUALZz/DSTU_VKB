import React, { useState } from 'react';
import axios from 'axios';
import {Form, Input, Button, Typography, Layout, message, Radio} from 'antd';

import { RadioChangeEvent } from 'antd/lib/radio';

const { Title } = Typography;
const { Header, Content } = Layout;

type AlgorithmType = 'huffman-encode' | 'lz77-encode' | 'lz78-encode' | 'lzw-encode' |
    "lzw-decode" | "lz77-decode" | "huffman-decode" | "lz78-decode";

const ALGORITHM_URLS: Record<AlgorithmType, string> = {
    'huffman-encode': '/fifth_semester/third_laboratory/encode-huffman',
    'lz77-encode': '/fifth_semester/third_laboratory/encode-lz77',
    'lz78-encode': '/fifth_semester/third_laboratory/encode-lz78',
    'lzw-encode': '/fifth_semester/third_laboratory/encode-lzw',
    "huffman-decode": "/fifth_semester/third_laboratory/decode-huffman",
    "lz77-decode": "/fifth_semester/third_laboratory/decode-lz77",
    "lz78-decode": "/fifth_semester/third_laboratory/decode-lz78",
    "lzw-decode": "/fifth_semester/third_laboratory/decode-lzw",
};

export function ThirdLaboratory() {
    const [file, setFile] = useState<File | null>(null);
    const [selectedAlgorithm, setSelectedAlgorithm] = useState<AlgorithmType>('huffman-encode');
    const [outputPath, setOutputPath] = useState<string>('output.txt');

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
        formData.append('output_path', outputPath);

        // Формируем URL динамически на основе выбранного алгоритма
        const url = `http://localhost:8002/api${ALGORITHM_URLS[selectedAlgorithm]}`;

        try {
            const response = await axios.post(url, formData);
            message.success("Файл успешно закодирован!");
            console.log("Результат:", response.data); // Вывести или использовать данные ответа

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
                <Typography style={{marginBottom: "10px"}}>
                    Необходимо закодировать текст, хранящийся в файле <br/> <br />

                    <b> Входные данные: </b> <br/>
                    Файл с текстом, работайте со всеми символами в нем (пробел тоже символ!) <br/> <br />

                    <b> Выходные данные: </b> <br/>
                    Закодированные последовательности 3х алгоритмов <br/> <br/>

                    Выберите алгоритм и загрузите файл для кодирования. <br/>
                    Результат будет сохранен по указанному пути. <br/>
                </Typography>

                <Typography>

                </Typography>
                <Form onFinish={handleSubmit} layout="vertical">
                    <Form.Item>
                        <Input type="file" onChange={handleFileChange} />
                    </Form.Item>
                    <Form.Item label="Путь для сохранения файла">
                        <Input value={outputPath} onChange={(e) => setOutputPath(e.target.value)} />
                    </Form.Item>
                    <Form.Item label="Выберите алгоритм">
                        <Radio.Group onChange={handleAlgorithmChange} value={selectedAlgorithm}>
                            <Radio value="huffman-encode">Алгоритм Хаффмана (Кодирование)</Radio>
                            <Radio value="lz77-encode">Алгоритм LZ77 (Кодирование)</Radio>
                            <Radio value="lz78-encode">Алгоритм LZ78 (Кодирование)</Radio>
                            <Radio value="lzw-encode">Алгоритм LZW (Кодирование)</Radio>
                            <br />
                            <Radio value="huffman-decode">Алгоритм Хаффмана (Декодирование)</Radio>
                            <Radio value="lz77-decode">Алгоритм LZ77 (Декодирование)</Radio>
                            <Radio value="lz78-decode">Алгоритм LZ78 (Декодирование)</Radio>
                            <Radio value="lzw-decode">Алгоритм LZW (Декодирование)</Radio>
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