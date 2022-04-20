var wordIndex;
var wordCount = 0;

function loading() {
    $('.word-box').hide();
    $('.word-count').hide();
    $('.spinner-border').removeClass('d-none');
}


function doneLoading() {
    $('.word-box').show();
    $('.spinner-border').addClass('d-none');
}

function indexUrl() {
    loading()
    var url = $('#urlInput').val();

    $.get('/index', { url }, function( data ) {
        doneLoading()
        wordIndex = data;
    });
}

function searchWord() {
    var word = $('#wordInput').val();

    wordCount = wordIndex[word] ?? 0;
    console.log(wordCount);
    $('.word-count h1').text(wordCount);
    $('.word-count').show();
}