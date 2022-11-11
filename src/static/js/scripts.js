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
        var unfiltered = document.getElementById(chartId+"_unfiltered").hidden,
            filtered = document.getElementById(chartId+"_filtered").hidden,
            tmp;
        tmp = unfiltered;
        unfiltered = filtered;
        filtered = tmp;

        document.getElementById(chartId+"_unfiltered").hidden = unfiltered;
        document.getElementById(chartId+"_filtered").hidden = filtered;
}