import React, {useState, useEffect, useCallback} from 'react';
import {Layout, Typography, Form, Select, Button, Table, InputNumber, Input} from 'antd';
import type {ColumnsType} from 'antd/es/table';
import axios from "axios";
import {DataDisplay} from "../../components/MatricesAndOtherData.tsx";

const {Header, Content} = Layout;
const {Title} = Typography;
const {Option} = Select;

interface MatrixCell {
    key: number;
    value: number;
}

interface MatrixRow {
    key: number;
    cells: MatrixCell[];
}

export const FourthLaboratory: React.FC = () => {
    const [matrixType, setMatrixType] = useState<string>('G');
    const [rows, setRows] = useState<number>(3);
    const [columns, setColumns] = useState<number>(3);
    const [matrixData, setMatrixData] = useState<MatrixRow[]>([]);
    const [columnsConfig, setColumnsConfig] = useState<ColumnsType<MatrixRow>>([]);
    const [wordInput, setWordInput] = useState<string>("");
    const [data, setData] = useState(null);

    const handleMatrixTypeChange = (value: string) => setMatrixType(value);
    const handleWordInputChange = (e: React.ChangeEvent<HTMLInputElement>) => setWordInput(e.target.value);

    // Генерация начальных данных для матрицы
    const initializeMatrixData = useCallback(() => {
        const initialMatrixData: MatrixRow[] = Array.from({length: rows}, (_, rowIndex) => ({
            key: rowIndex,
            cells: Array.from({length: columns}, (_, cellIndex) => ({
                key: cellIndex,
                value: 0
            }))
        }));
        setMatrixData(initialMatrixData);
    }, [rows, columns])

    // Обновляем данные и столбцы при изменении размеров
    useEffect(() => {
        initializeMatrixData();

        // Обновляем columnsConfig при изменении количества столбцов
        const updatedColumnsConfig: ColumnsType<MatrixRow> = Array.from({length: columns}, (_, i) => ({
            title: `Col ${i + 1}`,
            dataIndex: `col${i}`,
            render: (_: unknown, row: MatrixRow) =>
                row.cells[i] ? (
                    <InputNumber
                        min={0}
                        max={1}
                        value={row.cells[i]?.value || 0}
                        onChange={(value) => handleCellChange(row.key, i, value || 0)}
                    />
                ) : null,
        }));
        setColumnsConfig(updatedColumnsConfig);
    }, [rows, columns, initializeMatrixData]);

    // Обработка изменения значения в ячейке
    const handleCellChange = (rowIndex: number, cellIndex: number, newValue: number) => {
        setMatrixData((prevMatrix) => {
            const updatedMatrix = [...prevMatrix];
            updatedMatrix[rowIndex].cells[cellIndex].value = newValue;
            return updatedMatrix;
        });
    };

    // Обработка отправки данных на backend
    const handleSubmit = async () => {

        const data = {
            word: wordInput,
            matrix: matrixData.map(row => row.cells.map(cell => cell.value)),
            type_matrix: matrixType
        };
        console.log("Sending data to backend:", data);

        try {
            const response = await axios.post('http://localhost:8002/fifth_semester/fourth_laboratory/', data);
            setData(response.data)
            console.log("Response from backend:", response.data);
        } catch (error) {
            console.error("Error sending data to backend:", error);
        }
    };

    return (
        <Layout>
            <Header style={{padding: '0 24px', background: '#fff', textAlign: 'center'}}>
                <Title level={2}>Лабораторная работа №4 «Матричное представление блочных кодов»</Title>
            </Header>
            <Content style={{padding: '20px'}}>
                <Typography.Paragraph>
                    Введите параметры и создайте матрицу для кодирования.
                </Typography.Paragraph>

                <Form layout="inline" style={{marginBottom: '20px'}}>
                    <Form.Item label="Тип матрицы">
                        <Select defaultValue="G" onChange={handleMatrixTypeChange} style={{width: 120}}>
                            <Option value="G">Порождающая</Option>
                            <Option value="H">Проверочная</Option>
                        </Select>
                    </Form.Item>
                    <Form.Item label="Количество строк">
                        <InputNumber min={1} value={rows} onChange={(value) => setRows(value || 1)}/>
                    </Form.Item>
                    <Form.Item label="Количество столбцов">
                        <InputNumber min={1} value={columns} onChange={(value) => setColumns(value || 1)}/>
                    </Form.Item>
                </Form>

                <Form layout="inline" style={{marginBottom: '20px'}}>
                    <Form.Item label="Введите слово">
                        <Input
                            placeholder="введите свой текст"
                            value={wordInput}
                            onChange={handleWordInputChange}
                            style={{width: 200}}
                        />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" onClick={handleSubmit}>
                            Закодировать
                        </Button>
                    </Form.Item>
                </Form>

                <Table
                    columns={columnsConfig}
                    dataSource={matrixData}
                    pagination={false}
                    bordered
                    rowKey="key"
                />
            </Content>
            <Content>
                {data && <DataDisplay data={data} />}
            </Content>

        </Layout>
    );
};
