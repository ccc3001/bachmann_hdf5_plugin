def import_graph_lib(x,y):
    return [
        """
canvas {
      border: 1px solid #ccc;
      margin: 40px auto;
      display: block;
      outline: none;
       border: none;
    }

""",
"""<canvas id="graphCanvas" width="600" height="400"></canvas>"""
,
f"""<script>
  const xValues = {x};
  const yValues = {y};

  const canvas = document.getElementById('graphCanvas');
  const ctx = canvas.getContext('2d');

  const padding = 50;
  const width = canvas.width - padding * 2;
  const height = canvas.height - padding * 2;

  const minX = Math.min(...xValues);
  const maxX = Math.max(...xValues);
  const minY = Math.min(...yValues);
  const maxY = Math.max(...yValues);

  // Transform data point to canvas coordinates
  function getCanvasCoords(x, y) {{
    const xNorm = (x - minX) / (maxX - minX);
    const yNorm = (y - minY) / (maxY - minY);
    return {{
      x: padding + xNorm * width,
      y: canvas.height - padding - yNorm * height
  }};
  }}

  // Draw axes
  function drawAxes() {{
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.stroke();
  }}

  // Draw grid and labels
  function drawGrid() {{
    ctx.fillStyle = '#000';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';

    // X-axis labels
    xValues.forEach(x => {{
      const pt = getCanvasCoords(x, minY);
      ctx.fillText(x, pt.x, canvas.height - padding + 15);
    }});

    // Y-axis labels
    const ySteps = 5;
    for (let i = 0; i <= ySteps; i++) {{
      const y = minY + (i * (maxY - minY)) / ySteps;
      const pt = getCanvasCoords(minX, y);
      ctx.fillText(y.toFixed(2), padding - 25, pt.y + 3);
    }}
  }}

  // Draw line graph
  function drawLine() {{
    ctx.beginPath();
    xValues.forEach((x, i) => {{
      const pt = getCanvasCoords(x, yValues[i]);
      if (i === 0) ctx.moveTo(pt.x, pt.y);
      else ctx.lineTo(pt.x, pt.y);
    }});
    ctx.strokeStyle = 'blue';
    ctx.lineWidth = 2;
    ctx.stroke();
  }}

  // Draw data points
  function drawPoints() {{
    ctx.fillStyle = 'red';
    xValues.forEach((x, i) => {{
      const pt = getCanvasCoords(x, yValues[i]);
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, 4, 0, 2 * Math.PI);
      ctx.fill();
    }});
  }}
  function drawAxisLabels() {{
  ctx.fillStyle = '#000';
  ctx.font = '14px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  // X axis label
  ctx.fillText('X Axis', canvas.width / 2, canvas.height - padding + 35);

  // Y axis label (rotated)
  ctx.save(); // Save current canvas state
  ctx.translate(padding - 40, canvas.height / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText('Y Axis', 0, 0);
  ctx.restore(); // Restore original state
  }}

  // Render graph
  drawAxes();
  drawGrid();
  drawLine();
  drawPoints();
  drawAxisLabels(); 
</script>"""]


