function drawMultiHeatmap(patientData) {
    // Remove existing SVG element
    d3.select('#heatmaps').selectAll('*').remove();
    d3.select('#date').remove();

    // Convert data to suitable format
    const dataArray = [];

    // Use the first entry in patientData to get blood indicator keys
    const firstEntry = patientData[0];
    const bloodIndicatorKeys = Object.keys(firstEntry).filter(key => key !== 'DATE' && key !== 'Indicator not found in the reference');

    // Iterate over each blood test entry
    patientData.forEach(test => {
        const date = test['DATE'][0];

        // Iterate over the blood indicators
        bloodIndicatorKeys.forEach(key => {
            const value = test[key][0];
            const color = test[key][1];
            dataArray.push({ date, indicator: key, value, color });
        });
    });

    // Define margin and cell size
    const margin = { top: 20, right: 300, bottom: 10, left: 5 }; // Increased top margin and added right margin
    const cellSize = 30;
    const cellWidth = 80; // Adjust the width based on your preference
    const cellHeight = 25;

    // Extract unique indicators and dates
    const uniqueIndicators = Array.from(new Set(dataArray.map(d => d.indicator)));
    const uniqueDates = Array.from(new Set(dataArray.map(d => d.date)));

    // Create SVG element
    const svg = d3.select('#heatmaps').append('svg')
        .attr('width', uniqueDates.length * cellWidth + margin.left + margin.right)
        .attr('height', uniqueIndicators.length * cellHeight + margin.top + margin.bottom)
        .style('margin', margin.top + 'px ' + margin.right + 'px ' + margin.bottom + 'px ' + margin.left + 'px');

    // Define color scale based on color strings
    const colorScale = d3.scaleOrdinal()
        .domain(['green', 'yellow', 'red'])
        .range(['green', '#ffd800', '#c80815']);

    // create a tooltip
    const tooltip = d3.select("#heatmaps")
        .append("div")
        .style("opacity", 1)
        .attr("class", "tooltip")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "2px")
        .style("border-radius", "5px")
        .style("padding", "5px");

    // Add the squares
    svg.selectAll('rect')
        .data(dataArray)
        .enter().append('rect')
        .attr('x', d => uniqueDates.indexOf(d.date) * cellWidth + margin.left)
        .attr('y', d => uniqueIndicators.indexOf(d.indicator) * cellHeight + margin.top)
        .attr('width', cellWidth)
        .attr('height', cellHeight)
        .style('fill', d => colorScale(d.color))
        .style('stroke', 'none')  // Removed stroke
        .style('opacity', 2)
        .on('mouseover', function (event, d) {
            tooltip
                .style('opacity', 2)
                .html(`Blood Level: ${d.value}`)
                .style('left', (event.pageX + 5) + 'px') // Adjusted tooltip position
                .style('top', (event.pageY - 10) + 'px'); // Adjusted tooltip position
            d3.select(this)
                .style('stroke', 'black')
                .style('stroke-width', 2); // Increased border width
        })
        .on('mousemove', function (event, d) {
            tooltip
                .style('left', (event.pageX + 5) + 'px') // Adjusted tooltip position
                .style('top', (event.pageY - 10) + 'px'); // Adjusted tooltip position
        })
        .on('mouseleave', function (event, d) {
            tooltip
                .style('opacity', 0);
            d3.select(this)
                .style('stroke', 'none'); // Reset stroke
        });

    // Add y-axis labels with word wrapping on the right side
    svg.selectAll('text.indicator')
        .data(uniqueIndicators)
        .enter().append('text')
        .attr('class', 'indicator')
        .attr('x', uniqueDates.length * cellWidth + margin.left + 5) // Adjusted x position
        .attr('y', (d, i) => i * cellHeight + margin.top + cellHeight / 2)
        .attr('dy', '0.10em')
        .style('text-anchor', 'start') // Adjusted text-anchor
        .style('alignment-baseline', 'middle')
        .style('fill', 'black')
        .style('font-size', '15px') // Adjust the font size
        .text(function (d) {
            return d;
        });

    // Draw black lines between cells vertically (for each date)
    uniqueDates.forEach((date, i) => {
        svg.append('line')
            .attr('x1', i * cellWidth + margin.left)
            .attr('x2', i * cellWidth + margin.left)
            .attr('y1', margin.top)
            .attr('y2', uniqueIndicators.length * cellHeight + margin.top)
            .style('stroke', 'black');
    });

    // Draw x-axis labels (dates) on top with rotation
    svg.selectAll('text.date')
        .data(uniqueDates)
        .enter().append('text')
        .attr('class', 'date')
        .attr('x', (d, i) => i * cellWidth + margin.left + cellWidth / 2)
        .attr('y', margin.top - 5)
        .attr('dy', '0.10em')
        .style('text-anchor', 'middle')
        .style('alignment-baseline', 'middle')
        .style('fill', 'black')
        .style('font-size', '12px') // Adjust the font size
        .attr('transform', (d, i) => `rotate(-45, ${i * cellWidth + margin.left + cellWidth / 2}, ${margin.top - 5})`) // Rotate labels
        .text(function (d) {
            return d;
        });
}





