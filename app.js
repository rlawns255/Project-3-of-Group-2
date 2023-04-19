// function that builds a bar chart from the Apple TV+ data for genres
function buildBarChart() {
    // read in the data from genres_list
    d3.json("/genres").then((data) => {

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

// Function that updates the dashboard when the sample is changed
function optionChanged(newSample) {

    // log the new value
    console.log(newSample);

    // Call the functions to update the charts
    buildBarChart(newSample);
}

//Call the initial function to build the dashboard
init();

// /// Get the sample values for movie_shows, actors, release_year, and imdb_scores
// let movie_shows = firstSample.movie_shows;
// let actors = firstSample.actors;
// let release_year = firstSample.release_year;
// let imdb_scores = firstSample.imdb_scores;

// // log the data to the console
// console.log(movie_shows, actors, release_year, imdb_scores);

// // Set the top ten items to display in descending order
// let topTen = movie_shows.slice(0, 10).reverse();
// let topTenActors = actors.slice(0, 10).reverse();
// let topTenReleaseYear = release_year.slice(0, 10).reverse();
// let topTenImdbScores = imdb_scores.slice(0, 10).reverse();

// //Set up the trace for the bar chart
// let trace = {
//     x: topTenImdbScores,
//     y: topTen,
//     text: topTenActors,
//     type: "bar",
//     orientation: "h"
// };

// // Set up the layout
// let layout = {
//     title: "Top 10 Movies/Shows in Action & Adventure",
//     xaxis: { title: "IMDB Score" },
//     yaxis: { title: "Movie/Show" }
// };

// // Call plotly
// Plotly.newPlot("bar", [trace], layout);
// });
// }