"use strict";
"format cjs";

var DefineMap = require("can-define/map/map");
var namespace = require("can-namespace");
var route = require("can-route");
var stache = require("can-stache");

/**
 * Login Model
 * @constructor
 * @param {Object} event. An object representing a nav item.
 * @param {string} event.value
 */
var LoginViewModel = DefineMap.extend("LoginModel", {
    isLoading: {type: "boolean", default: false},
    hasError: {type: "boolean", default: false},
    errorMessage: {type: "string", default: null},
    content: {type: "observable"},
    /**
     *
     * @param element
     */
    connectedCallback: function(element) {
        console.log(element);
    },
    getFormData: function () {
        var fields = {};
        $.each($("#form-signin").serializeArray(), function(i, field) {
            fields[field.name] = [field.value];
        });
        return fields;
    }
});

module.exports = namespace.LoginViewModel = LoginViewModel;
