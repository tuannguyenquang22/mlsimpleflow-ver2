import React from 'react';
import Chart from 'react-apexcharts';


function normalize(value, minVal, maxVal) {
    if (maxVal === minVal) {
        return 0.5; // trường hợp toàn bộ giá trị giống nhau, đặt giữa khoảng
    }
    return (value - minVal) / (maxVal - minVal);
}


function TuneHistoryChart({ history }) {
    const paramKeys = Object.keys(history[0].params);
    const allParams = [...paramKeys, 'score'];

    const minMax = {};
    for (let p of allParams) {
        let values;
        if (p === 'score') {
            values = history.map(h => h.score);
        } else {
            values = history.map(h => h.params[p]);
        }
        const minVal = Math.min(...values);
        const maxVal = Math.max(...values);
        minMax[p] = { min: minVal, max: maxVal };
    }

    const series = history.map((h, i) => {
        const data = allParams.map(p => {
            const val = p === 'score' ? h.score : h.params[p];
            const normVal = normalize(val, minMax[p].min, minMax[p].max);
            return {
                x: p,
                y: normVal,
                original: val // lưu giá trị gốc để hiển thị tooltip
            };
        });

        return {
            name: `Trial ${i + 1}`,
            data: data
        };
    });

    const categories = [...paramKeys, 'score'];

    const options = {
        chart: {
            type: 'line',
            height: 350
        },
        xaxis: {
            categories: allParams,
            title: { text: 'Parameters & Score' }
        },
        yaxis: {
            title: { text: 'Normalized Value' },
            min: 0,
            max: 1,
            show: false
        },
        stroke: {
            width: 2 // đường mảnh hơn
        },
        markers: {
            size: 3
        },
        legend: {
            show: true
        },
        tooltip: {
            shared: false,
            intersect: true,
            custom: function ({ series, seriesIndex, dataPointIndex, w }) {
                const dp = w.config.series[seriesIndex].data[dataPointIndex];
                const paramName = dp.x;
                const origVal = dp.original;
                return `
              <div style="padding:10px;">
                <div><strong>${w.config.series[seriesIndex].name}</strong></div>
                <div>Param/Score: ${paramName}</div>
                <div>Value: ${origVal}</div>
              </div>
            `;
            }
        },
        title: {
            text: 'Hyperparameter Tuning History',
            align: 'left'
        }
    };

    return <Chart options={options} series={series} type="line" height={350} />;
}

export default TuneHistoryChart;
