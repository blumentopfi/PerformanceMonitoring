var MyBarChartMethods = {
    // sort a dataset
    sort: function (chart, datasetIndex) {
        var data = []
        chart.datasets.forEach(function (dataset, i) {
            dataset.bars.forEach(function (bar, j) {
                if (i === 0) {
                    data.push({
                        label: chart.scale.xLabels[j],
                        values: [bar.value]
                    })
                } else 
                    data[j].values.push(bar.value)
            });
        })

        data.sort(function (a, b) {
            if (a.values[datasetIndex] > b.values[datasetIndex])
                return -1;
            else if (a.values[datasetIndex] < b.values[datasetIndex])
                return 1;
            else
                return 0;
        })

        chart.datasets.forEach(function (dataset, i) {
            dataset.bars.forEach(function (bar, j) {
                if (i === 0)
                    chart.scale.xLabels[j] = data[j].label;
                bar.label = data[j].label;
                bar.value = data[j].values[i];
            })
        });
        chart.update();
    },
    // reload data
    reload: function (chart, datasetIndex, labels, values) {
        var diff = chart.datasets[datasetIndex].bars.length - values.length;
        if (diff < 0) {
            for (var i = 0; i < -diff; i++)
                chart.addData([0], "");
        } else if (diff > 0) {
            for (var i = 0; i < diff; i++)
                chart.removeData();
        }

        chart.datasets[datasetIndex].bars.forEach(function (bar, i) {
            chart.scale.xLabels[i] = labels[i];
            bar.value = values[i];
        })
        chart.update();
    }
}