import React, { useState, useEffect, useCallback } from 'react';
import { Layout, Typography, Form, Select, Button, Table, InputNumber } from 'antd';
import axios from 'axios';

const { Header, Content } = Layout;
const { Title } = Typography;
const { Option } = Select;

type Cell = {
    key: number;
    value: number;
};

type Row = {
    key: number;
    cells: Cell[];
};

type MatrixData = Row[];

type ColumnConfig = {
    title: string;
    dataIndex: string;
    render: (_: unknown, row: Row) => JSX.Element;
};

export const FifthLaboratory: React.FC = () => {
    const [algorithm, setAlgorithm] = useState<string>('shortening');
    const [matrixType, setMatrixType] = useState<string>('G');
    const [rows, setRows] = useState<number>(3);
    const [columns, setColumns] = useState<number>(3);
    const [matrixData, setMatrixData] = useState<MatrixData>([]);
    const [columnsConfig, setColumnsConfig] = useState<ColumnConfig[]>([]);

    const handleAlgorithmChange = (value: string) => setAlgorithm(value);
    const handleMatrixTypeChange = (value: string) => setMatrixType(value);

    // Initialize matrix data
    const initializeMatrixData = useCallback(() => {
        const initialMatrix: MatrixData = Array.from({ length: rows }, (_, rowIndex) => ({
            key: rowIndex,
            cells: Array.from({ length: columns }, (_, colIndex) => ({
                key: colIndex,
                value: 0
            }))
        }));
        setMatrixData(initialMatrix);
    }, [rows, columns]);

    useEffect(() => {
        initializeMatrixData();

        // Update table columns
        const updatedColumnsConfig: ColumnConfig[] = Array.from({ length: columns }, (_, i) => ({
            title: `Col ${i + 1}`,
            dataIndex: `col${i}`,
            render: (_: unknown, row: Row) => (
                <InputNumber
                    min={0}
                    max={1}
                    value={row.cells[i]?.value || 0}
                    onChange={(value) => handleCellChange(row.key, i, value || 0)}
                />
            ),
        }));
        setColumnsConfig(updatedColumnsConfig);
    }, [rows, columns, initializeMatrixData]);

    // Handle cell value change
    const handleCellChange = (rowIndex: number, cellIndex: number, newValue: number) => {
        setMatrixData((prevMatrix) => {
            const updatedMatrix = [...prevMatrix];
            updatedMatrix[rowIndex].cells[cellIndex].value = newValue;
            return updatedMatrix;
        });
    };

    // Handle form submission
    const handleSubmit = async () => {
        const formattedMatrix = matrixData.map(row => row.cells.map(cell => cell.value));
        const payload = {
            algorithm,
            matrixType,
            matrix: formattedMatrix
        };

        console.log('Sending data to backend:', payload);

        try {
            const response = await axios.post('http://localhost:8002/laboratory/', payload);
            console.log('Response from backend:', response.data);
        } catch (error) {
            console.error('Error sending data to backend:', error);
        }
    };

    return (
        <Layout>
            <Header style={{ padding: '0 24px', background: '#fff', textAlign: 'center' }}>
                <Title level={2}>Лабораторная работа: Методы модификации помехоустойчивых блочных кодов</Title>
            </Header>
            <Content style={{ padding: '20px' }}>
                <Form layout="inline" style={{ marginBottom: '20px' }}>
                    <Form.Item label="Алгоритм модификации">
                        <Select defaultValue="shortening" onChange={handleAlgorithmChange} style={{ width: 200 }}>
                            <Option value="shortening">Укорочение кода</Option>
                            <Option value="extension">Расширение кода</Option>
                            <Option value="perforation">Перфорация</Option>
                            <Option value="completion">Пополнение</Option>
                        </Select>
                    </Form.Item>
                    <Form.Item label="Тип матрицы">
                        <Select defaultValue="G" onChange={handleMatrixTypeChange} style={{ width: 150 }}>
                            <Option value="G">Порождающая</Option>
                            <Option value="H">Проверочная</Option>
                        </Select>
                    </Form.Item>
                    <Form.Item label="Количество строк">
                        <InputNumber min={1} value={rows} onChange={(value) => setRows(value || 1)} />
                    </Form.Item>
                    <Form.Item label="Количество столбцов">
                        <InputNumber min={1} value={columns} onChange={(value) => setColumns(value || 1)} />
                    </Form.Item>
                </Form>

                <Table
                    columns={columnsConfig}
                    dataSource={matrixData}
                    pagination={false}
                    bordered
                    rowKey="key"
                />

                <Button type="primary" style={{ marginTop: '20px' }} onClick={handleSubmit}>
                    Отправить данные
                </Button>
            </Content>
        </Layout>
    );
};
