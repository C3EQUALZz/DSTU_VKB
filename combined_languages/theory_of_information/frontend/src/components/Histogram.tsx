import React from 'react';
import { Row, Col } from 'antd';
import Plot from 'react-plotly.js';

export const Histogram: React.FC<HistogramProps> = ({ histogramData }) => {
    return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            {histogramData && (
                <Row gutter={16} style={{ width: '100%', height: '100%' }}>
                    <Col span={24} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                        <Plot
                            data={[
                                {
                                    x: histogramData.x,
                                    y: histogramData.y,
                                    type: 'scatter',
                                    mode: 'markers',
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
                </Row>
            )}
        </div>
    );
};
