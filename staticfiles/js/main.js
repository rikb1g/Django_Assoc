// Select all toggle buttons
var toggleButtons = document.querySelectorAll('[id^="toggleButton"]');
console.log(toggleButtons)

// Add event listeners to each button
toggleButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        
        // Get the related "moreButtons" element by constructing its ID
        var moreButtonsId = 'moreButtons' + button.id.replace('toggleButton', '');
        var moreButtons = document.getElementById(moreButtonsId);

        // Toggle the hidden and showbtn classes
        if (moreButtons.classList.contains('hidden')) {
            moreButtons.classList.remove('hidden');
            moreButtons.classList.add('showbtn');
        } else {
            moreButtons.classList.add('hidden');
            moreButtons.classList.remove('showbtn');
        }
    });
});





