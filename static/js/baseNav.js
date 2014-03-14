$(function() {
    (function() {
        var searchString;
    $('#searchField').keyup(function(event){
        searchString = event.target.value;

    });
    $('#searchField').keydown(function(event){
        if(event.keyCode == 13) {
            console.log(searchString);
            window.location = '/search/'+searchString+'/';
            return false;
        }
    })})();
    $(document).on('click', '.accordion-toggle', function(event) {
            event.stopPropagation();
            var $this = $(this);

            var chevron = $this.find('span.glyphicon.pull-right')
            chevron.toggleClass('glyphicon-chevron-up glyphicon-chevron-down')

            var parent = $this.data('parent');
            var actives = parent && $(parent).find('.collapse.in');

            // From bootstrap itself
            if (actives && actives.length) {
                actives.prev().find('span.glyphicon.pull-right').toggleClass('glyphicon-chevron-up glyphicon-chevron-down');
                actives.collapse('hide');
            }

            var target = $this.attr('data-target') ;

            $(target).collapse('toggle');
    });

    $('.vDateField').datepicker();

});