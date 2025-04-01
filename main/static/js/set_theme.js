const headerInfoColor = document.querySelector('.header__navigation__wrapper')
const headerNavColor = document.querySelector('.header__information__wrapper')
const mainWrapperColor = document.querySelector('.main__wrapper')
let statusTheme = getCookie('changeTheme') ? getCookie('changeTheme') : document.querySelector('.theme-checkbox').value
const inputTheme = document.querySelector('.theme-checkbox')
inputTheme.addEventListener('click', changeTheme)

function changeTheme () {
    console.log(statusTheme)
    if (statusTheme === 'on') {
        statusTheme = 'off'
        headerInfoColor.style.background = '#1f494b'
        headerNavColor.style.background = '#1f4e75'
        mainWrapperColor.style.background = '#3042519c'
    } else {
        statusTheme = 'on'
        headerInfoColor.style.background = '#3d9497'
        headerNavColor.style.background = '#59a0db'
        mainWrapperColor.style.background = '#d6dde1'
    }
document.cookie = `changeTheme=${statusTheme};  path=/;`;
}

if (statusTheme === 'off') {
        headerInfoColor.style.background = '#1f494b'
        headerNavColor.style.background = '#1f4e75'
        mainWrapperColor.style.background = '#3042519c'
        inputTheme.checked = true
    } else {
        headerInfoColor.style.background = '#3d9497'
        headerNavColor.style.background = '#59a0db'
        mainWrapperColor.style.background = '#d6dde1'
        inputTheme.checked = false
    }

function getCookie (name) {
    const cookies = decodeURIComponent(document.cookie).split('; ');
    const cookie = cookies.find(row => row.startsWith(name + '='));
    return cookie ? cookie.split('=')[1] : null;
}