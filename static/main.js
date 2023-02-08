let toastsX = document.getElementsByClassName('toastX')

for (i=0;toastsX.length > i; i++) {
    toastsX[i].addEventListener('click', (e) => {
        e.preventDefault()
        e.target.parentNode.parentNode.remove()
    })
}
