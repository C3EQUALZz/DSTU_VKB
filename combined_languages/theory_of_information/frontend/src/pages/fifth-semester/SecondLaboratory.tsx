import React, { useState } from 'react';
import axios from 'axios';
import { Form, Input, Button, Typography, Layout } from 'antd';
import { Histogram } from "../../components/Histogram";

const { Title, Paragraph } = Typography;
const { Header, Content } = Layout;

export function SecondLaboratory() {
    const [file, setFile] = useState<File | null>(null);
    const [entropy, setEntropy] = useState<{ text_entropy: number | null, file_entropy: number | null }>({
        text_entropy: null,
        file_entropy: null
    });
    const [textHistogramData, setTextHistogramData] = useState<HistogramData | null>(null);
    const [fileHistogramData, setFileHistogramData] = useState<HistogramData | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            setFile(event.target.files[0]);
        }
    };

    const handleSubmit = async () => {
        if (!file) {
            alert("Пожалуйста, выберите файл для загрузки.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const entropyResponse = await axios.post('http://localhost:8002/api/fifth_semester/second_laboratory/entropy', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setEntropy({
                text_entropy: entropyResponse.data.text_entropy ?? null,
                file_entropy: entropyResponse.data.file_entropy ?? null,
            });

            const histogramResponse = await axios.post('http://localhost:8002/api/fifth_semester/second_laboratory/histogram', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            // Проверка на наличие гистограммы текста и файла
            setTextHistogramData(histogramResponse.data.text_histogram || null);
            setFileHistogramData(histogramResponse.data.file_histogram || null);

        } catch {
            alert("Произошла ошибка при загрузке файла.");
        }
    };

    return (
        <Layout>
            <Header style={{ padding: '0 24px', background: '#fff', textAlign: 'center' }}>
                <Title level={1}>Лабораторная работа №2 «Энтропия файла и текста»</Title>
            </Header>
            <Content style={{ padding: '24px' }}>
                <Typography style={{marginBottom: "10px"}}>
                    Необходимо подсчитать энтропию файла (любого), если в этом файле есть текст – то сравнить энтропию файла и текста.. <br /><br />

                    Входные данные: <br />
                    Файл с любым расширением <br /><br />

                    Выходные данные: <br />
                    1. Гистограмма появления всех бит <br />
                    2. Энтропия файла <br />
                    3. Если файл содержит текст – энтропия текста <br /><br />

                    Язык: любой, кроме Паскаля, Делфи, Бейсика и подобных <br/>
                    Интерфейс – нужен<br/>
                </Typography>
                <Form onFinish={handleSubmit} layout="vertical">
                    <Form.Item>
                        <Input type="file" onChange={handleFileChange} />
                    </Form.Item>

                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Загрузить
                        </Button>
                    </Form.Item>
                </Form>

                {/* Render only if entropy is available */}
                {entropy.text_entropy !== null && (
                    <Paragraph>
                        <strong>Энтропия текста:</strong> {entropy.text_entropy}
                    </Paragraph>
                )}

                {entropy.file_entropy !== null && (
                    <Paragraph>
                        <strong>Энтропия файла:</strong> {entropy.file_entropy}
                    </Paragraph>
                )}

                {/* Render histograms only if the corresponding data exists */}
                {textHistogramData && (
                    <div>
                        <Title level={3}>Гистограмма текста</Title>
                        <Histogram histogramData={textHistogramData} />
                    </div>
                )}

                {fileHistogramData && (
                    <div>
                        <Title level={3}>Гистограмма файла</Title>
                        <Histogram histogramData={fileHistogramData} />
                    </div>
                )}
            </Content>
        </Layout>
    );
}
