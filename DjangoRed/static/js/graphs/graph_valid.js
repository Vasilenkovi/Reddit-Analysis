function add_dataset_button(e) {
    const reference = "prsr_"

    const dataset_container = document.getElementById("dataset-holder")

    const add_dataset_input = document.getElementById("add-dataset-source")
    const dataset_id = add_dataset_input.value
    
    if (dataset_id.includes(reference)) {
        const div_container = document.createElement("div")

            const input_tag = document.createElement("input")
            input_tag.type = "checkbox"
            input_tag.name = dataset_id
            input_tag.id = dataset_id
            input_tag.checked = true
            input_tag.classList.add("mx-1")

        div_container.appendChild(input_tag)

            const label_tag = document.createElement("label")
            label_tag.htmlFor  = dataset_id
            label_tag.innerHTML = dataset_id

        div_container.appendChild(label_tag)

        dataset_container.appendChild(div_container)
    }
    else {
        alert("You can only use reddit user datasets (prsr_ prefix)")
    }
}

function download_svg(e) {
    d3.select("svg").attr("href", 'data:application/octet-stream;base64,' + btoa(d3.select("#line").html())).attr("download", "graph.svg") 
}

function main() {
    const add_button = document.getElementById("add-dataset")
    add_button.addEventListener("click", add_dataset_button)

    const download_button = document.getElementById("download-button")
    download_button.addEventListener("click", download_svg)
}

window.addEventListener("DOMContentLoaded", main)