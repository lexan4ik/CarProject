const searchInpt = document.getElementById('search__input')
const searchDrop = document.querySelector('.search__drop-down')

searchInpt.addEventListener('input', fetchSearchQuery)

function fetchSearchQuery(event) {
    if (searchInpt.value.length >= 3) {
        fetch(`${window.location.origin}/api/search_cars/?brand=${searchInpt.value}`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            searchDrop.style.display = 'block'
            searchDrop.innerHTML = ''
            for (let item of data) {
                searchDrop.innerHTML += `
                <a href='${window.location.origin}/detail/${item.id}' class='search__drop-item'>
                <div class='search__drop-item-img'>
                <img src='${item.main_image.image}'>
                </div>
                <p class='search__drop-title'>${item.name} ${item.model.brand.brand} ${item.model.model}</p>
                </a>
                `
            }
            searchDrop.innerHTML += `
            <a href='${window.location.origin}/search_page/?brand=${searchInpt.value}' class='search__drop-item'>Посмотреть все результаты</a>
            `
            if (data.length === 0) {
                searchDrop.innerHTML = `
                <div class='search__drop-item'>
                <p class='search__drop-title'>Машин не найдено:(</p>
                </div>
                `
            }
        })
    }
    else {
        searchDrop.style.display = 'none'
    }

}
