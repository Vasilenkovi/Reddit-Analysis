function set_permament_position(node, position_x) {
    node.x = position_x
    node.removeEventListener("mouseenter")
    node.removeEventListener("mouseleave")
}

function main() {
    const resetbutton = document.getElementsByClassName("mpld3-resetbutton")

    for (tag of resetbutton) {
        set_permament_position(tag, 0)
    }
    
    const zoombutton = document.getElementsByClassName("mpld3-zoombutton")

    for (tag of zoombutton) {
        set_permament_position(tag, 32)
    }
    
    const boxzoombutton = document.getElementsByClassName("mpld3-boxzoombutton")

    for (tag of boxzoombutton) {
        set_permament_position(tag, 64)
    }
}

window.addEventListener("DOMContentLoaded", main)