function displayRedBloodIndicatorInfo(redIndicators) {
    // Define information for each blood indicator
    const bloodIndicatorKnowledgeBase = {
        "Alanine aminotransferase ALT": ["Liver health"],
        "Albumin": ["Liver function", "Kidney function"],
        "Alkaline phosphatase": ["Liver health", "Bone health"],
        "Aspartate aminotransferase AST": ["Liver health", "Heart health"],
        "Bicarbonate": ["Acid-base balance"],
        "Blood urea nitrogen": ["Kidney function"],
        "Chloride": ["Electrolyte balance", "Kidney function"],
        "Cholesterol": ["Cardiovascular health"],
        "Creatine Phosphokinase (CPK)": ["Muscle health", "Heart health"],
        "Creatinine": ["Kidney function"],
        "Gamma glutamyl transferase": ["Liver health", "Bile ducts"],
        "Globulin": ["Immune function"],
        "Glucose, serum": ["Blood sugar levels", "Diabetes"],
        "Iron, refrigerated": ["Iron levels in the body"],
        "Lactate Dehydrogenase": ["Tissue damage"],
        "Osmolality": ["Blood particle concentration"],
        "Phosphorus": ["Bone health", "Kidney function"],
        "Potassium": ["Heart function", "Muscle function"],
        "Sodium": ["Fluid balance", "Nerve function", "Muscle function"],
        "Total bilirubin": ["Liver function"],
        "Total calcium": ["Bone health", "Muscle function"],
        "Total protein": [""],
        "Triglycerides": ["Cardiovascular health"],
        "Uric acid": ["Gout", "Joint health"]
      };
      
      const bloodIndicatorRelations = {
        "Alanine Aminotransferase (ALT)": [],
        "Albumin": ["Globulin", "Total Protein"],
        "Alkaline Phosphatase": ["Total Calcium", "Phosphorus"],
        "Aspartate Aminotransferase (AST)": [],
        "Bicarbonate": ["Chloride", "Sodium"],
        "Blood Urea Nitrogen (BUN)": ["Creatinine"],
        "Chloride": ["Bicarbonate", "Sodium", "Potassium"],
        "Cholesterol": ["Triglycerides"],
        "Creatine Phosphokinase (CPK)": ["Lactate Dehydrogenase"],
        "Creatinine": ["BUN (Blood Urea Nitrogen)"],
        "Gamma Glutamyl Transferase": [],
        "Globulin": ["Albumin", "Total Protein"],
        "Glucose, Serum": [],
        "Iron, Refrigerated": [],
        "Lactate Dehydrogenase": ["CPK (Creatine Phosphokinase)"],
        "Osmolality": [],
        "Phosphorus": ["Alkaline Phosphatase"],
        "Potassium": ["Sodium", "Chloride"],
        "Sodium": ["Chloride", "Bicarbonate", "Potassium"],
        "Total Bilirubin": [],
        "Total Calcium": ["Alkaline Phosphatase", "Phosphorus"],
        "Total Protein": ["Albumin", "Globulin"],
        "Triglycerides": ["Cholesterol"],
        "Uric Acid": ["Potassium", "Sodium", "Chloride"]
      };

      const warningsDiv = document.getElementById("warnings");
      warningsDiv.innerHTML = '';
  
      redIndicators.forEach(originalIndicator => {
          const indicator = originalIndicator ? originalIndicator.split(' ').slice(0, -1).join(' ') : '';
  
          if (indicator && bloodIndicatorKnowledgeBase && bloodIndicatorKnowledgeBase[indicator]) {
              const indicatorInfo = bloodIndicatorKnowledgeBase[indicator];
              const relationships = bloodIndicatorsRelationships[indicator];
  
              const indicatorParagraph = document.createElement("p");
              const indicatorButton = document.createElement("button");
              indicatorButton.style.color = "red";
              indicatorButton.textContent = `\u25BC ${indicator}`;
              indicatorParagraph.appendChild(indicatorButton);
              warningsDiv.appendChild(indicatorParagraph);
  
              const infoParagraph = document.createElement("p");
              const relationshipsSpan = document.createElement("span");
              relationshipsSpan.innerHTML = `<strong>Possible Deficiencies:</strong> ${relationships ? relationships.join(', ') : ''}<br>`;
              relationshipsSpan.style.display = "none";
              const deficienciesSpan = document.createElement("span");
              deficienciesSpan.innerHTML = `<strong>Relationships:</strong> ${indicatorInfo ? indicatorInfo.join(', ') : ''}<br>`;
              deficienciesSpan.style.display = "none";
  
              indicatorButton.addEventListener("click", function () {
                  relationshipsSpan.style.display = (relationshipsSpan.style.display === "none") ? "inline" : "none";
                  deficienciesSpan.style.display = (deficienciesSpan.style.display === "none") ? "inline" : "none";
              });
  
              infoParagraph.appendChild(relationshipsSpan);
              infoParagraph.appendChild(deficienciesSpan);
              warningsDiv.appendChild(infoParagraph);
  
          } else {
              console.warn(`Information not available for blood indicator: ${indicator}`);
          }
      });
  }
    
  function FindRedIndicators(blood_test) {
    let redIndicators = [];

    if (blood_test) {
        for (const key of Object.keys(blood_test)) {
            const color = blood_test[key] ? blood_test[key][1] : '';

            if (color === "red") {
                redIndicators.push(key);
            }
        }
    }

    displayRedBloodIndicatorInfo(redIndicators);
    return redIndicators;
}