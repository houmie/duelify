/*jslint plusplus: true, browser: true, devel: true */
/*global $, jQuery, gettext, */

var isVisible = false;
var clickedAway = false;

function getCookie(name) {
    "use strict";
    var cookieValue, cookies, i, cookie;
    cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        cookies = document.cookie.split(';');
        for (i = 0; i < cookies.length; i++) {
            cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    "use strict";
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function (xhr, settings) {
        "use strict";
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

 /*, 0..n args */
function partial(func) {
    "use strict";
    var args = Array.prototype.slice.call(arguments, 1);
    return function () {
        var allArguments = args.concat(Array.prototype.slice.call(arguments));
        return func.apply(this, allArguments);
    };
}


if (!String.prototype.trim) {
   //code for trim
    String.prototype.trim = function () {
        "use strict";
        return this.replace(/^\s+|\s+$/g, '');
    };
}

// function draggable_modal(modal_id) {
    // "use strict";
    // $(modal_id).draggable({
        // handle: ".modal-header"
    // });
// }
// 
// function validation_rules(form) {
    // "use strict";
    // var validator = $(form).validate({
            // // options            
            // errorPlacement: function (error, element) {
                // var field_error = $(form).find('#id_' + element.attr('name')).siblings('.field_error');
                // if (field_error.length > 0) {
                    // error.appendTo(field_error);
                // } else {
                    // field_error = $(form).find('#id_' + element.attr('name')).closest('td').children('.field_error');
                    // if (field_error.length > 0) {
                        // error.appendTo(field_error);
                    // } else {
                        // field_error = $(form).find('#id_' + element.attr('name')).closest('.well').children('.field_error');
                        // error.appendTo(field_error);
                    // }
                // }
                // $(field_error).show();
            // },
            // // ignore: ':hidden:not(.chzn-done)'
            // ignore: "",
            // invalidHandler: function () {
                // $("#validation_summary").text(validator.numberOfInvalids() + gettext(" field(s) are invalid"));
            // },
            // errorContainer: "#validation_summary"            
        // });
// 
    // $(form).find('select.mandatory').each(function () {
        // $(this).change(function () {
            // $(this).valid();
        // });
        // $(this).rules('add', {
            // valueNotEquals: ""
        // });
    // });
// 
    // $(form).find('select.multi_select_mandatory').each(function () {
        // $(this).chosen().change(function () {
            // $(this).valid();
        // });
        // $(this).rules('add', {
            // required: true
        // });
    // });
    // return validator;
// }
// 
// 
// // This rebinds all rating classes within the templates (not forms)
// function rebind_ratings(parent) {
    // "use strict";
    // $(parent).find('.rating').each(function (i, v) {
        // // The radio button template tag shows which button was selected from None, 1, 2, 3. The number is then taken to use as score.
        // var selection = 0;
        // if ($(v).text().trim() !== 'None') {
            // selection = parseInt($(v).text().trim(), 10);
        // }
        // $(v).children('.star_small').raty({
            // score     : selection,
            // readOnly  : true,
            // half      : false,
            // size      : 24,
            // hints     : [gettext('Less Important'), gettext('Important'), gettext('Very Important')],
            // starOff   : 'star-off.png',
            // starOn    : 'star-on.png',
            // number    : 3,
            // path      : $.chasebot.STATIC_URL + 'raty/lib/img'
        // });
    // });
// }
// 
// // This binds the single rating class within the add or edit form
// function bind_rating_form() {
    // "use strict";
    // var i;
    // $('#star').raty({
        // cancel    : true,
        // cancelOff : 'cancel-off-big.png',
        // cancelOn  : 'cancel-on-big.png',
        // cancelHint: gettext('Cancel this rating'),
        // half      : false,
        // size      : 24,
        // hints     : [gettext('Less Important'), gettext('Important'), gettext('Very Important')],
        // starOff   : 'star-off-big.png',
        // starOn    : 'star-on-big.png',
        // number    : 3,
        // path      : $.chasebot.STATIC_URL + 'raty/lib/img',
        // click     : function (score, evt) {
            // if (score) {
                // $('#id_important_client_' + score).attr('checked', true);
            // } else {
                // $('#id_important_client_0').attr('checked', true);
            // }
        // }
    // });
// 
    // for (i = 1; i <= 3; i++) {
        // if ($('#id_important_client_' + i).is(':checked')) {
            // $('#star').raty('score', i);
        // }
    // }
// }
// 
// 
// 
// function chosenify_field(field_id, source) {
    // "use strict";
    // $(field_id, source).chosen({no_results_text: gettext('No results match')});
// }
// 
// 
// function add_more_tag_to_all_notefields(source) {
    // "use strict";
    // var showChars, ellipsesText, moreText, lessText, bag, countChars, openTags;
    // showChars = 135;
    // ellipsesText = "...";
    // moreText = gettext("more");
    // lessText = gettext("less");
// 
    // $('.cb_notes:not(:has(*))', source).each(function () {
        // var $this, content, c, inTag, i, tagName, j, html, tmp;
        // $this = $(this);
        // content = $this.html();
        // if (content.length > showChars) {
            // c = content.substr(0, showChars);
            // if (c.indexOf('<') >= 0) { // If there's HTML don't want to cut it            
                // inTag = false; // I'm in a tag?
                // bag = ''; // Put the characters to be shown here
                // countChars = 0; // Current bag size
                // openTags = []; // Stack for opened tags, so I can close them later
// 
                // for (i = 0; i < content.length; i++) {
                    // if (content[i] === '<' && !inTag) {
                        // inTag = true;
// 
                        // // This could be "tag" or "/tag"
                        // tagName = content.substring(i + 1, content.indexOf('>', i));
// 
                        // // If its a closing tag
                        // if (tagName[0] === '/') {
                            // if (tagName !== '/' + openTags[0]) {
                                // tmp = 1 + 1; //dummy to pass lint
                            // } else {
                                // openTags.shift(); // Pops the last tag from the open tag stack (the tag is closed in the retult HTML!)
                            // }
                        // } else {
                            // // There are some nasty tags that don't have a close tag like <br/>
                            // if (tagName.toLowerCase() !== 'br') {
                                // openTags.unshift(tagName);
                            // }
                        // }
                    // }
                    // if (inTag && content[i] === '>') {
                        // inTag = false;
                    // }
// 
                    // if (inTag) {
                        // bag += content[i]; // Add tag name chars to the result
                    // } else {
                        // if (countChars < showChars) {
                            // bag += content[i];
                            // countChars++;
                        // } else {
                            // if (openTags.length > 0) {
                                // for (j = 0; j < openTags.length; j++) {
                                    // bag += '</' + openTags[j] + '>';
                                    // // You could shift the tag from the stack to check if you end with an empty stack, that means you have closed all open tags
                                // }
                                // break;
                            // }
                        // }
                    // }
                // }
                // c = bag;
            // }
// 
            // html = '<span class="shortcontent">' + c + '&nbsp;' + ellipsesText +
                   // '</span><span class="allcontent">' + content +
                   // '</span>&nbsp;&nbsp;<span><a href="javascript:void(0)" class="morelink badge">' + moreText + '</a></span>';
// 
            // $this.html(html);
            // $(".allcontent").hide();
        // }
    // });
// 
    // $(".morelink").off('click').on('click', function () {
        // var $this = $(this);
// 
        // if ($this.hasClass('less')) {
            // $this.removeClass('less');
            // $this.html(moreText);
// 
            // $this.parent().prev().prev().show(); // shortcontent
            // $this.parent().prev().hide(); // allcontent       
        // } else {
            // $this.addClass('less');
            // $this.html(lessText);
// 
            // $this.parent().prev().prev().hide(); // shortcontent
            // $this.parent().prev().show(); // allcontent
        // }
        // return false;
    // });
// }
// 
// 
// 
// function initialize_validator() {
    // "use strict";
    // // add the rule here
    // $.validator.addMethod("valueNotEquals", function (value, element, arg) {
        // return arg !== value;
    // }, gettext('Please select an item!'));
// 
    // $.validator.addClassRules("email", {
        // email: true
    // });
// 
    // $.validator.addClassRules("input_mandatory", {
        // required: true
    // });
// 
    // $.validator.addClassRules("textarea_mandatory", {
        // required: true
    // });
// 
    // $.validator.addClassRules("date_picker", {
        // date: true
    // });
// }
// 
// function spinning_btn(btn_id, form_id) {
    // "use strict";
    // $(btn_id).click(function (event) {
        // event.preventDefault();
        // $(this).off('click');
        // $(this).addClass('disabled');
        // $(this).html('<i class="icon-spinner icon-spin"></i> Please wait...');
        // $(form_id).submit();
    // });
// }
// 
// function activate_menu(event) {
    // "use strict";
    // event.preventDefault();
    // var i, menu_id;
    // menu_id = event.data.menu_id;
    // for (i = 0; i < $(menu_id).parent().children().length; i++) {
        // $(menu_id).parent().children()[i].removeClass('active');
    // }
    // $(menu_id).addClass('active');
// }

function hide_form_errors() {
    "use strict";
    $('.errorlist').remove();
}

function process_form_errors(json, form) {
    "use strict";
    hide_form_errors();
    //form.clearForm();
    var errors, prefix, field;
    errors = json.errors;

    /*jslint nomen: true*/
    if (errors.__all__ !== undefined) {
        $('#all_error').append(errors.__all__);
    }
    /*jslint nomen: false*/

    prefix = form.find(":hidden[name='prefix']").val();

    prefix = ((prefix === undefined) ? '' : prefix + '-');
    for (field in errors) {
        if (errors.hasOwnProperty(field)) {
            $('#id_' + prefix + field).after(errors[field]);
        }
    }
}


function login(id) {
    "use strict";
    $(id).load('/side_login/', function () {
        jQuery(function ($) {
            var login_form = $('#form_login');
            login_form.ajaxForm({
                url : this.action,
                dataType : 'json',
                success : function (json) {
                    if (json.errors !== undefined) {
                        process_form_errors(json, login_form);
                    } else {
                        window.location.replace(json.redirect_to);
                    }
                }
            });
        });
    });
}


function datepicker_reload(source, isPast) {
    "use strict";
    var options;
    options = { format: $('#locale').text(),
            weekStart: 1,
            autoclose: 'True',
            todayHighlight: 'True' };

    // if (isPast) {
        // options.endDate = $('#user_date').text();
    // } else {
        // options.startDate = $('#user_date').text();
    // }

    //if (Modernizr.touch && Modernizr.inputtypes.date) {
    //    $(source).find('.date_picker').type = 'date';
    //} else {
    $(source).find('.date_picker').datepicker(options);
    //}
}

// function discuss_btn_clicked(event) {
    // "use strict";
    // event.preventDefault();
    // var url;
    // url = $(event.currentTarget).attrs('href');
    // if ($.cookie('sessionid') === null) {
        // var test = 1;
    // }
// }

function personal_invite(event) {
    "use strict";
    var action = event.data.action;
    $('#collapseOne').collapse(action);
}

// function punch_edit(event) {
    // "use strict";
    // event.preventDefault();
    // var url = $(event.currentTarget).attr('href');
    // $('#punch-row-{{punch.pk').load(url, function () {
        // $('.punch-form').empty();
    // });
// }

$(document).ready(function () {
    "use strict";
    // spinning_btn('#registration-button', '#form_registration');
    // spinning_btn('#login-button', '#form_login');
    // spinning_btn('#reset-button', '#form_reset');
    datepicker_reload('body', true);

    // $('#invite_menu').on('click').off('click', {menu_id: '#invite_menu'}, activate_menu);
    // $('#home_menu').on('click').off('click', {menu_id: '#home_menu'}, activate_menu);
    login('#login');
    $('#id_rule_1').off('click').on('click', {action: 'show'}, personal_invite);
    $('#id_rule_0').off('click').on('click', {action: 'hide'}, personal_invite);
    if ($('#id_rule_1').is(':checked')) {
        $('#id_rule_1').click();
    }
    $('.carousel').carousel({
        interval: 5000
    });
    //$('.punch-edit').off('click').on('click', punch_edit);
    //$('.discuss_btn').off('click').on('click', discuss_btn_clicked);
});