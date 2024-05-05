function add_dataset_button(e) {
    const dataset_container = document.getElementById("dataset-holder")

    const add_dataset_input = document.getElementById("add-dataset-source")
    const dataset_id = add_dataset_input.value
    
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

function main() {
    const add_button = document.getElementById("add-dataset")

    add_button.addEventListener("click", add_dataset_button)
}

window.addEventListener("DOMContentLoaded", main)