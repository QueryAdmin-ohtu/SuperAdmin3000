// Notification dismissal
window.dismissNotification = function () {
    document.getElementById('notification').style.display = 'none'
}

// Opening and closing of deletion confirmation modal
window.openModal = function (modalId) {
    document.getElementById(modalId).style.display = 'block'
    document.getElementsByTagName('body')[0].classList.add('overflow-y-hidden')
}

window.closeModal = function (modalId) {
    document.getElementById(modalId).style.display = 'none'
    document.getElementsByTagName('body')[0].classList.remove('overflow-y-hidden')
}