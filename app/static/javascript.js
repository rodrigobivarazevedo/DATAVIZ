let input = document.getElementById('patientID');
    input.addEventListener('input', async function () {
        let response = await fetch('/blood_dates?q=' + input.value);
        let dates = await response.json();
        let html = '';
        for (let date of dates) {
            // Add a button element with an onclick event to handle the HTTP request
            html += `<li><button class="date-button" onclick="drawHeatmap('${input.value}', '${date.DATE}'); return false;">${date.DATE}</button></li>`;
        }
        document.querySelector('ul').innerHTML = html;
    });


    function drawHeatmap(patientID, date) {

        // Remove existing SVG element
        d3.select('#heatmap').selectAll('*').remove();

        fetch(`/blood_tests/raw/${patientID}?date=${date}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
                
            })
            .then(data => {
                 
            // Convert data to suitable format
            const dataArray = [];
            const dict = data[0]; // Assuming there's only one dictionary in the list
            drawPieChart(dict)

            for (const key in dict) {
                const [value, color] = dict[key];
                dataArray.push({ value, color, key });
            }

            // Define margin and cell size
            const margin = { top: 20, right: 250, bottom: 20, left: 275 };
            const cellSize = 30;
            const cellWidth = 200;
            const cellHeight = 30;

            // Create SVG element
            const svg = d3.select('#heatmap').append('svg')
                .attr('width', 1000) // Increased width to accommodate values on the right
                .attr('height', dataArray.length * cellHeight + margin.top + margin.bottom)
                .style('margin', margin.top + 'px ' + margin.right + 'px ' + margin.bottom + 'px ' + margin.left + 'px');

            // Define color scale based on color strings
            const colorScale = d3.scaleOrdinal()
                .domain(['green', 'yellow', 'red'])
                .range(['green', '#ffd800', '#c80815']);

            // Draw cells
            svg.selectAll('rect')
                .data(dataArray)
                .enter().append('rect')
                .attr('x', margin.left)
                .attr('y', (d, i) => margin.top + i * cellHeight)
                .attr('width', cellWidth)
                .attr('height', cellHeight)
                .style('fill', d => colorScale(d.color))
                .on('mouseover', function (event, d) {
                    // Display blood level on mouse hover
                    d3.select(this).append('title').text(`Blood Level: ${d.value}`);
                });

            // Add y-axis labels with word wrapping
            svg.selectAll('text')
                .data(dataArray)
                .enter().append('text')
                .attr('x', margin.left - 10)
                .attr('y', (d, i) => margin.top + i * cellHeight + cellHeight / 2)
                .attr('dy', '0.35em')
                .style('text-anchor', 'end')
                .style('alignment-baseline', 'middle')
                .style('fill', 'black')
                .text(function (d) {
                    // Split and wrap text to fit in the available space
                    const words = d.key.split(/\s+/);
                    let line = '';
                    const lines = [];
                    const lineHeight = 1.1; // ems

                    for (const word of words) {
                        const testLine = line.length === 0 ? word : `${line} ${word}`;
                        const metrics = this.getComputedTextLength();
                        if (metrics > margin.left - 10 && line.length > 0) {
                            lines.push(line);
                            line = word;
                        } else {
                            line = testLine;
                        }
                    }

                    lines.push(line);
                    return lines.join('\n');
                });

            // Draw black lines between cells
            svg.selectAll('line')
                .data(dataArray)
                .enter().append('line')
                .attr('x1', margin.left)
                .attr('x2', margin.left + cellWidth)
                .attr('y1', (d, i) => margin.top + (i + 1) * cellHeight)
                .attr('y2', (d, i) => margin.top + (i + 1) * cellHeight)
                .style('stroke', 'black');

            // Add text elements to display values and metric units on the right side of the heatmap
            // Add text elements to display values and metric units on the right side of the heatmap
            svg.selectAll('.value-text')
            .data(dataArray)
            .enter().append('text')
            .attr('class', 'value-text')
            .attr('x', margin.left + cellWidth + 10)
            .attr('y', (d, i) => margin.top + i * cellHeight + cellHeight / 2)
            .attr('dy', '0.35em')
            .style('fill', 'black')
            .text(d => `${d.value} ${d.key.split(/\s+/).pop()}`); // Only display the last part of the key

        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Add error handling here, e.g., display an error message to the user
        });
}

    function searchPatient() {
        // Get values from form inputs
        var patientID = document.getElementById('patientIDPatientInfo').value;

        // Use JavaScript to fetch data from the Flask route
        const url = `/${patientID}/raw`;

        fetch(url, {
            method: 'POST', // Use POST method
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(data);

                // Check if data is not an empty list
                if (data.length > 0) {
                    const patientInfo = data[0]; // Assuming there's only one element in the list

                    // Construct HTML to display patient information
                    const patientInfoHtml = `
                        <p><strong>Patient ID:</strong> ${patientInfo.ID}</p>
                        <p><strong>First Name:</strong> ${patientInfo.FIRST_NAME}</p>
                        <p><strong>Last Name:</strong> ${patientInfo.LAST_NAME}</p>
                        <p><strong>Birth Date:</strong> ${patientInfo.BIRTH_DATE}</p>
                        <p><strong>Gender:</strong> ${patientInfo.GENDER}</p>
                        <p><strong>Age:</strong> ${patientInfo.AGE}</p>
                    `;

                    // Display patient information in the HTML
                    document.getElementById('patientInfo').innerHTML = patientInfoHtml;
                } else {
                    // Handle the case where the data list is empty
                    console.error('Empty response data.');
                }
            })
            .catch(error => {
                console.error('Error fetching patient data:', error);
                // Add error handling here, e.g., display an error message to the user
            });
    }

    function calculateColorPercentages(blood_test) {
    let green = 0.0;
    let yellow = 0.0;
    let red = 0.0;

    // Iterate over the properties of the blood_test object
    for (const key of Object.keys(blood_test)) {
        const color = blood_test[key][1];

        if (color === "green") {
            green += 1;
        }
        if (color === "yellow") {
            yellow += 1;
        }
        if (color === "red") {
            red += 1;
        }
    }

    const totalIndicators = 37;
    const percentages = [green / totalIndicators, yellow / totalIndicators, red / totalIndicators];

    return percentages;
}




    function drawPieChart(data) {
        d3.select('#pieChart').selectAll('*').remove();
        const percentages = calculateColorPercentages(data);

        const width = 300;
        const height = 300;
        const radius = Math.min(width, height) / 2;

        const color = d3.scaleOrdinal()
            .domain(['Green', 'Yellow', 'Red'])
            .range(['green', '#ffd800', '#c80815']);

        const pie = d3.pie()
            .value(d => d)
            .sort(null);

        const arc = d3.arc()
            .innerRadius(0)
            .outerRadius(radius);

        const svg = d3.select("#pieChart")
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", `translate(${width / 2},${height / 2})`);

        const dataValues = Object.values(percentages);

        const chartData = pie(dataValues);

        const path = svg.selectAll("path")
            .data(chartData)
            .enter()
            .append("path")
            .attr("d", arc)
            .attr("fill", (d, i) => color(i));

        // Add percentage labels
        svg.selectAll("text")
            .data(chartData)
            .enter()
            .append("text")
            .text((d, i) => `${(percentages[i] * 100).toFixed(2)}%`)
            .attr("transform", d => `translate(${arc.centroid(d)})`)
            .style("text-anchor", "middle")
            .style("fill", "black");

        // Add legend
        const legend = svg.selectAll(".legend")
            .data(color.domain())
            .enter()
            .append("g")
            .attr("class", "legend")
            .attr("transform", (d, i) => `translate(0,${i * 20})`);

        legend.append("rect")
            .attr("x", width - 18)
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", color);

        legend.append("text")
            .attr("x", width - 24)
            .attr("y", 9)
            .attr("dy", ".35em")
            .style("text-anchor", "end")
            .text(d => d);
    }
