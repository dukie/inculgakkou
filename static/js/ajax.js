if(typeof(django) != 'undefined') {$ = django.jQuery;}

$(function() {

    function updateInnerHTML(data, elemId) {

        var options = '';
	    for (var i = 0; i < data.length; i++) {
		    options += "<option value=" + data[i].pk + ">" + data[i].value + "</option>";
		}
		$("#" + elemId).html(options);
    }

    // Building relations between Master and Bound Select input widgets
    var bindingsInfoObject = {};
    var selectElements = $('[data-ajax-select="ajaxSelectWidget"]');

    $.each(selectElements, function(index,element){

        var optionsObj = JSON.parse(element.attributes["data-plugin-options"].value);
        if(!(optionsObj.masterSelectId in bindingsInfoObject)) {
            bindingsInfoObject[optionsObj.masterSelectId] = {};
            bindingsInfoObject[optionsObj.masterSelectId]['boundInput'] = [];
            bindingsInfoObject[optionsObj.masterSelectId]['ajaxSource'] = optionsObj.source;
        }
        bindingsInfoObject[optionsObj.masterSelectId]['boundInput'].push(optionsObj.boundSelectId);
    });

    $.each(bindingsInfoObject, function(masterName, value) {

            var masterNode = $("#" + masterName);
            masterNode.change(function() {

                   $.getJSON(value.ajaxSource, {'term': masterNode.val()}, function(data){

                        $.each(value['boundInput'], function(index,boundName) {

                            updateInnerHTML(data, boundName);
                        });
                   });

            })
    });
});