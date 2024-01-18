 // Function to update the box plot with user input
 async function updateBoxPlot(bloodIndicator) {
    // Fetch blood indicator statistics
    var response = await fetch('/statistics/' + bloodIndicator);
    var fetchedData = await response.json();

    // Draw the box plot with fetched data and user input
    drawBoxPlot(fetchedData);
}



// Function to draw the box plot
function drawBoxPlot(data) {
    // set the dimensions and margins of the graph
    var margin = { top: 10, right: 40, bottom: 30, left: 10 },
        width = 400 - margin.left - margin.right,
        height = 200 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#box-plot")
        .html("")  // Clear previous content
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Compute summary statistics used for the box
    var q1 = data.q1;
    var median = data.median;
    var q3 = data.q3;
    var iqr = data.iqr;

    // Use lower_bound and upper_bound directly
    var min = data.lower_bound;
    var max = data.upper_bound;

    // Show the X scale with dynamic domain
    var x = d3.scaleLinear()
        .domain([min, max])
        .range([0, width]);
    svg.call(d3.axisBottom(x));

    
    var center = height / 2;
    var boxHeight = 50;

    // Show the main horizontal line
    svg.append("line")
        .attr("class", "main-line")
        .attr("y1", center)
        .attr("y2", center)
        .attr("x1", x(min))
        .attr("x2", x(max))
        .attr("stroke", "#333"); // Dark gray

    // Show the box
    svg.append("rect")
        .attr("class", "box")
        .attr("y", center - boxHeight / 2)
        .attr("x", x(q1))
        .attr("width", (x(q3) - x(q1)))
        .attr("height", boxHeight)
        .attr("stroke", "#333") // Dark gray
        .style("fill", "#ddd"); // Light gray

    // Show median, min, and max vertical lines
    svg.selectAll(".lines")
        .data([min, median, max])
        .enter()
        .append("line")
        .attr("class", "lines")
        .attr("y1", center - boxHeight / 2)
        .attr("y2", center + boxHeight / 2)
        .attr("x1", function (d) { return x(d); })
        .attr("x2", function (d) { return x(d); })
        .attr("stroke", "#666"); // Dark gray
}




let input = document.getElementById('patientIDPatientInfo');
input.addEventListener('input', async function () {
    // Get values from form inputs
    var patientID = input.value;

    // Check if there is no input
    if (!patientID) {
        // Clear patient information and blood test dates if no input
        document.getElementById('patientInfo').innerHTML = '';
        document.getElementById('blood_test_dates').innerHTML = '';
        return;
    }

    // Use JavaScript to fetch patient data
    const patientData = await fetchPatientData(patientID);

    // Display patient information
    displayPatientInfo(patientData);

    // Fetch and display blood dates
    let response = await fetch('/blood_dates?q=' + patientID);
    let dates = await response.json();

    // Create a new select element
    let select = document.createElement('select');
    select.id = 'blood_test_dropdown';
    select.classList.add('form-control', 'dropdown_item');

    // Create and add the default option
    let defaultOption = document.createElement('option');
    defaultOption.disabled = true;
    defaultOption.selected = true;
    defaultOption.textContent = 'Select Blood Test Date...';
    select.appendChild(defaultOption);

    // Add options for each date
    for (let date of dates) {
        let option = document.createElement('option');
        option.value = date.DATE;
        option.textContent = date.DATE;
        select.appendChild(option);
    }

    // Attach a change event listener to the dropdown
    select.addEventListener('change', function () {
        let selectedDate = this.value;
        if (selectedDate !== 'Select Blood Test Date...') {
            // Call the desired functions when an option is selected
            drawHeatmap(patientID, selectedDate);
            //toggleButton(selectedDate);
        }
    });

    // Add the select element to the container
    document.getElementById('blood_test_dates').innerHTML = ''; // Clear previous content
    document.getElementById('blood_test_dates').appendChild(select);
});




async function fetchPatientData(patientID) {
    const url = `/${patientID}/raw`;

    try {
        const response = await fetch(url, { method: 'POST' });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    } catch (error) {
        console.error('Error fetching patient data:', error);
        // Handle errors here, e.g., display an error message to the user
    }
}

