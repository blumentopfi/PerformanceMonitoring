//Create horizontalBar plug-in for ChartJS
  var originalLineDraw = Chart.controllers.bar.prototype.draw;
  Chart.helpers.extend(Chart.controllers.bar.prototype, {
      draw: function () {
          originalLineDraw.apply(this, arguments);
          var chart = this.chart;
          var ctx = chart.chart.ctx;
          var index = chart.config.options.lineAtIndex;

          if (index) {
              var xaxis = chart.scales['x-axis-0'];
              var yaxis = chart.scales['y-axis-0'];
              var x1 =  yaxis.width ;
              var y1 =  yaxis.getPixelForValue(index);
              var x2 = xaxis.width + yaxis.width;
              var y2 = yaxis.getPixelForValue(index);
              ctx.save();
              ctx.beginPath();
              ctx.moveTo(x1, y1);
              ctx.strokeStyle = 'red';
              ctx.lineTo(x2, y2);
              ctx.stroke();

              ctx.restore();
          }
      }
  });