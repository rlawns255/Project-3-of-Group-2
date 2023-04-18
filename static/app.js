// data endpint

const actors_list = "http://127.0.0.1:5000/api/v1.0/actors"


//build actors table
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
    let firstActor = actors[0]
    
   buildActorsTable(firstActor)
    })
}

    function optionChanged(newActor){
        buildActorsTable(newActor)
    }


init();