function displayPatientInfo(data) {
    if (data && data.length > 0) {
        const patientInfo = data[0];
        const patientInfoHtml = `
            <p><strong>Patient ID:</strong> ${patientInfo.ID}</p>
            <p><strong>First Name:</strong> ${patientInfo.FIRST_NAME}</p>
            <p><strong>Last Name:</strong> ${patientInfo.LAST_NAME}</p>
            <p><strong>Birth:</strong> ${patientInfo.BIRTH_DATE}</p>
            <p><strong>Gender:</strong> ${patientInfo.GENDER}</p>
            <p><strong>Age:</strong> ${patientInfo.AGE}</p>
        `;
        document.getElementById('patientInfo').innerHTML = patientInfoHtml;
    } else {
        // Clear patient information if there's no data
        document.getElementById('patientInfo').innerHTML = '';
    }
}



let dropdown = document.getElementById('bloodIndicators');
dropdown.addEventListener('change', async function () {
    try {
        let references = await fetch('/blood_tests_references/raw/' + input.value);
        let ranges = await references.json();
        let response = await fetch('/all_blood_tests/raw/' + input.value);
        let blood_tests = await response.json();
        getValuesOverTime(blood_tests, dropdown.value, ranges);
    } catch (error) {
        console.error('Error fetching or parsing data:', error);
    }
});

let boxPlotFormCreated = false; // Use a flag to track if the form is created

function getValuesOverTime(formattedBloodTests, selectedIndicator, ranges) {
    // Filter blood tests for the selected indicator
    const filteredTests = formattedBloodTests.filter(test => selectedIndicator in test);

    // Check if the selected indicator is present in the test
    if (filteredTests.length === 0) {
        console.log('No data found for the selected indicator:', selectedIndicator);
        document.getElementById('resultsContainer').innerHTML = 'No data found for the selected indicator: ' + selectedIndicator;
        return;
    }

    // Extract dates and values for the selected indicator
    const blood_indicator_history = filteredTests.map(test => {
        return {
            DATE: test['DATE'][0],
            Value: test[selectedIndicator]
        };
    });
    const range = ranges[selectedIndicator]
   
    // Display results on the screen
    const resultContainer = document.getElementById('resultsContainer');
    //resultContainer.innerHTML = '<h4>Results overtime for ' + selectedIndicator + '</h4>';

    display_history_mean(range, blood_indicator_history, selectedIndicator)
    generateHistogram(blood_indicator_history,selectedIndicator);
    
    // Display results on the screen
    const violinPlotDiv = document.getElementById('violin_plot');
    if (!boxPlotFormCreated) {
        // Create demographic distribution elements
        const demographicDistributionDiv = document.createElement('div');
        demographicDistributionDiv.classList.add('mt-1');

        const label = document.createElement('label');
        label.classList.add('mt-1');
        label.innerHTML = '<strong>Demographic Distribution:</strong>';
        demographicDistributionDiv.appendChild(label);

        const boxPlotDiv = document.createElement('div');
        boxPlotDiv.setAttribute('id', 'box-plot');
        demographicDistributionDiv.appendChild(boxPlotDiv);

        violinPlotDiv.appendChild(demographicDistributionDiv);
        boxPlotFormCreated = true; // Set the flag to true after creating the form
    } 
    updateBoxPlot(selectedIndicator.split(" ").slice(0, -1).join(' ').trim())
   
    generateLineChart(formattedBloodTests, selectedIndicator, blood_indicators_relationships(selectedIndicator));

}

function blood_indicators_relationships(selectedIndicator){
    const bloodIndicatorRelations = {
        "Alanine aminotransferase ALT (U/L)": [],
        "Albumin (g/dL)": ["Globulin (g/dL)", "Total protein (g/dL)"],
        "Alkaline phosphatase (U/L)": ["Total calcium (mg/dL)", "Phosphorus (mg/dL)"],
        "Aspartate aminotransferase AST (U/L)": [],
        "Bicarbonate (mmol/L)": ["Chloride (mmol/L)", "Sodium (mmol/L)"],
        "Blood urea nitrogen (mg/dL)": ["Creatinine (mg/dL)"],
        "Chloride": ["Bicarbonate (mmol/L)", "Sodium (mmol/L)", "Potassium (mmol/L)"],
        "Cholesterol (mg/dL)": ["Triglycerides (mg/dL)"],
        "Creatine Phosphokinase (CPK) (IU/L)": ["Lactate Dehydrogenase (U/L)"],
        "Creatinine": ["Blood urea nitrogen (mg/dL)"],
        "Gamma Glutamyl Transferase": [],
        "Globulin": ["Albumin (g/dL)", "Total protein (g/dL)"],
        "Glucose, Serum": [],
        "Iron, Refrigerated": [],
        "Lactate Dehydrogenase": ["Creatine Phosphokinase (CPK) (IU/L)"],
        "Osmolality": [],
        "Phosphorus": ["Alkaline phosphatase (U/L)"],
        "Potassium": ["Sodium (mmol/L)", "Chloride (mmol/L)"],
        "Sodium": ["Chloride (mmol/L)", "Bicarbonate (mmol/L)", "Potassium (mmol/L)"],
        "Total Bilirubin": [],
        "Total calcium (mg/dL)": ["Alkaline phosphatase (U/L)", "Phosphorus (mg/dL)"],
        "Total Protein": ["Albumin (g/dL)", "Globulin (g/dL)"],
        "Triglycerides": ["Cholesterol (mg/dL)"],
        "Uric Acid": ["Potassium (mmol/L)", "Sodium (mmol/L)", "Chloride (mmol/L)"]
      };
      
      return bloodIndicatorRelations[selectedIndicator];    
}

