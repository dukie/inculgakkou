$(function() {
    console.log("inKanji");
    (function() {
        var answerString;
    $('#answerField').keyup(function(event){
        answerString = event.target.value;

    });
    $('#answerField').keydown(function(event){
        if(event.keyCode == 13) {
            console.log(answerString);
            window.location = '/incul/kanji/quizze/'+answerString+'/';
            return false;
        }
    })})();
});