def import_avg_plot_basics():
    return ["""  
    .scale-wrapper {
      position: relative;
      width: 400px;
      margin: 60px auto;
      font-family: Arial, sans-serif;
    }

    .scale-container {
      position: relative;
      width: 100%;
      height: 20px;
      background: #ddd;
      border-radius: 10px;
    }

    .scale-soft-range {
      position: absolute;
      top: 0;
      height: 20px;
      background: #8bc34a;
      border-radius: 10px;
    }

    .scale-marker {
      position: absolute;
      top: -10px;
      width: 2px;
      height: 40px;
      background: #333;
    }

    .soft-min-marker { background: orange; }
    .soft-max-marker { background: blue; }
    .avg-marker      { background: purple; }

    .label-row {
      position: relative;
      height: 20px;
      margin-top: 8px; /* spacing between scale and labels */
    }

    .label {
      position: absolute;
      font-size: 12px;
      transform: translateX(-50%);
      white-space: nowrap;
    }
"""
,
"""
<script>
  function createScale({ hardMin, hardMax, softMin, softMax, avg, containerId }) {
    softMin =parseFloat(softMin.toFixed(2));
    softMax=parseFloat(softMax.toFixed(2));
    avg=parseFloat(avg.toFixed(2));
    
    const wrapper = document.getElementById(containerId);

    const valueToPercent = val => ((val - hardMin) / (hardMax - hardMin)) * 100;

    // === Scale container ===
    const scale = document.createElement('div');
    scale.className = 'scale-container';

    const softRange = document.createElement('div');
    softRange.className = 'scale-soft-range';
    softRange.style.left = valueToPercent(softMin) + '%';
    softRange.style.width = (valueToPercent(softMax) - valueToPercent(softMin)) + '%';
    scale.appendChild(softRange);

    // Add markers
    const markerData = [
      { val: softMin, className: 'soft-min-marker' },
      { val: softMax, className: 'soft-max-marker' },
      { val: avg,     className: 'avg-marker' }
    ];

    markerData.forEach(({ val, className }) => {
      const marker = document.createElement('div');
      marker.className = `scale-marker ${className}`;
      marker.style.left = valueToPercent(val) + '%';
      scale.appendChild(marker);
    });

    wrapper.appendChild(scale);

    // === Label row below ===
    const labelRow = document.createElement('div');
    labelRow.className = 'label-row';

    markerData.forEach(({ val, className }) => {
      const label = document.createElement('div');
      label.className = 'label';
      label.style.left = valueToPercent(val) + '%';
      label.textContent = `${className.includes('min') ? 'Min' : className.includes('max') ? 'Max' : 'Avg'}: ${val}`;
      labelRow.appendChild(label);
    });

    wrapper.appendChild(labelRow);
  }
</script>
  """]

def import_avg_plot(minimum,maximum,average,container_name):
    return [f"""
    <div class="scale-wrapper" id="{container_name}"></div>
    """,
    f"""
    <script>
      createScale({{hardMin: 1, hardMax: 50, softMin: {minimum}, softMax: {maximum}, avg: {average}, containerId: '{container_name}'}});
    </script>
    """]




def import_print_button()
  return ["""
  button.print-button {
  width: 100px;
  height: 100px;
}
span.print-icon, span.print-icon::before, span.print-icon::after, button.print-button:hover .print-icon::after {
  border: solid 4px #333;
}
span.print-icon::after {
  border-width: 2px;
}

button.print-button {
  position: relative;
  padding: 0;
  border: 0;
  
  border: none;
  background: transparent;
}

span.print-icon, span.print-icon::before, span.print-icon::after, button.print-button:hover .print-icon::after {
  box-sizing: border-box;
  background-color: #fff;
}

span.print-icon {
  position: relative;
  display: inline-block;  
  padding: 0;
  margin-top: 20%;

  width: 60%;
  height: 35%;
  background: #fff;
  border-radius: 20% 20% 0 0;
}

span.print-icon::before {
  content: "";
  position: absolute;
  bottom: 100%;
  left: 12%;
  right: 12%;
  height: 110%;

  transition: height .2s .15s;
}

span.print-icon::after {
  content: "";
  position: absolute;
  top: 55%;
  left: 12%;
  right: 12%;
  height: 0%;
  background: #fff;
  background-repeat: no-repeat;
  background-size: 70% 90%;
  background-position: center;

}

button.print-button:hover {
  cursor: pointer;
}

button.print-button:hover .print-icon::before {
  height:0px;
  transition: height .2s;
}
  """ ,"""
  <div class="content">
<button href="#" id="print" class="print-button"><span class="print-icon"></span> <a href="#" id="print"></a></button>
  """
  ,"""
  <script>
  document.addEventListener("DOMContentLoaded", () => {
    let printLink = document.getElementById("print");
    let container = document.getElementById("container");

    printLink.addEventListener("click", event => {
        event.preventDefault();
        printLink.style.display = "none";
        window.print();
        printLink.style.display = "flex";
    }, false);
}, false);
</script>
  """]