function display_history_mean(referenceRange, blood_indicator_history, selectedIndicator) {
    // Calculate the mean of the blood indicator values
    const values = blood_indicator_history.map(entry => entry.Value[0]);
    
    // Display the mean and reference range in the "mean" div
    const blood_indicator = document.getElementById('blood_indicator');
    blood_indicator.innerHTML = `
        <h5>${selectedIndicator}</h5>
        <p><strong>Reference Range:</strong> ${referenceRange.min.toFixed(2)} - ${referenceRange.max.toFixed(2)}</p>
    `;
}


function generateHistogram(data, selectedIndicator) {
d3.select('#histogram').selectAll('*').remove();

// Set up margin, width, and height
const margin = { top: 50, right: 20, bottom: 100, left: 40 };
const width = 700 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

// Create SVG element
const svg = d3.select("#histogram")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Extract unique values for color mapping
const uniqueColors = Array.from(new Set(data.map(entry => entry.Value[1])));

// Define color scale
const colorScale = d3.scaleOrdinal()
    .domain(['green', 'yellow', 'red'])
    .range(['green', '#ffd800', '#c80815']);

// Set up X and Y scales
const xScale = d3.scaleBand()
    .domain(data.map(entry => entry.DATE))
    .range([0, width])
    .padding(0.1); // Adjust the padding as needed

const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, entry => entry.Value[0])])
    .range([height, 0]);

// Add X-axis
svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale))
    .selectAll("text")
    .style("text-anchor", "end")
    .attr("transform", "rotate(-45)")
    .attr("dy", ".35em")
    .attr("dx", "-.8em")
    .style("font-size", "12px");

// Add Y-axis
svg.append("g")
    .call(d3.axisLeft(yScale))
    .selectAll("text")
    .style("font-size", "12px");

// Add title
svg.append("text")
    .attr("x", width / 2)
    .attr("y", 0 - margin.top / 2)
    .attr("text-anchor", "middle")
    .style("font-size", "16px")
    .text(`${selectedIndicator} Over Time`);

// Calculate bar width based on available space, but limit to a maximum width
const maxBarWidth = 90; // Set a maximum width for the bars
const barWidth = Math.min(xScale.bandwidth(), maxBarWidth);

// Add bars
svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", entry => xScale(entry.DATE) + (xScale.bandwidth() - barWidth) / 2)
    .attr("y", entry => yScale(entry.Value[0]))
    .attr("width", barWidth)
    .attr("height", entry => height - yScale(entry.Value[0]))
    .attr("fill", entry => colorScale(entry.Value[1]));

// Add labels for each bar
svg.selectAll(".bar-label")
    .data(data)
    .enter().append("text")
    .attr("class", "bar-label")
    .attr("x", entry => xScale(entry.DATE) + xScale.bandwidth() / 2)
    .attr("y", entry => yScale(entry.Value[0]) - 5)
    .attr("text-anchor", "middle")
    .style("font-size", "12px")
    .text(entry => entry.Value[0]);
}

