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

function send_form(e) {
    const real_button = document.getElementById("download-button-true")
    const confirm_text = `Reddit API terms of use require that no deleted content may be stored outside of platform. To comply with this policy, parsed data is not stored for longer than 48 hours. By downloading the dataset, you take the responsibility of data disposal upon yourself.`

    if (window.confirm(confirm_text)) {
        real_button.click()
    }
}

function main() {
    const add_button = document.getElementById("add-dataset")
    add_button.addEventListener("click", add_dataset_button)
    
    const send_button = document.getElementById("download-button-false")
    send_button.addEventListener("click", send_form)
}

window.addEventListener("DOMContentLoaded", main)