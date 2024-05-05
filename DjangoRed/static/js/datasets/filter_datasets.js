function filter_datasets(e) {
    const search_str = e.target.value
    const set_type = e.target.dataset.set_type
    const cards = document.getElementsByClassName(set_type)

    if (!search_str) {
        for (c of cards) {
            c.style.display = "flex"
        }

        return
    }

    for (c of cards) {
        const set_id = c.getElementsByClassName("set-id")[0].textContent
        const context = c.getElementsByClassName("set-context")[0].textContent

        if (set_id.includes(search_str) || context.includes(search_str)) {
            c.style.display = "flex"
        }
        else {
            c.style.display = "none"
        }
    }
}

function main() {
    const filter_buttons = document.getElementsByClassName("filter-button-class")

    for (button of filter_buttons) {
        button.addEventListener("input", filter_datasets)
    }
}

window.addEventListener("DOMContentLoaded", main)