function drawHeatmap(patientID, date) {

    // Remove existing SVG element
    d3.select('#heatmap').selectAll('*').remove();
    d3.select('#date').remove();
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
            
        const combined_dict = data; 
        // Convert data to suitable format
        const dataArray = [];
        const dict = data; // Assuming there's only one dictionary in the list

        // Iterate over the dictionary entries
        for (const [key, [value, color]] of Object.entries(dict)) {
            dataArray.push({ key, value, color });
        }

    
        // Define margin and cell size
        const margin = { top: 10, right: 0, bottom: 20, left: 10};
        const cellSize = 30;
        const cellWidth = 250;
        const cellHeight = 25;

        d3.select('#date').text(`Blood test: ${date}`);
        // Create SVG element
        const svg = d3.select('#heatmap').append('svg')
            .attr('width', 600) // Increased width to accommodate values on the right
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
            .attr('x', margin.left + cellWidth / 2) // Place text in the center of the cell
            .attr('y', (d, i) => margin.top + (i + 0.5) * cellHeight) // Use the center of each cell
            .attr('dy', '0.10em')
            .style('text-anchor', 'middle') // Center the text horizontally
            .style('alignment-baseline', 'middle')
            .style('fill', 'black')
            .text(function (d) {
                // Extract and display only the relevant part of the key
                const words = d.key.split(/\s+/);
                const keyWithoutUnits = words.slice(0, -1).join(' '); // Exclude the last word (metric unit)
                return keyWithoutUnits;
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
        svg.selectAll('.value-text')
        .data(dataArray)
        .enter().append('text')
        .attr('class', 'value-text')
        .attr('x', margin.left + cellWidth + 10)
        .attr('y', (d, i) => margin.top + i * cellHeight + cellHeight / 2)
        .attr('dy', '0.20em')
        .style('fill', 'black')
        .text(d => `${d.value} ${d.key.split(/\s+/).pop()}`); 

        

    })
    .catch(error => {
        console.error('Error fetching data:', error);
        // Add error handling here, e.g., display an error message to the user
    });
}


function generateLineChart(data, selectedIndicator, Indicators) {
    // Clear existing content in the 'linechart' div
    d3.select('#linechart').selectAll('*').remove();

    // Set up margin, width, and height
    const margin = { top: 50, right: 20, bottom: 100, left: 40 };
    const width = 700 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Create SVG element
    const svg = d3.select("#linechart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Extract dates from data
    const dates = data.map(entry => entry['DATE'][0]);

    // Create a color scale based on the provided colors in the data
    const colorScale = d3.scaleOrdinal()
        .domain(Indicators)
        .range(['#3498db', '#ffd800', '#c0392b']);

        if (Indicators.length > 0) {
            // Create a line for each indicator
            Indicators.forEach((indicator, index) => {
                const values = data.map(entry => entry[indicator][0]);
        
                const line = d3.line()
                    .x((d, i) => i * (width / (dates.length - 1)))
                    .y(d => height - (d * (height / d3.max(data, entry => entry[indicator][0]))));
        
                // Add line
                svg.append('path')
                    .datum(values)
                    .attr('fill', 'none')
                    .attr('stroke', colorScale(indicator))
                    .attr('stroke-width', 2)
                    .attr('d', line);
        
                // Add label text with dynamic y-position
                svg.append('text')
                    .attr('x', width / 2)  // Adjust the x-position as needed
                    .attr('y', (index + 1) * 20)  // Space out labels vertically
                    .attr('dy', '1em')
                    .style('font-size', '12px')
                    .style('text-anchor', 'middle')
                    .style('fill', colorScale(indicator))
                    .text(indicator);
            });
        } else {
            // Display only the selected indicator if Indicators is empty
            const values = data.map(entry => entry[selectedIndicator][0]);
        
            const line = d3.line()
                .x((d, i) => i * (width / (dates.length - 1)))
                .y(d => height - (d * (height / d3.max(data, entry => entry[selectedIndicator][0]))));
        
            // Add line
            svg.append('path')
                .datum(values)
                .attr('fill', 'none')
                .attr('stroke', colorScale(selectedIndicator))
                .attr('stroke-width', 2)
                .attr('d', line);
        
            // Add label text at a fixed position above the line
            svg.append('text')
                .attr('x', width / 2)  // Adjust the x-position as needed
                .attr('y', 20)  // Place the label above the chart
                .attr('dy', '1em')
                .style('font-size', '12px')
                .style('text-anchor', 'middle')
                .style('fill', colorScale(selectedIndicator))
                .text(selectedIndicator);
        }

    // Add X axis
    svg.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(d3.scalePoint().domain(dates).range([0, width])));

    // Add Y axis
    svg.append('g')
        .call(d3.axisLeft(d3.scaleLinear().domain([0, d3.max(data, entry => entry[selectedIndicator][0])]).range([height, 0])));
}
