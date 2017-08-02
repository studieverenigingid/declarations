var contains = function(needle) {
    // Per spec, the way to identify NaN is that it is not equal to itself
    var findNaN = needle !== needle;
    var indexOf;

    if(!findNaN && typeof Array.prototype.indexOf === 'function') {
        indexOf = Array.prototype.indexOf;
    } else {
        indexOf = function(needle) {
            var i = -1, index = -1;

            for(i = 0; i < this.length; i++) {
                var item = this[i];

                if((findNaN && item !== item) || item === needle) {
                    index = i;
                    break;
                }
            }

            return index;
        };
    }

    return indexOf.call(this, needle) > -1;
};


var toStore = ['committee','name','email','iban','owner'];

// Function to get date input (HTML el) value
Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});

$(document).ready(function() {
    $('#js-date').val(new Date().toDateInputValue());

	$('.decl-form__answer').each(function () {
		var inputName = $(this).attr('name');
		if (contains.call(toStore, inputName)) {
			$(this).val(Cookies.get(inputName));
		}
	});
});​



$('#js-form').submit(function(e) {
	e.preventDefault();

	var declaration = {
		purchase: $('input[name=purchase]').val(),
		amount: $('input[name=amount]').val(),
		committee: $('input[name=committee]').val(),
		post: $('input[name=post]').val(),
		date: $('input[name=date]').val(),
		name: $('input[name=name]').val(),
		email: $('input[name=email]').val(),
		iban: $('input[name=iban]').val(),
		owner: $('input[name=owner]').val(),
	};

	for (var i = 0; i < toStore.length; i++) {
		Cookies.set(toStore[i], declaration[toStore[i]]);
	}

	$('.js-rm').remove();

    var formData = new FormData($(this)[0]);

	$.ajax({
		url: '/declare/',
		dataType: 'JSON',
        data: formData,
        processData: false,
        contentType: false,
		type: 'POST',
	}).done(function (r) {
		if (r.success) {
			$('#js-form').append('<p class="success js-rm">Nice! Je hebt een declaratie ingediend. Topper, hé, zeg!</p>');
        } else if (r.error === 'emptiness') {
			$('#js-form').append('<p class="error js-rm">Hmmm je moet wel alles invullen!</p>');
        } else if (r.error === 'file-not-allowed') {
			$('#js-form').append('<p class="error js-rm">Oooh, probeer je nou een verboden bestand toe te voegen?! :O</p>');
		} else {
			console.log(r);
		}
	});
})
