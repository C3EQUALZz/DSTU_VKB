import React from 'react';
import { Row, Col } from 'antd';
import Plot from 'react-plotly.js';

export const Histogram: React.FC<HistogramProps> = ({ histogramData }) => {
    return (
        <Row justify="center" align="middle">
            {histogramData && (
                <Col span={24} style={{ justifyContent: 'center', alignItems: 'center' }}>
                    <Plot
                        data={[
                            {
                                x: histogramData.x,
                                y: histogramData.y,
                                type: 'bar',
                            }
                        ]}
                        layout={{
                            title: 'Гистограмма вероятностей символов',
                            xaxis: { title: 'Символы' },
                            yaxis: { title: 'Вероятность', range: [0, 1] },
                        }}
                        style={{ width: '100%', height: '100%' }}
                    />
                </Col>
            )}
        </Row>
    );
};
