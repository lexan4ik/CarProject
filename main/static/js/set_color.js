const body = document.getElementById('my_body')
const inputColor = document.getElementById('color')
const colorButton = document.getElementById('color_button')

inputColor.addEventListener('change', changeColor)

function changeColor () {
    body.style.background = inputColor.value
}

console.log(body)