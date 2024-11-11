import React from 'react';
import {Table, List, Typography} from 'antd';
import {CodeTableDisplay} from "./CodeTableDisplay.tsx";
import {TableOfErrorVectorsAndSyndromesDisplay} from "./TableOfErrorsAndSyndromes.tsx";

interface MatrixDisplayProps {
    matrix: number[][];
}

const MatrixDisplay: React.FC<MatrixDisplayProps> = ({matrix}) => {
    const columns = matrix[0].map((_, i) => ({
        title: `Col ${i + 1}`,
        dataIndex: i,
        key: i,
    }));

    const dataSource = matrix.map((row, i) => ({
        key: i,
        ...row,
    }));

    return <Table columns={columns} dataSource={dataSource} pagination={false} size="small"/>;
};

interface DataDisplayProps {
    data: any;
}


export const DataDisplay: React.FC<DataDisplayProps> = ({data}) => {
    return (
        <List
            bordered
            dataSource={[
                {
                    title: 'GMatrix', content: data.GMatrix ? (
                        <MatrixDisplay matrix={data.GMatrix}/>
                    ) : null
                },
                {
                    title: 'HMatrix', content: data.HMatrix ? (
                        <MatrixDisplay matrix={data.HMatrix}/>
                    ) : null
                },
                {
                    title: 'GSystematicMatrix',
                    content: data.GSystematicMatrix ? (
                        <MatrixDisplay matrix={data.GSystematicMatrix}/>
                    ) : null
                },
                {
                    title: 'HSystematicMatrix',
                    content: data.HSystematicMatrix ? (
                        <MatrixDisplay matrix={data.HSystematicMatrix}/>
                    ) : null
                },
                {
                    title: 'Параметр n GSystematicMatrix',
                    content: data['Параметр n GSystematicMatrix'] ? data['Параметр n GSystematicMatrix'] : null
                },
                {
                    title: 'Параметр k HSystematicMatrix',
                    content: data['Параметр k HSystematicMatrix'] ? data['Параметр k HSystematicMatrix'] : null
                },
                {
                    title: 'Параметр n HSystematicMatrix',
                    content: data['Параметр n HSystematicMatrix'] ? data['Параметр n HSystematicMatrix'] : null
                },
                {
                    title: 'Параметр k GSystematicMatrix',
                    content: data['Параметр k GSystematicMatrix'] ? data['Параметр k GSystematicMatrix'] : null
                },
                {title: 'Количество исправляющих ошибок', content: data['Количество исправляющих ошибок']},
                {title: 'Количество обнаруживающих ошибок', content: data["Количество обнаруживающих ошибок p"]},
                {title: 'Минимальное расстояние Хэмминга', content: data['Минимальное расстояние Хэмминга']},

                {
                    title: 'Транспонированная проверочная систематическая матрица HSystematicMatrix',
                    content: <MatrixDisplay
                        matrix={data['Транспонированная проверочная систематическая матрица HSystematicMatrix']}/>
                },
                {
                    title: 'Таблица информационных и кодовых слов CodeTable',
                    content: <CodeTableDisplay codeTable={data["Таблица информационных и кодовых слов CodeTable"]}/>
                },
                {
                    title: 'Таблица векторов ошибок и синдромов',
                    content: <TableOfErrorVectorsAndSyndromesDisplay
                        table={data['Таблица синдромов и векторов ошибок TableOfErrorVectorsAndSyndromes']}/>
                }
            ]}
            renderItem={item =>
                item && (
                    <List.Item>
                        <Typography.Text strong>{item.title}: </Typography.Text>
                        {item.content}
                    </List.Item>
                )
            }
        />
    );
};
