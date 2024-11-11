import {Table} from "antd";
import React from "react";

interface TableOfErrorVectorsAndSyndromesDisplayProps {
    table: {
        errors: number[][];
        syndromes: number[][];
    };
}

export const TableOfErrorVectorsAndSyndromesDisplay: React.FC<TableOfErrorVectorsAndSyndromesDisplayProps> = ({table}) => {
    const columns = [
        {title: 'Errors', dataIndex: 'errors', key: 'errors', render: (text: number[]) => text.join(', ')},
        {title: 'Syndromes', dataIndex: 'syndromes', key: 'syndromes', render: (text: number[]) => text.join(', ')},
    ];

    const dataSource = table.errors.map((error, i) => ({
        key: i,
        errors: error,
        syndromes: table.syndromes[i],
    }));

    return <Table columns={columns} dataSource={dataSource} pagination={false} size="small"/>
}