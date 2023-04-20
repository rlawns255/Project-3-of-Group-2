// data endpint

const actors_list = "http://127.0.0.1:5000/api/v1.0/actors"
const titles_list = "http://127.0.0.1:5000/api/v1.0/titles"


//function that populates actors table
function buildActorsTable(actor) {
    d3.json(actors_list).then(data => {
        let metadata = data.metadata

        currentActor = metadata.filter((subject) => subject.actor == actor);

        let panel = d3.select('#sample-metadata');

        currentActor.forEach(actorInfo =>{
            panel.html("")
            for (let key in actorInfo) {
                panel
                    .append("table")
                    .text(`${key} : ${actorInfo[key]}`)
                    .property("value" , `${key} : ${actorInfo[key]}`)
            }
        })
        
    })


}

////// Function that populates titles table

function buildTitlesTable(title) {
    d3.json(titles_list).then(data => {

        let metadata = data.metadata

        
        let currentTitle =  metadata.filter((subject) => subject.title == title);

        panel = d3.select('#title-metadata')

        currentTitle.forEach(titleInfo =>{
            panel.html("")
            for (let key in titleInfo) {
                panel
                    .append("table")
                    .text(`${key} : ${titleInfo[key]}`)
                    .property("value" , `${key} : ${titleInfo[key]}`)
            }
})
    })

}



function init() {

    let dropdownMenu = d3.select("#selDataset");

    d3.json(actors_list).then(data => {
        
        let actors= data.names
        
        for (let i = 0; i < actors.length; i++) {
            dropdownMenu
                .append("option")
                .text(actors[i])
                .property("value" , actors[i])        
        }
    let firstActor = actors[0];
    
   buildActorsTable(firstActor)
    })
    /// titles dropdown list
    let dropdownMenu2 = d3.select("#selTitle");

    d3.json(titles_list).then(data =>{

        let titles = data.titles
        
        for (let i = 0; i < titles.length; i++){
            dropdownMenu2
                .append("option")
                .text(titles[i])
                .property("value" , titles[i])
        }
        let firstTitle = titles[0];

        buildTitlesTable(firstTitle)

    })
    
}
    function optionChanged(newActor){
        buildActorsTable(newActor)
    }
    function movieChanged(newTitle){
        buildTitlesTable(newTitle)
    }


init();
