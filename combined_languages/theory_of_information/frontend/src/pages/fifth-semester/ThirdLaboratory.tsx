import React, {useState} from 'react';
import axios from 'axios';
import {Form, Input, Button, Typography, Layout, message, Radio} from 'antd';
import {RadioChangeEvent} from 'antd/lib/radio';
import { saveAs } from 'file-saver';

const {Title, Text} = Typography;
const {Header, Content} = Layout;

type AlgorithmType = 'huffman-encode' | 'lz77-encode' | 'lz78-encode' | 'lzw-encode'
    | 'huffman-decode' | 'lz77-decode' | 'lz78-decode' | 'lzw-decode';

const ALGORITHM_URLS: Record<AlgorithmType, string> = {
    'huffman-encode': '/fifth_semester/third_laboratory/encode-huffman',
    'lz77-encode': '/fifth_semester/third_laboratory/encode-lz77',
    'lz78-encode': '/fifth_semester/third_laboratory/encode-lz78',
    'lzw-encode': '/fifth_semester/third_laboratory/encode-lzw',
    'huffman-decode': '/fifth_semester/third_laboratory/decode-huffman',
    "lz77-decode": "/fifth_semester/third_laboratory/decode-lz77",
    "lz78-decode": "/fifth_semester/third_laboratory/decode-lz78",
    "lzw-decode": "/fifth_semester/third_laboratory/decode-lzw",
};

export function ThirdLaboratory() {
    const [file, setFile] = useState<File | null>(null);
    const [selectedAlgorithm, setSelectedAlgorithm] = useState<AlgorithmType>('huffman-encode');
    const [metadata, setMetadata] = useState<string | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = event.target.files?.[0] || null;
        setFile(selectedFile);
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

        const url = `http://localhost:8002/api${ALGORITHM_URLS[selectedAlgorithm]}`;

        try {
            const response = await axios.post(url, formData, {responseType: 'json'});
            const {download_link, metadata} = response.data;

            await downloadFile(download_link);

            setMetadata(JSON.stringify(metadata, null, 2));
            message.success("Файл успешно закодирован!");

        } catch (error) {
            message.error("Произошла ошибка при обработке файла.");
            console.error(error);
        }
    };

    const downloadFile = async (url: string) => {
    try {
        const response = await axios.get("http://localhost:8002" + url, { responseType: 'blob' });

        // Проверяем, что ответ содержит данные
        if (response.status === 200) {
            const filename = url.split('/').pop(); // Извлекаем имя файла из URL
            saveAs(response.data, filename); // Сохраняем файл с помощью file-saver
        } else {
            message.error("Ошибка при скачивании файла.");
        }
    } catch (error) {
        message.error("Ошибка при скачивании файла.");
        console.error(error);
    }
};

    return (
        <Layout>
            <Header style={{padding: '0 24px', background: '#fff', textAlign: 'center'}}>
                <Title level={1}>Лабораторная работа №3 «Сжатие данных»</Title>
            </Header>
            <Content style={{padding: '24px'}}>
                <Typography style={{marginBottom: "10px"}}>
                    Необходимо закодировать текст, хранящийся в файле <br/> <br/>
                    <b> Входные данные: </b> <br/>
                    Файл с текстом, работайте со всеми символами в нем (пробел тоже символ!) <br/> <br/>
                    <b> Выходные данные: </b> <br/>
                    Закодированные последовательности 3х алгоритмов <br/> <br/>
                    Выберите алгоритм и загрузите файл для кодирования. <br/>
                </Typography>

                <Form layout="vertical" onFinish={handleSubmit}>
                    <Form.Item label="Выберите файл">
                        <Input type="file" onChange={handleFileChange}/>
                    </Form.Item>

                    <Form.Item label="Выберите алгоритм">
                        <Radio.Group onChange={handleAlgorithmChange} value={selectedAlgorithm}>
                            {Object.keys(ALGORITHM_URLS).map((algorithm) => (
                                <Radio key={algorithm} value={algorithm}>
                                    {algorithm.replace(/-/g, ' ').replace(/^\w/, (c) => c.toUpperCase())}
                                </Radio>
                            ))}
                        </Radio.Group>
                    </Form.Item>

                    <Form.Item>
                        <Button type="primary" htmlType="submit">Закодировать</Button>
                    </Form.Item>
                </Form>

                {metadata && (
                    <div style={{marginTop: '20px'}}>
                        <Title level={4}>Метаданные:</Title>
                        <Text code>{metadata}</Text>
                    </div>
                )}
            </Content>
        </Layout>
    );
}
