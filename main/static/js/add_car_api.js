const CarFrom = document.getElementById('cars_form')
const SendBtn = document.getElementById('id_button')

SendBtn.addEventListener('click', SendData)

function SendData() {

    let data = new FormData(CarFrom)
    fetch (`${window.location.origin}/api/cars/`,
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: data,
        }
    )
        .then((response) => response.json())
        .then((data) => {
        if (data.errors) {
            const errors = data.errors
            if (errors.price) {
                console.log(data)
                let priceInput = document.getElementById('id_price')
                console.log(priceInput.classList)
                priceInput.classList.add('input_error')

                const errorText = document.createElement('p')
                errorText.textContent = `${errors.price}`

                priceInput.parentElement.append(errorText)
                console.log(priceInput.classList.contains('input_error'))
                priceInput.oninput = () => {
                    if (priceInput.classList.contains('input_error')) {
                        priceInput.classList.remove('input_error')
                        priceInput.parentElement.children[1].remove()
                        console.log('johan')
                    }
                }
            }
        }

    })
}

function getCookie (name) {
    const cookies = decodeURIComponent(document.cookie).split('; ');
    const cookie = cookies.find(row => row.startsWith(name + '='));
    return cookie ? cookie.split('=')[1] : null;
}