function generic_add_more(e) {
    const form_reference = e.target.dataset.ephemeral

    const ephemeral_div = document.getElementById(form_reference + "-div")
    
    const new_input = document.createElement("input")
    new_input.classList.add(form_reference + "-multiple")
    new_input.classList.add("ephemeral-multiple")
    new_input.classList.add("btn")
    new_input.classList.add("active")
    new_input.classList.add("my-1")
    new_input.classList.add("text-start")
    new_input.type = "text"

    ephemeral_div.appendChild(new_input)
}

function parsing_target(e) {
    const destroy_ephemeral = document.getElementsByClassName("ephemeral-multiple")
    for (tag of destroy_ephemeral) {
        tag.remove()
    }

    if (e.target.value == "submission_comments") {
        const deactivate = document.getElementsByClassName("parser-form-option")
        for (div of deactivate) {
            div.style.display = "none"
        }
        
        const activate = document.getElementsByClassName("parser-form-comments-submission")
        for (div of activate) {
            div.style.display = "block"
        }

    }
    else if (e.target.value == "subreddit_comments") {
        const deactivate = document.getElementsByClassName("parser-form-option")
        for (div of deactivate) {
            div.style.display = "none"
        }
        
        const activate = document.getElementsByClassName("parser-form-comments-subreddit")
        for (div of activate) {
            div.style.display = "block"
        }
    }
    else if (e.target.value == "subreddit_users") {
        const deactivate = document.getElementsByClassName("parser-form-option")
        for (div of deactivate) {
            div.style.display = "none"
        }
        
        const activate = document.getElementsByClassName("parser-form-users")
        for (div of activate) {
            div.style.display = "block"
        }
    }
}

function generic_submit_transform(e) {
    const form_reference = e.target.dataset.ephemeral

    const ephemeral_fields = document.getElementsByClassName(form_reference + "-multiple")
    const common_input = document.getElementById(form_reference + "-input")

    var sub_strings_array = []
    sub_strings_array.push(common_input.value)
    for (sub_input of ephemeral_fields) {
        sub_strings_array.push(sub_input.value)
    }

    common_input.value = sub_strings_array.join(";")
}

function main() {
    const target_select = document.getElementById("parser-form-select")
    target_select.addEventListener("change", parsing_target)

    const add_more_buttons = document.getElementsByClassName("form-add-more")
    for (button of add_more_buttons) {
        button.addEventListener("click", generic_add_more)
    }

    const submit_buttons = document.getElementsByClassName("parser-form-submit")
    for (button of submit_buttons) {
        button.addEventListener("click", generic_submit_transform)
    }
}

window.addEventListener("DOMContentLoaded", main)