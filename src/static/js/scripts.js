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

// switch the hidden attribute values of unfiltered and filtered charts
function switchChart(chartId) {

    const unfiltered = document.getElementById(chartId + "_unfiltered"),
        filtered = document.getElementById(chartId + "_filtered")

    if (filtered.classList.contains('block') && unfiltered.classList.contains('hidden'))  {
        // Currently displaying filtered version
        filtered.classList.remove('block')
        filtered.classList.add('hidden')
        unfiltered.classList.remove('hidden')
        unfiltered.classList.add('block')
        return
    }

    if (filtered.classList.contains('hidden') && unfiltered.classList.contains('block')) {
        // Currently displaying nonfiltered
        filtered.classList.remove('hidden')
        filtered.classList.add('block')
        unfiltered.classList.remove('block')
        unfiltered.classList.add('hidden')
        return
    }
}