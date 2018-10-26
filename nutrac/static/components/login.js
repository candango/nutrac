"use strict";
"format cjs";

var LoginViewModel = require("./login-view-model");
var Component = require("can-component");

//import template from "./nav.stache";
var loginTemplate = require("./login.stache");

//import canMap from "can-connect/can/map/map";
//import connect from "can-connect";
//import dataUrl from "can-connect/data/url/url";
//import constructor from "can-connect/constructor/constructor";

var helpers = {

};

Component.extend({
    tag: "login-form",
    view: loginTemplate,
    ViewModel: LoginViewModel,
    events: {
        "#signinButton click": function (button, event) {
            console.log(this.viewModel.getFormFields());
            console.log($(button))
        }
    },
    helpers: helpers
});
