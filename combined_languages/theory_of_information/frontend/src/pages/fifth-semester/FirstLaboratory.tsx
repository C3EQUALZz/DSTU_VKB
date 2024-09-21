import React, { useState } from 'react';
import axios from 'axios';
import { Form, Input, Button, Typography, Layout } from 'antd';
import { Histogram } from "../../components/Histogram";

const { Title, Paragraph } = Typography;
const { Header, Content } = Layout;

export function FirstLaboratory() {
    const [file, setFile] = useState<File | null>(null);
    const [entropy, setEntropy] = useState<number | null>(null);
    const [histogramData, setHistogramData] = useState<HistogramData | null>(null);
    const [ignorePattern, setIgnorePattern] = useState<string>("");

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            setFile(event.target.files[0]);
        }
    };

    const handleIgnorePatternChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setIgnorePattern(event.target.value);
    };

    const handleSubmit = async () => {
        if (!file) {
            alert("Пожалуйста, выберите файл для загрузки.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('ignore_pattern', ignorePattern);

        try {
            const entropyResponse = await axios.post('http://localhost:8002/api/fifth_semester/first_laboratory/entropy', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setEntropy(entropyResponse.data.entropy);

            const histogramResponse = await axios.post('http://localhost:8002/api/fifth_semester/first_laboratory/histogram', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            console.log(histogramResponse.data);

            // Данные возвращаются как объект с полями x и y
            setHistogramData(histogramResponse.data);
        } catch (error) {
            alert("Произошла ошибка при загрузке файла.");
        }
    };

    return (
        <Layout>
            <Header style={{ padding: '0 24px', background: '#fff', textAlign: 'center' }}>
                <Title level={1}>Лабораторная работа №1 «Энтропия текста»</Title>
            </Header>
            <Content style={{ padding: '24px' }}>
                <Typography style={{marginBottom: "10px"}}>
                    Необходимо подсчитать энтропию текста, содержащегося в файле <br /><br />

                    Входные данные: <br />
                    Файл с текстом (можете сами себе поставить ограничения на разрешение файла)
                    В данных файлах содержаться различные буквы (латиница и кириллица), знаки
                    препинаний, цифры. Символы {`@ # $ ^ & * {} [] < > <= >= / \ | = + `} можете удалять. Не
                    забывайте, что пробел тоже символ <br /><br />

                    Выходные данные: <br />
                    1. Гистограмма появления всех символов, которые встретились в тексте, возможны три
                    варианта построения гистограммы:<br/>
                    а. полная гистограмма всех символов на одной оси <br/>
                    б. 3-4 разных гистограмм, разбитых по смыслу (отдельно кириллица, латиница,
                    символы) <br/>
                    в. полная таблица символ-частота (вероятность) а гистограмма – первые 10-20 часто
                    встречаемых символов <br/>
                    2. Энтропия текста <br/><br/>

                    Язык: любой, кроме Паскаля, Делфи, Бейсика и подобных <br/>
                    Интерфейс – нужен, конкретных требований к нему на первой лабе не предъявляю<br/>
                </Typography>
                <Form onFinish={handleSubmit} layout="vertical">
                    <Form.Item>
                        <Input type="file" onChange={handleFileChange} />
                    </Form.Item>
                    <Form.Item label="Игнорируемый паттерн">
                        <Input
                            type="text"
                            value={ignorePattern}
                            onChange={handleIgnorePatternChange}
                            placeholder="Введите игнорируемый паттерн"
                        />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Загрузить
                        </Button>
                    </Form.Item>
                </Form>

                {entropy && (
                    <Paragraph>
                        <strong>Энтропия:</strong> {entropy}
                    </Paragraph>
                )}

                {histogramData && (
                    <Histogram histogramData={histogramData} />
                )}
            </Content>
        </Layout>
    );
}
