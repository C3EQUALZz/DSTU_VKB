import {Table} from "antd";
import React from "react";

interface CodeTableDisplayProps {
    codeTable: {
        information_words_column: number[][];
        code_words_column: number[][];
        hamming_weights_column: number[];
    };
}

export const CodeTableDisplay: React.FC<CodeTableDisplayProps> = ({codeTable}) => {
    const columns = [
        {
            title: 'Information Words',
            dataIndex: 'information_words_column',
            key: 'information_words_column',
            render: (text: number[]) => text.join(', ')
        },
        {
            title: 'Code Words',
            dataIndex: 'code_words_column',
            key: 'code_words_column',
            render: (text: number[]) => text.join(', ')
        },
        {title: 'Hamming Weights', dataIndex: 'hamming_weights_column', key: 'hamming_weights_column'},
    ];

    const dataSource = codeTable.information_words_column.map((infoWord, i) => ({
        key: i,
        information_words_column: infoWord,
        code_words_column: codeTable.code_words_column[i],
        hamming_weights_column: codeTable.hamming_weights_column[i],
    }));

    return <Table columns={columns} dataSource={dataSource} pagination={false} size="small"/>;
};