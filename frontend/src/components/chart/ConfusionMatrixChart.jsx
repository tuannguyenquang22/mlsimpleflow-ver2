import React from 'react';
import Chart from 'react-apexcharts';
import { computeConfusionMatrixMulticlass } from '../../utils/compute';


function ConfusionMatrixChart({ target_true, target_pred }) {
    const { matrix, classes } = computeConfusionMatrixMulticlass(target_true, target_pred);
    const series = classes.map((actualClass, i) => ({
        name: `Actual ${actualClass}`,
        data: matrix[i]
    }));

    const maxValue = Math.max(...matrix.flat());

    const options = {
        chart: {
            type: 'heatmap',
            height: 350
        },
        plotOptions: {
            heatmap: {
                shadeIntensity: 0.5,
                colorScale: {
                    ranges: [{
                        from: 0,
                        to: maxValue,
                        color: '#008FFB'
                    }]
                }
            }
        },
        xaxis: {
            categories: classes.map(c => `Pred ${c}`)
        },
        yaxis: {
            labels: {
                show: true
            }
        },
        dataLabels: {
            enabled: true
        },
        title: {
            text: 'Confusion Matrix (Multiclass)'
        }
    };

    return <Chart options={options} series={series} type="heatmap" height={350} />;
};

export default ConfusionMatrixChart;