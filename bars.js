//////Trey's Code//////
const url = "https://2u-data-curriculum-team.s3.amazonaws.com/dataviz-classroom/v1.1/14-Interactive-Web-Visualizations/02-Homework/samples.json";
// Initialize the dashboard at start up 
function init() {

    // Use D3 to select the dropdown menu
    let dropdownMenu = d3.select("#selDataset");

    // Use D3 to get sample names and populate the drop-down selector
    d3.json(url).then((data) => {
        
        // Set a variable for the sample names
        let names = data.names;

        // Add  samples to dropdown menu
        names.forEach((id) => {

            // Log the value of id for each iteration of the loop
            console.log(id);
            
            // Append the option to the dropdown menu
            dropdownMenu.append("option")
            .text(id)
            .property("value",id);
        });

        // Set the first sample from the list
        let sample_one = names[0];

        // Log the value of sample_one
        console.log(sample_one);

        // Build the initial plots
        buildMetadata(sample_one);
        buildBarChart(sample_one);
    });
};

// Function that populates metadata info
function buildMetadata(sample) {

  // Use D3 to retrieve all of the data
  d3.json(url).then((data) => {

      // Retrieve all metadata
      let metadata = data.metadata;

      // Filter based on the value of the sample
      let value = metadata.filter(result => result.id == sample);

      // Log the array of metadata objects after the have been filtered
      console.log(value)

      // Get the first index from the array
      let valueData = value[0];

      // Clear out metadata
      d3.select("#sample-metadata").html("");

      // Use Object.entries to add each key/value pair to the panel
      Object.entries(valueData).forEach(([key,value]) => {

          // Log the individual key/value pairs as they are being appended to the metadata panel
          console.log(key,value);

          d3.select("#sample-metadata").append("h5").text(`${key}: ${value}`);
      });
  });

};

  // function that builds a bar chart from the Apple TV+ data for genres
  function buildBarChart() {
    // read in the data from genres_list
    d3.json("/api/v1.0/genres").then((data) => {
  
        // Retrieve all data samples
        let genres = data.genres;
  
        //Filter based on the value of the genres
        let filteredGenres = genres.filter(result => result.genre === genres);
  
        // Get the first sample from the list
        let firstSample = filteredGenres[0];
  
        //Get the sample values for genres
        let genres_sample = firstSample.genres;
  
        // log the data to the console
        console.log(genres_sample);
  
        // Set the top ten items to display in descending order
        let topTen = genres_sample.slice(0, 10).reverse();
  
        //Set up the trace for the bar chart
        let trace = {
            x: topTen,
            y: topTen,
            text: topTen,
            type: "bar",
            orientation: "h"
        };
        
        // Set up the layout
        let layout = {
            title: "Top 10 Genres",
            xaxis: { title: "Genre" },
            yaxis: { title: "Count" }
        };
        
        // Call plotly
        Plotly.newPlot("bar", [trace], layout);
    });
  }
  // Function that updates the dashboard when the sample is changed
  function optionChanged(newSample) {
  
    // log the new value
    console.log(newSample);
  
    // Call the functions to update the charts
    buildBarChart(newSample);
  }
  
//Call the initial function to build the dashboard
init();