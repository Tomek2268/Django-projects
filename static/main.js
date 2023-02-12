let toastsX = document.getElementsByClassName('toastX')

for (i=0;toastsX.length > i; i++) {
    toastsX[i].addEventListener('click', (e) => {
        e.preventDefault()
        e.target.parentNode.remove()
    })
}

let logo = document.getElementById('logo')
logo.addEventListener('mouseover', (e)=>{
    e.target.classList.add('fa-flip')
    setTimeout(() => {
        e.target.classList.remove('fa-flip')
    }, 1000)
})

let message = document.getElementById('message')
if (message) {
    setTimeout(()=>{
        message.style.animation = 'fade_out 3s'
        setTimeout(()=>{
        message.remove()
        },2500)
    },5000)
}
